# Matriz de supuestos de referencia analógica — 2026-09-02

Inventario de sólo lectura para decidir entre la topología actualmente
modelada (AMS1117-ADJ) y una referencia externa de 2,5 V con ramas IDAC. **No
se modificó la arquitectura eléctrica.**

## Distinción necesaria

La red actual `VREF` de 2,5 V es la salida `Ref2V5` bufferizada del propio PSoC
y polariza guarda/geófono y etapas analógicas. `VREF_2V048` es otra red: en el
modelo actual la genera un AMS1117-ADJ y alimenta las cuatro resistencias de
30 kΩ usadas por los IDAC. Una futura referencia externa de 2,5 V no debe
confundirse automáticamente con la `VREF` interna ya existente.

Con los valores que realmente compila el PSoC:

```text
R22 = 1.0 kΩ, R23 = 620 Ω, VREFint = 1.250 V, IADJ = 60 µA
VOUT = 1.250*(1 + 620/1000) + 60e-6*620 = 2.0622 V
IDAC full scale = 31.875 µA; R = 30 kΩ; excursión = 0.95625 V
rango nominal calculado = 2.0622 … 3.01845 V; LSB = 3.75 mV
```

Por lo tanto, el nombre y la serigrafía `VREF_2V048` no coinciden exactamente
con el modelo numérico vigente de 2,0622 V. Esto queda como decisión de
hardware/documentación; no se corrigió forzando uno de los dos valores.

## Archivo → supuesto → consecuencia

