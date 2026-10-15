# Estado v30 (2026-10-14): larga con registro impersonal, títulos que presentan y dos slides nuevas

**Archivo:** `Presentacion_v30_LARGA_INLINE_123_slides.pptx` (123 slides). La comprimida sigue en v29: se actualiza al final.

**Scripts, en orden:**
1. `apply_v30_larga_textos.py`
2. `restructure_v30_larga.ps1`
3. `apply_v30_larga_nuevas.py`
4. `apply_v30_larga_ajustes.py`
5. `refs_dedupe_reparto.py`
6. `fix_content_types.py`

Los helpers están en `pptx_helpers_v30.py`.

## Reglas aplicadas a toda la larga
- **Registro impersonal (R2.4).** No queda primera persona en títulos ni viñetas. Por ejemplo: «Nos proponemos…» pasó a «Se propone…», «Elegimos ESP-NOW» a «Se eligió ESP-NOW», «Diezmamos» a «Diezmado por media móvil» y «Nuestras señales» a «Las señales de este trabajo». Las notas del orador conservan el tono oral.
- **El título presenta y las viñetas profundizan.** Unos 65 títulos repetían lo que decían sus viñetas y pasaron a presentar el tema. Ejemplos: «Ensayo downhole», «Onda P: onda de compresión», «Polarización de la onda S respecto de la superficie libre» y «Límites de la inversión». Codex (luna, esfuerzo bajo) hizo una primera pasada, pero detectó solo 11 casos; el resto se revisó slide por slide.
- **Un término, un significado (R1.1):** «pequeña señal» pasó a «pequeña deformación».

## Cambios puntuales (numeración v30)
| Slide | Cambio |
|---|---|
| **21 (nueva)** | «Del medio homogéneo al modelo en capas». Figura `figuras_es_v25/fig_capas_es.py`. Las viñetas del terreno en capas salieron de la slide de interfaces |
| 22 | Interfaces: «Al llegar a una interfaz, la onda de cuerpo se divide». Se agregó «Cuánto se refleja depende del contraste entre los dos medios» |
| 23 | Snell: «Se aplica tanto a ondas P como S» |
| 33 | «La superficie libre: una interfaz con su propia condición de frontera». La viñeta de la energía ya no repite el título |
| 37 y 38 | Love y Rayleigh: los sensores aparecen en general, no un geófono en particular («la mayoría de los sensores, que miden en vertical…») |
| 39 | El supuesto va arriba («Suponiendo ν = 0,25, …»). Se quitó la viñeta de porcentajes, que repetía el gráfico |
| 41 | Se quitó Vs ≈ cR/0,9, que repetía cR ≈ 0,9·Vs. «No hay dispersión» pasó a «Todas las frecuencias viajan a la misma cR», porque el concepto todavía no se presentó |
| 44 | «Velocidad de fase y frecuencia en un terreno en capas». La palabra «dispersión» queda solo en la viñeta |
| **54 (nueva)** | «Transductores posibles para la componente vertical»: SM-24, RTC 4,5 Hz, MEMS ADXL355 y Güralp 3ESPC, con precios al 31/08/2026 (tabla de `latex-reestructurado/03_diseno.tex`). Cierra con «Se eligió el SM-24 por disponibilidad» |
| 55 y 56 | El SM-24 quedó antes de la plataforma, que ahora es la 56 |
| Ref. 119–123 | Tres referencias nuevas: Analog Devices, DigiKey y Güralp. Son cinco slides, con 38 entradas únicas |

**Verificación:** `validate.py` pasa. Se midieron los desbordes contra la v29: no hay ninguno nuevo; los 15 que quedan ya estaban en la v29. Se exportaron y miraron las slides 21, 23, 39, 41, 54 y 123.

**Errores corregidos en el camino:**
- La quinta slide de referencias se creó como copia de la cuarta y duplicaba 7 entradas. `refs_dedupe_reparto.py` quita duplicados por texto.
- Al principio moví una referencia a la slide equivocada.

## Para revisar juntos
- **Slide 57:** las cajas de precio (4,5 Hz contra SM-24) repiten parte de la tabla de la 54. ¿Se quitan?
- **Títulos que presentan y «action titles»:** el skill académico prefiere títulos que afirmen la conclusión. Se siguió tu regla: el título presenta y las viñetas profundizan.
- **Gráficos nativos (41 y otros):** usan punto decimal («0.95»).
- **Comprimida:** portar todo y renumerar sus notas («[Slide larga NN]»). Desde la 21 se suma 1; desde la 54, se suma 2, salvo el SM-24, que queda en 55, y la plataforma, en 56.
