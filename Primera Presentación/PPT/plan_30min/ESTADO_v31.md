# Estado v31 (2026-10-14): larga de 125 slides

**Archivo:** `Presentacion_v31_LARGA_INLINE_125_slides.pptx`. La comprimida sigue en v29.

**Scripts, en orden:**
1. `restructure_v31_larga.ps1`
2. `apply_v31_larga.py`
3. `apply_v31_ajustes.py`
4. `fix_content_types.py`

Las figuras nuevas están en `figuras_es_v25/`: `fig_rayleigh_profundidad_es.py` y `fig_v31_varias_es.py` (reflexión en la superficie libre, media móvil, bloques del HAMMER y geófonos de 10 Hz y 4,5 Hz).

## Cambios (numeración v31)
| Slide | Cambio |
|---|---|
| 13, 16 y 19 | **Notación única: G.** μ pasó a G en Navier, Vp, Vs y G = Gmax. «λ, G: constantes de Lamé». En la 16: «G: módulo de corte» |
| **35 (nueva)** | Reflexión de P, SV y SH en la superficie libre: P y SV generan P y SV, y SH solo SH. Ángulos según Snell con ν = 0,25. Fuente: Foti et al. (2014), cap. 2, p. 49, fig. 2.10 |
| 36 | Conversión de modos, con la fuente Foti p. 49 |
| **39 (nueva)** | «Condición de existencia de las ondas Rayleigh». Curva de amplitud contra profundidad calculada con la solución de Lamb para ν = 0,25: c/Vs = 0,919, cociente vertical/horizontal = 1,47 (Foti da ≈1,5) y cambio de signo de la componente horizontal a 0,19 λ. Viñetas: basta una superficie libre, acople P-SV, una longitud de onda de profundidad y ventaja frente a Love |
| 40 | «Onda Rayleigh: movimiento de las partículas», sin las viñetas que pasaron a la 39 |
| 41 | «De vuelta al primer modelo: reparto de la energía de una fuente vertical» |
| 44 | «Qué cambia en un modelo estratificado» |
| 56 | MEMS: «Triaxial, salida digital. Ruido: 22,5 µg/√Hz». 3ESPC: «Banda muy amplia. Pesa 8,4 kg» |
| 61 | Sin cajas de precio. En su lugar, la respuesta de los geófonos de 10 Hz y 4,5 Hz, con ζ = 0,6 ilustrativo: a 1 Hz, −40 dB contra −26 dB |
| 62 | Compensación inversa: «Amplifica el ruido de baja frecuencia y lleva fácilmente a la inestabilidad». Ma: «…se amplifica en su totalidad» |
| 75 | Offset: «llegó hasta el 45,8 %», con cita a la fig. 4 de URUCON |
| 84 | Media móvil común: D = 4, eje f/fs de 0 a 0,5. Sin «banda de interés» |
| 89 | HAMMER: diagrama de bloques nuevo (martillo → fuente de corriente → desacople y protección → PGA y pasa-bajos → ADC ΔΣ) |

## Orden nuevo de la parte de sistema
GEO, parte analógica (validación 74–78) → GEO, parte digital y almacenamiento (79–88) → **HAMMER (89)** → **interfaz web (90)** → **sesión de campo (91)** → **geometría (92)** → **receptor móvil (93)** → comunicación: maestro y ESP-NOW (94–95), descarga por lotes (96) y escalabilidad (97) → sincronización: por qué importa (98–99), disparo (100–101), jitter (102–103) y deriva (104) → **flujo completo (105)** → análisis (106–113).

**Verificación:** `validate.py` pasa. No hay desbordes nuevos: los que quedan ya estaban en la v29. Se exportaron y miraron las slides 13, 16, 35, 39, 61, 62, 84 y 89.

## Abierto
- **Slide 94:** repite la figura de la 56. Hay propuestas en el chat.
- Se ubicó la geometría (92) y el receptor móvil (93) **antes** de la sincronización. El mensaje decía primero que la 102 iba después de la sincronización, y después que iba junto con la 104 tras el HAMMER. Se siguió lo segundo.
- Las imágenes Fallback de las fórmulas siguen mostrando μ, pero solo se ven en PowerPoint 2007.