| Archivo o grupo | Supuesto hard-coded | Consecuencia si cambia la topología |
|---|---|---|
| `PCBs/JitX/tesis_carrier/spec.py` | U1=`AMS1117-ADJ`; R22=1 kΩ, R23=620 Ω; C18=22 µF, C19=10 µF; cuatro R11–R14=30 kΩ conectadas a `VREF_2V048`; red `VREF_ADJ` | Cambia BOM, netlist, jerarquía, placement, clases de red y puertos de subsistemas. Es la fuente programática activa del PCB. |
| `PCBs/JitX/tesis_carrier/components.py` | Símbolo/landpattern SOT-223 y MPN AMS1117-ADJ | Debe sustituirse o dejar de instanciarse si se elige una referencia dedicada. |
| `PCBs/JitX/tesis_carrier/main.py` | Bloque jerárquico AMS1117, fórmula del divisor y serigrafía `VREF 2.048V REGULATOR` | El esquema generado y la serigrafía quedarían falsos aunque sólo se cambiara `spec.py`. |
| `PCBs/JitX/tesis_carrier/validate.py` | Exige U1/R22/R23, `VREF_ADJ` y que R11–R14 cuelguen de `VREF_2V048`, no de `VREF` | El validador rechazará deliberadamente cualquier nueva topología hasta que la decisión se implemente junto con reglas nuevas. No relajarlo antes. |
| `PCBs/JitX/tesis_carrier/rules.py` y `kicad_postprocess.py` | Tratan 2,048 V/ADJ como referencia analógica y pin especial | Afecta reglas de ruteo, nombres y postproceso KiCad. |
| `PCBs/JitX_para_port/tesis/tesis/{spec,components,main,rules,validate,kicad_postprocess}.py` | Copia casi completa de los mismos supuestos AMS1117 | Hay dos árboles que deberán actualizarse juntos o declararse uno no autoritativo; cambiar sólo el JitX activo deja el port divergente. |
| `PCBs/JitX_para_port/tesis/README.md` | Rotulado `VREF_2V048`/`VREF 2.048V REGULATOR` | Documentación y capturas generadas quedarían obsoletas. |
| `PCBs/KiCad/generate_complete_schematic.ps1` | Generador histórico de la placa completa; incluye la arquitectura analógica del port | Si aún se usa para regenerar, puede reintroducir la topología anterior. Debe compararse con JitX antes de reutilizarse. |
| `PCBs/KiCad/Tesis_complete.kicad_sch` y `Tesis_complete_analysis.json` | Artefactos generados con redes/valores actuales | Son evidencia/salida, no el lugar para decidir la topología; deben regenerarse después de cambiar la fuente. |
| `src/firmware/psoc/AcondicionamientoAnalogico.cydsn/psoc_hw.h` | Fórmula AMS1117, R22/R23, 30 kΩ, 31,875 µA y máximo 255 | Define la conversión código↔µV que usa el firmware de campo. Cambiar sólo PCB sesga tensiones nominales, targets y diagnósticos. |
| `src/firmware/psoc/AcondicionamientoAnalogico.cydsn/psoc_hw.c` | Inicializa globales con esos defaults y calcula `Vref + I·R` | Todas las conversiones nominales parten de 2,0622 V hasta que algún código escriba las globales; hoy no se encontró un override activo. |
| `src/firmware/psoc/AcondicionamientoAnalogicoTest/AcondicionamientoAnalogico.cydsn/psoc_hw.{h,c}` | Copia del mismo modelo numérico | El autotest puede discrepar del firmware de campo si sólo se actualiza uno de los dos árboles. |
| `src/firmware/psoc/AcondicionamientoAnalogicoTest/.../calibration.{c,h}`, `main.c`, `psoc_selftest.h` | Cuatro IDAC8 como estímulo de calibración y barrido de taps | La maquinaria sigue siendo válida sólo si se redefine y valida el modelo de planta; D8 ya está deshabilitado porque el port VDAC→IDAC no está validado. |
| `src/firmware/psoc/BUILD_PROGRAM_PSOC.md` | Publica todavía 2,048–3,004 V, aunque el header calcula 2,0622–3,01845 V | Riesgo de usar documentación nominal distinta del binario. Requiere decisión: renombrar/retocar divisor o actualizar objetivos/documentos. |
| `src/firmware/psoc/AUTOTEST_NODO_ESCLAVO.md` | D2 usa IDAC→tap; D8 queda SKIP hasta validar planta/targets PI | D2 puede medir conectividad y pendiente, pero no valida por sí solo la exactitud absoluta de la referencia. D8 no debe habilitarse por un cambio documental. |
| `src/firmware/esp32/Nodo comunicación/slave/src/main_selftest.cpp` | Umbrales de pendiente IDAC y D8 deshabilitado; consume resultados nominales PSoC | Un nuevo LSB o sentido de inyección exige nuevos ground truths de banco antes de tocar umbrales. |
| `src/firmware/esp32/Nodo comunicación/slave/src/psoc_uart.h`, `autotest_runner.py`, `test_autotest_format.py` | Protocolo/nombres IDAC y formato de resultados | En general no dependen del valor absoluto de VREF; cambiar sólo el texto/formato no arregla el modelo eléctrico. |
| `*.cycdx` y `*.svd` de ambos workspaces PSoC | Metadatos generados de componentes IDAC | Confirman instancias internas, pero no describen la referencia externa ni sustituyen el esquema de placa. |
| `artifacts/autotest_placa_2026-09-02_post_resoldado.json` | Evidencia histórica de una corrida | No debe reescribirse si cambia la arquitectura; sirve para comparar revisiones. |

## Decisiones requeridas antes de editar

1. Tensión nominal y tolerancia/ruido requeridos para la referencia de las
   ramas IDAC.
2. Componente concreto (y disponibilidad/encapsulado) si se adopta referencia
   dedicada de 2,5 V.
3. Si la nueva red será independiente de `Ref2V5` del PSoC o si se pretende
   unirlas; esta última opción cambia polarización, guarda y filtros, no sólo
   calibración.
4. Rango objetivo de tensión por etapa, sentido de corriente IDAC y margen a
   rieles/ADC.
5. Fuente autoritativa entre `JitX/` y `JitX_para_port/`.
6. Medición de banco de VREF, LSB y pendiente por rama antes de reactivar D8 o
   declarar exactitud absoluta.

