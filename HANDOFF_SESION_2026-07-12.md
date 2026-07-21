# HANDOFF — Sesión 2026-07-11/12 (auditoría pre-campo + SD PSoC + encadenado)

> **Para la próxima sesión (Claude/codex): leer esto PRIMERO.** Complementa
> `docs/plan_pruebas_precampo.md` (matriz de pruebas y hallazgos, la referencia fina) y
> `docs/plan_2929_decimation_sd.md` (historia de decimación/SD). Rama: `codex/capture-engine-verilog`.

## 1. Qué es el sistema hoy (foto completa)

- **PSoC5LP** (GEO, `firmware/psoc/AcondicionamientoAnalogico.cydsn`): ADC 2604 Hz nativo (4 configs
  de rango, assert de compilación), decimación con promedio en ISR (0xBB, 1..100, Fs=2604/N),
  captura RAM 512 lotes con **encadenado** (>512 crudos re-arma superMaquina sin resetear, un solo
  DUMP_DONE al final), **SD FatFs** (SPI Master del TopDesign, GEOLAST.BIN, hasta 60000 lotes ≈
  11.5 min a 2604 Hz), comandos SD UART: 0xBC status / 0xBD selftest / 0xBE captura-a-SD /
  0xBF leer lote. Build actual: Flash 64700 B, SRAM 79.3 %, filas 0..252, flasheado y validado.
- **ESP32 esclavo** (COM12, `slave/`, env slave1 NODE_ID=1): UART al PSoC, ESP-NOW al maestro,
  arena RAM paginada (512 lotes), jerarquía **ESP RAM → encadenado PSoC → SD PSoC**.
  Comandos de banco USB (SLAVE_LAB_TOOLS): probe/status/cap/decim/stream/sdcap/sdinfo/sdtest/
  **sdread N** (lee lote N de la SD por 0xBF e imprime por USB — mismo camino que REQ_BATCH).
- **ESP32 maestro** (COM8, AP GeoNetwork/192.168.4.1): relay stop-and-wait REQ_BATCH con
  `dumpBatchesForNode()` (N efectivo por HOTWAIT_ACK), pausa/reanuda dump según cliente WS,
  duración por tipo (0xAD HAMMER, clamp RAM), web LittleFS.
- **Web**: N (decimación) global, Duración GEOs/HAMMER, **Máx RAM (512)** y **Máx SD (60000)**,
  panel esclavo con SD auto-oculta y decimación como indicador.

## 2. Validado en hardware ESTA sesión (todo por radio/WS salvo E9)

E1 RAM 4 lotes ✅ · E2 SD 600 ✅ · E3 SD 3000 ✅ · E6 decim-2 radio 3000/3000 ✅ ·
E6b FIR radio 3000/3000 ✅ · E7 0xBE ✅ · E8 0xAD ✅ · E9 USB estricto 33/33 ✅ ·
E10 UI Chrome ✅ · E12 reconexión WS ✅ · E13 STOP vivo ✅ · E14 operador UI ✅ ·
E15 SD 60000 ✅ · E16 transiciones rango/decim 49/49 ✅ · E17 power-cycle+recovery 30/30 ✅ ·
E18 mini-soak 5/5 ✅ ·
**E5b: captura de 10 min PERFECTA (52080 lotes a SD, F1 fix validado) + dump 93.2 % impecable**
(el corte fue del cliente Python, F5). Un E5c heredado tampoco sirve como aceptación: la SD
capturó 52080/52080, pero el archivo del cliente terminó truncado en 147451/1562400 muestras.
**La repetición final E5c cerró PASS E2E:** 52080/52080 lotes en SD, 1562400/1562400
muestras por radio, 4687200 bytes, una conexión, cero desconexiones, cleanup limpio y SHA-256
recalculado coincidente. Ver evidencia completa en §5.

Además quedó verificado en banco:

- builds limpios del maestro (`pio run -e esp32dev`) y esclavo (`pio run -e slave1`): **PASS**;
- `uploadfs` del W6 a COM8: **PASS**, reconexión nativa con `WlanConnect` y `/health`: **PASS**;
- UI publicada real: Máx RAM pone input **5.89 s**, calcula **512 lotes**, muestra preview real
  **5.90 s** y la consola del navegador no reportó errores;
