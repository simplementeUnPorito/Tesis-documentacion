# Handoff: PSoC CaptureEngine / superMaquina

Fecha: 2026-07-02
Branch: `codex/capture-engine-verilog`
Proyecto: `firmware/psoc/AcondicionamientoAnalogico.cydsn`

## Objetivo

Mover a Verilog la logica repetitiva de captura que antes vivia en varias ISR
del ARM. No se busca que el ARM no haga nada: sigue configurando DMA/ADC,
cargando parametros y copiando muestras cuando corresponde. La mejora es que
`superMaquina` decide en hardware que DRQ deja pasar, cuando empieza/termina la
captura, cuantos lotes van, y que interrupciones llegan al ARM.

## Actualizacion ADC 2604 Hz (vigente desde 2026-07-11)

- La frecuencia nativa canonica es **2604 Hz para las cuatro configuraciones
  ADC**: 1 (±2.5 V, default), 2 (±0.512 V), 3 (±1.024 V) y 4 (±0.625 V).
  El factor de decimacion `N` produce una Fs efectiva `floor(2604/N)` y no
  cambia al seleccionar el rango. Esta migracion no modifica coeficientes.
- Comando UART `PSOC_CMD_ADC_CONFIG = 0xBA`: parametro `1|2|3|4`, aceptado
  solo en `PSOC_IDLE`. El PSoC responde `CFG_ACK(0xBA, config)` y luego
  `FS_REPORT(2604)` para `N=1` (o la Fs efectiva si hay decimacion). Rechazo:
  `CFG_ACK(0xBA, 0)`.
- La calibracion siempre corre forzada en `ADC_CF_2V5`, porque sus targets de
  counts pertenecen al rango ±2.5 V. Al terminar se limpia el override y
  `psoc_prepare_capture_path()` restaura el rango seleccionado por el host.
- Bug corregido: `psoc_adc_counts_right_aligned()` ya no usa los macros viejos
  `ADC_CFG1*`; divide por `ADC_CF_2V5_DEC_DIV` solo cuando `ADC_Config` es
  `ADC_CF_2V5`. Sin este fix la config 2V5 quedaba 32x sobredimensionada.
- `PGAp`/`PGAn` no se tocan: son parte del INA. El unico PGA variable de la UI
  sigue siendo `PGAgain`, cuyo mapeo codigo->ganancia fue auditado como OK.

## TopDesign actual esperado

La instancia `superMaquina` NO usa counters externos. Los pines esperados son:

- `clk`: `BUS_CLK`.
- `reset`: Control Reg `reset`.
- `ctrl[7:0]`: Control Reg `ctrl`.
- `cfg[7:0]`: Control Reg `cfg`.
- `status[7:0]`, `error[7:0]`, `state[7:0]`: Status Regs hacia ARM.
- `timer_event[7:0]`: Status Reg hacia ARM. En el TopDesign generado quedo
  como componente/API `tmr_event`. Desde 2026-07-02 (politica de eventos)
  expone la vista LIVE de los TC solo como diagnostico; el firmware ya no lo
  lee en el camino operativo (poll directo del STATUS_TC de cada timer).
- `sync_det`: salida `det` de `EdgeDetect`.
- `button_pos`: salida `pos` del `Debouncer`; en `IDLE` genera IRQ por
  `superMaquina` y queda reflejada en `status[7]`.
- `eoc_adc`: `EOC` del DelSig ADC.
- `dma_req_filter`: `DMA_Req_A` del Filter.
- `nrq_dma_adc`: `nrq` de `DMA_DelSig_RAM`.
- `nrq_dma_filter`: `nrq` de `DMA_Filter_RAM`.
- `drq_adc_ram`: a `drq` de `DMA_DelSig_RAM`.
- `drq_adc_to_filter`: a `drq` de `DMA_DelSig_Filter`.
- `drq_filter_ram`: a `drq` de `DMA_Filter_RAM`.
- `tc_uart`: TC de `Tmr_UartRxWatchdog`.
- `tc_ping`: TC de `Tmr_PingCalTick`.
- `tc_led`: TC de `Tmr_LedWait`.
- `tc_watcdog`: TC de `Tmr_CaptureWatchdog`. El typo externo se mantiene por
  compatibilidad con el TopDesign; en Verilog se usa alias interno
  `tc_capture_watchdog`.
- `irq`: a `isr_SuperMaquina`.

