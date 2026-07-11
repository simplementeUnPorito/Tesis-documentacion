# Plan 2929 Hz nativo + decimación con promedio + duración por tipo + SD opcional

> **Archivo de seguimiento para agentes (Claude/codex).** Al completar cada ítem: marcar el checkbox
> y anotar una fila en el "Registro de progreso" del final ANTES de seguir. Si una sesión queda a
> medias, la siguiente retoma desde aquí. Ver también el plan aprobado original (fuera del repo, en
> `~/.claude/plans/quiero-implementar-un-plan-bright-matsumoto.md` de la sesión que lo generó) para el
> razonamiento completo — este documento es el resumen accionable y el que persiste en el repo.

Fecha de creación: 2026-07-10. Plan diseñado y aprobado en sesión Claude (rama `codex/capture-engine-verilog`).

## ✅ SESIÓN 2026-07-11 (tarde) — ENCADENADO + DECIMACIÓN VALIDADOS EN BANCO (GEO+PSoC en COM12) — LEER PRIMERO

Banco de esta sesión: **maestro COM8, esclavo GEO+PSoC en COM12**. Se trabajó solo por USB en COM12
(no se tocó COM8 para no tirar el WiFi/AP del maestro). El geófono ya está conectado (hw=0/GEO).

### Dos causas raíz encontradas y resueltas (invalidan la teoría vieja de "degradación de hardware / pérdida de frames UART")

1. **Carrera en el comando de banco `cap` (esclavo)** — RESUELTO EN CÓDIGO Y VALIDADO.
   `requestCaptureFromUsb()` hacía `requestPrestartFromUsb()` e **inmediatamente** `requestUsbStartFromHotWait()`,
   pero el PSoC confirma `PSOC_EVT_ARMED` (→ `g_psoc_arm_ready`) de forma asíncrona ~100-300 ms
   después del `preStart()`. El sync se disparaba antes de ARMED → `sync ignored ready=0` → la captura
   quedaba colgada en HOT_WAIT con `fill=0/N`. Como la latencia del ACK ARMED variaba, el síntoma era
   **no-monotónico** (cap chico ✓, cap grande ✗) — exactamente lo que la sesión previa había atribuido
   por error a "pérdida de frames UART / degradación del banco". Fix: `requestCaptureFromUsb()` ahora
   espera (busy-wait acotado 800 ms, sirviendo `psoc.poll()`/`servicePsocConfigAck()`/watchdog) a que
   `storeReadyForHotWait()` sea true antes de disparar el sync. El path real maestro→esclavo NO sufría
   esto (PRESTART y START llegan separados por radio); es solo la herramienta de banco `cap`.
   Archivo: `slave/src/main.cpp` `requestCaptureFromUsb()`.

2. **El PSoC se cuelga al reflashear el ESP esclavo** — OPERATIVO, workaround validado.
   Reflashear el ESP por USB hace un `Hard reset via RTS`; ese reset glitchea las líneas compartidas
   (SYNC/UART) hacia el PSoC y **cuelga al PSoC si venía con uptime largo** (el de esta sesión tenía
   ~2 días sin reset). Síntoma tras reflashear el ESP: `uartBytes=0`, `edge=0`, `probe psoc=0`,
   `PSoC cfg probe failed age=-1`, SETN nunca ackea. **Workaround: resetear el PSoC (NO reflashear)**
   con `ToggleReset` vía KitProg — ver "Reset de target" en `src/psoc/BUILD_PROGRAM_PSOC.md`
   (`KitProg (CMSIS-DAP/236111)`, `ToggleReset 0 100`). Tras el ToggleReset el PSoC re-corre su HEX +
   auto-cal (~8-13 s) y la UART revive (`probe psoc=1`, `uartBytes` creciendo, `fs=2604`).
   **Regla operativa: cada vez que se reflashea el ESP esclavo, resetear el PSoC después.**

### Resultados validados en hardware (COM12, `bBad=0` en todos, drops ~14-24 por corrida, estables)

Tasa nativa real del ADC = **2604 Hz** (no 2929; el customizer regenerado quedó en 2604 y el código lo
asegura con `#if` de compilación: `PSOC_ADC_NATIVE_FS_HZ 2604u` en `psoc_adc.h` vs `ADC_CF_*_SRATE`, y
`PSOC_NATIVE_SAMPLE_RATE_HZ 2604UL` en `psoc_uart.h`). Fs efectiva = 2604/decim.

| decim | cap (lotes) | raw batches | encadenado | fs (Hz) | **adquisición** | wall (cap→dump) |
|-------|-------------|-------------|------------|---------|-----------------|-----------------|
| 1 | 10 / 60 / 360 | =lotes | no | 2604 | — / — / 4.15s | — |
| 1 | 512 | 512 | no | 2604 | 5.90s | ~6.8s |
| 3 | 360 | 1080 | **sí (×3)** | 868 | **12.44s** | ~12.5s |
| 2 | 512 | 1024 | **sí (×2)** | 1302 | **11.80s** | ~13.5s |
| 3 | 512 | 1536 | **sí (×3)** | 868 | **17.70s** | ~18.6s |

**El objetivo "más segundos, debe funcionar" (superar los 10.59 s del build viejo de 1020 Hz) está
cumplido y validado**: con decim≥2 y 512 lotes se pasa de 11.8 s, y con decim 3 se llega a 17.7 s,
todo RAM-only (arena paginada `STORE_PAGE_BATCHES=32`, sin SD). El cap de hardware de 512 lotes RAW
(=512×30/2604=5.9 s por corrida) se supera **encadenando** trozos crudos: el PSoC rearma superMaquina
sin resetear `g_capture_wr` ni el acumulador de decimación y solo emite `DUMP_DONE` al final.

### Estado del código al cierre de esta sesión

- `slave/src/main.cpp`: fix de la carrera `cap` (arriba) + set previo de robustez de HOT_WAIT
  (watchdog re-arm/abort, limpieza de flags viejos en ARM, bookkeeping de sync-edge en `loop()`,
  STATUS visible si HOT_WAIT se estira). Compila (`pio run -e slave1` OK, RAM 13.6%, Flash 58.1%),
  flasheado a COM12 y **validado**. **Commiteado** en esta sesión junto a este doc.
- `master/src/main.cpp` y `master/data/js/app.js`: cambios de relay de decimación + web (Máx 512,
  preservados reescalados por fs) quedan en working-tree, **sin flashear a COM8** (regla WiFi).
  Pendiente subir cuando el usuario esté para reconectar a GeoNetwork.
- PSoC: **NO se reflasheó** (sigue con su HEX conocido-bueno). El BLOCKER de abajo (TopDesign GEO no
  fitea → no se puede construir el firmware con SD) **sigue vigente**, pero el encadenado RAM-only ya
  da hasta 17.7 s sin necesitar SD.

## ⛔ BLOCKER PSoC (2026-07-11 ~01:30) — EL TOPDESIGN GEO NO FITEA — LEER ANTES DE TOCAR EL PSoC

El TopDesign fue cambiado a la variante **GEO** (con SPI Master para SD y una conexión nueva
`vRef Vdda/2 → LPF_2.Vin`, `Net_7100`) a las **2026-07-10 23:38** (después del último build
exitoso, que era HAMMER+SPI de las 16:30). Ese esquemático GEO **falla el ruteo analógico**
(`apr.M0003 Unable to find a solution for the analog routing`) de forma **determinística**:
4 intentos con semillas distintas (seed del fit HAMMER 16:30, seed del fit fallido, seed del
.cyfit de git y arranque virgen sin .cyfit). Redes en conflicto: `Net_4664` (VDAC_ref_PGA),
`Net_4547` (PGAn.Vin), `Net_4661` (OPAref.Vout), `Net_2195` (PGAp.Vout→LPF_1), `Net_7100`
(vRef nuevo) — overuse de `AGL[4/5/7]`, `AGR[0]`, `amuxbusL`, `sc* Wire`, `dsm0+ Wire`.
La fábrica analógica está saturada: 4 PGAs (PGAp/PGAn/PGAgain/PGAshield) = 4/4 SC blocks,
4 opamps = 4/4, 2 LPF dedicados = 2/2.

Además el regen del ADC en esta variante GEO quedó **parcial**: netlist elaborado muestra
`Sample_Rate=3000` solo en Config1 y `1020` en Configs 2-4 (la variante HAMMER sí quedó 2929×4).

**Qué necesita el usuario hacer en PSoC Creator (GUI)**: abrir la variante GEO, terminar el regen
del ADC (2929 en las 4 configs, igual que HAMMER) y resolver el ruteo analógico — candidato #1:
la conexión nueva `vRef_1 (Vdda/2) → LPF_2` (el warning M0029 dice que no tiene conexión de
hardware directa y consume globals analógicos); probar revertirla o alimentar esa referencia de
otra forma. Recién entonces se puede compilar/flashear el código SD de abajo (ya escrito y listo:
`sd_spi.h` + driver en `psoc_hw.c` + integración captura/dump en `main.c`).

