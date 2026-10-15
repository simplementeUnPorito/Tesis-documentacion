# Estado v36 (2026-10-15): larga de 125 slides, lista para la comprimida

**Archivo:** `Presentacion_v36_LARGA_INLINE_125_slides.pptx`. Parte de la v35. Script: `apply_v36_larga.py` y después `refs_dedupe_reparto.py`.

## Cambio
**64, Balance de fuerza.** El esquema propio de la v35 no tenía fuente y su pie le atribuía el diagrama a Zhang 2025 sin haberlo leído. Se reemplazó por la **fig. 2 de X. Zhang et al. (2020)**, *Sensors and Actuators A* 312, 112074, que Elías tradujo. Es el modelo en Simulink de un geófono con balance de fuerza por una sola bobina y un modulador ΣΔ de 4.º orden.

La slide queda con:
- una línea con el resultado del artículo: un lazo PID por la misma bobina lleva un geófono de 4,5 Hz hasta 0,16 Hz;
- el mensaje: «Funciona, pero su complejidad pesa en un nodo multicanal barato y replicable»;
- notas del orador nuevas.

Las citas a Zhang 2025 se distinguen ahora como «Z. Zhang et al. (2025)», según la norma APA para autores con el mismo apellido. Se agregó la referencia de X. Zhang (2020); quedan 40 referencias únicas.

El esquema propio (`figuras_es_v25/fig_balance_fuerza_es.py`) ya no se usa.

## Pendiente de verificar
- Según el resumen de Z. Zhang (2025), su balance de fuerza se implementa **con** un convertidor de resistencia negativa. Separar la 63 y la 64 como dos técnicas es una forma de presentarlas, no una distinción de esa fuente.
- La referencia de Z. Zhang (2025) dice «34(6), 1678–1688». La página de la revista mostraba volumen y número sin asignar.
- En X. Zhang (2020) falta la lista completa de autores (está como «Zhang, X., Wei, X. et al.»).

## Siguiente paso
La comprimida: portar todo, renumerar las notas «[Slide larga NN]» y reponer los 35 Hz.
