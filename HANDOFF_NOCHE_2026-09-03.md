# Noche del 2026-09-03 — estado, plan y lo que tenés que hacer vos

Este archivo tiene tres partes: **lo que hay que saber antes de tocar nada**, **el
plan de la noche** (lo que va haciendo la sesión sola) y **la lista para vos**.
Se actualiza a medida que avanza la noche; mirá la fecha de cada sección.

---

## 1. Lo que hay que saber antes de tocar nada

### Hallazgos que corrigen cosas dichas antes

Tres conclusiones anteriores eran **falsas** y ya están corregidas. Las dejo
escritas porque si alguien lee los mensajes viejos se va a confundir:

1. **«La curva en S del barrido es recorte de la etapa»** — NO. Era un limitador
   propio del firmware que acotaba todo código a ±127. Todo barrido más allá de
   eso devolvía el mismo valor y se leía como saturación.
2. **«Las referencias del sumador y del pasabajos no mueven nada»** — NO. Con el
   limitador sacado, `Vref_ADDER` recorre 370,7 mV y `Vref_LP` 318,8 mV.
3. **«El mux se traba»** — NO. El banco tomaba la primera respuesta que se
   pareciera a la que esperaba, sin comprobar el canal; una respuesta atrasada
   quedaba etiquetada con el canal viejo y dos taps aparecían intercambiados.

### Autoridad real de cada referencia (medida en placa, 2026-09-03)

Con `PSOC_IDAC_SIGNED_MAX = 255`, recorrido de cada referencia sobre su propio
tap, barriendo −255…+255:

| referencia | recorrido | nota |
|---|---:|---|
| `Vref_PGA` | 28,2 mV | con PGA en 1×; con PGA en 50× daba 355 mV |
| `Vref_BP` | 123,6 mV | |
| `Vref_ADDER` | 370,7 mV | 78 % de los 478 mV nominales |
| `Vref_LP` | 318,8 mV | |

Que la etapa 0 escale con la ganancia del PGA es lo que modela
`cal_pi_stage_gain_x1000()`. La cadena está sana.

### Escala del ADC: la conversión a µV es CORRECTA

Verificado contra las cabeceras generadas. Las cuatro configuraciones son de
18 bits y todas dan fondo de escala en 131 072 cuentas a su propio rango:

```
2V5     52 429 c/V × 2,500 V = 131 072
0V512  256 000 c/V × 0,512 V = 131 072
1V024  128 000 c/V × 1,024 V = 131 072
0V625  209 715 c/V × 0,625 V = 131 072
```

El `SELFTEST_ADC_FS_COUNTS` hardcodeado sirve para las cuatro. Config 1 es
`ADC_IR_VNEG_2VREF_DIFF`: diferencial contra Vneg, ±2,5 V, o sea que los valores
negativos son alcanzables (se midió −1 158 mV en un tap).

### Trampas que cuestan horas si no se saben

- **Abrir COM8 resetea el ESP.** Si eso cae en mitad de un byte, la UART de
  bajada del PSoC se desincroniza: los pings siguen llegando (los origina el
  PSoC, suben por I2C) pero **ninguna medida contesta**. Se sale con el botón
  *Reiniciar PSoC* de la ventana, o con `reset_psoc.ps1`.
- **`program_psoc.ps1` graba sólo las filas que el HEX ocupa.** La versión que
  grababa las 4×256 dejaba el chip sin arrancar. No usar `-AllRows`.
- **Reflashear el ESP cuelga el PSoC**: después de cada upload hay que hacer
  ToggleReset.
- **Nunca editar a mano** `.cyprj` / `.cydwr` / `.cysch` / `.cyfit`.

---

## 2. Plan de la noche

Orden deliberado: primero lo que deja el repo consistente, después el pipeline.

### A. Port al proyecto de campo — PSoC COMPILA, INTEGRACIÓN PENDIENTE

`src/firmware/psoc/AcondicionamientoAnalogico.cydsn`

- [x] Copiados desde el proyecto de test: `psoc_hw.[ch]`, `psoc_nv.[ch]`,
      `calibration_tables*.h` (dominio con signo, tablas enteras, sin
      limitador, Kp/Ki de la simulación).
- [x] `calibration.[ch]` copiados sin el bloque de autotest (395 líneas), con
      las doce funciones públicas verificadas una por una.
- [x] `main.c`: `nv_dac` pasa a `int16`; borrados los cinco llamados al servo
      legacy. Era seguro: el arranque hacía `servo_enable(0u)`, o sea que el
      servo estaba apagado desde el boot y ni el `service()` ni los `abort()`
      hacían nada. El PI asíncrono ya se atendía igual en los dos proyectos.
