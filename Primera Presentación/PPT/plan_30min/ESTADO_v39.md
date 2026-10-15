# ESTADO v39 — comprimida (2026-10-15)

**Entrega vigente para el tutor:** `Presentacion_v39_COMPRIMIDA_INLINE_32_slides.pptx` (32 slides, 130 pasos por clic).
Vista previa: `Presentacion_v39_COMPRIMIDA_por_clics.pdf`. La larga sigue siendo la v37.

## Cambio respecto de la v38
Elías rechazó la escena final «En resumen» con chips grandes: las palabras clave van **en el riel lateral derecho,
durante el desarrollo**. En la v39:
- Cada palabra clave entra al riel en el clic en que se presenta su concepto y queda hasta el final del tema.
- El riel intercala miniaturas y palabras clave en orden de aparición; se reparte en N casilleros entre 1,1 y 4,95 pulgadas.
- Si el contenido de un tema ocupaba todo el ancho, se escala (fuentes incluidas) para terminar en x = 8,12 pulgadas.
- En las escenas tomadas de la larga, las miniaturas del riel siguen visibles.
- Las palabras clave y la escena en la que entran están en `comp_v37/spec.py`, diccionario `KEYS`.
  La versión con escena de resumen quedó en `comp_v37/spec_v38_resumen.py`.

## Verificación
- validate.py PASS; check_anim_todas: 28 slides con timing, 0 problemas; recorrido completo en PowerPoint revisado.
- check30 marca desbordes de 3 a 20 pt en algunas cajas; a la vista no se solapan con nada.

## Pendientes
Los mismos de `ESTADO_v38.md`.