- W7 cambia el `step` de Duración GEO de 0.1 a **0.01** para que 5.89 sea editable sin que el
  control HTML lo considere inválido. El segundo `uploadfs` pasó, la imagen fue verificada y
  el HTML servido confirmó `step=0.01`;
- gate USB persistente `usb_regression_test.py`: **33/33 PASS** sobre COM12, incluyendo RAW
  d1/d3, SD+`sdread`, FIR d2, ACKs, restauración y probe final PSoC IDLE/fs=2604/fill=0;
- repetibilidad E2E corta con el mismo nombre de salida y `--force`: **10/10 PASS**, cada ciclo
  con 120/120 muestras, 360 bytes, extra=0, una conexión, cero desconexiones y cleanup limpio;
- E12 (corte WS inyectado durante dump): **PASS exacto**, reconectó una vez y terminó
  18000/18000 muestras, 54000 bytes, extra=0, SHA coincidente y cleanup limpio;
- E13 (STOP en vivo): **PASS** tanto en RUNNING como en DUMPING, en el mismo socket, y ambos
  casos quedaron seguidos por un smoke 120/120 limpio. El detalle operativo importante del
  STOP durante RUNNING está en §4.8 y §5.

## 3. Bugs encontrados y su estado (detalle en plan_pruebas_precampo.md)

| ID | Qué | Estado |
|----|-----|--------|
| F1 | Watchdog SYNC_STALL re-disparaba START_NOW y destruía sesiones SD largas (causa raíz del "10 min = 0 muestras") | ✅ CORREGIDO (esclavo `a85565c1`) y validado en E5b |
| F5 | Tool WS sin watchdog de silencio → colgado en socket half-open | ✅ base `7e4e332b`; endurecimiento pre-DATA + self-test en `8c80a15e`; reconexión real validada en E12 |
| F7 | `--force` podía dejar un JSON viejo asociado a un binario nuevo/truncado si la corrida abortaba temprano | ✅ CORREGIDO en el tool: invalida metadata antes de truncar y prueba también el orden seguro ante fallo de unlink |
| H3 | 3.6 % lecturas SD >250 ms → NACKs | ✅ timeout **250→450 ms ya aplicado** en `a85565c1` (los picos son ~1.2-1.5 s, el retry salva SIEMPRE) |
| W1 | Botón Máx RAM no existía | ✅ agregado |
| W6 | Máx RAM 513 lotes (ceil) | ✅ floor (`c7414403`), publicado por `uploadfs` y validado en UI real: 5.89 s/512 lotes |
| W7 | Input Duración GEO con `step=0.1` marcaba 5.89 como inválido | ✅ `step=0.01` en `8c80a15e`, publicado y verificado en COM8 |
| F2 | ACKs muestran value&0xFF (600→88) | 📝 cosmético, documentado |
| F6 | 0xBB/0xBE puede devolver ACK 0 transitorio al reconfigurar | ✅ MITIGADO EN TOOL: máximo 2 intentos dirigidos, ACK filtrado por timestamp y evidencia por intento; E13 observó BE 0→1 real |
| W3 | STOP durante dump: sin re-dump desde UI (datos quedan en SD) | 📝 documentado |
| W5 | Preview N usa input, no ACK | 📝 documentado |
| H4 | Prefetch de bloque en PSoC = dump ~2× más rápido | 📝 mejora post-campo |
| F8 | Contador `drop`/`_syncDrops` del esclavo (bytes UART descartados por el framer) bloqueaba criterios de tests aunque fuera benigno | ✅ CORREGIDO en `sd_max_regression_test.py`: solo bBad/badLen bloquean |
| F9 | **CRÍTICO — START rompía el nodo (roto hasta reset físico), SIEMPRE, cualquier N** | ✅ CORREGIDO y validado E2E en hardware — ver §3.1 |

### 3.1 F9 en detalle — START rompía el nodo

**Síntoma reportado por el usuario**: VER funcionaba siempre (N=1, Máx RAM, +20% encadenado),
pero START no funcionaba nunca y dejaba el sistema roto — requería reiniciar el nodo.