Los bloques `Counter_Samples`, `Counter_Batches` y `Counter_Aux` fueron
retirados del diseno. No volver a cambiarlos a UDB ni intentar clockear fixed
counters desde DSI.

Timers fixed del TopDesign:

- `Tmr_UartRxWatchdog`: watchdog del parser UART RX. Se arma solo al recibir
  bytes de un frame y vence una vez.
- `Tmr_PingCalTick`: one-shot para ping de arranque/idle y tick de
  calibracion. No concurren: antes de calibrar se detienen los pings.
- `Tmr_LedWait`: one-shot para LED/esperas cortas.
- `Tmr_CaptureWatchdog`: watchdog de captura. Es el unico timer que queda vivo
  durante `PSOC_SAMPLING`.

Las ISR legacy `isr_Timer`, `isr_Timer_1`, `isr_Timer_2` e `isr_Timer_3`
siguen compiladas como fallback muerto, pero no se registran con `StartEx`.
`fixed_timers_init()` las deja deshabilitadas, limpia pending y les fija
prioridad 7. Los TC de estos timers entran a `superMaquina` solo como vista
de diagnostico (`timer_event`); desde la politica de eventos 2026-07-02 NO
generan IRQ: el unico IRQ operativo es `isr_SuperMaquina` para muestras,
sync->sampling, fin de captura, error y boton en IDLE.

## Protocolo ARM -> Verilog

`ctrl`:

- bit 0 `ARM`: pulso para quedar armado esperando sync.
- bit 1 `START_NOW`: pulso para entrar directo a muestreo.
- bit 2 `STOP`: pulso de abort/error.
- bit 3 `CLEAR_FLAGS`: pulso para limpiar flags.
- bit 4 `USE_SYNC`: si esta armado, `sync_det` inicia muestreo.
- bit 5 `LOAD_BATCH_LO`: carga `cfg` en el byte bajo de `N` lotes.
- bit 6 `ENGINE_ENABLE`: habilita gateo/control por `superMaquina`.
- bit 7 `LOAD_BATCH_HI`: carga `cfg` en el byte alto de `N` lotes.

`cfg` en modo normal:

- bits 1:0 fuente: `0=raw`, `1=filter`, `2=combined`, `3=debug/raw`.
- bit 2 `IRQ_BATCH_EN`: reservado para IRQ al completar lote.
- bit 3 `IRQ_SYNC_EN`: IRQ al pasar de armado a muestreo por sync.
- bit 4 `IRQ_ERROR_EN`: IRQ en error.

Para configurar `N`, el firmware carga `N-1` para ahorrar logica de comparador
en PLD: guarda `cfg`, escribe el byte bajo de `N-1`, pulsa `LOAD_BATCH_LO`,
escribe el bit alto en `cfg[0]`, pulsa `LOAD_BATCH_HI`, y restaura `cfg`.
Desde el protocolo externo el valor sigue siendo `N` lotes.

## Comportamiento de superMaquina

Estados:

- `0=IDLE`
- `1=ARMED`
- `2=SAMPLING`
- `3=DONE`
- `4=ERROR`

`status`:

- bit 0 idle.
- bit 1 armed.
- bit 2 sampling.
- bit 3 done.
- bit 4 error.
- bit 5 sync_seen.
- bit 6 batch_seen.
- bit 7 button_seen (flanco de `button_pos` aceptado en `IDLE`).

`timer_event`:

- bit 0 `CE_TIMER_EVT_UART`: TC de `Tmr_UartRxWatchdog`.
- bit 1 `CE_TIMER_EVT_PING`: TC de `Tmr_PingCalTick`.
- bit 2 `CE_TIMER_EVT_LED`: TC de `Tmr_LedWait`.
- bit 3 `CE_TIMER_EVT_CAPTURE_WD`: TC de `Tmr_CaptureWatchdog`.
- bits 7:4 siempre 0.

## Politica de eventos determinismo-primero (2026-07-02)

Fuera de IDLE todo lo secundario espera o se descarta; el muestreo manda.

- Muestras DMA y sync: unicas fuentes de IRQ durante una captura. Cada IRQ de
  `superMaquina` sin DONE/ERROR/BUTTON en status ES una muestra — sin
  ambiguedad y con latencia fija (antes habia que leer `timer_event` para
  distinguir, y un sticky rezagado podia hacer descartar una muestra real).