Mientras tanto el banco COM12 sigue con el **HEX HAMMER+SPI del 2026-07-10 23:07** (encadenado
validado, sin comandos SD — el ESP debe tolerar timeout de 0xBC y reportar `sd_present=0`).

## ESTADO ACTUAL (2026-07-10 noche / 2026-07-11 madrugada) — LEER PRIMERO

El banco quedó funcionando por USB en `COM12` con el PSoC y el ESP esclavo usando memoria conjunta.
Este bloque SUPERA las notas históricas de más abajo que dicen "encadenado revertido" o "SD en ESP32".

### Resultado validado en hardware

- **PSoC flasheado con encadenado activo**: build `cyprjmgr` OK, flash `42302 B`, SRAM `49088 B`;
  programado con `ppcli` en `KitProg (CMSIS-DAP/248355)`, filas `0..165`, log
  `%TEMP%\psoc_program_chain_arena_20260710_230805.log`.
- **ESP esclavo COM12 flasheado** con arena RAM paginada (`STORE_PAGE_BATCHES=32`) y herramientas de
  banco (`SLAVE_USB_CMD_ENABLE=1 SLAVE_LAB_TOOLS_ENABLE=1 SLAVE_LOGS_ENABLE=1 DBG_HUMAN=1`).
- **`N=3`, modo real (`debugpsoc 0`, `stream 0`)**:
  - `cap 360`: `SETN ack val=255`, `FULL -> STOPPED (360 batches)`, `DUMP_DONE`, status final
    `bBad=0`, `fill=360/360`, `fs=976`. Tiempo `sync start`→`DUMP_DONE`: ~14.08 s
    (≈11.06 s de adquisición + dump UART).
  - `cap 512`: `store arena n=512 pages=16`, heap libre ~69 KB, `maxAlloc≈53 KB`, `SETN ack val=255`,
    `FULL -> STOPPED (512 batches)`, status final `bBad=0`, `fill=512/512`, `fs=976`.
    Tiempo `sync start`→`DUMP_DONE`: ~20.03 s (≈15.74 s de adquisición + dump UART).
- Esto corrige el bug reportado por la captura web de `N=3`: antes `cap 360` terminaba en `170`
  porque el PSoC recortaba a `512/N`; ahora el PSoC encadena trozos crudos de hasta 512 y solo emite
  `DUMP_DONE` al final.

### Cambios clave de esta tanda

- **PSoC (`main.c`)**: `capture_rearm_next_chunk()` rearmado entre trozos sin resetear
  `g_capture_wr` ni el acumulador de decimación; `capture_next_hw_target()` calcula por muestras
  para preservar restos parciales de decimación; `CHAIN_NEXT` queda como evento intermedio y
  `DUMP_DONE` solo al final.
- **ESP esclavo (`slave/src/main.cpp`)**: arena paginada en vez de un `malloc` contiguo gigante.
  El límite RAM-only sube a **512 lotes decimados** porque ya no depende de `ESP.getMaxAllocHeap()`.
- **Fix importante de banco USB**: `enterHotWait()` ahora confirma `PSOC_EVT_SETN` antes de mandar
  `preStart()`. Sin esto, la ruta `cap` podía arrancar con el largo viejo del PSoC y aparentar dumps
  parciales (`fill=60/360`).
- **Web/plot**: código cambiado para que `Máx` sea **512 lotes** y para que los preservados usen su
  propia `fs` al dibujarse; así un preservado a 2929 Hz no se estira al cambiar el vivo a `N=3`.
  **Pendiente**: subir estos cambios a COM8 (`pio upload` + `uploadfs`) solo con el usuario listo para
  reconectar a GeoNetwork.

### SD: decisión actual

El usuario corrigió el alcance: la SD va en el **PSoC** (componente SPI Master cableado en TopDesign),
no en el ESP32. Jerarquía deseada: **ESP32 RAM paginada -> RAM PSoC -> SD en PSoC**. El código previo
`slave/src/sd_storage.*` para SD-en-ESP32 queda **obsoleto** y no debe ampliarse sin revalidar el
diseño con esta decisión. Falta implementar/probar la SD del lado PSoC cuando haya tarjeta/módulo.

### Pendiente inmediato

1. Subir maestro/web a `COM8` si el usuario confirma que puede reconectarse a GeoNetwork.
2. Probar desde navegador: aplicar `N=3`, botón `Máx (512 lotes)`, confirmar `15360 muestras` y
   preservados reescalados por `fs` propia.
3. Documentar/implementar después la SD en PSoC, no en ESP32.


## Objetivo

1. Volver el ADC del PSoC a su tasa nativa **2929 Hz** en las 4 configs de rango (`CF_2V5/CF_0V512/CF_1V024/CF_0V625`) — el regen del customizer en PSoC Creator **ya lo hizo el usuario** (`Generated_Source/PSoC5/ADC.h` ya reporta `SRATE=2929` en las 4). Falta el código C.
2. Agregar un **factor de decimación configurable con promedio** (no descarte) corriendo en el PSoC, antes de mandar por UART, aplicado después de la selección RAW/FIR existente (`PSOC_CMD_SELECT_STREAM`). Factor 1 = sin decimar (2929 Hz tal cual); factor D = promedia D muestras consecutivas → Fs efectiva = 2929/D.
3. Permitir **duración de captura distinta para HAMMER vs GEO** (hoy es un único `n_batches` broadcast a todos los esclavos).
4. **SD opcional en el PSoC** (corrección del usuario, 2026-07-10 noche): el maestro NO necesita SD y la SD tampoco va en el ESP32 esclavo. La jerarquía objetivo es **ESP32 RAM paginada -> RAM PSoC -> SD en PSoC** usando el SPI Master cableado en TopDesign. El código viejo de SD-en-ESP32 queda documentado solo como historial obsoleto.
5. Documentar (sin implementar) la idea de cola PSoC↔ESP para expandir memoria sin SD.

## Contexto y hechos confirmados

- El sistema corría a 1020 Hz desde `docs/plan_adc_1020.md` (2026-07-06/07), migración deliberada para "no mezclar frecuencias entre nodos". Costo colateral documentado: el FIR de hardware fue diseñado para ~2929 Hz y quedaba ~3× desalineado a 1020 Hz (riesgo R3 de ese plan). Volver a 2929 nativo con decimación software generaliza esa idea y de paso realinea el FIR.
- El regen de `ADC_DelSig` en el customizer de PSoC Creator **ya está hecho por el usuario** (2026-07-10, esta sesión) — verificado leyendo `Generated_Source/PSoC5/ADC.h`: `ADC_CF_2V5_SRATE=2929`, `ADC_CF_0V512_SRATE=2929`, `ADC_CF_1V024_SRATE=2929`, `ADC_CF_0V625_SRATE=2929`. `DEC_DIV`/`ALIGNMENT`/`COUNTS_PER_VOLT` de cada config no cambiaron de forma respecto al build de 1020 Hz, solo la Fs — es decir, `psoc_adc_counts_right_aligned()` (que condiciona en `ADC_Config==ADC_CF_2V5` para dividir por `ADC_CF_2V5_DEC_DIV`) sigue siendo válido sin cambios.
- PSoC↔ESP es **UART** (no SPI) — `slave/src/psoc_uart.cpp:5` documenta que reemplazó un `psoc_spi` viejo. La SD, en cambio, ahora sí queda del lado PSoC por decisión del usuario y debe usar el SPI Master cableado en TopDesign.
- Banco disponible hoy (2026-07-10): maestro COM8, esclavo **HAMMER real está en COM12** (confirmado por el usuario), aunque `slave/platformio.ini` todavía etiqueta `slave2`/COM12 como GEOPHONE y `slave1`/COM10 como HAMMER. **No tocar las etiquetas del `.ini` esta sesión** — al flashear el entorno `slave1` (HAMMER) usar `--upload-port COM12`. El geófono no está conectado esta sesión.
- Batch UART fijo en 30 muestras en 3 lugares (`main.c BATCH_SAMPLES`, Verilog `sample_count_reg`, ESP `psoc_uart.h SPI_BATCH_SAMPLES`). La decimación NO debe atarse a ese framing — acumular en el ISR de forma continua, el empaquetado de a 30 solo lee lo que ya está decimado.
- `g_fir_discard` (`main.c:240,995-998`) descarta el transitorio de grupo del FIR (63 muestras), NO es decimación — debe correr ANTES del acumulador de decimación para no promediar muestras del transitorio.
- `g_capture_raw` es un array estático `512×90` bytes ≈ 45 KB (`main.c:183,233`), ~93% de la SRAM usada hoy. Decimar antes de guardar reduce cuántos batches hace falta almacenar para la misma duración real → gana margen de RAM.
- Opcode UART libre: `0xBB` (siguiente a `PSOC_CMD_ADC_CONFIG=0xBA`) → `PSOC_CMD_SET_DECIMATION`.
- `MsgSetRecLen`/`MsgPrestart` no llevan `node_id` — hoy van por `ESPNOW_BROADCAST`. Duración por tipo de nodo se resuelve en el maestro iterando esclavos y mandando **unicast** según `hw_class` cacheado (`g_cachedHello[]`), sin tocar el struct ni el esclavo.
- `app.js applyGlobalFs()` pisa `nd.fs` de TODOS los nodos con el último HELLO recibido — hay que corregirlo a "solo el nodo que mandó el HELLO" para que Fs por nodo se muestre bien.
- El maestro NO acumula datos hoy (relevo en vivo, stop-and-wait por batch) y **no va a acumular SD tampoco** (decisión 2026-07-10, ver sección "SD: descartado en el maestro" más abajo) — sigue mandando a la web en lotes chicos que ya maneja sin problema.
- Pines SD ESP32 propuestos en una tanda anterior: SPI custom `SCK=18, MISO=19, MOSI=4, CS=5`.
  **Histórico/obsoleto**: con la corrección actual, la SD se retoma en el PSoC, no en esos pines ESP32.

