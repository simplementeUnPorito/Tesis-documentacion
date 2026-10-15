# ESTADO v38 — comprimida (2026-10-15)

**Entrega vigente para el tutor:** `Presentacion_v38_COMPRIMIDA_INLINE_32_slides.pptx` (32 slides, 157 pasos por clic).
Vista previa clic a clic: `Presentacion_v38_COMPRIMIDA_por_clics.pdf`.
La larga sigue siendo `Presentacion_v37_LARGA_INLINE_126_slides.pptx`.

## Qué es
- Un tema por slide (28 temas + portada, conclusiones, preguntas, referencias y anexo).
- Se conserva la coreografía original de la comprimida v29 (anim3): zoom a la tabla de métodos, cambio de nombres por fotos,
  objetos que persisten y se mueven, viñetas de a una.
- Los textos se actualizaron a la larga v37 (textmap); los párrafos con fórmulas se injertan desde la v37 con su OMML.
- Las escenas que no existían en la v29 se arman con el contenido de la larga v37 (slides 18, 21, 35, 39, 56, 60, 63–65, 69, 80, 116, 117, 120–124).
- Cada tema cierra con una escena «En resumen» de palabras clave en color.
- Las notas de cada slide dicen de qué slide de la larga viene cada escena.

## Cómo se regenera
`comp_v37/build.sh` (compose.py + spec.py + textmap.json, sobre la comprimida v29 y la choreo de `toolkit/tesis_toolkit_codigo_v27.zip`).
La estructura y las palabras clave están en `comp_v37/spec.py`.

## Verificación
- validate.py PASS; check_anim_todas: 28 slides con timing, 0 problemas.
- Recorrido completo en PowerPoint (walk_powerpoint.ps1), 157 capturas revisadas.

## Pendientes conocidos
- Slide 21 lleva el pie «[REVISAR GRAFICO]», heredado de la larga v37.
- Slide 17: «ζ1 ≈ 938», tal como figura en la larga (revisar con la nota de la memoria sobre ζ).
- Siguen los pendientes de la v37: «Frequencia» en la fig. 9 de Zhang, el volumen y las páginas de Z. Zhang (2025) y la fecha de la portada.