- TC de timers: HOLD. Ya no generan IRQ ni tienen sticky en PLD; cada TC queda
  retenido en el `STATUS_TC` (clear-on-read) de su propio timer fixed hasta
  que `service_runtime()` lo lea por polling. `timer_event` quedo como vista
  live de diagnostico. Esto ademas libero PLD (4 FFs + terminos de OR).
- Durante `PSOC_ARMED`/`PSOC_SAMPLING`, `service_runtime()` solo sondea
  `Tmr_CaptureWatchdog` (`capture_engine_poll_capture_wd()`) y sirve
  unicamente `CE_TIMER_EVT_CAPTURE_WD`; uart/ping/led quedan holdeados en su
  `STATUS_TC` (los timers estan ademas detenidos por
  `runtime_timers_stop_for_quiet_window()`). Al volver a un estado tranquilo
  se sondean y sirven todos.
- `service_timer_events(mask)` ya no pulsa `CLEAR_FLAGS`: no hay sticky que
  limpiar y un `CLEAR_FLAGS` en pleno SAMPLING reseteaba los contadores de
  muestra/lote del Verilog (bug latente del disenio anterior, eliminado).
- Boton: DESCARTE fuera de IDLE. `superMaquina` solo genera irq/flag de boton
  en `ST_IDLE`; en firmware, `service_button_calibration()` descarta el flag
  en ARMED/SAMPLING sin emitir siquiera diagnostico UART.
- El troceo del watchdog de captura (chunks de 600 ms de `Tmr_CaptureWatchdog`)
  se sirve por polling en el lazo principal; toda captura >600 ms lo ejercita
  y quedo validado en hardware con 50 lotes.

Conteo interno:

- Un lote son 30 muestras (`BATCH_SAMPLES` en C y `sample_count_reg` en
  Verilog).
- En raw/debug cuenta `nrq_dma_adc`.
- En filter/combined cuenta `nrq_dma_filter`.
- Al completar 30 muestras compara `batch_count_reg` contra el limite `N-1`.
- Si ya llego al limite, pasa a `DONE` y genera `irq`; si no, incrementa
  `batch_count_reg`.

DMA:

- Con `ENGINE_ENABLE=0`, la maquina funciona como bypass segun `cfg[1:0]`.
- Con `ENGINE_ENABLE=1`, solo deja pasar DRQ en `ST_SAMPLING`.
- El IRQ unico tambien se usa para muestras DMA aceptadas. En C,
  `isr_SuperMaquina_Handler()` llama al helper raw/filter correspondiente para
  copiar la muestra y alimentar calibracion.

## Firmware tocado

Archivo principal:
`firmware/psoc/AcondicionamientoAnalogico.cydsn/main.c`

Puntos clave:

- Ya no incluye ni configura `Counter_Samples`, `Counter_Batches` o
  `Counter_Aux`.
- `capture_engine_configure_target()` carga `N` lotes dentro de
  `superMaquina`.
- `dma_route_select()` escribe `cfg[1:0]`; no usa `Reg_Select`.
- `psoc_arm()` configura fuente/target, habilita maquina con `USE_SYNC`, pulsa
  `ARM` y arranca ADC. Al inicio detiene timers de runtime para que
  `ARMED/HOT_WAIT` quede silencioso.
- `psoc_enter_sampling()` configura fuente/target, habilita maquina sin sync,
  pulsa `START_NOW`, detiene timers de runtime y arranca ADC.
- `isr_SuperMaquina_StartEx(isr_SuperMaquina_Handler)` se registra con
  prioridad 0 mediante `isr_SuperMaquina_SetPriority(0u)`.
- El Status Reg generado para eventos de timer se llama `tmr_event`; `main.c`
  lo aliasa como `timer_event_Read()`. Los defines publicos son
  `CE_TIMER_EVT_UART`, `CE_TIMER_EVT_PING`, `CE_TIMER_EVT_LED` y
  `CE_TIMER_EVT_CAPTURE_WD`.
- `isr_SuperMaquina_Handler()` lee primero `timer_event_Read()`, acumula esos
  bits en `g_timer_event_pending` y solo llama al handler de muestra cuando no
  fue un IRQ puramente de timer.
- `service_runtime()` llama `capture_engine_poll_timer_events()` y
  `service_timer_events()` antes de cualquier retorno temprano de
  `PSOC_ARMED` o `PSOC_SAMPLING`.