## SD: descartado en el maestro (2026-07-10)

El usuario revirtió esta parte: el maestro NO necesita SD. Ya hoy el volcado (`DUMPING`) es
stop-and-wait por lote (`CMD_REQ_BATCH` → recibe → transmite por WS/USB → descarta) — alcanza con
mandar a la web en lotes chicos que el maestro pueda manejar sin acumular todo en RAM, sin agregar
ninguna etapa de staging a SD del lado maestro. La SD queda **solo en los esclavos GEO**, sin ningún
límite compuesto con una SD del maestro (que ya no existe). **Corrección 2026-07-10 (2da)**: la
implementación de la SD NO está forzada a software puro — usar el periférico SPI hardware del ESP32
(el mismo que ya usan `SPI.begin()`/`SD.h`, con DMA) si mejora throughput/latencia de escritura;
"software" acá solo describía que la lógica de derrame RAM→SD y el manejo del filesystem viven en
el firmware del ESP32 (no en el PSoC), no que haya que evitar el hardware SPI del propio ESP32.

## Verilog/hardware para la decimación: evaluado y descartado (2026-07-10)

A pedido del usuario se evaluó mover el promediado de decimación a `superMaquina.v` aprovechando
margen libre de UDB (screenshot del reporte de fitting: 81.3% UDB usado pero Datapath Cells 4/24 y
Control Cells 5/24 casi libres). Conclusión (con el advisor): **no conviene, se descarta**.
- El acumulador (suma) sí cabría en una Datapath Cell (libre), pero el **paso que falta es dividir por
  un factor D configurable en tiempo de ejecución (1..100, no potencia de 2)** — eso requiere una
  máquina de estados iterativa que consume Control Cells + Macrocells + **P-terms**, y P-terms es
  justo el recurso más ajustado (312/384, 81.3%) — el mismo que hizo fallar (`E2071`) los 2 intentos
  previos de agregar lógica mucho más chica en Verilog (ver `docs/psoc_supermaquina_handoff.md`).
- Además requeriría cambiar el TopDesign (routear ADC/DMA a una Datapath Cell, no es un cambio de
  solo `.v`) y pasar de IRQ-por-muestra a IRQ-cada-D-muestras, tocando la "política de eventos
  determinismo-primero" ya validada en hardware (2026-07-02) — riesgo alto sobre una parte del
  sistema que ya funciona.
- No hay ningún cuello de botella real que justifique el riesgo: a 2929 Hz el ISR en software
  (decodificar + sumar + comparar, dividir solo 1 de cada D muestras) es trivial para el Cortex-M3.
- **Se mantiene la decimación 100% en software** (ya implementada y flasheada en `main.c`/`psoc_adc.c`).
  No se identificó ninguna otra pieza de este set de features (duración por tipo = lógica de control
  del ESP; SD = I/O) con una ganancia real de mover a hardware.

## Checklist

### H0 — Este archivo
- [x] Crear `docs/plan_2929_decimation_sd.md` con checklist y registro.

### H1 — PSoC (`src/psoc/AcondicionamientoAnalogico.cydsn`) — solo .c/.h, PROHIBIDO .cyprj/.cydwr/.cysch/.cyfit (el regen de ADC ya lo hizo el usuario en PSoC Creator)
- [x] `psoc_adc.h`/`psoc_adc.c`: `psoc_adc_effective_fs_hz()` → `2929u / g_psoc_decimation_factor`. Nueva `psoc_adc_set_decimation(uint8)`/`psoc_adc_get_decimation()`, default 1, rango 1..100, rechaza fuera de `PSOC_IDLE`.
- [x] `main.c`: acumulador de decimación (`g_decim_acc`,`g_decim_n`) en `sm_sample_capture_raw()`/`sm_sample_capture_filt()`, DESPUÉS de `g_fir_discard`. Cuando `n==factor`: promedio → `g_capture_wr`, reset.
- [x] `main.c`: `psoc_arm()`/`psoc_enter_sampling()` — target de hardware por trozo <=512 lotes crudos (contador de 9 bits); si el pedido total necesita más, H7 lo encadena sin truncar ni resetear el buffer.
- [x] `psoc_hw.h`: `#define PSOC_CMD_SET_DECIMATION 0xBBu`.
- [x] `main.c`: case `PSOC_CMD_SET_DECIMATION` en el switch de comandos (mismo bloque que `PSOC_CMD_ADC_CONFIG`): gate `PSOC_IDLE`, `psoc_adc_set_decimation()`, `uart_send_cfg_ack(0xBB, factor)`, `uart_send_fs_report()`.
- [x] Build `cyprjmgr` OK (flash 41094B/15.7%, SRAM 49088B/74.9%, sin warnings).
- [x] Flash `ppcli` OK (filas 0..160, `psoc_program_decimation_20260710_160635.log`).

**Prueba de aceptación H1**: ✅ ver H2 (prueba conjunta) — `decim 1/2/3` en RAW y FIR, `FS_REPORT` verificado exacto (2929/1464/976), `fill=N/N`, `bBad=0`.

### H2 — ESP slave (`src/esp/Nodo comunicación/slave/src`)
- [x] `psoc_uart.h`: `#define PSOC_CMD_SET_DECIMATION 0xBB` + `void setDecimation(uint8_t factor);`.
- [x] `psoc_uart.cpp`: `setDecimation` → `_sendCmd1(PSOC_CMD_SET_DECIMATION, factor)`.
- [x] Comando USB de banco `decim N` (bajo `SLAVE_LAB_TOOLS_ENABLE`, junto a `range N`) para probar sin pasar por el maestro. De paso se agregó `fs=%u` a `logPsocUartDiag()` (antes no había forma de ver la Fs efectiva por USB).
- [x] `pio run -e slave1 -t upload --upload-port COM12` OK (HAMMER real hoy).

**Prueba de aceptación H2**: ✅ `decim 2`, `cap 5`, `status` → `fill=5/5`, `bBad=0`, repetido también con `decim 3` y en stream FIR (`stream 1`) con `decim 1/2/3` — todo `bBad=0`. `fs=` confirmado exacto: 2929/1464/976/585 para factor 1/2/3/5. Ver fila de "Registro de progreso" para el detalle completo (incluye una observación no bloqueante sobre auto-calibración lenta, no relacionada con este código).