**Causa raíz** (confirmada con driver WS dirigido + logger COM12): el maestro espera el
HOTWAIT_ACK de un esclavo con `HOTWAIT_QUERY_TIMEOUT_MS=120 ms`, pero la confirmación real de
"PSoC ARMADO" (`PSOC_EVT_ARMED` por UART) tarda ~130 ms — más que el timeout. El primer query
del maestro casi siempre llega antes y recibe `ok=0`. La rama de retry del flujo START normal
(no-VER) entonces **volvía a mandar `broadcastPrestart()` completo**, forzando al esclavo a
reenviar SETN (0xA3 UART) por segunda vez. Pero el PSoC, una vez en `PSOC_ARMED`, entra en
silencio UART total por diseño (`service_runtime()`: ventana de muestreo sin RX/TX/LED/pings).
El segundo SETN nunca se ackea, vence a los 500 ms, y el esclavo interpreta el timeout como
fallo: libera el store (`allocStore(0)`) y pasa a `STOPPED` — mientras el PSoC físico sigue
armado de verdad, sordo, esperando un flanco SYNC que nadie volverá a mandar. Nodo roto hasta
`ToggleReset`. El ciclo se repetía cada ~522 ms mientras el maestro seguía reintentando.
VER nunca mostró el bug porque su rama de retry (`PRESTART_ACTION_VER`) solo re-consulta, sin
re-emitir PRESTART — la carrera 120 ms vs 130 ms es casi determinística, por eso rompía siempre
y sin depender de N.

**Fix (dos capas)**:
1. `master/src/main.cpp`: el retry de HOT_WAIT del flujo START ya no re-emite
   `broadcastPrestart()`, solo re-consulta (alineado con VER).
2. `slave/src/main.cpp`: `CMD_PRESTART` es idempotente — si el nodo ya está `HOT_WAIT` con el
   store listo para el mismo N, responde el ACK directo sin repetir `enterHotWait()`/SETN.

**Validación E2E en hardware**: reflash esclavo+maestro, ToggleReset+auto-cal, reconexión
WiFi. Runner persistente `master/start_flow_regression_test.py` (self-test 4/4): START
pequeño (261 lotes/3 s) **PASS** 7830/7830; START encadenado SD (600 lotes) **PASS**
18000/18000; 3 repeticiones consecutivas adicionales **3/3 PASS**; log COM12 de las 4
corridas con **0 SETN_TIMEOUT, 0 HOT_WAIT_ABORT**. VER (regresión) sigue PASS. Probe final
limpio. Evidencia: `master/artifacts/f9_start_flow_pass.json`.

## 4. Trampas operativas (¡leer antes de tocar el banco!)

1. **Reflashear el ESP esclavo cuelga el PSoC** → SIEMPRE `ToggleReset` por KitProg después
   (`GetPorts` → runfile con `ToggleReset 0 100`, ver `firmware/psoc/BUILD_PROGRAM_PSOC.md`).
2. **Tras ToggleReset esperar la auto-cal (~10-60 s)** antes de mandar configs (0xBB/…): si no,
   el PSoC no ackea en 750 ms y el esclavo NACKea (parece bug y no lo es).
3. **Prefijos de log del esclavo = `micros()`, dan la vuelta a los 4294.97 s** — un salto de
   timestamp NO es un reboot.
4. **Reflashear/uploadfs el maestro tira el AP** y en esta máquina `netsh wlan connect` está
   bloqueado; ejecutar desde `firmware/esp32/Nodo comunicación/master`:
   `python reconnect_geonetwork.py --timeout 120`. El script usa **WlanConnect por ctypes**
   (perfil `GeoNetwork`, sin escaneo) y no termina OK hasta que
   `http://192.168.4.1/health` responde con `littlefs=ok`. Si el AP no vuelve: pulso RTS por
   COM8 (reset estilo esptool) y reintentar.
5. **`ws_capture_test.py` fuerza decim=1** (hardcodeado): no sirve para probar captura decimada
   por radio — usar driver WS propio (patrón en scratchpad `ws_directed.py`, secuencia
   BB→A2→AE→B2 y contar DATA).
6. **No abrir la web UI mientras corre un test WS por consola**: pelean el takeover del socket.
7. pyserial a COM8/COM12 SIEMPRE con `dtr=False; rts=False` (si no, resetea el ESP).
8. **STOP durante RUNNING no cancela instantáneamente la captura SD dentro del PSoC**: el
   maestro vuelve a ARMED y ACKea STOP=0, pero el PSoC termina en segundo plano la sesión ya
   iniciada y mientras tanto puede rechazar 0xBB/0xBE. Antes del siguiente ARM, esperar de
   forma conservadora la duración nominal configurada **+5 s**. Para 600 lotes a 2604 Hz:
   600×30/2604 = 6.912 s; E13 esperó **11.912 s** y el smoke posterior pasó.

