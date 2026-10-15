# Estado v29 (2026-10-14): citas solo ajenas + reestructura de la larga

**Archivos:** `Presentacion_v29_LARGA_INLINE_120_slides.pptx` (larga, ahora con 120 slides) y `Presentacion_v29_COMPRIMIDA_INLINE_29_slides.pptx`. La v28 y la v27 quedan sin tocar.

## 1. Citas: solo se cita lo ajeno (las dos versiones)
Script: `apply_v29_citas_solo_ajenas.py`. Se quitó toda mención de autoría propia: «Esquema propio», «Cálculo propio», «Figura propia», «Diagrama propio (…drawio)», «Elaboración propia», «aportado por el autor», nombres de archivo (.py, .tex, main.c), «Resumen firmado» y «documento de tesis». 36 pies de fuente quedaron vacíos porque solo nombraban material propio.

**Se conservó:**
- Lo que marca el grado de certeza: «ilustrativo», «por confirmar», «NO MEDIDO», «INFERENCIA».
- El artículo URUCON (Álvarez, González y Vargas), porque tiene coautores y está en las referencias.
- En la slide de la cuña: «L ≳ 2·λmáx es criterio adoptado, no de Foti». Sin esa aclaración, el criterio quedaría atribuido a Foti.

En el cuerpo de las slides: «(propuesta propia)» y «(resumen)» se quitaron, e «INFERENCIA PROPIA» pasó a «INFERENCIA».

## 2. Larga: reestructura de la parte de ondas
Scripts: `restructure_v29_larga.ps1` (PowerPoint: duplicar y mover), `apply_v29_larga_estructura.py` (contenido) y `rebalance_refs.py`.

| Slide nueva | Qué cambió |
|---|---|
| 5 | Título: «…por su resistencia a la penetración o por cómo se propagan las ondas en él» |
| **10 (nueva)** | Puente: «Para medir la rigidez sin recurrir a correlaciones, se usan las ondas». Es el mapa de la 5 con la fila de penetración en gris |
| 11 | Título: «Un golpe deforma el terreno por un instante, y esa deformación se propaga». En la viñeta, «viaja» pasó a «se propaga» |
| 12 | Título: «Primera aproximación: un medio homogéneo, isótropo y elástico lineal» |
| 17 | Primera viñeta: «En pequeña deformación, τ y γ son proporcionales» |
| **18 (nueva)** | Curva G/G_max contra γ (modelo hiperbólico, Hardin y Drnevich, 1972), con la ecuación G(γ) = G_max/(1 + γ/γ_r). Define G_max como el máximo de la curva. γ_r = 10⁻³ es ilustrativo. Figura: `figuras_es_v25/fig_g_gamma_es.py` |
| 21 | Interfaces (antes la 28), movida antes del downhole |
| 22 | Snell (antes la 31), movida antes del downhole. Dice «P y S» en lugar de «P, SV y SH», y se agregó el ángulo crítico: sin θc = V₁/V₂ |
| 32 | Título: «La superficie libre es una interfaz especial: casi toda la energía vuelve al terreno» |

- Las notas del orador se ajustaron en las slides 10, 12, 17, 18, 21, 22, 23 y 32.
- Los números de slide citados en los pies se corrieron: 39 → 41, 41 → 43, y 54 → 56 en una nota.
- Se agregó la referencia Hardin y Drnevich (1972) y las referencias se redistribuyeron entre las cuatro slides. Ninguna desborda. El artículo es pago: se verificó la cita, no el texto.

**Verificación:** `validate.py` pasa en las cuatro versiones v28 y v29. Antes, python-pptx omitía el tipo .jpg en `[Content_Types].xml`; lo corrige `fix_content_types.py`. Se exportaron las slides 10, 11, 12, 17, 18, 21, 22 y 32 y se miraron.

**Trampa encontrada:** al guardar, PowerPoint convierte la versión de respaldo (Fallback) de los cuadros con fórmulas en una *imagen* del texto. Si se copia esa versión, se ve el texto viejo. Siempre hay que copiar la versión Choice.

## Pendiente
- **Pasar todo esto a la comprimida.** Sus notas citan las slides de la larga por número («[Slide larga NN: …]»), así que hay que renumerar: +1 desde la 10, +2 desde la 18, y aplicar el cambio de lugar de interfaces y Snell.
- Puntos que siguen abiertos de `ESTADO_v28.md`: «extrapolarla» (slide 10 de la comprimida, 45 de la larga), títulos que son rótulos de tema, la slide «Preguntas» y la primera persona.
- Para evaluar: en las slides 19 y 20 se dice «pequeña señal», y en la 17 y la 18, «pequeña deformación». En geotecnia se usa «pequeña deformación».