### H3 — ESP master + web (factor de decimación por esclavo) — SOLO COMPILAR, no subir a COM8 sin confirmar con el usuario
- [x] Maestro (`master/src/main.cpp`): NO hizo falta agregar un case nuevo — `handleDirectedCmd()` ya tiene un `else` genérico que envuelve cualquier `sub_cmd` no especial-caseado en `MsgSetConfig` (el mismo camino que ya usaba `ADC_CONFIG`), así que `0xBB` ya viaja maestro→esclavo sin tocar el C++ del maestro.
- [x] **Corrección**: sí hacía falta un cambio en el ESP esclavo — `handleSetConfig()` (`slave/src/main.cpp`) tiene una whitelist propia de `sub_cmd` aceptados que NO incluía `0xBB` (el comando USB de banco lo probó por un camino distinto, directo a `psoc.setDecimation()`, sin pasar por este switch). Se agregó `case PSOC_CMD_SET_DECIMATION` en los dos switches de `handleSetConfig()` (validación + despacho) con `isDecimationFactor()` nueva (rango 1..100), igual patrón que `PSOC_CMD_ADC_CONFIG`/`isAdcConfigCode()`. Sin esto, el maestro/web hubiera mandado el comando pero el esclavo lo habría rechazado en silencio (`ok=0`, no llega nunca al PSoC).
- [x] Web (`config.js`: `SUBCMD_DECIMATION=0xBB`, `slave_panel.js`: input numérico + dot + label por panel, `app.js`: `onDecimationChanged`/ACK/resend-all encadenado tras ADC_CONFIG/localStorage/`applyNodeDecimation`, `export.js`: `decimation_factor` en metadata) — mismo patrón que el dropdown de rango ADC.
- [x] `pio run -e slave1` y `pio run -e esp32dev` OK (compile-check). JS revisado a mano (balance de llaves/paréntesis, sin Node.js disponible en esta máquina para lint automático).
- [x] Confirmar con el usuario antes de `-t upload`/`-t uploadfs` a COM8 (tira el WiFi/AP) — hecho, usuario confirmó y se subió. Ver prueba end-to-end abajo.

### H4 — Duración de captura por tipo de nodo (Fase A, maestro + web) — PAUSADA, ver nota
> **2026-07-10, checkpoint deliberado**: NO se implementó esta sesión (a diferencia de B.7). Motivo:
> a diferencia de B.7 (aditivo — opcode/campo nuevo, si falla solo rompe la feature nueva), Fase A
> **modifica** `g_rec_n_batches` dentro de la máquina de estados de `DUMPING` del maestro, que hoy es
> compartida entre todos los nodos y está validada en hardware (corrida "11/11 OK" documentada). El
> propósito mismo de esta fase es comportamiento DIFERENCIAL hammer≠geo — imposible de probar hoy
> (geo no conectado, además el maestro no se puede reflashear sin el usuario presente). Coincide
> además con la regla explícita del usuario ("cada vez que implementas algo DEBES probar antes de
> avanzar"). Se prefirió dejar el diseño listo y preciso para la próxima sesión de banco (con GEO
> conectado) en vez de tocar a ciegas una máquina de estados compartida y validada.
>
> **Diseño ya acotado (evaluado con el advisor) para cuando se retome**: NO hace falta convertir
> `g_rec_n_batches` en array en los ~15 sitios donde se usa — la mayoría son guardias `>0`/`==0` o
> "hay una captura configurada", que pueden seguir siendo escalares (semántica: "largo canónico").
> Solo 2 puntos tienen semántica genuinamente por-nodo:
> 1. **Los sitios de envío** — `broadcastPrestart()`/`broadcastRecordLength()` pasan a iterar los
>    esclavos conocidos y mandar **unicast** con `nBatchesForNode(node)` en vez de un único broadcast.
> 2. **El corte del volcado** — `main.cpp:1548` (`if (g_dumpBatchSeq >= g_rec_n_batches)`, dentro del
>    loop de `DUMPING` que pide lotes nodo por nodo) pasa a comparar contra `nBatchesForNode(g_dumpSlaveIdx)`
>    en vez del global compartido.
>
> Nueva función `nBatchesForNode(nodeId)`: lee `g_cachedHello[nodeId].hw_class` (ya existe, cacheado
> desde el HELLO) y devuelve la duración configurada para HAMMER o GEO (fallback a GEO si `hw_class`
> todavía es `SLAVE_HW_UNKNOWN`, o al valor único legado si el usuario no configuró ambos por separado).
>
> **Invariante de seguridad a preservar**: cuando `duración_hammer == duración_geo`,
> `nBatchesForNode()` debe devolver lo mismo para cualquier nodo — el camino tiene que quedar
> byte-idéntico al actual. Eso protege el camino de un solo tipo de nodo (ya validado) y es lo único
> que se puede verificar hoy si se implementa sin GEO conectado.
- [ ] `master/src/main.cpp`: nueva `nBatchesForNode(nodeId)`; `broadcastRecordLength()`/`broadcastPrestart()` → unicast por nodo; corte de `DUMPING` en `main.cpp:1548` usa `nBatchesForNode(g_dumpSlaveIdx)`.
- [ ] Web: dos inputs "Duración HAMMER"/"Duración GEO" en vez de uno; `captureBatches()` calcula ambos; preview de lotes muestra ambos.
- [ ] `app.js`: fix `applyGlobalFs()` → setear `nd.fs` solo del nodo que mandó el HELLO.
- [ ] `pio run -e esp32dev` OK (compile-check) — se puede hacer sin hardware.
- [ ] **Bloqueado hasta la próxima sesión de banco con GEO conectado**: confirmar con el usuario antes de subir a COM8 (mismo flash que B.7 — batchear ambos en una sola subida); probar con HAMMER+GEO ambos conectados: duración HAMMER cambia solo la captura de hammer, duración GEO solo la de geo, y con duraciones iguales el comportamiento es idéntico al de hoy (invariante de arriba).

### H5 — SD opcional (HISTORIAL OBSOLETO: fue ESP32/GEO, ahora debe rehacerse en PSoC)
> **No continuar esta implementación como camino principal.** El usuario corrigió después que la SD va
> en el PSoC mediante el SPI Master cableado en TopDesign. El bloque de abajo queda como historial del
> intento SD-en-ESP32 y de los archivos existentes `slave/src/sd_storage.*`; no debe ampliarse sin
> rediseñar primero el pipeline PSoC->SD.
>
> Ruta nueva pendiente: inicializar SPI/FAT o escritura binaria cruda del lado PSoC, volcar desde la RAM
> PSoC a SD cuando la ventana supere lo que puede sostener RAM-only, y mantener al ESP32 como control/
> dump paginado hacia maestro/web.
- [x] `slave/platformio.ini` (envs `slave2`/`slave3`, los GEO — NO `slave1`/HAMMER): pines SPI custom `SCK=18,MISO=19,MOSI=4,CS=5` (VSPI hardware del ESP32, no bit-bang) vía `-DSD_SPI_*_PIN`.
- [x] Esclavo GEO: `sd_storage.h/.cpp` nuevo módulo — `SPI.begin(18,19,4,5)` + `SD.begin(5, spiSpi)` (periférico SPI hardware + DMA vía `SD.h` estándar), auto-detección en `setup()` (`sdStorageBegin()`), campo nuevo `sd_present` en `MsgHello` (reportado hacia el maestro/web cada ~2s, mismo ciclo que `hw_class`). **Diseño**: API `sdStorage*()` siempre presente y segura de llamar en cualquier firmware — si `SD_SPI_CS_PIN` no está definido (HAMMER), `sd_storage.cpp` compila la variante stub (todo no-op/false), así que `main.cpp` no necesita `#ifdef` esparcidos.
- [x] Toggle SD por esclavo GEO en panel web: nuevo sub_cmd `SLAVE_CMD_SET_SD_ENABLE=0xC0` (NO pasa por el PSoC, se resuelve 100% en `handleSetConfig()` del esclavo con ack inmediato) + checkbox en `slave_panel.js` (deshabilitado/gris hasta que llega `sd_present=1` por HELLO).
- [x] **Histórico/obsoleto**: en el intento SD-en-ESP32, el límite efectivo se pensó como capacidad de
  la SD del esclavo GEO y se dejaba pasar `n_batches > PSOC_CAPTURE_MAX_BATCHES(360)` si
  `sdStorageEnabled()` era true. Hoy el RAM-only validado es `512` lotes y la SD se rehace en PSoC.
- [x] **Histórico/obsoleto**: el derrame RAM→SD del ESP32 se diseñó como captura entera en
  `/capture.bin` si el pedido no entraba en RAM. No continuar por este camino salvo rediseño explícito.
- [ ] **Pendiente de hardware**: validar con módulo SD soldado (próxima sesión de banco, geófono no está conectado hoy).
- [x] **Superado por H7**: la web/maestro ya fueron cambiados en código a `PSOC_CAPTURE_MAX_BATCHES=512`.
  Falta únicamente subir a COM8/uploadfs cuando el usuario esté listo para reconectar a GeoNetwork.

### H7 — RAM-only ESP32 + PSoC al máximo actual (validado 2026-07-10/11)
- [x] PSoC: re-arme encadenado entre trozos de hasta `PSOC_CAPTURE_MAX_BATCHES=512` lotes crudos,
  conservando `g_capture_wr`, `g_decim_acc/g_decim_n` y emitiendo `DUMP_DONE` solo al final.
- [x] PSoC: cálculo de próximo trozo por muestras (`capture_written_samples()`), no por lotes
  enteros, para no perder restos parciales cuando `N` no divide exactamente el final de un trozo.
