# Memoria de auditoría de correctness — 2026-09-02

Documento de coordinación para continuar la auditoría sin perder evidencia.
No constituye el informe final. Cada ítem sólo pasa a `FIXED` después de una
reproducción que falle antes y un test que pase después.

## Reglas invariantes

- No cambiar algoritmos científicos sin ground truth sintético reproducible.
- No usar `abs(fase)` para ocultar una convención de signo incorrecta.
- No modificar topología analógica hasta una decisión explícita de hardware.
- No reescribir regresiones F1/F5/F9 cuando los tests existentes pasan.
- No borrar código legacy sin comprobar importadores y pipeline vigente.
- Seeds fijas para toda prueba estocástica.
- No hacer push durante esta auditoría sin autorización explícita.

## Estado de trabajo

| ID | Prioridad | Tema | Estado | Evidencia siguiente |
|---|---:|---|---|---|
| MASW-1 | P0 | coherencia en `two_receiver_dispersion` | FIXED | ruido independiente: mediana 1.0 antes, 0.0077 después |
| MASW-2 | P0 | signo y ambigüedad de fase de dos receptores | FIXED + LIMITATION | 4 ground truths pasan; alias 400/80 m/s demostrado |
| MASW-3 | P0 | signos de las dos imágenes phase-shift | FIXED | onda 300 m/s: legacy fallaba 4/4; ahora coincide con activo/referencia |
| INV-1 | P0 | mínimo de raíces en `dispersion_misfit` | FIXED | N=3,5 y pares cubiertos; usa ceil(N/2) |
| INV-2 | P1 | semántica `reversals` y fallback | FIXED | perfiles monótono/1/2 inversiones; suffix-sort preserva contrato maswavespy |
| INV-3 | P1 | cancelación de `progress_cb` | FIXED | cancelación antes/durante y callback final cubiertos |
| PROTO-1 | P2 | ACK/configuración uint8 | CLASSIFIED + FIXED PROBE | wire low8 deliberado; `ws_cmd_test` dejó de formar uint16 falso |
| PCB-1 | P2 | conteos README vs `validate.py/spec.py` | FIXED DOCS | README sin conteos duplicados; validador deriva 53/41 |
| HW-1 | DECISION | VREF/AMS1117/ADJ/IDAC | NEEDS HARDWARE | matriz completa creada; topología intacta |
| REG-F1 | REG | watchdog de captura SD larga | PASS | 16/16; branch SD nunca llama START_NOW |
| REG-F5 | REG | WebSocket half-open | PASS | watchdog pre-DATA; ping/actividad y pausa/reanudación revisados |
| REG-F9 | REG | carrera START/HOT_WAIT/ARMED | PASS | 4/4; retry sólo reconsulta HOT_WAIT, no reenvía PRESTART |

## Evidencia P0

- MASW-1: `tests.test_masw_analysis` falló antes con coherencia mediana 1.0
  para dos ruidos independientes. Welch/CSD segmentado produce mediana
  0.0077038 y percentil 95 de 0.0256409 con seed 20260902.
- MASW-2: para `cos(2πf(t-x/c))`, `angle(CSD(x1,x2))=-kΔx`; el estimador
  correcto es `-2πfΔx/dphi`. Cuatro casos no ambiguos pasan con SNR 8–30 dB.
  Dos velocidades de 400 y 80 m/s dan la misma fase envuelta cuando
  `fΔx/c=0.25` y `1.25`; dos receptores no pueden distinguirlas.
- MASW-3: la imagen offline daba 240/500/455/125 m/s para ground truth de
  300 m/s. El backend activo y la ecuación de MASWavesPy daban 300 m/s. Tras
  usar compensación positiva sobre la fase FFT sin conjugar, coinciden.
- INV-1: antes se aceptaban 1/3 y 2/5 raíces. El mínimo correcto es
  `ceil(N/2)`; se cubrieron además 2/4 y 3/6 como límites aceptados.

## Evidencia P1/P2 y regresiones

- INV-2: maswavespy restringe `beta[reversals:]`; el fallback local ordenaba
  todo el perfil. Tests forzaron los 50 rechazos y demostraron pérdida de una
  y dos inversiones. Ahora sólo se ordena el sufijo restringido.
- INV-3: retornar `False` en callback inicial ejecutaba igualmente una
  propuesta. Ahora devuelve el modelo inicial, una llamada forward y history
  vacío. Cancelación durante y final conservan 1/N iteraciones.
- PROTO-1: 0xAD/0xAE transportan N en uint16 hacia el maestro/esclavo, pero el
  ACK de seis bytes sólo refleja low8 en b1; ningún consumidor activo lo usa
  como longitud completa. `ws_cmd_test` sí combinaba b1:b0 y mostraba 22528
  para low8=88; quedó corregido y cubierto.
- PCB-1: README declaraba 46 partes/37 redes, Micro-USB y 175x125; `spec.py`
  deriva 53/41, header 1x02 y 200x300. Se eliminó duplicación documental.
- HW-1: `docs/proyecto/HARDWARE_REFERENCE_ASSUMPTIONS_2026-09-02.md` calcula que los valores
  compilados producen 2.0622 V, aunque nombres/serigrafía dicen 2.048 V. No se
  eligió topología ni se cambió firmware/PCB.
- F1/F5/F9: gates offline 16/16, PASS de watchdog pre-DATA y 4/4; rutas
  alternativas inspeccionadas sin reescribir mecanismos.
- El árbol PSoC conserva un archivo personal `.cywrk.elias` modificado desde
  antes de la auditoría. Debe permanecer fuera de commits.

## Hallazgo adicional de validez numérica

- `masw_bench/test_sintetico.py` evaluaba una onda no dispersiva de 90 m/s en
  20–35 Hz con dx=2 m, aunque su límite espacial es 22,5 Hz. El propio mask
  forzaba una aparente cresta de ~112 m/s. No era un bug del algoritmo sino un
  benchmark inválido (`LEGACY TEST`). La banda se limitó a 12–20 Hz y ahora los
  ocho métodos recuperan exactamente 90 m/s; se agregó aserción cuantitativa.

## Última ejecución

- Inicio: 2026-09-02, America/Asuncion.
- Repositorios prioritarios localizados y búsquedas iniciales realizadas.
- Último avance: P0/P1/P2 solicitados clasificados; 28 tests de interfaces,
  4 tests MASW nuevos, 16 tests históricos sin pytest, 2 verificadores de
  transforms, JitX y regresiones F1/F5/F9 pasan. Benchmark sintético legacy
  corregido para respetar aliasing espacial.
- Firmware recompilado sin programar hardware: ESP32 `master/esp32dev`,
  `slave/slave2` y `slave/slaveTest` OK; PSoC de campo OK (flash 23,1%, SRAM
  79,2%) y PSoC autotest OK (flash 25,7%, SRAM 26,5%). PSoC Creator conserva
  warnings preexistentes de P15[1], timing CyBUS_CLK y duplicados M0072 durante
  API generation, pero ambos enlaces y HEX finalizaron con `Rebuild Succeeded`.
- Commits creados: cálculos `2c93e19`, interfaces `d1475a5`, ESP32 `247cb0c`,
  PCB `9e6e4ec`. No se hizo push. Los artefactos generados del rebuild PSoC,
  el archivo personal `.cywrk.elias` y un `.pyc` del ESP permanecen fuera.
- Próximo paso: preparar informe final raíz, repetir gates finales y registrar
  commit raíz sin incluir estado personal/generado.
