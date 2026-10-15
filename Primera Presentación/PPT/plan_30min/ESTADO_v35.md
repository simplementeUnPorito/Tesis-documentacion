# Estado v35 (2026-10-15): larga de 125 slides, esperando el visto bueno antes de la comprimida

**Archivo:** `Presentacion_v35_LARGA_INLINE_125_slides.pptx`. Parte de la v34, que a su vez parte de la v33 reordenada por Elías.

**Scripts:**
- `apply_v34_larga.py`
- `restructure_v35_larga.ps1`
- `apply_v35_larga.py`, que incluye `layout_64`

Figuras: `figuras_es_v25/fig_afe_bloques_control_es.py` y `figuras_es_v25/fig_balance_fuerza_es.py`.

## Cambios desde la v33
| Slide | Cambio |
|---|---|
| 48 | «Otras mediciones: acotan los parámetros supuestos, como ρ, a rangos más realistas y reducen la incertidumbre» |
| 64 | Balance de fuerza como lazo de control: −m·a_g → sumador → 1/(ms²+cs+k) → G₀s (la bobina como sensor) → v_o. La realimentación pasa por C(s) y por G₀ (la bobina como actuador, en triángulo) y entra con signo −. Diagrama más ancho, viñetas a 16 pt |
| 68 | AFE como diagrama de control: H_a(s), triángulos K_dif·K_PGA, K_sum y K_LP, H_LP(s), y el compensador 1 − H_BP(s) en un recuadro punteado. La viñeta da los valores: K_dif = 2, K_PGA de 1 a 50, K_sum = 3,6 y K_LP = 5 |
| 96–105 | Orden de comunicación: ESP-NOW → desfase y error de fase → error en velocidad de fase → disparo → por qué broadcast → jitter → alcance → deriva → descarga por lotes → pares |

La plataforma queda en la 80, después de los dos frentes analógicos (GEO y HAMMER) y antes de la parte digital.

**Verificación:** `validate.py` pasa. No hay desbordes en las slides tocadas. Se exportaron y miraron la 48, la 64 y la 68.

## Siguiente paso
Con el visto bueno de Elías, se porta todo a la comprimida. Hay que renumerar sus notas «[Slide larga NN]» y reponer la viñeta de los 35 Hz, que era su slide 19.