- [x] ESP esclavo: arena RAM paginada (`STORE_PAGE_BATCHES=32`) en lugar de `malloc` contiguo;
  `PSOC_CAPTURE_MAX_BATCHES=512` ahora es un límite conjunto ESP+PSoC, no `maxAlloc` del ESP.
- [x] ESP esclavo: `enterHotWait()` confirma `PSOC_EVT_SETN` antes de `preStart()` para evitar
  arrancar el PSoC con el largo anterior.
- [x] Web/master: constantes actualizadas a 512 lotes y preservados dibujados con `fs` propia.
  **Pendiente de upload a COM8** por la reconexión manual a GeoNetwork.
- [x] Hardware COM12: `debugpsoc 0`, `stream 0`, `decim 3`, `cap 360` y `cap 512` limpios
  (`bBad=0`, `fill=N/N`, `fs=976`). Ver registro de progreso.

### H6 — Cola PSoC↔ESP para expandir memoria sin SD (Fase D, diseño, NO implementar)
- [x] Redactar sección de diseño abierto (ver abajo). NO implementar esta sesión — es una idea preliminar del usuario, documentada para que una sesión futura decida si vale la pena.

#### Diseño abierto: cola de re-pedido PSoC→ESP (NO implementada)

**Motivación original (usuario)**: en vez de que el esclavo dependa solo de su propia RAM (360 lotes)
o de una SD física (Fase C/H5), que el PSoC retenga muestras adicionales en su propia SRAM cuando el
ESP se queda sin lugar, y que el ESP se las vuelva a pedir más adelante cuando libere memoria (p. ej.
tras volcar parte de lo ya capturado). La idea original del usuario era de 3 contadores/etapas: (1) el
contador de hardware de `superMaquina` (lotes CRUDOS, ya existe: `batch_limit_reg`, 512 lotes — ver
el hallazgo de hardware más abajo en este documento), (2) una cola en la RAM del PSoC (esto, nuevo),
(3) derrame a SD del lado ESP (esto ya se implementó en H5, más simple).

**Estado actual sin esta cola (ya verificado, no hipotético)**:
- El PSoC hoy **empuja muestras a tasa fija por UART sin ningún control de flujo** una vez armado
  (`sm_sample_capture_raw/filt` en `main.c`, llamadas desde el ISR de `superMaquina`) — no existe
  comando de "pausar"/"reanudar" el envío. El ESP debe seguir el ritmo o perder datos; no hay forma de
  decirle al PSoC "esperá, no tengo dónde guardar esto todavía".
- `g_capture_raw` (PSoC) ya usa **~75% de la SRAM del PSoC** (45 KB de 64 KB) — margen libre real
  ronda ~19 KB, que ya compite con pila, variables de calibración, etc. Una cola adicional de tamaño
  útil (para que valga la pena frente a la RAM del ESP, ~360 lotes × 90 B ≈ 32 KB) casi no entra.
- El techo de 512 lotes CRUDOS del contador de hardware (`superMaquina.v:99`, ver sección de hallazgo
  más abajo) es un eje **totalmente independiente**: aunque hubiera cola en el PSoC, seguiría haciendo
  falta re-armar encadenado para superar ~5.25 s de muestreo continuo por corrida.

**Qué requeriría implementarlo** (boceto, no comprometido):
1. Nuevo comando UART `PSOC_CMD_QUEUE_MODE` (habilitar/deshabilitar): cuando `g_capture_wr` llega al
   tope de `g_capture_raw`, en vez de parar la captura, seguir escribiendo en un segundo buffer circular
   más chico (tamaño acotado por los ~19 KB libres, quizás unos pocos cientos de lotes YA decimados —
   la decimación de Fase B ayuda acá, reduce el footprint post-store).
2. Nuevo comando UART `PSOC_CMD_QUEUE_PULL(n)`: el ESP, tras liberar espacio propio (volcando al maestro
   o derramando a SD), le pide al PSoC los próximos `n` lotes de la cola.
3. Del lado ESP: hoy la arquitectura es estrictamente "store-then-dump" (primero se captura TODO,
   después se vuelca) — nada permite volcar/liberar memoria a mitad de una captura en curso. Soportar
   esta cola requeriría romper ese modelo y permitir volcado parcial concurrente con el muestreo, un
   cambio de arquitectura bastante más grande que H4 (Fase A) o H5 (Fase C).

**Por qué no se prioriza (recomendación, no implementar salvo necesidad concreta)**: Fase C (H5, SD en
el esclavo) ya resuelve el problema real ("capturas más largas que la RAM del ESP") con un diseño mucho
más simple — un periférico SPI que ya existe en el ESP32, sin protocolo nuevo hacia el PSoC, sin
competir por la SRAM ya ajustada del PSoC, y sin romper el modelo store-then-dump. El único caso donde
esta cola aportaría algo que SD no aporta es un esclavo GEO **sin módulo SD soldado** que igual necesite
capturas largas — un caso de borde que no está pedido hoy. Se deja documentado por si en el futuro
aparece esa necesidad puntual; no se recomienda implementar como parte de este plan.

## ⚠️ Hallazgo crítico de hardware (2026-07-10, durante H1): techo de 512 lotes crudos en `superMaquina`

Verificado en `superMaquina/superMaquina.v:99` (`reg [8:0] batch_limit_reg`, cargado en dos partes por
`capture_engine_configure_target()` — `main.c:604-613` — con el byte alto enmascarado a **1 bit**,
`superMaquina.v:212` `batch_limit_reg[8] <= cfg[0]`): es un registro de **9 bits real**, no una
subutilización de firmware. Tope duro: **512 lotes crudos = 15360 muestras** que `superMaquina` cuenta
en HARDWARE antes de pasar a `DONE`, contados sobre el flujo crudo del ADC — la decimación de firmware
corre DESPUÉS del IRQ por muestra, así que NO estira este contador. A 2929 Hz eso es
**~5.246 s de muestreo continuo por corrida** (512×30/2929), sea cual sea el factor de decimación.

**Aclaración importante (para no confundir dos límites distintos)**:
- **Techo del contador de hardware** (512 lotes CRUDOS por corrida): se resuelve con **re-arme
  encadenado en firmware** (pulsar de nuevo `START_NOW`/`ARM` al llegar a `DONE`, sin resetear
  `g_capture_wr` ni el acumulador de decimación entre corridas) — 100% firmware, no necesita SD ni
  memoria extra del PSoC. `hw_target` (lotes crudos) para una duración real T = `T × 2929 / 30`,
  independiente de D; hace falta encadenar solo si esa cantidad supera 512 (T > ~5.25 s).
- **Techo de almacenamiento** (cuántos lotes DECIMADOS caben en `g_capture_raw`, 512 lotes de RAM):
  eje totalmente separado. Con decimación factor D, lotes almacenados = `hw_target / D`. Ejemplo
  "geo 10 s": `hw_target = 976` lotes crudos (2 corridas encadenadas de ≤512), con D=2 → 488 lotes
  almacenados, entra en los 512 de RAM sin necesitar SD. La SD (Fase C) solo hace falta cuando los
  lotes DECIMADOS a almacenar superan 512 (ventanas muy largas con decimación baja).
- **HAMMER (ejemplo del usuario, 3 s) no dispara el problema del contador**: `3s × 2929/30 ≈ 293`
  lotes crudos, por debajo de 512 con cualquier D — o sea Fase B (fs 2929 + decimación) es
  100% probable HOY con hammer solo, sin necesitar el encadenamiento todavía.
- **SD va en el PSoC, NO en el ESP32 ni en el maestro** — corrección final del usuario tras esa tanda.
  El componente SPI Master ya fue cableado en TopDesign, así que el diseño SD-en-ESP32 de H5 queda
  obsoleto. Mantener el modelo RAM-only validado ahora (`512` lotes decimados con arena ESP + RAM PSoC)
  y retomar la SD como una etapa nueva del lado PSoC cuando haya hardware para probar.
- **Se descarta (por ahora) el diseño de streaming continuo de 3 niveles** que el usuario esbozó
  (contador hardware → cola en RAM del PSoC → SD) — el análisis de arriba muestra que alcanza con
  store-then-dump + re-arme encadenado + derrame a SD del ESP cuando corresponda, sin rediseñar todo
  a streaming continuo en vivo (eso reabriría el problema de saturación UART: a D=1 y 2929 Hz el
  tráfico UART crudo ya ronda ~8.8 KB/s contra ~10-11 KB/s útiles del baudrate 115200, muy ajustado
  para sostener en vivo sin el colchón de "muestrear todo primero, volcar después" que ya existe).