- `service_timer_events()` contiene la logica que antes estaba en
  `isr_Timer*` y emite `CLEAR_FLAGS` despues de consumir eventos para limpiar
  el sticky `timer_event_reg`.
- Por defecto `PSOC_SUPERMAQUINA_OWNS_DMA_IRQ=1` y
  `PSOC_SUPERMAQUINA_OWNS_SYNC_IRQ=1`, para evitar dobles ISR si el TopDesign
  viejo aun genera headers de las ISR antiguas.
- El descarte FIR de 63 muestras sigue en C (`g_fir_discard`) con objetivo de
  hardware extendido `+ceil(63/30)=+3` lotes en captura filtrada armada.
  Se intento moverlo a Verilog el 2026-07-02, pero no entro en recursos
  PLD/UDB.
- `psoc_now_ticks()` queda solo como compatibilidad para el servo legacy
  desactivado (`CAL_ALGO_SERVO_ENABLE=0`). La calibracion activa usa
  `psoc_cal_timer_start/stop/take_*()` sobre `Tmr_PingCalTick`.
- Se agrego fallback local `CY_NUM_INTERRUPTS=32` y se llama
  `install_irq_traps()` tras registrar las ISR reales. Las IRQ que queden en
  `IntDefaultHandler` pasan a una trampa que reporta evento `0x7E` y deshabilita
  esa IRQ en vez de colgar el firmware.
- Como `superMaquina` posee el sync (`PSOC_SUPERMAQUINA_OWNS_SYNC_IRQ=1`), se
  instala el vector de `isr_SyncIn_SafeVector` sin habilitar la IRQ. Si algun
  flujo legacy/calibracion la re-habilita, limpia el interrupt y no cae en una
  trampa generica.

## Archivos importantes

- `firmware/psoc/AcondicionamientoAnalogico.cydsn/superMaquina/superMaquina.v`
- `firmware/psoc/AcondicionamientoAnalogico.cydsn/superMaquina/superMaquina.cysym`
- `firmware/psoc/AcondicionamientoAnalogico.cydsn/TopDesign/TopDesign.cysch`
- `firmware/psoc/AcondicionamientoAnalogico.cydsn/AcondicionamientoAnalogico.cyprj`
- `firmware/psoc/AcondicionamientoAnalogico.cydsn/main.c`
- `firmware/psoc/AcondicionamientoAnalogico.cydsn/psoc_hw.h`

## Build

Comando usado:

```powershell
& "C:\Program Files (x86)\Cypress\PSoC Creator\4.4\PSoC Creator\bin\cyprjmgr.exe" `
  -wrk "C:\Github\Tesis\firmware\psoc\AcondicionamientoAnalogico.cydsn\AcondicionamientoAnalogico.cywrk" `
  -prj AcondicionamientoAnalogico `
  -c Debug `
  -build
```

Si falla por `floating net`, revisar primero buses visibles de `TopDesign`:
`ctrl`, `cfg`, `status`, `error`, `state`, `irq`, entradas `nrq`, y cualquier
AND que haya quedado suelto tras quitar counters.

Build validado el 2026-07-02 17:13:43, con la politica de eventos
determinismo-primero (TC sin IRQ ni sticky):

- `Build Succeeded`.
- Flash: 40758 bytes (15.5%; filas 0..159 para programacion por PPCLI).
- SRAM: 49352 bytes (75.3%).
- El fitter acepto el Verilog reducido sin `E2071` (quitar el sticky de
  `timer_event` libero 4 FFs y terminos de OR en PLD).

Build anterior (2026-07-02 16:01:18, `timer_event` sticky): flash 39574,
SRAM 49336, filas 0..154. Superseded por el de arriba.

Intento de optimizacion Verilog probado y descartado el 2026-07-02:

- Variante A: contador dedicado de 6 bits para descartar 63 salidas FIR
  post-sync sin IRQ/conteo. Resultado: fitter fallo con `E2071`, no entraba en
  24 UDB.
- Variante B: estado `ST_DISCARD` reutilizando `sample_count_reg` y
  `batch_count_reg` para contar `2*30+3`. Resultado: fallo en tech mapping por
  recursos (`Macrocells max=192 needed=243`, `Unique P-terms max=384
  needed=430`).
- Conclusion: el descarte FIR en hardware queda bloqueado hasta liberar PLD,
  por ejemplo reduciendo UART UDB, quitando componentes legacy o moviendo otra
  logica fuera de PLD. El codigo quedo revertido al camino C compilable.

