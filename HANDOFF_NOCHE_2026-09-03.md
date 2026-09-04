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

### A. Port al proyecto de campo — PSoC Y TRANSPORTE COMPLETADOS

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

**Cerrado por Codex a las 17:06:** el contrato quedó portado de punta a punta.
El frame USB dirigido usa 7 bytes solamente para `0xAA`; los demás comandos
dirigidos conservan sus 6 bytes. `MsgSetConfig` entre maestro y esclavo lleva
`param2`, el esclavo manda la trama PSoC de dos parámetros, y la web expone una
fila IDAC manual en los paneles GEO. El helper Python es
`encode_manual_idac(node_id, stage, code)`.

Commits de implementación: ESP32 `f748bdb` (`Portar el IDAC firmado de punta a
punta`) y Python `7e66739` (`Agregar encoder del IDAC manual firmado`). Los
commits PSoC previos son `b122112` (port) y `b801b72` (TopDesign de campo).

Compatibilidad deliberada: un cliente viejo que mande `0xAA` en el formato
dirigido de 6 bytes ya no es válido. Los demás comandos dirigidos siguen
idénticos. No volver al `setVdac(uint8_t)` muerto: fue reemplazado por
`setStageDac(signo_etapa, magnitud)`.

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

El firmware de campo del ESP ahora agrega `idac <etapa> <codigo>` para probar
el `0xAA` correcto sin usar el comando homónimo del autotest (`0xA2`). En COM8
se verificaron ACK reales para etapa 3 con `+200`, `-200` y `0`; el último
comando dejó la referencia restaurada a cero. Transcript:
`hardware_idac_signed_2026-09-03.txt`.

### B. Pipeline completo — CONFIGURACIÓN **Y** CAPTURA/INGESTA PROBADAS

Hay un ESP maestro en **COM6** y el esclavo en **COM8**; el PSoC por KitProg en
COM3.

1. PSoC → ESP esclavo: probado con firmware de campo y ACK de `0xAA` firmado.
2. USB binario → maestro → ESP-NOW → esclavo → PSoC: `+200/-200/0`, 3/3 ACK.
3. Página real del master → WebSocket → misma ruta: `+200/-200/0`, 3/3 ACK.
4. LittleFS: `app.js`, `protocol.js` y `slave_panel.js` servidos desde
   `http://192.168.4.1` contienen la UI nueva cargada al master.
5. Helper Python: trama exacta validada para `encode_manual_idac(2,3,-200)`.

Evidencia compacta: `hardware_idac_end_to_end_2026-09-03.txt`.

Builds posteriores a la integración: master `esp32dev`, slave1/2/3 y
`slaveTest`, todos `SUCCESS`. Los firmwares físicos cargados son master COM6 y
slave2 COM8; el filesystem LittleFS del master también quedó cargado.

**Los datos que se ingesten van a una carpeta `lab/`** para no mezclarlos con
los buenos. Se hace con una sola variable: `TESIS_DATA_ROOT=C:\Github\Tesis\data\lab`
manda `raw`, `processed` y `server` adentro de `data/lab`. No hizo falta tocar
código.

#### Ronda de la noche 19:20–20:15 — la ruta de DATOS quedó cerrada

Andaba entera y sin intervención: PSoC → slave2 → ESP-NOW → master → USB →
ZIP v4 → `/ingest` → catálogo. Evidencia:
`docs/hardware_pipeline_captura_2026-09-03.txt`.

- 20 lotes dan 600 muestras exactas; 100 lotes dan 3000. Todas del nodo 2, con
  131 valores distintos de 600, o sea señal y no un valor pegado.
- Ida y vuelta exacta por el ZIP: media 52467 cuentas capturadas, 52467
  releídas del `raw_f32le.bin`.
- El server cataloga la captura: fs 2604, 1,152 s, nodo 2 rol geo,
  `plottable: true`, `estado: "Sin martillo"` (correcto: hay un solo esclavo).
- Lo que hace creíble el número: 52467 cuentas son +1000,6 mV, el **mismo**
  punto de trabajo que venía midiendo el banco por COM8 con el firmware de
  autotest. Dos caminos independientes coinciden.
- Detalle que había que acertar: `raw_f32le.bin` guarda **volts**, no cuentas.
  Verificado contra una captura real de Canchiga antes de escribir nada.

Gate de humo del servidor: **57 de 58**. El único que falla es
`masw.canchita_compatibilidad`, y no es del pipeline — ver la lista de abajo.

