# Estado v37 (2026-10-15): larga de 126 slides, lista para la comprimida

**Archivo:** `Presentacion_v37_LARGA_INLINE_126_slides.pptx`. Script: duplicado de la 64 con PowerPoint, `apply_v37_larga.py` y `refs_dedupe_reparto.py`.

## Cambio
El balance de fuerza ocupa dos slides, con figuras de X. Zhang et al. (2020) traducidas por Elías:
- **64, «Balance de fuerza»:** el modelo (fig. 2), con la línea «La misma bobina mide el movimiento y, con un lazo PID, aplica la fuerza de balance».
- **65 (nueva), «Balance de fuerza: respuesta medida»:** la fig. 9 y tres viñetas verificadas en el PDF.
  - Con un SM-6 de 4,5 Hz, el punto de −3 dB baja de 4,5 Hz a 0,16 Hz.
  - Arriba se limita a 120 Hz por los modos espurios.
  - Ruido equivalente: 4,3 ng/√Hz a 1 Hz.

  El mensaje «Funciona, pero su complejidad pesa…» pasó de la 64 a esta.

La referencia quedó completa: Zhang, X., Wei, X., Wang, T., Li, X., Xiao, W. y Wu, Z. (2020), Sens. Actuators A 312, 112074, doi:10.1016/j.sna.2020.112074.

## Archivos movidos al repositorio
- `docs/investigacion/sources/research/papers/pdf/Zhang2020_digital_geophone_sigma_delta_single_coil.pdf`, con su `.txt`.
- `figuras_es_v25/zhang2020_fig2_traducida.png` y `figuras_es_v25/zhang2020_fig9_traducida.png`.

## Nota
En la fig. 9 traducida, el eje dice «Frequencia», sin la c de «Frecuencia». Hay que corregirlo en la imagen.

---

# Comprimida v37 (2026-10-15): lista para mostrar al tutor

**Archivo:** `Presentacion_v37_COMPRIMIDA_INLINE_32_slides.pptx`, con 32 slides. **Es la misma larga v37, comprimida**: cada slide reúne varias slides de la larga como escenas, una por clic. Todo lo corregido en la larga (v30 a v37) está también en la comprimida, porque sale de ella y no se portó a mano.

**Cómo se arma:** `python build_comprimida_v37.py Presentacion_v37_LARGA_INLINE_126_slides.pptx <salida>`. Después se corre `fix_content_types.py`. Para cambiar cómo se agrupa, se edita la lista `GROUPS` del script y se vuelve a generar. Así, cualquier corrección futura en la larga se pasa a la comprimida en un minuto.

| Comprimida | Slides de la larga | Tema |
|---|---|---|
| 1 | 1 | Portada |
| 2 | 2–4 | Motivación y propuesta |
| 3 | 5–10 | Ensayos de penetración y puente a las ondas |
| 4 | 11–13 | Origen de las ondas, primera aproximación, P y S |
| 5 | 14–20 | P, S, velocidades, G, modelo hiperbólico, Gmax |
| 6 | 21–23 | Capas, interfaces, Snell |
| 7 | 24–27 | Downhole y crosshole |
| 8 | 28–32 | Refracción y reflexión |
| 9 | 33–36 | Superficie libre, SV y SH, conversión de modos |
| 10 | 37–43 | Love, Rayleigh, energía, atenuación, cR |
| 11 | 44–48 | Modelo estratificado, dispersión, inversión |
| 12 | 49–53 | SASW y MASW |
| 13 | 54–56 | Requerimientos, condiciones, transductores |
| 14 | 57–60 | SM-24 |
| 15 | 61–65 | Técnicas de baja frecuencia, compensación inversa, resistencia negativa, balance de fuerza |
| 16 | 66–68 | Método de Ma et al. |
| 17 | 69–74 | AFE |
| 18 | 75–79 | Validación y offset |
| 19 | 80–81 | HAMMER y plataforma |
| 20 | 82–86 | ADC y camino digital |
| 21 | 87–91 | Máquina de estados, almacenamiento, diezmado, registro |
| 22 | 92–96 | Interfaz web, sesión, geometría, receptor móvil |
| 23 | 97–99 | ESP-NOW y error de fase |
| 24 | 100–104 | Disparo, jitter, deriva |
| 25 | 105–107 | Descarga, escalabilidad, flujo completo |
| 26 | 108–110 | Procesamiento y resultado |
| 27 | 111–113 | SNR |
| 28 | 114–117 | Evidencia, trabajo futuro, FTM, martillete |
| 29 | 118 | Conclusiones |
| 30 | 119 | Preguntas |
| 31 | 120–124 | Referencias |
| 32 | 125–126 | Anexo |

**Transiciones:** en cada clic, la escena anterior sale con un fundido de 0,25 s y la siguiente entra con un fundido de 0,4 s. Es más simple que la coreografía vieja (`anim2.py`, con objetos que se movían entre escenas), pero muestra exactamente el contenido de la larga.

**Notas del orador:** cada slide comprimida tiene las notas de sus escenas, rotuladas «[Slide larga NN: título]» con la numeración de la v37.

**Verificación:**
- `validate.py` pasa.
- PowerPoint la abre: 32 slides y 1433 efectos.
- `check_anim_todas.py`: 29 slides con animación, sin problemas. Es una copia de `check_anim.py` que recorre todas las slides; el original se cortaba en el primer hueco de numeración.
- Se recorrieron clic a clic, en modo presentación, las slides 5, 10, 15 y 24: escenas limpias, ecuaciones y gráficos nativos bien.

**Ojo:** la comprimida tiene **126 escenas**, el mismo contenido que la larga. Para 30 minutos hay que recortar. Ese es el trabajo para hacer con el tutor.

## Para revisar con el tutor
1. Qué escenas sacar para entrar en 30 minutos. La teoría (comprimidas 4 a 12, unas 50 escenas) es la candidata natural a resumir.
2. El orden del bloque de sistema (comprimidas 19 a 25).
3. La separación entre resistencia negativa y balance de fuerza (comprimida 15): según Z. Zhang (2025), su balance de fuerza se implementa con una resistencia negativa.

## Detalles menores pendientes
- En la fig. 9 traducida de X. Zhang, el eje dice «Frequencia».
- Confirmar el volumen y las páginas de Z. Zhang (2025).
- La fecha de la portada.
