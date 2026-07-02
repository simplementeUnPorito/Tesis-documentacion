# Handoff: PSoC CaptureEngine / superMaquina

Fecha: 2026-07-02
Branch: `codex/capture-engine-verilog`
Proyecto: `src/psoc/AcondicionamientoAnalogico.cydsn`

## Objetivo

Mover a Verilog la logica repetitiva de captura que antes vivia en varias ISR
del ARM. No se busca que el ARM no haga nada: sigue configurando DMA/ADC,
cargando parametros y copiando muestras cuando corresponde. La mejora es que
`superMaquina` decide en hardware que DRQ deja pasar, cuando empieza/termina la
captura, cuantos lotes van, y que interrupciones llegan al ARM.

## TopDesign actual esperado

La instancia `superMaquina` NO usa counters externos. Los pines esperados son:

- `clk`: `BUS_CLK`.
- `reset`: Control Reg `reset`.
- `ctrl[7:0]`: Control Reg `ctrl`.
- `cfg[7:0]`: Control Reg `cfg`.
- `status[7:0]`, `error[7:0]`, `state[7:0]`: Status Regs hacia ARM.
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
- `irq`: a `isr_SuperMaquina`.

Los bloques `Counter_Samples`, `Counter_Batches` y `Counter_Aux` fueron
retirados del diseno. No volver a cambiarlos a UDB ni intentar clockear fixed
counters desde DSI.

Timers fixed del TopDesign:

- `Timer` viejo: queda dedicado al watchdog del parser UART RX. No es tick de
  sistema; se arma solo al recibir bytes de un frame y vence una vez.
- `Timer_1`: one-shot general para ping de arranque/idle. El firmware escribe
  periodo/counter y reencadena delays largos en chunks de 600 ms maximo.
- `Timer_2`: one-shot para LED/esperas cortas: parpadeos de conexion y
  comando `blink`/identificacion.
- `Timer_3`: one-shot de calibracion async: progreso cada 500 ms y watchdog
  global equivalente al timeout legacy.

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
`src/psoc/AcondicionamientoAnalogico.cydsn/main.c`

Puntos clave:

- Ya no incluye ni configura `Counter_Samples`, `Counter_Batches` o
  `Counter_Aux`.
- `capture_engine_configure_target()` carga `N` lotes dentro de
  `superMaquina`.
- `dma_route_select()` escribe `cfg[1:0]`; no usa `Reg_Select`.
- `psoc_arm()` configura fuente/target, habilita maquina con `USE_SYNC`, pulsa
  `ARM` y arranca ADC.
- `psoc_enter_sampling()` configura fuente/target, habilita maquina sin sync,
  pulsa `START_NOW` y arranca ADC.
- Por defecto `PSOC_SUPERMAQUINA_OWNS_DMA_IRQ=1` y
  `PSOC_SUPERMAQUINA_OWNS_SYNC_IRQ=1`, para evitar dobles ISR si el TopDesign
  viejo aun genera headers de las ISR antiguas.
- Por defecto `PSOC_SUPERMAQUINA_FILTER_DISCARD=0`: no se descartan las 63
  muestras de retardo FIR al entrar por sync, porque Verilog ya cuenta `nrq`
  desde la primera muestra filtrada. Si se quiere recuperar compensacion de
  retardo, conviene agregar un contador de descarte en Verilog o cargar una
  meta de muestras, no hacerlo solo en C.
- `psoc_now_ticks()` queda solo como compatibilidad para el servo legacy
  desactivado (`CAL_ALGO_SERVO_ENABLE=0`). La calibracion activa usa
  `psoc_cal_timer_start/stop/take_*()` sobre `Timer_3`.

## Archivos importantes