## 5. Estado del banco AL CIERRE + aceptación E5c

### Evidencia E5c heredada (NO PASS)

En el scratchpad heredado **no existe** `e5c_geo10min.json`. Sólo quedó
`e5c_geo10min.i24le`, truncado en **442353 bytes = 147451/1562400 muestras**. Por eso ese
intento no puede cerrar la aceptación. El log `e5c_com12.txt` sí prueba que la adquisición
física terminó completa en SD:
**52080/52080 lotes**, con **0 `SYNC_STALL` y 0 `SD_ERROR`**. Esto vuelve a validar F1 y la
captura SD, pero no el transporte E2E ni el conteo final del cliente. La auditoría de cierre
encontró además que el reloj de silencio de F5 comenzaba recién con el primer DATA: `8c80a15e` lo
inicia con el ACK `VER/B2=2`, cubre también el estado pre-DATA, fuerza reconexión/takeover a
los 20 s y tiene un self-test específico que pasa.

La repetición final se ejecutó como `e5c.i24le`; al cerrar se movieron el binario y JSON crudos
al scratchpad como `e5c_final_geo10min.i24le/.json`. El JSON persistente y versionado es
`firmware/esp32/Nodo comunicación/master/artifacts/e5c_geo10min_2604_pass.json`; el log paralelo es
`e5c_rerun_com12.txt` en `%TEMP%/claude/C--Github-Tesis/8e89e144-*/scratchpad/`.

<!-- E5C_FINAL_BEGIN: CERRADO 2026-07-12 -->
> **E5c FINAL: ✅ PASS — SISTEMA DEL BANCO LISTO PARA CAMPO.**
>
> JSON: `artifacts/e5c_geo10min_2604_pass.json` · `status="ok"` · `error=null` ·
> `expected_samples=samples_written=1562400` ·
> `bytes_written=actual_file_bytes=4687200` · `extra_samples=0` ·
> `final_cleanup_ok=true` · `cleanup_errors=[]` · 1 conexión/0 desconexiones ·
> tiempo total 2626.472 s · SHA-256 recalculado:
> `6332b571f9f688ef828b23906d51cdc0d82c1e5b294a3f522a34cacfeedd64db`.
<!-- E5C_FINAL_END -->

El log COM12 final contiene 0 `SYNC_STALL`, 0 `SD_ERROR` y una sola confirmación de
`SD_SESSION 0x01`/`VIEW SD complete=1 err=0 fill=52080/52080`. Durante el dump registró 2449
timeouts en 1230 secuencias (2.36 % de 52080): 1219 secuencias con dos timeouts, 11 con uno y
ninguna con más de dos; todos los lotes terminaron recuperados.

El único criterio correcto de PASS es verificar **todos** estos campos del JSON, no solamente
el tamaño aparente del archivo:

- `status == "ok"` y `error == null`;
- `expected_samples == samples_written == 1562400`;
- `bytes_written == actual_file_bytes == 4687200`;
- `extra_samples == 0`;
- `final_cleanup_ok == true` y `cleanup_errors == []`;
- `sha256` es un digest hexadecimal de 64 caracteres y coincide con el SHA-256 recalculado
  sobre el `.i24le`.

### Estado operativo restante

- W6 y W7 están publicados y verificados. El segundo `uploadfs` validó el hash de la imagen;
  `WlanConnect` recuperó GeoNetwork, ping respondió 4/4 (3-5 ms), `/health` devolvió
  `littlefs=ok` y GET del HTML/JS confirmó `step=0.01`, botón Máx RAM y el floor W6.
- El PSoC quedó flasheado con el build SD validado; el esclavo con F1+H3+`sdread`; maestro y
  esclavo compilan PASS. F5 pre-DATA+self-test, W7, la aclaración del script de reconexión y
  el JSON E5c persistente están en `8c80a15e`. Un smoke post-upload con ese tool pasó 120/120,
  HELLO `psoc_ok=1`, Fs=2604, SD presente y cleanup limpio.
- Probe final COM12 con DTR/RTS desactivados: `psoc=1`, `fs=2604`, `bBad=0`, estado IDLE y
  `fill=0/0`. El smoke E11 usa SD y dejó `GEOLAST.BIN` con la sesión corta de 4 lotes; la
  captura larga E5c ya está preservada íntegra en el scratchpad y su JSON en el repo.
