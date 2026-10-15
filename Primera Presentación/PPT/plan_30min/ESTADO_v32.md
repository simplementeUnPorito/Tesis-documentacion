# Estado v32 (2026-10-14): larga de 124 slides

**Archivo:** `Presentacion_v32_LARGA_INLINE_124_slides.pptx`. Parte de la v31 tal como la dejó Elías: con slides movidas, la 94 borrada (figura repetida), «Una captura real» borrada y el HAMMER en la 79 sin el diagrama de bloques. La v31 no se tocó.

**Scripts, en orden:**
1. `restructure_v32_larga.ps1`
2. `apply_v32_larga.py`
3. `refs_dedupe_reparto.py`
4. `apply_v32_ajustes.py`
5. `fix_content_types.py`

## Cambios (numeración v32)
| Slide | Cambio |
|---|---|
| 62 | Compensación inversa: «…amplifica el ruido de baja frecuencia y el offset, y lleva fácilmente a la saturación». Antes decía «inestabilidad», y eso chocaba con la 66, que define como estable a todo filtro en serie sin lazo; la compensación inversa también es un filtro en serie. La 63 y Hakimitoroghi hablan de saturación |
| 64 | La viñeta acompaña la Z_L de la ecuación: «Una carga activa Z_L (resistencia negativa) modifica el amortiguamiento» |
| 79 | HAMMER: se agregó la cita PCB Piezotronics (2025). La tercera viñeta ahora anticipa la parte digital del GEO, que se explica después |
| 80 | Delta-sigma: la punta de la flecha cae sobre la curva naranja. Antes quedaba 7 dB por debajo |
| 94 | Error de posición (antes 104), movido junto a la geometría y al receptor móvil |
| 95 | Tabla de alternativas con fuentes: Wi-Fi, IEEE Std 802.11-2020; LoRa, Semtech AN1200.13; GPS, Geometrics Atom-3C. La fila UWB pasó a Wi-Fi FTM (≈150 ns, preliminar, trabajo en curso). Se actualizaron las notas |
| 103–104 | La descarga por lotes y los pares de ESP-NOW quedaron después de la sincronización |
| **114 (nueva)** | Trabajo en curso: sincronización por Wi-Fi FTM. Captura de osciloscopio de `FTM-test` y 85 de 85 sesiones completas. Entre esclavos, ≲150 ns: es preliminar, porque los canales no están identificados |
| **115 (nueva)** | Trabajo en curso: martillete de leva inspirado en Da Vinci. Usa las figuras del concepto y del estado actual de `latex-15p-review` |
| — | Se borraron la slide de UWB y la de riesgo del watchdog. Lo del watchdog quedó anotado como pendiente de firmware, fuera de la presentación |
| **123 (nueva)** | Divisor «Anexo»; la 124 (separación y apertura) queda en el anexo |
| Referencias | Entraron IEEE 802.11-2020, Semtech AN1200.13, Geometrics Atom-3C y abbbe/fts. Salieron Korsimaa, Xue y Pérez-Solano, que ya no se citan |

**Verificación:** `validate.py` pasa. Los únicos desbordes son los que ya estaban en la v29. Se exportaron y miraron las slides 64, 79, 80, 95, 114, 115 y 123.

## Para conversar
- Se borró «Una captura real». ¿Fue a propósito? Era la que mostraba el HAMMER y el geófono en una misma captura.
- Wi-Fi FTM: los ≈150 ns son una observación tuya sobre GPIO4, que conmuta por software. El paso siguiente es medir GPIO7 contra GPIO7 con los canales identificados (`FTM-test/experiments/ESTADO_ACTUAL.md`).
