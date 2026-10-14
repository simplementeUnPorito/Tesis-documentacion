# Estado v27 (2026-10-13, 16:10): entrega vigente

**Usar:** `Presentacion_v27_COMPRIMIDA_INLINE_29_slides.pptx` (28,3 MiB) y `Presentacion_v27_LARGA_INLINE_118_slides.pptx` (27,3 MiB), más el anexo `Presentacion_v24_ANEXO_VIDEOS_ondas_4_slides.pptx`. Lo anterior sigue en `ESTADO_v26.md` y `ESTADO_v25.md`. No se borró nada.

## Cambios v26 → v27
- **Slide 23 (larga) cerrada.** Leí el informe USGS OFR 87-103-A (Haeni, Grantham y Ellefsen, 1987). La figura de la slide es una adaptación de su fig. 1, p. 4: mismos rayos, rótulos y capas. Solo se simplifica el rayo 1, porque no se dibuja la energía que se transmite a la capa 2. La cita lo dice. El informe es del gobierno de EE. UU. y es de dominio público.
- **Slide 24 (larga) cerrada.** El archivo de Commons existe («Refraction dia.jpg», L. Antiga, 2010, dominio público), pero la figura de la slide no es una copia suya: es un esquema propio con los elementos de la fig. 2, p. 6, del mismo informe USGS (tiempo de intercepto, distancia de cruce, pendientes 1/V₁ y 1/V₂). La cita ahora dice eso.
- **Referencias:** se agregó Haeni et al. (1987). Son 34 y siguen entrando en 4 slides.
- Lo mismo vale para la slide 7 de la comprimida, que reúne las dos figuras.

Validación: `validate.py` y `check_anim.py` pasan (26 slides animadas, 0 problemas). Las dos abren en PowerPoint (118 y 29 slides). Exporté las slides 23, 24 y 116 de la larga y recorrí clic a clic las slides 7 y 29 de la comprimida: cada cita entra en una línea y nada se superpone.

**Slide 24, figura corregida (16:13).** La figura anterior dibujaba la onda refractada desde x = 0, pero la onda de cabeza recién existe a partir de la distancia crítica. La redibujé con `fig_dromo_es.py` (copia en `figuras_es_v25/`): antes de la distancia crítica la recta va punteada, con el rótulo «no se registra», como en la fig. 2 de Haeni. Los valores son ilustrativos: V₁ = 500 m/s, V₂ = 1500 m/s, espesor 3 m. La figura vieja (`refr_dromo_b.png`) no se borró. Verificada en PowerPoint en la larga (24) y en la comprimida (7, clic a clic).

## Lo que sigue abierto
| Slide larga | Qué falta | Por qué no se cerró |
|---|---|---|
| 38 | Autoría de la fórmula aproximada (Freund) | Solo fuentes secundarias; el texto de Freund no es accesible |
| 44, 46 | Fuente original del esquema SASW/MASW | Imagen aportada sin fuente |
| 52 | Original del corte del SM-24 (Breslin 2020, DESY) | No aparece en la web |
| 60 | «Estable / no amplifica ruido» | Es inferencia propia y está declarada así; es correcto que quede marcada |
| 63 | Topología exacta de la entrada instrumental | Es un esquema que aportaste vos |
| 81 (nota) | Si D = 10 es buen techo | Decisión tuya con tu director |

Además: la **fecha de la portada**, y mirar vos las animaciones de la comprimida en F5.

Nada commiteado. `latex/secciones/04_arquitectura.tex` sigue con la corrección aplicada y sin commitear (ver `ESTADO_v25.md`).