- **Gate USB ampliado:** `usb_regression_test.py` cerró **33/33** checks. Verificó preflight,
  RAW d1 (60/60), RAW d3 (60/60 a fs=868), captura SD de 100 lotes con `sdread 0/99` y rechazo
  fuera de rango 100, FIR d2 (30/30 a fs=1302), ACKs BB/B7/BE sin retry y cleanup final a
  PSoC IDLE, fs=2604, fill=0/0 y `bBad=0`.
- **Repetibilidad y metadata:** diez ejecuciones consecutivas de 4 lotes sobre el mismo
  `repeat_e2e.i24le/.json`, siempre con `--force`, pasaron 10/10 (120 muestras/360 bytes,
  extra=0 y cleanup limpio). El tool ahora elimina primero el JSON previo y recién después
  trunca el binario; el self-test cubre tanto esa invalidación como el fallo seguro de unlink.
- **E12 reconexión real:** se cortó deliberadamente el socket después de 3000 muestras. El
  resultado fue `status=ok`, conexiones=2, desconexiones=1, 18000/18000 muestras, 54000 bytes,
  extra=0, SHA-256 recalculado coincidente y cleanup final limpio.
- **E13 STOP durante RUNNING:** STOP se envió por el mismo socket en estado RUNNING, antes de
  DATA; ACK=0, retorno del maestro a ARMED, 0 muestras parciales y aborto esperado limpio.
  Como el PSoC conserva la captura SD interna hasta terminar, se esperaron 11.912 s
  (duración nominal 6.912 s +5 s); el smoke posterior pasó 120/120 y 360 bytes. Esta corrida
  también ejercitó F6 en hardware: BE intento 1 devolvió 0 y el intento 2 pasó.
- **E13 STOP durante DUMPING:** STOP en el mismo socket tras el primer lote dejó 30 muestras
  parciales, ACK=0 y retorno a ARMED; después de 1.0 s, el smoke pasó 120/120 y cleanup limpio.
- **E15 captura SD máxima de 60000 lotes: ✅ PASS** (2026-07-12, corrida completa por USB):
  sesión SD 60000/60000 completa en 695.2 s, 0 SYNC_STALL/SD_ERROR, `sdread` de extremos
  0/59999 sin timeouts, seq=60000 rechazado OOR, GEOLAST COMPLETE preservado con capture=off
  y cleanup final limpio. Evidencia versionada: `slave/artifacts/e15_sd_max_60000_pass.json`.
  Hallazgo de la primera corrida (F8, del runner, no del firmware): el criterio de cleanup
  contaba el delta de `drop` (`_syncDrops`) como corrupción UART; ese contador crece de forma
  benigna con cada byte de texto UART del PSoC descartado por el framer (incluso en idle).
  Corregido: solo `bBad`/`badLen` bloquean; el delta de drops queda informativo en el JSON.
- **Ampliación de cobertura CERRADA (2026-07-12, todo PASS; detalle en la matriz):**
  - **E14 UI real**: panel esclavo con RSSI real (-16 dBm, cierra el pendiente RSSI de
    `WEB_FIELD_TESTS.md`), Máx RAM 5.89 s/512, captura UI E2E 512 lotes/15360 muestras
    exactas, ZIP de export íntegro (15360×4 B raw), `beforeunload` activo/limpio verificado
    por dispatch sintético (sin disparar el modal), rango ADC round-trip navegador→PSoC con
    ACK verde, 0 errores de consola. Nota entorno: Chrome deja el ZIP como `.tmp` (Safe
    Browsing sin internet en el AP); el `.tmp` es el ZIP completo.
  - **E16 transiciones** (`adc_decim_transitions_test.py`): 49/49 — r1→r2→r4→r3→r1 y
    d1→d2→d6→d3→d4→d1 con fs exacta en cada paso, combo r4+d3, rechazos locales de valores
    inválidos, restauración. Confirmó que la clase transitoria F6 también afecta a 0xB7 y al
    `cap` post-config (ignorado en silencio); el retry acotado de 2 intentos lo salva SIEMPRE.
  - **E17 power-cycle** (`psoc_reset_recovery_test.py`, ejecuta ToggleReset por ppcli él
    solo): 30/30 — auto-cal 18.2 s, GEOLAST de 60000 recuperado COMPLETE tras el reset,
    **capture re-armado por diseño al boot** (`g_sd_cap_en=1` con SD montada — esperar 0x40
    ENCENDIDO post-reset, no apagado), ACKs y capturas RAM+SD+sdread post-reset limpias.
  - **E18 mini-soak**: 5×120/120 con SHA únicos + probe final limpio + `/health` ok.
