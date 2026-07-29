# Continuidad — compresión a 5 páginas de Urucom_2026_compact

Última actualización: 2026-07-27.

Copia de trabajo de `docs/Urucom_2026/` para el pase de compresión a 5 páginas (límite duro URUCON, §2.2 de `Propuesta Urucom/URUCON_REQUIREMENTS.md`). El original en `Urucom_2026/` no se tocó.

## Protocolo seguido (heredado de `Propuesta Urucom/CONTINUIDAD_REVISION.md`)

- Cambios de contenido/texto: marcados con `\rev{...}` (rojo) para revisión visual.
- Cambios puramente de maquetación (espaciado, tamaño de imagen): **no** se marcan con `\rev` porque no hay texto que colorear; se documentan acá.

## Punto de partida

Tras restaurar 4 figuras y una referencia cruzada que faltaban (ver conversación previa: `fig:analog_path`, `fig:analog_response`, `fig:calibration_trace`, `fig:waterfall`, `sec:pga-note`), el paper compilaba correcto pero en **6 páginas** en vez de 5.

## Recortes aplicados, en orden

1. **Cortada la subsección "Analog Front-End Characterization"** (§IV-A): figura `fig:analog_response` (chequeo de barrido inicial) + sus dos párrafos. El propio texto la describía como *"a consistency check... rather than an end-to-end validation"* — no es evidencia de la calibración en sí. `waterfall` **no se tocó**, según pedido explícito. → seguía en 6 páginas, pero el desborde bajó a ~235 palabras en página 6 (solo cola de referencias).

2. **Cortadas dos frases genéricas** (sin contenido científico):
   - Roadmap de la Introducción ("*The remainder of this paper is organized as follows...*").
   - Lista de future-work al final de la Conclusión ("*gain calibration, thermal compensation, and adaptive bias adjustment*" → reemplazada por una cláusula corta genérica).
   → bajó a 115 palabras en página 6.

3. **Espaciado de referencias apretado** (`references/references.tex`): `\baselinestretch` local a 0.92 dentro del grupo de la bibliografía, más `\topsep`/`\partopsep` a 0. Tamaño de fuente (`\scriptsize`) sin cambios. → bajó a 86 palabras en página 6 (4 referencias colgando, ~11 líneas).

4. **Compresión global de layout** (`config/preamble.tex` + los 4 `\includegraphics` del documento):
   - `\linespread{0.97}` global (interlineado del cuerpo).
   - `\textfloatsep` 6pt→4pt, `\intextsep` 5pt→3pt, `\abovecaptionskip` 3pt→2pt.
   - Las 4 imágenes del paper (`grafico_churro`, `psoc_foreground_calibration_flow...`, `autocalibration_scope_sum`, `waterfall_wiggle_horizontal`) reducidas a 95% de su ancho de columna/página.
   → **5 páginas**, 0 `??`, 0 citas indefinidas, sin overfull hboxes (solo underfull \vbox benignos).

## Cumplimiento con URUCON_REQUIREMENTS.md

Ninguno de estos 4 pasos toca márgenes, tamaño de página, o la plantilla IEEE Conference A4 (§2.2). El tamaño de fuente del cuerpo tampoco cambió — solo interlineado, espaciado entre floats/caption, y escala de imagen al 95%. Verificado: no hay overfull hbox (nada invade márgenes).

## Pendiente / a decisión del usuario

- Si en algún momento se agrega más contenido y vuelve a desbordar, el próximo candidato en el ranking de la revisión previa es achicar `fig:analog_path` (diagrama "churro") de `figure*` a una columna, o recién ahí tocar `fig:waterfall`.
- Falta trasladar estos mismos recortes a `Urucom_2026/` (el original) si el usuario decide adoptarlos como versión final, o descartarlos si prefiere mandar la versión de 6 páginas a otro venue sin límite de 5.
