> **Superado por `ESTADO_v27.md`** (2026-10-13, 16:10): slides 23 y 24 cerradas.

# Estado v26 (2026-10-13, 14:00)

**Usar:** `Presentacion_v26_COMPRIMIDA_INLINE_29_slides.pptx` (28,7 MiB) y `Presentacion_v26_LARGA_INLINE_118_slides.pptx` (27,7 MiB), más el anexo `Presentacion_v24_ANEXO_VIDEOS_ondas_4_slides.pptx`. Código: `toolkit/tesis_toolkit_codigo_v26.zip`. El detalle de las verificaciones anteriores está en `ESTADO_v25.md`.

Lo guardé como v26 porque a las 13:55 abriste `Presentacion_v25_COMPRIMIDA…` en PowerPoint y no quise pisar un archivo abierto. La v26 tiene los cambios de abajo; `Presentacion_v25_LARGA_INLINE_118_slides.pptx` es idéntica a la larga v26.

## Cambios v25 → v26
- **Referencias completas:** se agregaron las que se citaban y faltaban (Achenbach 1984, Ewing et al. 1957, Socco y Strobbia 2004, Xia et al. 1999, URUCON 2026, Hakimitoroghi 2018), todas verificadas contra el PDF, la bibliografía de Foti o el repo. Se quitaron Kramer y Wood y Cox, que ya no se citan. Son 4 slides de referencias (larga 115–118).
- **Slide 45:** límites de SASW verificados en Foti, cap. 4, pp. 213 y 217.
- **Slide 70:** la notación del modelo es la misma que la del paper URUCON, sec. II.
- **Slide 81:** verificado en el firmware que el tope de 512 lotes cuenta muestras ya diezmadas (`main.c:185`, `:191` y `capture_target_batches`).
- **Slide 23:** se identificó el informe USGS (Haeni, Grantham y Ellefsen, 1987, OFR 87-103-A, doi:10.3133/ofr87103A).
- **Slides 39, 56 y 57:** sin Kramer, y con Hakimitoroghi verificado en su tesis (ver `ESTADO_v25.md`).
- **`latex/secciones/04_arquitectura.tex`:** corrección aplicada; compila sin errores con `pdflatex`. Sin commitear.

Validación: `validate.py` y `check_anim.py` pasan; las dos abren en PowerPoint (29 y 118 slides). Revisé en PowerPoint cada slide cambiada.

## Marcas «por confirmar» que quedan, y por qué
| Slide larga | Qué falta | Por qué no se cerró |
|---|---|---|
| 23 | Que la recreación coincida con la figura del informe USGS | El informe está identificado, pero no pude ver su PDF |
| 24 | Autor y fidelidad de la dromocrónica de Wikimedia | No encontré el archivo de Commons |
| 38 | Autoría de la fórmula aproximada (Freund) | Solo fuentes secundarias; el texto de Freund no es accesible |
| 44, 46 | Fuente original del esquema SASW/MASW | Imagen aportada sin fuente; solo aparece en una presentación secundaria |
| 52 | Original del corte del SM-24 (Breslin 2020, DESY) | No aparece en la web |
| 60 | «Estable / no amplifica ruido» | Es inferencia propia y está declarada así; es correcto que quede marcada |
| 63 | Topología exacta de la entrada instrumental | Es un esquema que aportaste vos; solo vos sabés de dónde sale |
| 81 (nota) | Si D = 10 es buen techo | Lo tenés que decidir con tu director |

Y la **fecha de la portada**, que solo vos sabés.