- [x] `0xAA` mueve un IDAC manualmente con dos parámetros:
      `[signo|etapa][magnitud]`, usando el bit 7 como `0xA2`. Un ajuste manual
      invalida el resultado de calibración de esa etapa y no puede guardarse
      accidentalmente como una calibración verificada; la próxima calibración
      vuelve a determinar el valor.
- [x] Corregidos dos huecos adicionales que reveló el compilador: el snapshot
      para EEPROM seguía siendo `uint8` aunque la API ya usa `int16`, y
      `psoc_hw.c` había recibido el diagnóstico SD sin las banderas/prototipos
      correspondientes en `sd_spi.h`.
- [x] Build limpio con PSoC Creator 4.4 a las 16:29: 61 352 B flash (23,4 %),
      51 952 B SRAM (79,3 %), sin errores ni warnings del compilador.

#### Ronda de Codex 16:26–16:31 — evidencia y punto exacto de continuación

Commit del submódulo PSoC: `b122112` (`Completar el port de calibracion al
firmware de campo`). Incluye solamente los quince fuentes del port; no incluye
los reportes ni archivos personales/regenerados por PSoC Creator que ya estaban
modificados en el árbol.

Comando de verificación que pasó:

```powershell
Set-Location C:\Github\Tesis\src\firmware\psoc\AcondicionamientoAnalogico.cydsn
& 'C:\Program Files (x86)\Cypress\PSoC Creator\4.4\PSoC Creator\bin\cyprjmgr.exe' `
  -wrk AcondicionamientoAnalogico.cywrk -build
```

El primer build falló porque `psoc_hw.c` ya usaba `SD_DIAG_MISO_*`,
`SD_DIAG_SCK_*`, `SD_DIAG_MOSI_*` y `SD_DIAG_CS_*`, pero el port no había
copiado sus definiciones/prototipos a `sd_spi.h`. Se sincronizó esa API y el
segundo build terminó en `Build Succeeded`. También se detectó y corrigió
`dac_snap` en `PSOC_CMD_SAVE_EEPROM`: seguía como `uint8[4]` aunque
`psoc_nv_save_for_gain()` ya recibe `int16*`.

Contrato PSoC nuevo para `0xAA`:

```text
[0xAB][0xAA][signo|etapa][magnitud][0xAA^p1^p2]
                  bit7 ^       ^ 0..255
                  bits0..3 = etapa
```

Respuesta: `CFG_ACK(0xAA, p1)` si la etapa existe, o `CFG_ACK(0xAA, 0xFF)` si
no existe. El ajuste actualiza `g_psoc_cal_results[stage].final_dac`, limpia su
`ok` y pone `g_last_calibration_ok=0`, de modo que `SAVE_EEPROM` no pueda
presentar el ajuste manual como calibración verificada.

**Pendiente inmediato para Claude:** este contrato todavía no está portado de
punta a punta. El ESP de campo conserva `PsocUART::setVdac(uint8_t)` y manda la
trama vieja de un parámetro; la web/maestro también representa `0xAA` con un
solo `param`. Si se usa hoy desde ese camino, el PSoC espera el segundo byte y
el pedido termina por watchdog/timeout. Antes de probar el pipeline hay que
actualizar el transporte ESP/maestro o definir explícitamente otra ruta que
conserve etapa, signo y magnitud. No volver silenciosamente al comando muerto
de un byte.

**Desbloqueado por Elías a las 16:40:** el TopDesign de campo ya tiene
`polarity_reg`, con sus cuatro salidas conectadas a `ipolarity` en el orden de
las etapas. Creator generó `polarity_reg.c/.h`, `project.h` lo incluye y el
rebuild compiló explícitamente `polarity_reg.o`; el `#if
defined(CY_CONTROL_REG_polarity_reg_H)` de `psoc_hw.c` ya toma la rama real.

El proyecto de campo se programó después por KitProg
`CMSIS-DAP/246475`, **sin `-AllRows`**: 61.328 bytes, Fs 4x2604 Hz, 248 filas
ocupadas escritas y verificadas, `ProtectAll`, `VerifyProtect` y
`DAP_ReleaseChip` en `0 OK`. Log original:
`%TEMP%\psoc_program_geo_2604_20260903_164236.log`. Al reiniciar el ESP de
test en COM8, `probe` confirmó `probe=1`, 10 pings, 0 tramas malas y 4 eventos
de diagnóstico: el firmware de campo arrancó y el enlace volvió arriba.

No usar el comando `idac` del ESP de autotest para validar este firmware de
campo: ese comando todavía manda el protocolo de test `0xA2` y espera un
`ST_ID_IDAC`; el campo ahora recibe el contrato manual `0xAA` documentado
arriba y responde `CFG_ACK`. La prueba hecha así devolvió `#IDAC ... 0` y
medidas nulas, como corresponde a protocolos incompatibles; **no dice nada del
sentido eléctrico de la polaridad**. Primero portar `0xAA` al ESP y recién
entonces comparar +200/0/-200.