### C. Cosas abiertas que conviene cerrar

**Nuevo, y es lo mas importante de la noche: la cadena tarda 31 s en
recuperarse.** Evidencia:
`docs/hardware_recuperacion_saturacion_2026-09-03.txt`.

Al saturar la salida moviendo una etapa de aguas arriba, vuelve al reposo con
un decaimiento exponencial limpio de tau ~ 31 s; entra en banda de 5 mV recien a
los 94 s. La calibracion espera `CAL_PI_SETTLE_SAMPLES_* = 512` muestras =
**0,197 s** en las cuatro etapas, o sea 0,006 tau.

Dos aclaraciones para no sacar la conclusion equivocada:

- Los lazos **no** estan rotos. Se verifico en `calibration_tables.h` que cada
  etapa calibra contra su propio tap (0->ch0, 1->ch1, 2->ch2, 3->ch3), asi que
  el acople de alterna no esta dentro de ningun lazo.
- Lo que si queda en pie es el **acoplamiento entre etapas**: mover una de
  arriba perturba los taps de abajo con ese tau, y la calibracion pasa a la
  siguiente en 0,197 s.
- Falta la medida que decide si hay que subir el settle: el transitorio cruzado
  en los taps intermedios. Necesita el firmware de autotest, o sea el KitProg.
  Sin eso, subir el settle seria adivinar.

**La transferencia de `Vref_LP` no es lineal.** Evidencia:
`docs/hardware_transferencia_vref_lp_2026-09-03.txt`. La pendiente va de 29
cuentas por codigo cerca de Vref a 75,6 en -224, creciendo de forma continua, y
reproduce al repetir bajando y subiendo (histeresis de 0,7 a 1,9 mV). La
sintonia Kp/Ki del Monte Carlo asume ganancia de etapa fija; medida varia un
factor 2,6 segun donde trabaje el lazo. El peor caso es arrancar desde el
extremo negativo.

**Las etapas 0, 1 y 2 no se pueden caracterizar desde la salida.** Su efecto en
continua se lo come el acople; solo dejan un transitorio largo. Hay que medirlas
en su propio tap, y eso tambien necesita el autotest.

**Las cuatro configuraciones del ADC no coinciden entre sí.** Evidencia:
`docs/hardware_adc_configs_2026-09-04.txt`. Con la misma entrada física, config 1
da 999,6 mV (repite, y coincide con el banco por COM8), config 3 da 39,2 mV,
config 4 da 42,4 mV y config 2 da −440,6 mV. Si midieran lo mismo con su escala
correcta, todas darían ~1000 mV. **Sólo la configuración 1 está validada**, y eso
reencuadra la anomalía que estaba anotada como "config 2 falla a veces": la
premisa de D5 —comparar un nodo entre configuraciones— no se puede cumplir
todavía, y su SKIP no era un falso negativo.

**Capturas vacías esporádicas, ~4 %.** Evidencia:
`docs/hardware_capturas_vacias_2026-09-04.txt`. Se descartó la explicación
razonable (que fallara la primera captura tras abrir el puerto): con esperas de
2,5 / 5 / 8 / 12 s ninguna primera falló, y la única vacía fue una segunda. No se
agregó ningún reintento: taparía el síntoma. El camino de COMANDOS no falla
(0 de 60 en 0xAA, SET_RECLEN y ARM).

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
- El hardware ahora tiene cargados el PSoC de **campo** con `polarity_reg`, el
  ESP slave2 de campo y el ESP master nuevos. No interpretar los resultados D8
  antiguos como estado del firmware que está actualmente en la placa.
- Hubo un timeout aislado de ACK al mandar tres cambios directos muy seguidos
  por COM8; `probe` mostró el enlace vivo y el reintento respondió. Las dos
  rondas de punta a punta (USB master y WebSocket) dieron 3/3 cada una.
- El snapshot ADC de campo mostró una vez +200 en etapa 3 como ~1106 mV y el
  negativo cayó a 0, pero después las lecturas quedaron en 0 incluso al volver
  a positivo. No usar esa secuencia como prueba concluyente del sentido físico:
  repetir con DMM/osciloscopio en LPo o depurar el snapshot antes de afirmar
  polaridad en campo.
- Los cuatro taps recortan en valores parecidos (~750 y ~1120 mV) cuando la
  cadena está contra un tope. Con el limitador sacado hay que volver a
  caracterizarlo: puede que ya no aparezca.

---