## Programacion PSoC por ppcli

Ojo con `ppcli`: con rutas Windows usando `\` puede decir que no abre el HEX.
Usar ruta corta con `/`, por ejemplo `C:/Temp/psoc_supermaquina_full.hex`.

Para este PSoC5LP el programador reporta ECC presente y ECC hardware status 0,
por lo que `PSoC3_ProgramRowFromHex` debe usar `eccOption=1`. Con
`eccOption=0` aparecen timeouts de SPC en filas pares.

Flujo validado:

```text
OpenPort "KitProg (CMSIS-DAP/236111)" "C:/Program Files (x86)/Cypress/Programmer/"
SetAcquireMode Reset
SetProtocol 8
SetProtocolClock 152
SetProtocolConnector 1
HEX_ReadFile C:/Github/Tesis/firmware/psoc/AcondicionamientoAnalogico.cydsn/CortexM3/ARM_GCC_541/Debug/AcondicionamientoAnalogico.hex
DAP_Acquire
PSoC3_EraseAll
PSoC3_ProgramRowFromHex 0x00 <row 0..lastRow> 0x01
PSoC3_VerifyRowFromHex 0x00 <row 0..lastRow> 0x01
PSoC3_ProtectAll
PSoC3_VerifyProtect
DAP_ReleaseChip
ClosePort
```

Para el build validado mas reciente del 2026-07-02 16:01:18: `lastRow=154`.

Scripts/logs usados durante la prueba:

- `C:\Temp\ppcli_program_timers_20260702_000546.cli`
- `C:\Temp\ppcli_program_timers_20260702_000546.log`
- `C:\Temp\ppcli_program_timers_20260702_000902.cli`
- `C:\Temp\ppcli_program_timers_20260702_000902.log`
- `C:\Users\elias\AppData\Local\Temp\psoc_program_opt_20260702_021826.cli`
- `C:\Users\elias\AppData\Local\Temp\psoc_program_opt_20260702_021826.log`
- `C:\Users\elias\AppData\Local\Temp\psoc_program_opt_20260702_022316.cli`
- `C:\Users\elias\AppData\Local\Temp\psoc_program_opt_20260702_022316.log`
- `C:\Users\elias\AppData\Local\Temp\psoc_program_sticky_20260702_160118.log`

No hubo errores: erase, program, verify, protect y release terminaron `0 OK`.

Para diagnostico UART se uso temporalmente `PSOC_EARLY_UART_TEST=1` en
`main.c`, se confirmo que ESP recibia `PING/BOOT`, y luego se volvio a
`PSOC_EARLY_UART_TEST=0`. No dejar ese test activado en firmware normal.

## Comandos USB de laboratorio en ESP

Firmware ESP `firmware/esp32/Nodo comunicacion/slave`, entorno `slave2`, puerto usado:
`COM12`.

El firmware final queda silencioso:

- `SLAVE_LOGS_ENABLE=0`
- `DBG_HUMAN=0`
- `DBG_MACHINE=0`
- `SLAVE_USB_CMD_ENABLE=0`
- `SLAVE_LAB_TOOLS_ENABLE=0` por default en `src/main.cpp`

Para diagnostico de banco, compilar temporalmente con
`SLAVE_USB_CMD_ENABLE=1`. Con ese define aparecen:

- `help`: lista comandos.
- `probe`: fuerza deteccion PSoC y muestra diagnostico UART.
- `status` / `s`: pide estado PSoC y muestra contadores UART.
- `stream N`: `0=raw`, `1=FIR hardware`.
- `debugpsoc N` / `dpsoc N`: activa/desactiva rampa debug en PSoC.
- `pre N`: configura N lotes y deja HOT_WAIT.
- `sync` / `go`: levanta `SYNC_TO_PSOC_PIN` y arranca desde HOT_WAIT.
- `cap N`: hace `pre N` + `sync`.
- `startnow N`: arranque inmediato por UART.
- `clear` / `flush`: libera store local para poder repetir pruebas.
- `stop`: baja sync, desactiva debug y tambien libera store.

Con `SLAVE_LAB_TOOLS_ENABLE=1` se habilitan ademas:

- `diag`: contadores internos del enlace PSoC.
- `pins`: estado de pines relevantes.
- `quiet N MS`: arma N lotes y mide silencio real durante HOT_WAIT.
- `capwait N`: `pre N`, `sync` y espera cierre.
- `startwait N`: arranque inmediato y espera cierre.
- `rawcap N`: selecciona RAW, captura y reporta `fill/bBad`.
- `fircap N`: selecciona FIR, captura y reporta `fill/bBad`.

`clear` y `stop` fueron agregados/ajustados para que una captura USB previa
no deje `STOPPED fill=N/N` bloqueando el siguiente ensayo.

## Pruebas con hardware

1. Build limpio.
2. Programar PSoC si el `.hex` se genero correctamente.
3. Detectar puertos COM del ESP/PSoC.
4. Probar comando de ping/status.
5. Probar `SET_N_BATCHES` con N chico.
6. Probar `START_NOW` en raw.
7. Probar debug ramp.
8. Probar `PRESTART/ARM` y un pulso real/simulado de `SYNC_IN`.
9. Probar ruta filtrada.
10. Verificar que llegan 30 muestras por lote y N lotes exactos.

Resultados medidos el 2026-07-01 con ESP en `COM8`:

- UART base: `probe psoc=1`, `uartBytes` crece, `ping` y `diag` llegan.
- `startnow 2` con debug PSoC: `FULL -> STOPPED (2 batches)`.
- `cap 2` con debug PSoC: `HOT_WAIT`, `sync start`, `FULL -> STOPPED (2 batches)`,
  `status ... bBad=0 ... fill=2/2`.
- RAW real, `stream 0`, `cap 1`: `FULL -> STOPPED (1 batches)`, `fill=1/1`.
- FIR real, `stream 1`, `cap 3`: `FULL -> STOPPED (3 batches)`, `fill=3/3`.
- RAW debug, `cap 5`: `FULL -> STOPPED (5 batches)`, `fill=5/5`.

Todos esos ciclos terminaron con `bBad=0`.

Resultados medidos el 2026-07-02 tras migrar timers:

- Build y programacion PPCLI OK en el build anterior, filas 0..146 verificadas.
- `probe`: `probe psoc=1`, PSoC reporto `hw=1/HAMMER pstate=0/IDLE`.
- `stream 0`, `debugpsoc 0`, `cap 2`: `FULL -> STOPPED (2 batches)`,
  luego `clear` volvio a `WAIT_ARM`.
- Ping idle por `Timer_1` verificado: contador `ping` del ESP subio de 3256 a
  3270 durante la espera idle/prueba posterior.

Resultados medidos el 2026-07-02 tras trampas IRQ/SyncIn y build final:

- Build final OK, flash 38294 bytes, SRAM 49328 bytes, filas PPCLI `0..149`.
- Programacion final PPCLI OK: erase, program, verify, protect y release `0 OK`
  en log `psoc_program_opt_20260702_022316.log`.
- `probe`: `probe psoc=1`, PSoC `hw=1/HAMMER pstate=0/IDLE`.
- RAW real: `stream 0`, `debugpsoc 0`, `cap 1` -> `FULL -> STOPPED (1 batches)`,
  `bBad=0`, `fill=1/1`.
- FIR real: `stream 1`, `cap 2` -> `FULL -> STOPPED (2 batches)`, `bBad=0`,
  `fill=2/2`.
- Prueba previa mas amplia antes del ultimo reflasheo: RAW `cap 2`, FIR
  `cap 3`, debug `startnow 2`, todos `FULL -> STOPPED`, `bBad=0`.
- `blink` no bloqueo la comunicacion. Durante idle, `ping` subio
  `745 -> 749 -> 755`.
- `cal` por USB fue enviado y no colgo el sistema; no aparecio un `CAL done`
  explicito en el log USB observado, asi que queda como prueba de no-regresion
  de Timer_1/idle y no como validacion fina de calibracion analogica. Tras esa
  espera, `cap 1` volvio a funcionar con `bBad=0`.

Resultados medidos el 2026-07-02 tras migrar TC de timers a
`superMaquina` y agregar `timer_event` sticky:

- Build PSoC OK a las 16:01:18: flash 39574 bytes, SRAM 49336 bytes.
- Programacion PPCLI OK con filas `0..154`; erase/program/verify/protect y
  release terminaron `0 OK` en
  `psoc_program_sticky_20260702_160118.log`.
- Chequeo estatico: no quedan llamadas activas a `isr_Timer*_StartEx`; existe
  `tmr_event_Read()` generado y aliasado como `timer_event_Read()`.
- ESP esclavo `slave2` final silencioso subido por PlatformIO a `COM12`:
  `SLAVE_LOGS_ENABLE=0`, `DBG_HUMAN=0`, `DBG_MACHINE=0`,
  `SLAVE_USB_CMD_ENABLE=0`.
- Web master en `192.168.4.1`: `/health` respondio `200 OK`,
  `littlefs=ok`.
- WebSocket FIR, nodo 2, 2 lotes, `--stream 1`: `RUNNING -> DUMPING`, ACK
  `CMD_VIEW ok=2`, 60 paquetes DATA, una sola conexion.
- WebSocket RAW, nodo 2, 2 lotes, `--stream 0`: `RUNNING -> DUMPING`, ACK
  `CMD_VIEW ok=2`, 60 paquetes DATA, una sola conexion.
- Antes de apagar herramientas USB, pruebas locales en `COM12`: `probe`
  detecto PSoC; `quiet 2 2000` mostro ventana HOT_WAIT limpia
  (`winBytes=0 winPing=0 winDiag=0`); `rawcap 2`, `fircap 2` y
  `startwait 2` cerraron con `fill=2/2` y `bBad=0`.

Resultados medidos el 2026-07-02 (tarde) con la politica de eventos
determinismo-primero (build 17:13:43, filas 0..159, log
`psoc_program_eventpolicy_20260702_171417.log`, erase/program/verify/
protect/release `0 OK`):

- Banco serial COM12 (lab tools ON), 11/11 OK en una sola sesion:
  - `probe` detecto PSoC y auto-cal volvio a `pstate=0/IDLE`.
  - Ping idle por POLLING (ya sin IRQ de Timer_1): contador `ping` subio
    12 -> 23 en ~10 s de espera.
  - `quiet 2 2000`: `winBytes=0 winPing=0 winDiag=0`.
  - `rawcap 2`, `fircap 2`, `startwait 2`: `fill=2/2`, `dBad=0`.
  - `rawcap 50` (~934 ms de muestreo, varios chunks de 600 ms del capture
    watchdog servidos por polling EN pleno SAMPLING): `fill=50/50`, `dBad=0`.
  - `fircap 20`: `fill=20/20`, `dBad=0`.
  - `cal` por USB volvio a idle y `rawcap 1` posterior cerro `fill=1/1`.
- Web (192.168.4.1): `/health` 200 `littlefs=ok`; capturas VER nodo 2 de
  2 lotes en RAW y FIR con `DATA=60/60`, `RUNNING -> DUMPING`, ACK
  `CMD_VIEW ok=2`; verificado ANTES y DESPUES de silenciar el esclavo.
  Cross-check en el log USB del esclavo: `cfg B7 ok=1`, `HOT_WAIT`,
  `START_OK sync 0->1`, `FULL -> STOPPED (2 batches)` en ambos streams.
- Ojo al probar por WS con una pestania del navegador abierta en la UI:
  el master permite UN cliente WS y una conexion nueva desde la misma IP
  roba el socket (takeover). Una pestania olvidada reconecta sola y aborta
  el dump de VER a mitad (`DUMPING -> ARMED` sin DATA). Ver
  `WEB_FIELD_TESTS.md` para el procedimiento con `ws_fast_probe`/`/ws-reset`.

## Notas para continuar

- No editar `TopDesign.cysch` a mano; PSoC Creator lo serializa en formato
  propio.
- El arbol puede mostrar muchos cambios en `codegentemp` por regeneracion de
  Creator. No tratarlos como fuente manual.
- Si hace falta diagnostico fino extra, ampliar `timer_event`/status con mucho
  cuidado: `timer_event` es vista live (los TC son pulsos de 1 BUS_CLK, una
  lectura de CPU casi nunca los ve); el hold real vive en el `STATUS_TC`
  clear-on-read de cada timer fixed. No volver a mezclar TC con el IRQ de
  `superMaquina`: la ausencia de ambiguedad muestra-vs-timer en la ISR
  depende de eso.
- `Tmr_CaptureWatchdog` ya no esta libre: su TC entra por `tc_watcdog` a
  `timer_event[3]` (vista) y su `STATUS_TC` es la unica actividad periodica
  que `service_runtime()` atiende durante `PSOC_SAMPLING`.
- No intentar de nuevo el descarte FIR en Verilog sin antes liberar PLD: las
  dos variantes anteriores ya fueron compiladas y fallaron por recursos.