- `src/psoc/AcondicionamientoAnalogico.cydsn/superMaquina/superMaquina.v`
- `src/psoc/AcondicionamientoAnalogico.cydsn/superMaquina/superMaquina.cysym`
- `src/psoc/AcondicionamientoAnalogico.cydsn/TopDesign/TopDesign.cysch`
- `src/psoc/AcondicionamientoAnalogico.cydsn/AcondicionamientoAnalogico.cyprj`
- `src/psoc/AcondicionamientoAnalogico.cydsn/main.c`
- `src/psoc/AcondicionamientoAnalogico.cydsn/psoc_hw.h`

## Build

Comando usado:

```powershell
& "C:\Program Files (x86)\Cypress\PSoC Creator\4.4\PSoC Creator\bin\cyprjmgr.exe" `
  -wrk "C:\Github\Tesis\src\psoc\AcondicionamientoAnalogico.cydsn\AcondicionamientoAnalogico.cywrk" `
  -prj AcondicionamientoAnalogico `
  -c Debug `
  -build
```

Si falla por `floating net`, revisar primero buses visibles de `TopDesign`:
`ctrl`, `cfg`, `status`, `error`, `state`, `irq`, entradas `nrq`, y cualquier
AND que haya quedado suelto tras quitar counters.

Build validado el 2026-07-02:

- `Build Succeeded`.
- Flash: 37510 bytes (filas 0..146 para programacion por PPCLI).
- SRAM: 49312 bytes.
- Avisos observados: `sta.M0019` setup CyBUS_CLK y mensajes `prj.M0072` de
  items ya existentes durante API generation. No bloquearon el build ni el HEX.

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
HEX_ReadFile C:/Github/Tesis/src/psoc/AcondicionamientoAnalogico.cydsn/CortexM3/ARM_GCC_541/Debug/AcondicionamientoAnalogico.hex
DAP_Acquire
PSoC3_EraseAll
PSoC3_ProgramRowFromHex 0x00 <row 0..lastRow> 0x01
PSoC3_VerifyRowFromHex 0x00 <row 0..lastRow> 0x01
PSoC3_ProtectAll
PSoC3_VerifyProtect
DAP_ReleaseChip
ClosePort
```

Para el build del 2026-07-02: `lastRow=146`.

Scripts/logs usados durante la prueba:

- `C:\Temp\ppcli_program_timers_20260702_000546.cli`
- `C:\Temp\ppcli_program_timers_20260702_000546.log`
- `C:\Temp\ppcli_program_timers_20260702_000902.cli`
- `C:\Temp\ppcli_program_timers_20260702_000902.log`

No hubo errores: erase, program, verify, protect y release terminaron `0 OK`.

Para diagnostico UART se uso temporalmente `PSOC_EARLY_UART_TEST=1` en
`main.c`, se confirmo que ESP recibia `PING/BOOT`, y luego se volvio a
`PSOC_EARLY_UART_TEST=0`. No dejar ese test activado en firmware normal.

## Comandos USB de laboratorio en ESP

Firmware ESP `src/esp/Nodo comunicacion/slave`, entorno `slave2`, puerto usado:
`COM8`.

Comandos disponibles por USB:

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

- Build y programacion PPCLI OK, filas 0..146 verificadas.
- `probe`: `probe psoc=1`, PSoC reporto `hw=1/HAMMER pstate=0/IDLE`.
- `stream 0`, `debugpsoc 0`, `cap 2`: `FULL -> STOPPED (2 batches)`,
  luego `clear` volvio a `WAIT_ARM`.
- Ping idle por `Timer_1` verificado: contador `ping` del ESP subio de 3256 a
  3270 durante la espera idle/prueba posterior.

## Notas para continuar

- No editar `TopDesign.cysch` a mano; PSoC Creator lo serializa en formato
  propio.
- El arbol puede mostrar muchos cambios en `codegentemp` por regeneracion de
  Creator. No tratarlos como fuente manual.
- Si hace falta diagnostico fino, agregar un registro de razon de IRQ en
  Verilog antes de ampliar mas el estado visible.