## 3. Lista para vos (mañana)

Ordenada por lo que desbloquea más.

1. **No rehacer el port `0xAA`: ya está probado y documentado.** Revisar los
   commits del ESP/Python y las dos evidencias antes de continuar.

2. ~~Confirmar el sentido del bit de polaridad.~~ **RESUELTO en la noche, no
   hay nada que hacer.** El bit está al derecho: `+240` da 1122,2 mV y `-240`
   da 745,7 mV, una diferencia de +376,5 mV, medida por la ruta de captura. El
   control es sólido: el código 0 medido tres veces intercalado entre los
   extremos dispersa 0,42 mV, o sea 900 veces menos que la señal. **No** hay que
   dar vuelta `PSOC_IDAC_POLARITY_NEGATIVE_BIT`.

2ante. **Mirá si la tapa cerrada apaga dispositivos.** Hay un patrón: el
   KitProg no enumera *y* el adaptador WiFi, estando habilitado
   (`AdminStatus: Up`), devuelve **cero** redes en un scan, lo cual es
   imposible en un entorno normal. Las dos cosas empezaron después de cerrar la
   tapa. Si abrirla los recupera, se destraban de una vez dos pendientes: la
   medición por tap (necesita el KitProg) y la prueba de la página web (necesita
   asociarse al AP `GeoNetwork`, cuyo perfil está guardado). No toqué la radio:
   deshabilitar y rehabilitar el adaptador de madrugada, sin nadie mirando,
   podía dejarte sin WiFi a las 8.

2bis. **Enchufá el KitProg cuando puedas.** Es lo único que bloquea de verdad.
   Sin él no puedo poner el firmware de autotest en el PSoC, y eso es lo que
   hace falta para medir los taps intermedios: caracterizar las etapas 0, 1 y 2
   (que desde la salida no se ven) y medir el transitorio cruzado que decide si
   hay que subir el tiempo de asentamiento de la calibración.

2ter. **Mirá los picks de Canchita: puede que se hayan perdido.** El gate de
   humo falla en `masw.canchita_compatibilidad` y al investigarlo aparece esto:
   `data/processed/Canchita/field_review_masw_state.json` dice 2 picks, 1 grupo
   y 0 regiones, pero el `.npz` de al lado guarda `inv_freqs`, `inv_c_obs` e
   `inv_c_t` con **112 puntos** y `wf_group_ids` con **2 grupos**. O sea que el
   JSON se truncó y el npz conservó la evidencia de lo que había. El archivo es
   del 2026-08-20, muy anterior a esta sesión, y `data/` no está versionado, así
   que no hay historial. La curva pickeada se puede reconstruir desde el npz
   (`inv_freqs` + `inv_c_obs` son exactamente eso). Decidí vos si reconstruirla
   o si simplemente el chequeo quedó viejo respecto de tu trabajo posterior.

3. **Revisar los Kp/Ki contra la placa real**, ahora con dos motivos nuevos y
   concretos: la ganancia de etapa varía un factor 2,6 a lo largo del rango
   (la sintonía la asume fija) y el acoplamiento entre etapas tiene tau ~31 s
   contra 0,197 s de espera. Nunca corrió una calibración completa sobre
   hardware.

4. La decisión conservadora ya quedó aplicada: `0xAA` sirve para ensayo manual,
   pero la próxima calibración lo pisa y no se guarda en EEPROM como resultado
   bueno sin volver a verificar la cadena.

---

### D. Reanudación nocturna

- Tarea de Windows `ClaudeReanudarTesis`: `Ready`, próxima corrida 19:22,
  repetición horaria hasta 09:22, política `IgnoreNew`.
- Script: `src/firmware/psoc/reanudar_sesion.ps1`.
- Commit del script actualizado: `00241cc`; ya identifica COM8 como firmware
  de campo y ordena continuar captura/ingesta sin repetir el port `0xAA`.
- Sesión exacta: `claude --resume 17391455-01f5-43a8-8b39-2717439e180c`.
- Log: `%LOCALAPPDATA%\claude_reanudar`.
- La última corrida manual terminó limpiamente al encontrar la cuota de Claude;
  el scheduler volverá a intentar. Ethernet mantiene salida a Internet aunque
  WiFi quede conectado al AP `GeoNetwork` para el banco.

---

*Última actualización: 2026-09-04 00:50. Ruta de datos e ingesta cerradas,
polaridad resuelta, y cinco hallazgos de planta/instrumentación en la
sección C.*