### B. Pipeline completo

Hay un ESP maestro en **COM6** y el esclavo en **COM8**; el PSoC por KitProg en
COM3.

1. PSoC → ESP esclavo: ya probado esta tarde (autotest, taps, barridos).
2. Esclavo → maestro por ESP-NOW, con la página web.
3. Esclavo → inyección con el server de Python
   (`src/interfaces/python/server`).

Gate previo: cerrar la integración end-to-end de `0xAA` descrita arriba y
compilar los entornos ESP afectados. El resto de los comandos de captura no
depende de `0xAA`, pero la interfaz no debe confirmar como aplicado un formato
que el PSoC ya no acepta.

**Los datos que se ingesten van a una carpeta `lab/`** para no mezclarlos con
los buenos.

### C. Cosas abiertas que conviene cerrar

- **ACK de configuración ADC reprobado el 2026-09-03 a las 16:40 sobre COM8:**
  el enlace estaba arriba (`probe=1`, 10 pings, 0 tramas malas). Los comandos
  manuales `adc 1 0` ... `adc 4 0` recibieron ACK para las cuatro configs; luego
  se hicieron cinco ciclos consecutivos 2 -> 3 -> 4 sin captura y dieron
  **15/15 ACK correctos** (`#ADC N -1 0 0 1`). Por lo tanto, la pérdida de ACK
  observada antes no se reproduce en este estado y no conviene tocar el retry
  a ciegas. Transcript completo:
  `hardware_adc_ack_2026-09-03.txt`.
- La captura manual inmediatamente posterior al cambio sí mostró una anomalía
  distinta: `adc 2 0` devolvió `#ADC 2 0 0 0 0`, mientras configs 1, 3 y 4
  devolvieron medidas válidas. Al correr el grupo D completo, D5 no llegó a
  comparar rangos: dio `SKIP` porque el tap estaba fuera de +-0,45 V y la
  config 2 recortaría. Separar entonces dos problemas: transporte/ACK (hoy
  15/15) y captura/asentamiento de config 2 (todavía abierta).
- El hardware tiene cargados el PSoC/ESP de **test anteriores al port**: D8
  todavía informa que la autocal está desactivada. El port de campo compilado
  en `b122112` no se flasheó durante esta prueba, para no mezclar la evidencia
  ni arriesgar el PSoC sin el `polarity_reg` del TopDesign.
- Los cuatro taps recortan en valores parecidos (~750 y ~1120 mV) cuando la
  cadena está contra un tope. Con el limitador sacado hay que volver a
  caracterizarlo: puede que ya no aparezca.

---

## 3. Lista para vos (mañana)

Ordenada por lo que desbloquea más.

1. **Portar y probar el nuevo `0xAA` de punta a punta.** El TopDesign ya está
   resuelto y el PSoC de campo está cargado. Falta que ESP esclavo, transporte
   maestro y web conserven etapa, signo y magnitud; después comparar +200/0/-200
   sobre una misma etapa y restaurarla.

2. **Confirmar el sentido del bit de polaridad.** Que el bit en 1 signifique
   sumidero (referencia por debajo de `Vref`) está *supuesto*, no verificado. Si
   sale al revés, alcanza con dar vuelta `PSOC_IDAC_POLARITY_NEGATIVE_BIT` en
   `psoc_hw.h`. Se comprueba con `idac 3 -200` y `idac 3 +200` mirando `LPo`:
   el negativo tiene que dar MENOS milivoltios.

3. **Revisar los Kp/Ki contra la placa real.** Salieron de Monte Carlo con la
   planta medida, pero nunca corrieron una calibración completa sobre hardware.

4. La decisión conservadora ya quedó aplicada: `0xAA` sirve para ensayo manual,
   pero la próxima calibración lo pisa y no se guarda en EEPROM como resultado
   bueno sin volver a verificar la cadena.

---

*Última actualización: 2026-09-03 16:48. Reanudación automática de Claude
programada desde las 19:22, cada hora hasta las 09:22, sin corridas solapadas.*