- **Guardia obligatoria en el código de armado actual**: una corrida individual de hardware nunca debe
  programar `hw_target > 512`; si el pedido total requiere más, el firmware debe partirlo en trozos
  encadenados y conservar acumuladores/punteros. NUNCA dejar que `cfg_Write((limit>>8)&0x01)` trunque
  en silencio (ej. pedir 599 lotes crudos como una sola corrida truncaría a 87 sin avisar).
- **Pendiente de decisión del usuario** (no bloquea Fase B/hammer): si además de encadenar corridas de
  512 lotes se necesita captura verdaderamente continua/tiempo real sin ningún tope práctico, o si
  "encadenar hasta cubrir la duración pedida, con derrame a SD si no entra en RAM" alcanza. Se
  retoma cuando haga falta una ventana >~5.25 s de verdad (geófono, sesión futura).

## Registro de progreso

| Fecha | Hito | Resultado | Notas |
|-------|------|-----------|-------|
| 2026-07-11 | Código SD-en-PSoC completo (driver + captura ring→SD + dump) | ✅ código / ⛔ build | `sd_spi.h` nuevo + driver SD modo-SPI en `psoc_hw.c` (init CMD0/CMD8/ACMD41/CMD58 con clock lento 187.5kbps→1Mbps, read/write bloque, self-test, CS P2.3 desenganchado del ss hardware vía bypass del puerto — patrón tx1_gpio_detach_dsi; verificado modo 0/MSB en netlist BSPIM). `main.c`: comandos `0xBC SD_STATUS`/`0xBD SD_TEST`/`0xBE SD_CAPTURE`, evento `0x48 SD_STATUS` en boot, y captura a SD gateada por flag: ring de muestras decimadas en `g_capture_raw` (contadores monotónicos ISR/main sin RMW compartido), drenaje concurrente a SD durante SAMPLING, sesiones persistentes (dir LBA 2048 `GDIR` + header `GSES` + datos 5 lotes/bloque), dump UART desde SD transparente (mismo framing), N hasta 60000 lotes con SD. Con SD off el camino RAM-only queda byte-idéntico (handlers ISR clásicos intactos). **NO flasheado**: bloqueado por el fit analógico del TopDesign GEO (ver blocker arriba). |
| 2026-07-11 | ⛔ Blocker: TopDesign GEO no fitea | ⛔ | 4 builds fallidos `apr.M0003` (ruteo analógico) con semillas distintas. Cambio del usuario 23:38 (GEO + SPI + vRef Vdda/2→LPF_2) nunca se buildeó antes de esta sesión. Regen ADC GEO parcial (3000/1020/1020/1020). Necesita GUI de PSoC Creator. Detalle completo en la sección blocker del inicio. **Aclaración posterior**: diffeando el netlist elaborado contra el GEO de campo (commit f59e9e2f, 1020 Hz, fiteaba OK), la topología ANALÓGICA es idéntica (solo cambian números de red por resave); lo nuevo es el SPI (digital) y `Sample_Rate` Config1 3000. La conexión vRef→LPF_2 YA EXISTÍA en el GEO de campo. También se probó re-fitear con el `.cyfit` GEO de ese commit como semilla y un intento con `-q20`: sin éxito. El diseño analógico está saturado (4 PGAs=4/4 SC, 4 opamps=4/4, 2 LPF=2/2) y el router ya convergía "de milagro" antes; el usuario probablemente pueda destrabarlo desde el GUI (effort de placement/routing, o pinear placement analógico previo). |
| 2026-07-11 | Banco COM12: el PSoC del banco ahora es GEO | ✅ dato | `probe` vía USB nuevo firmware ESP: `[PSoC] boot hw=0/GEO`, `fs=1020` — el usuario cambió la placa del banco a la GEO (con SD soldada) y tiene el firmware GEO VIEJO (1020 Hz, sin decimación/encadenado/SD). Coincide con el switch del TopDesign a GEO. Hasta destrabar el fit no se puede flashear el firmware nuevo a esta placa. |
| 2026-07-11 | ESP esclavo: sd_present desde el PSoC + purga SD-en-ESP32 | ✅ código | `psoc_uart.h/.cpp`: comandos 0xBC/0xBD/0xBE + eventos 0x48/0x49/0x4A. `main.cpp`: `g_psoc_sd_status` (evento SD_STATUS del PSoC → HELLO.sd_present; query 0xBC cada 3 s hasta 5 intentos, firmware PSoC viejo la ignora ⇒ sd_present=0), `handleSetConfig` acepta 0xBE (relay al PSoC, expectedAck=param ya correcto), 0xC0 (SD-en-ESP32) rechazado siempre, comandos USB `sdinfo/sdtest/sdcap N`. `platformio.ini`: -DSD_SPI_* eliminados de slave2/3 (sd_storage.* queda stub en TODOS). Builds slave1/2/3 OK. slave1 flasheado a COM12 con flags de banco. |
| 2026-07-11 | Web: decimación global-only + SD oculta + 1/dt + duraciones por tipo | ✅ código | `slave_panel.js`: input de decimación por panel ELIMINADO (queda solo el dot de confirmación; el valor vive en el control global "N (decimación)" que ya existía y se aplica a todos los nodos), fila SD invisible salvo `sd_present=1` (en HAMMER no aparece nada). `config.js`: `SUBCMD_SD_CAPTURE=0xBE` (SD del PSoC), `SUBCMD_SD_ENABLE=0xC0` marcado obsoleto, `CMD_SET_RECLEN_HAMMER=0xAD`. `app.js`: toggle SD → 0xBE; inputs "Duración GEOs" + "Duración HAMMER" (vacío/0 = igual a GEOs), `sendHammerRecLen()` antes de START y de VER, persistencia localStorage, preview muestra ambos largos. `plot.js`: `1/dt` (Hz) debajo del `dt` del cursor B. `index.html`: labels nuevos. |
| 2026-07-11 | Maestro: duración por tipo (H4 Fase A) | ✅ código | `main.cpp`: `g_rec_n_batches_hammer` (0=legado byte-idéntico), `nBatchesForNode()` por `hw_class` cacheado, `broadcastRecordLength/Prestart` = broadcast canónico + unicast override SOLO a HAMMERs conocidos con largo distinto, corte de DUMPING y NACK-skip por `nBatchesForNode(g_dumpSlaveIdx)`, VER usa `nBatchesForNode(node)`, timeout de rescate usa el largo MAYOR, comando web `0xAD` (SET_RECLEN_HAMMER). `pio run -e esp32dev` OK. Invariante preservada: sin 0xAD (o =0) todos los caminos ejecutan exactamente el código anterior. NOTA: el fix `applyGlobalFs` por-nodo del checklist H4 quedó OBSOLETO a propósito — con decimación GLOBAL todos los nodos comparten Fs por diseño. |
| 2026-07-11 | Script reconexión GeoNetwork | ✅ | `master/reconnect_geonetwork.py`: espera SSID visible → `netsh wlan connect` → verifica `/health`. Encadenable: `pio run -e esp32dev -t upload && python reconnect_geonetwork.py`. Perfil WiFi GeoNetwork confirmado en esta PC. |
| 2026-07-11 | Regresión banco COM12: ESP nuevo + PSoC GEO viejo | ✅ | Con el firmware ESP nuevo (sd_present-desde-PSoC + purga SD-ESP32): `probe` OK (`hw=0/GEO`, `fs=1020`), `sdinfo` contra PSoC viejo (sin 0xBC) queda sin respuesta y `sd_present=0` sin efectos colaterales (camino negativo diseñado), `cap 5` limpio: `SETN ack val=5` → `HOT_WAIT ready` → `FULL -> STOPPED (5 batches)` → `DUMP_DONE`, `fill=5/5`, `bBad=0`. Dos gotchas de banco documentados: (1) el PSoC GEO viejo corre calibración PI **en cada boot** y tarda varios minutos (mientras tanto rechaza SETN — el primer `cap` falló por eso); (2) `PSOC_AUTO_CAL_ON_READY=0` puesto en platformio.ini para no re-disparar esa cal eterna en cada reset del ESP (⚠ decidir antes de campo si vuelve a 1). El PSoC del banco se puede resetear sin tocar nada con ppcli: `SetAcquireMode Reset` + `DAP_Acquire` + `DAP_ReleaseChip` (KitProg `CMSIS-DAP/236111`). |
| 2026-07-10/11 | Encadenado PSoC + arena ESP RAM-only | ✅ | PSoC build OK (`42302 B` flash, `49088 B` SRAM) y flash ppcli OK en `KitProg (CMSIS-DAP/248355)`, filas `0..165`, log `%TEMP%\psoc_program_chain_arena_20260710_230805.log`. ESP esclavo `slave1` subido a COM12 con flags de banco; arena paginada de 32 lotes por página. Prueba real (`debugpsoc 0`, `stream 0`, `decim 3`): `cap 360` -> `FULL -> STOPPED (360 batches)`, `DUMP_DONE`, status `bBad=0 fill=360/360 fs=976`, tiempo sync->dump ~14.08 s. `cap 512` -> `store arena n=512 pages=16`, `FULL -> STOPPED (512 batches)`, status `bBad=0 fill=512/512 fs=976`, tiempo sync->dump ~20.03 s. Este es el nuevo estado conocido-bueno de COM12. |
| 2026-07-10/11 | Corrección de bug `cap`/SETN en ESP esclavo | ✅ | Durante prueba USB, `cap 360` llegó a fallar como `fill=60/360` porque la ruta `cap` podía arrancar antes de confirmar que el PSoC procesó el nuevo `SETN`; quedaba usando el largo anterior. Se agregó espera corta de `PSOC_EVT_SETN` en `enterHotWait()` antes de `preStart()`, con contador de eventos porque el valor se satura a 255 para `N>255`. Tras el fix, `SETN ack val=255` aparece antes de `HOT_WAIT` en 360/512. |
| 2026-07-10/11 | Web/GUI Max 512 + preservados con Fs propia | ✅ código / ⏳ upload | Código web/maestro actualizado: `PSOC_CAPTURE_MAX_BATCHES=512`, botón `Máx (512 lotes)`, tooltip "ESP32 + PSoC"; plot y spectrum usan `overlay.fs` para preservados, evitando que una traza preservada a 2929 Hz se reescale mal al cambiar el vivo a `N=3`. `pio run -e esp32dev` había compilado OK. **No subido a COM8 en esta tanda** para respetar la advertencia del usuario: reprogramar maestro corta GeoNetwork y requiere reconexión manual. |
| 2026-07-10/11 | Corrección final SD: va en PSoC | ⚠️ pendiente | El usuario corrigió que la SD va en el PSoC (SPI Master cableado en TopDesign), no en ESP32. El código `slave/src/sd_storage.*` de la tanda anterior queda obsoleto/histórico. Próxima sesión SD: diseñar e implementar PSoC->SD; no continuar ampliando SD-en-ESP32 sin reabrir diseño. |
| 2026-07-10 | H0 | ✅ | Plan aprobado por el usuario; archivo creado. Usuario ya regeneró el ADC a 2929 Hz en PSoC Creator (GUI) antes de empezar esta sesión de código. |
| 2026-07-10 | Hallazgo techo 512 lotes | ⚠️ histórico | Ver sección de arriba. No bloquea Fase B con hammer (3s=293 lotes crudos < 512). Esta fila originalmente decía "encadenamiento + SD en ESP32"; queda superada: el encadenamiento ya fue validado en H7 y la SD se retoma en PSoC. |
| 2026-07-10 | H1 código PSoC | ✅ | `psoc_adc.c/.h` (fs=2929/factor, set/get_decimation), `main.c` (acumulador decimación en sm_sample_capture_raw/filt tras g_fir_discard, guardia 512 lotes crudos en psoc_arm/psoc_enter_sampling con exención para rampa debug, PSOC_CMD_SET_DECIMATION=0xBB), `psoc_hw.h`. Build OK (flash 41094B/15.7%, SRAM 49088B/74.9%, sin warnings). Flasheado y verificado OK vía ppcli (filas 0..160, `psoc_program_decimation_20260710_160635.log`). Pendiente: prueba de banco por USB (bloqueada por H2). |
| 2026-07-10 | Corrección de alcance (usuario) | ✅ | (1) Maestro SIN SD — manda a la web en lotes chicos, se descarta diseño de "buffer de relevo" y el límite `min(SD esclavo,SD maestro)`. (2) SD solo en esclavos GEO (no genérico a cualquier esclavo). (3) Evaluado con el advisor mover el promedio de decimación a Verilog/superMaquina aprovechando UDB libre (Datapath Cells 4/24, Control Cells 5/24) — DESCARTADO: el paso que falta (dividir por un factor D configurable no potencia de 2) necesita una máquina de estados que consume P-terms, el recurso más ajustado (312/384, el mismo que hizo fallar los 2 intentos previos de Verilog); además tocaría el TopDesign y la política de eventos determinismo-primero ya validada. Decimación queda 100% software. Documento y checklist (H5) actualizados. |
| 2026-07-10 | H2 código ESP esclavo + prueba de banco H1+H2 | ✅ | `psoc_uart.h/.cpp`: `PSOC_CMD_SET_DECIMATION=0xBB` + `setDecimation()`. `main.cpp`: comando USB `decim N` (patrón calcado de `range N`) + campo `fs=%u` agregado a `logPsocUartDiag()` (antes no se podía ver la Fs efectiva por USB). Build `pio run -e slave1` OK. Subido a COM12 (HAMMER real) con flags de banco (`SLAVE_USB_CMD_ENABLE=1 SLAVE_LAB_TOOLS_ENABLE=1 SLAVE_LOGS_ENABLE=1 DBG_HUMAN=1`). **Prueba de banco COM12 — TODO OK**: tras un reset explícito del PSoC (`ToggleReset`, necesario porque tras programar con ppcli el PSoC no arrancaba solo — no relacionado con el firmware) y esperar a que la auto-calibración terminara (tardó ~4 min esta vez, fuera de lo habitual pero dentro del watchdog de 400s de `calibration.c`, código no tocado por esta feature — posible tema a revisar en otra sesión, no bloqueante), captura RAW y FIR con `decim 1/2/3` — todas `FULL -> STOPPED`, `bBad=0`, `fill=N/N`. `FS_REPORT` verificado exacto vía el nuevo campo `fs=`: `decim 1→2929`, `decim 2→1464`, `decim 3→976`, `decim 5→585` (=2929/factor con división entera, como se esperaba). Un timeout aislado de ACK en el primer `decim 1` tras un reset de ESP (no reproducido en los intentos siguientes) — no bloqueante, anotar si se repite. Factor dejado en 1 (reposo seguro) al terminar. |
| 2026-07-10 | Observación no bloqueante | ⚠️ | Auto-calibración del PSoC (HAMMER, `calibration.c`, código NO tocado por esta feature) tardó ~4 minutos en una corrida durante las pruebas de banco (se recuperó con `stop` a los ~4 min, dentro del watchdog de 400s pero mucho más lento que los ~8-30s históricos documentados). No se identificó relación con los cambios de esta sesión (calibration.c no llama `psoc_adc_effective_fs_hz()` ni depende de la Fs del ADC). Podría ser específico de este PSoC/banco hoy. Si se repite en sesiones futuras, investigar aparte — no es parte del alcance de decimación/2929Hz. |
| 2026-07-10 | Corrección de alcance SD (usuario, 2da) | ✅ | La SD de los esclavos GEO NO está forzada a software puro — usar el periférico SPI hardware del ESP32 (`SPI.begin()`/`SD.h`, con DMA) si mejora throughput; lo único obligatorio es que la lógica de derrame/filesystem viva en el ESP32 (no en el PSoC, por las razones de SRAM/PLD ya documentadas). Sección "SD: descartado en el maestro" y checklist H5 actualizados. |
| 2026-07-10 | Checkpoint Fase A (H4) — pausada deliberadamente | ⏸️ | Consultado con el advisor antes de tocar `master/src/main.cpp`: a diferencia de H3 (aditivo), H4 modifica el corte del loop `DUMPING` (`g_rec_n_batches` compartido, `main.cpp:1548`), máquina de estados validada en hardware (11/11 OK) e intestable hoy (sin GEO conectado, maestro no reflasheable sin el usuario presente) — coincide con la regla explícita del usuario de probar antes de avanzar. Diseño acotado a 2 puntos de cambio (`nBatchesForNode()` en envío + corte de dump) documentado en H4 para la próxima sesión con GEO presente, sin tocar código todavía. |
| 2026-07-10 | H5 código esclavo+protocolo+web (SD opcional GEO) | ✅ | Nuevo módulo `slave/src/sd_storage.h/.cpp` (stub no-op si `SD_SPI_CS_PIN` no está definido — HAMMER no compila SD real). `slave/platformio.ini`: pines SPI SD solo en `slave2`/`slave3`. Protocolo: `SLAVE_CMD_SET_SD_ENABLE=0xC0` (sub_cmd local al ESP, no PSoC) + `MsgHello.sd_present` (campo nuevo al final del struct, tolerado por el parseo ya length-tolerant de `espnow_rx.h` vía `MSG_HELLO_LEGACY_BYTES`) — actualizado en AMBAS copias de `sync_protocol.h` (slave y master). `main.cpp` esclavo: `clampPsocCaptureBatches()`/`allocStore()`/`onBatch()`/`handleReqBatch()`/`storeReadyForHotWait()` con rama SD (derrame TOTAL, no incremental — ver nota en H5), gateado por `sdStorageEnabled()` que es `false` por defecto y siempre `false` en HAMMER: la rama nueva es código estrictamente inalcanzable en cualquier escenario que corre hoy (HAMMER, o GEO con SD off, o `n≤360`), así que no hay superficie de regresión sobre el camino validado. `main.cpp` maestro: `CachedHello.sd_present` + `sendHelloNotif()`/`matlab_transport.h` con subtipo `0x07` nuevo (mismo patrón que `hw_class`=0x06). Web: `config.js` (`SUBCMD_SD_ENABLE`), `protocol.js` (`helloSdPresent`), `data_store.js` (`sdPresent`/`sdEnabled`), `slave_panel.js` (checkbox+dot+label, deshabilitado hasta `sd_present=1`), `app.js` (`onSdEnabledChanged`/ACK/HELLO sub 0x07 → `panel.setSdPresent()`), `export.js` (`sd_present`/`sd_enabled` en metadata, no en CSV, mismo criterio que `decimation_factor`). `pio run` OK en los 4 envs (`slave1/2/3`, `esp32dev`) — `slave2` con SD real creció ~59KB de flash (confirma que `SD.h`/`SPI.h` se linkearon de verdad, no quedaron fuera por macro). **Hallazgo importante**: el motor queda completo pero NO alcanzable desde la web hoy — ver nota debajo del checklist H5 (acoplado a Fase A/H4). **No subido a ningún puerto** (slave2/slave3 no tienen hardware conectado hoy; slave1/HAMMER no lleva este código). |
| 2026-07-10 | Regresión de banco HAMMER (COM12) tras H5 | ✅ | El usuario no tiene SD para probar hoy — pidió probar "lo demás" primero. Reflasheado `slave1` (HAMMER, flags de banco) a COM12 con el código de H5 y corrida `test_h5_regression.py`: `cap 1/5/10/200/360` en RAW y FIR, `decim 1/2/3` (fs exacto 2929/1464/976), `cap 400` → clampeado correctamente a `store alloc n=360` (ejercita la rama nueva `if (sdStorageEnabled())` dentro de `clampPsocCaptureBatches()`, que cae al comportamiento viejo porque `sdStorageEnabled()` es `false` en este firmware sin SD), `stop` a mitad de una captura de 200 lotes → reset limpio a `fill=0/0` (ejercita `allocStore(0)`+`sdStorageEndSession()` stub). `bBad=0` en todas las corridas, sin regresiones. Confirma que los cambios compartidos de H5 (`allocStore`/`onBatch`/`handleReqBatch`/`storeReadyForHotWait`/`clampPsocCaptureBatches`) no rompieron el camino RAM-only que usa HAMMER — la invariante de diseño ("SD off/no compilada ⇒ comportamiento idéntico al de antes") quedó verificada empíricamente, no solo por inspección. Dejado en reposo: `decim 1`, `stream 0`. |
| 2026-07-10 | H3 subido a COM8 + prueba end-to-end web→maestro→esclavo | ✅ | Usuario autorizó el flash de COM8 (dos intentos de `pio run -t upload` fallaron con "No serial data received"/esptool no pudo entrar a bootloader — el usuario lo programó manualmente sosteniendo BOOT, confirmó "Ya programé"). Tras reconexión del usuario al WiFi del maestro, prueba **sin navegador**: script Python (`test_master_ws.py`, librería `websocket-client`) abre `ws://192.168.4.1/ws` y decodifica paquetes binarios de 6 bytes igual que `protocol.js`. Resultados: (1) HELLO cacheado confirma `hw_class=1/HAMMER`, `fs_exact=2929Hz`, y el campo **nuevo `sd_present=0`** llega correcto (confirma el wire-format H5 extendido — `MsgHello.sd_present` → `CachedHello` → `sendHelloNotif` sub 0x07 → `protocol.js helloSdPresent` — funciona end-to-end real, no solo compilado). (2) `{"cmd":"BD","node":1,"sub":"BB","param":2}` (decimación factor 2 vía WS, mismo JSON que manda `sendDirected()` de `app.js`) → `ACK sub=0xBB val=1` en <1s: confirma el camino completo web→`web_relay.h`→ESP-NOW→`handleSetConfig()` (con el fix de whitelist de H3) →PSoC→ACK de vuelta, con hardware real. (3) Decimación factor 1 (reposo) → ACK val=1 igual de limpio. (4) `{"cmd":"BD","node":1,"sub":"C0","param":1}` (SD enable en HAMMER) → `ACK val=0`, rechazo correcto porque HAMMER no compila `SD_SPI_CS_PIN` — confirma que el sub_cmd `0xC0` nuevo de H5 viaja bien por el mismo camino y falla seguro en un nodo sin SD, tal como se diseñó. Sin errores en ninguna prueba. H3 queda 100% validado en hardware real (no solo USB directo); H5 queda validado en su "camino negativo" (rechazo correcto sin SD) — el camino positivo (SD real habilitada) sigue pendiente de hardware. |
| 2026-07-10 | H6 diseño cola PSoC↔ESP (Fase D) | ✅ | Documentado, NO implementado (por diseño — era el pedido explícito del usuario). Sección "Diseño abierto" agregada bajo H6: motivación original del usuario (3 contadores/etapas), estado actual sin flow-control PSoC→ESP, boceto de protocolo (`PSOC_CMD_QUEUE_MODE`/`PSOC_CMD_QUEUE_PULL`), y por qué no se prioriza frente a H5/SD (que ya resuelve el caso de uso real con mucho menos riesgo — sin protocolo nuevo, sin competir por la SRAM ya ajustada del PSoC, sin romper el modelo store-then-dump). Recomendación: no implementar salvo que aparezca el caso de borde concreto (GEO sin módulo SD que igual necesite capturas largas). |
| 2026-07-10 | H3 código maestro+web (decimación por nodo) | ✅ | Maestro C++ no necesitó cambios (`handleDirectedCmd()` ya relayaba cualquier `sub_cmd` no especial-caseado vía `MsgSetConfig`). **Hallazgo importante**: el ESP esclavo SÍ necesitaba un cambio — `handleSetConfig()` tiene su propia whitelist de `sub_cmd` y no incluía `0xBB` (el `decim N` de banco probado en H2 usaba un camino directo a `psoc.setDecimation()`, no este switch); sin el fix, el maestro/web hubiera mandado el comando y el esclavo lo habría rechazado en silencio. Agregado `case PSOC_CMD_SET_DECIMATION` + `isDecimationFactor()` en los 2 switches de `handleSetConfig()`, mismo patrón que `ADC_CONFIG`. Re-subido a COM12 con el fix. Web: `config.js` (`SUBCMD_DECIMATION`, `DEFAULT_SAMPLE_RATE_HZ`→2929, `ADC_CONFIGS[].fsHz`→2929), `data_store.js` (`nd.decimationFactor`), `slave_panel.js` (input+dot+label, `setDecimation()`/`setDecimationLock()`), `app.js` (`onDecimationChanged`, ACK, resend-all encadenado PGA→ADC→decim, restore de localStorage, `applyNodeDecimation()`), `export.js` (`decimation_factor` en metadata, no se tocaron las columnas CSV — queda pendiente si se quiere en el CSV además de en el JSON de metadata). `pio run -e slave1`/`-e esp32dev` OK; JS revisado a mano (sin Node.js en esta máquina para lint automático) — sin problemas encontrados. **No subido a COM8** (falta confirmación del usuario, tira el WiFi/AP). |
| 2026-07-11 | Diagnóstico GeoNetwork tras reprogramación usuario | ⚠️ | Maestro COM8 accesible por GeoNetwork (`/health` OK, LittleFS OK, IP cliente 192.168.4.2). Un probe `ws_capture_test.py --batches 360` quedó interrumpido y dejó al maestro en `DUMPING`; se recuperó sin reprogramar con `A7 param=0` (debug off, fuerza estado a `IDLE`) + `AE value=0` (limpia `g_rec_n_batches`). Intento posterior de `ARM n=1` quedó en `ARMING` durante 65 s: no llegó `ARM_ACK` del esclavo por ESP-NOW (`READY n=0`). Los STATUS cacheados del nodo 1 siguen mostrando `fs=0x0B71=2929`, pero `link_rssi` reporta RSSI/age `null`, consistente con enlace esclavo→maestro no fresco. No continuar con `cap 360`/encadenado hasta recuperar ARM_ACK; revisar que COM12 tenga firmware de esclavo correcto, NODE_ID esperado, canal/WiFi/ESP-NOW y alimentación. |
