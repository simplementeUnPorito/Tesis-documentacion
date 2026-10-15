# Estado v33 (2026-10-14): larga de 125 slides, lista para la lectura final de Elías

**Archivo:** `Presentacion_v33_LARGA_INLINE_125_slides.pptx`. Parte de la v32 guardada por Elías a las 23:45, que no se tocó.

**Scripts:** duplicado de la 64 con PowerPoint, `apply_v33_larga.py`, `apply_v33_coherencia.py` y `fix_content_types.py`. Figura nueva: `figuras_es_v25/fig_balance_fuerza_es.py`.

## Cambios
| Slide | Cambio |
|---|---|
| 64 | **Resistencia negativa.** Tiene la ecuación de ζ con Z_L. Viñetas: una carga activa Z_L negativa cancela parte de R_i y sube el amortiguamiento; es un lazo con realimentación positiva que puede volverse inestable si R_i cambia con la temperatura; a frecuencias altas, la inductancia distorsiona la respuesta (Ma et al., 2023, la fuente que cita el capítulo 02b) |
| 65 (nueva) | **Balance de fuerza.** Figura del lazo (geófono → medición → controlador → bobina) y tres viñetas. Cierra con «Funciona. Pero para un nodo multicanal barato y replicable…». Fuentes: Zhang et al. (2025) y Song et al. (2016), según Ma |
| 62 | La tarjeta de técnicas activas describe las dos: «con una carga negativa o con corriente en la bobina» |
| 63 | «cerca de DC» pasó a «cerca de continua», el término que usa el resto de la presentación |
| 95 | Se quitó «No se conservaron coordenadas ni azimut», que ya está en la 93 |
| 96 | La frase final ahora dice «…no se cumple: por eso se prueba Wi-Fi FTM», en coherencia con la 115 |
| 97 | **Se repuso «Con 400 µs, los 5° se cumplen hasta unos 35 Hz».** La limpieza de citas de la v29 la había borrado por error porque terminaba en «(cálculo propio)». El pie explicaba los 35 Hz, pero la slide no los mostraba. Fue el único caso; se revisó la lista completa de la limpieza |

**Verificación:** `validate.py` pasa y no hay desbordes nuevos. Se exportaron y miraron las slides 64, 65 y 97.

## Lectura preliminar: lo que no se cambió, para decidir
1. **48, «Extrapolarla reduce la incertidumbre».** Sigue pendiente desde la v28. Extrapolar un dato puntual suele aumentar la incertidumbre. ¿La idea era «usarla como restricción de la inversión»?
2. **58, plataforma.** Queda entre el SM-24 (57) y el modelo mecánico del geófono (59), así que corta el bloque del geófono. Es el orden que pediste para definir el geófono antes de hablar de nodos GEO. La otra opción es poner el modelo mecánico (59–61) antes de la plataforma.
3. **Comprimida:** cuando se porte, tiene el mismo faltante de los 35 Hz (era su slide 19).