- **Pendientes que requieren hardware ausente del banco:** duración HAMMER E2E con nodo
  HAMMER físico y escenario multi-esclavo (2 GEO + HAMMER).
- **Mejora opcional post-campo, no bloqueante:** H4, prefetch de bloque SD en el PSoC para
  llevar el dump a aproximadamente 2× de velocidad.
- **Gate de salida CERRADO:** E5c y la publicación final pasaron. El sistema disponible en
  este banco queda **LISTO PARA CAMPO**; HAMMER E2E y multi-esclavo siguen explícitamente fuera
  de alcance por falta de hardware, no como fallos. La segunda tanda (E12-E18, 2026-07-12)
  ratificó el veredicto con el tope de jerarquía SD (60000), el recorrido de operador real y
  el ciclo de power-cycle validados en hardware.

## 6. Commits de la sesión (más viejo→nuevo)

- `a6600941` esclavo: fix carrera cap (ARMED antes de sync) + encadenado validado (11.8/17.7 s)
- `3d9dbdf9` SD en PSoC validada + comando sdread N
- `738f9454` PSoC: snapshot TopDesign GEO arreglado (fitea) + build SD
- `a85565c1` esclavo: **F1** watchdog SYNC_STALL vs SD + H3
- `42fd0b71` maestro+web: fixes dump/ACK + botón Máx RAM + matriz
- `dea23474` artifacts: evidencia del fallo F1 (`geo_10min_2604.json`)
- `7e4e332b` `ws_capture_test`: watchdog de silencio en fase dump (F5)
- `c7414403` web: W6 floor (Máx RAM 513→512) + matriz actualizada
- `89816ca5` docs: handoff de la auditoría pre-campo 2026-07-11/12
- `8c80a15e` tool: F5 pre-DATA+self-test + W7 + receta WlanConnect corregida + JSON E5c PASS
- `ae2d0315` docs: cierre E5c y veredicto pre-campo del banco disponible
- `f4461dd9` testbench: E15 SD max 60000 PASS + runners E16/E17 + gate USB/E12/E13 + evidencia

Después de `f4461dd9` se ejecutaron y cerraron PASS: E17 (con fix de criterio post-boot),
E16 (con retry acotado en capturas post-config), E14 y E18; sus evidencias están en
`slave/artifacts/` y el cierre documental es el commit siguiente. El banco quedó sano al
cierre (probe limpio, fs=2604, bBad=0, `/health` ok).

## 7. Herramientas de la sesión (scratchpad, recrear si hace falta)

`com12_logger.py` (logger pyserial), `ws_directed.py` (comandos WS + ACKs), `test_e9_regression.py`
(regresión USB 9 checks), `test_caprace.py`/`test_maxdur.py` (encadenado), `test_sdread.py` (SD).
Patrón común: pyserial dtr/rts=False timeout=0.2; WS handshake manual + takeover=1 + frames 6-byte
0x56 (ptype 0=DATA, 1=HB, 3=READY, 7=ACK). Para la reconexión WiFi ya no hace falta recrear
un scratch: usar el script persistente versionado
`firmware/esp32/Nodo comunicación/master/reconnect_geonetwork.py`.

Herramientas persistentes ya versionadas (todas con `--self-test` offline):
`slave/usb_regression_test.py` (gate USB 33/33), `slave/sd_max_regression_test.py` (E15 PASS),
`slave/adc_decim_transitions_test.py` (E16 PASS), `slave/psoc_reset_recovery_test.py` (E17
PASS; descubre el KitProg con GetPorts y ejecuta ToggleReset por ppcli él solo) y
`master/ws_fault_test.py` (E12/E13). Evidencia versionada en `slave/artifacts/`
(`e15_sd_max_60000_pass.json`, `e16_adc_decim_transitions_pass.json`,
`e17_reset_recovery_pass.json`) y `master/artifacts/` (E5c). Evidencia cruda adicional en el
scratchpad de las sesiones: `repeat_e2e.json`, `e12_reconnect.json`,
`e13_stop_running_settled.json`, `e13_stop_dump.json` y sus `.i24le`/smokes.
