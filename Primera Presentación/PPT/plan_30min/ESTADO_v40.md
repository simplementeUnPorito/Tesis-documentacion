# ESTADO v40 — comprimida (2026-10-15, en revisión por loop)

Vigente: `Presentacion_v40_COMPRIMIDA_INLINE_32_slides.pptx`. Se regenera con `comp_v37/build.sh`.

## Cambios pedidos por Elías sobre la v39
- **Slide 6:** se quitó la miniatura del aire, que no se había mostrado. Se agregó la escena SV/SH (polarización) con su propia animación, antes de Snell.
- **Slide 7:** las fotos de downhole y crosshole sí iban a la celda de la tabla, pero la tabla quedaba encima. Ahora todo lo que se mueve queda delante (z-order).
- **Slide 8 y todas las demás:** el riel se compacta hacia arriba en cada clic; si una miniatura sale del riel (por ejemplo, porque va a la tabla), las de abajo suben.
- **En todas:** cada palabra clave entra al riel en el clic SIGUIENTE al que presenta su concepto, como ayuda memoria. Si el concepto está en la última escena, se agrega un clic de cierre en el que solo entra la palabra clave.
- **En todas:** se descartan del riel las miniaturas de contenido que no se mostró en esa slide.
- **Chips:** una palabra corta final (≤3 letras) ya no queda sola en un renglón.
- No se cambió ningún texto de contenido.

## Nota
La v39 que se envió quedó pisada por una compilación intermedia; su contenido equivale a la v40 sin estos ajustes.

## v41 (segunda vuelta del loop)
`Presentacion_v41_COMPRIMIDA_INLINE_32_slides.pptx`: la figura principal (imagen, gráfico o grupo) de cada escena tomada de la larga también pasa al riel al avanzar. Por ejemplo: las capas en la 6, las reflexiones en la 9, G(γ) en la 5, el balance de fuerza en la 15 y FTM en la 28. Así el riel resume todas las escenas, no solo las de la comprimida v29. Recorrido completo revisado.

## Tercera vuelta
Codex (gpt-5.6-luna) controló que cada palabra clave corresponda a su escena. Se aceptó una de sus tres observaciones: en la slide 23, «400 µs: 5° hasta 35 Hz» pasa a la escena 1 y se agrega «Δc/c = c·Δt/Δx», tomado de la ecuación de la escena 2. Las otras dos se descartaron: «Vs pesa el doble» está sostenido por la viñeta, y la clave que falta en la escena 4 de la slide 20 es menor.
