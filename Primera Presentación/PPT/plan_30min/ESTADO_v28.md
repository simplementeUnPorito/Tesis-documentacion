# Estado v28 (2026-10-14): corrección de redacción sobre la v27

**Archivos:** `Presentacion_v28_COMPRIMIDA_INLINE_29_slides.pptx` y `Presentacion_v28_LARGA_INLINE_118_slides.pptx`. La v27 queda sin tocar. El anexo de videos sigue siendo el de la v24.

## Qué se hizo
Se aplicó una pasada de redacción con el criterio de ASD-STE100, adaptado al español académico (skill `ste-academico-es`). Solo se tocó el texto visible de las diapositivas. **No se tocaron las notas del orador**, las fuentes ni las referencias.

- Comprimida: 51 cambios. Larga: 44 cambios. La larga no tiene los títulos de sección que agrupan diapositivas en la comprimida, así que esos 7 títulos solo cambian en la comprimida.
- No se cambió ningún número, unidad, cita ni cautela («por confirmar», «inferencia propia», «NO MEDIDO» siguen igual).

| Regla | Qué se corrigió | Ejemplo |
|---|---|---|
| Sin punto y coma (STE 8.1) | Unas 35 frases unidas con «;» se separaron en dos oraciones o se unieron con «y» o «pero» | «…es viable; falta validar…» → «…es viable, pero falta validar…» |
| Oraciones de más de 25 palabras (R2.1) | Slide 14 (comprimida), slide 60 (larga): la frase sobre Pazos se partió en tres | — |
| Verbo comodín y nominalización (R1.3) | «realiza la medición» → «mide»; «método de medición del terreno que, mediante el procesamiento de lo sensado…» → «método que mida el terreno y procese lo medido…» | — |
| Impersonal con «se» (R2.4) | «Se decidió que sea Bessel» → «Se eligió un Bessel»; «(propuesta mía)» → «(propuesta propia)», como dice el pie de esa misma slide | — |
| Elipsis | «El hardware decide cuándo y el software qué valores» → «…y el software decide qué valores» | — |
| Un término, un significado (R1.1) | «fallo» → «falla», como en el título de la misma slide | — |
| Concordancia (R8.5) | «Más canales significa» → «significan» | — |
| Repetición | «se deforma de forma transitoria» → «se deforma transitoriamente» | — |

## Cómo se verificó
- `check_anim.py`: la comprimida tiene 26 slides animadas y 0 problemas, igual que la v27. La larga no tiene animaciones, igual que la v27.
- PowerPoint (COM): se midió el alto de cada texto que cambió contra la v27. Dos cuadros pasaban de 1 a 2 líneas y se acortaron. Quedan 6 cuadros con una línea más, todos dentro de su caja. Se exportaron las slides 103 y 108 de la larga: no hay superposición.
- **No se recorrió la comprimida clic a clic.** Hay que mirarla en F5, sobre todo las slides 20, 24, 25 y 26 (una línea más en un cuadro).

## Para decidir juntos (no se aplicó)
1. **Slide 10 comprimida / 43 larga: «Dan información inicial y localizada del terreno. Extrapolarla reduce la incertidumbre».** Extrapolar un dato puntual suele *aumentar* la incertidumbre. ¿La idea era «usarla como restricción de la inversión reduce la incertidumbre»? No lo cambié porque cambia el contenido.
2. **Títulos que son rótulos de tema y no afirmaciones** (skill académico, «action titles»). Si se leen solo los títulos, el argumento se corta en estos:
   - 7: «Refracción y reflexión: métodos de superficie con condiciones»
   - 9: «Love y Rayleigh: las ondas de superficie que usa el método». Propuesta: «La Rayleigh domina el registro en superficie y el geófono vertical la capta».
   - 15: «El AFE: entrada instrumental, pasabanda inversor, sumador y antialias Bessel». Propuesta: «El AFE reparte la ganancia en cuatro etapas para recuperar lo que atenúa el compensador».
   - 21, 22 y 24: «Descarga en lotes, escalabilidad y nodo HAMMER», «Del flujo completo del sistema a la operación de campo», «De la captura al registro espacio–tiempo y al servidor».
   - 23: «Geometría: 21 posiciones, límites de Δx y L, y su incertidumbre».
3. **Diapositiva «Preguntas» (28).** El skill académico recomienda dejar las conclusiones en pantalla durante las preguntas. Se podría quitar la 28 o agregar el contacto a la 27.
4. **Primera persona del plural** («Elegimos», «Nos proponemos», «Usamos»). En una exposición oral es aceptable. La regla R2.4 pide «se». Lo dejé como estaba: es una decisión de registro que te corresponde.

Asistente: Codex `gpt-5.6-luna` (esfuerzo bajo) hizo la primera detección. Claude decidió y aplicó cada cambio.
