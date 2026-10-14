> **OBSOLETO (2026-10-13, 08:30).** Ver `ESTADO_v25.md`.

# Estado v24 (2026-10-13, mañana): entrega vigente

**Usar estos archivos:**
- `Presentacion_v24_COMPRIMIDA_INLINE_29_slides.pptx` (28,7 MiB): 29 slides, 93 clics (más 26 primeras escenas que arrancan solas).
- `Presentacion_v24_LARGA_INLINE_116_slides.pptx` (27,6 MiB): 116 slides.
- `Presentacion_v24_ANEXO_VIDEOS_ondas_4_slides.pptx` (14,9 MiB): animaciones de P, S, Rayleigh y Love (ver punto 5 de «Abierto»).
- `toolkit/tesis_toolkit_codigo_v24.zip`: código para regenerar. `build/build_v23.sh` reconstruye y valida todo; `build/walk_powerpoint.ps1` recorre los clics en PowerPoint y guarda capturas. `build/v23_edits_log.json` registra cada edición (antes y después); los módulos originales están en `build/_orig_modules/`.

Todo lo de v22 y v23 queda superado. No se borró nada.

## Cómo se validó (esta vez sí en PowerPoint)
PowerPoint está instalado en la PC. Lo manejé por COM, sin ventana y sobre copias:
1. `validate.py` PASA en las dos. `check_anim.py` en la comprimida: 26 slides, 0 problemas.
2. Las dos **abren en PowerPoint sin error ni pedido de reparación**.
3. **Larga:** exporté las 116 slides con el renderizado de PowerPoint (ecuaciones OMML reales) y las revisé todas.
4. **Comprimida:** presentación a pantalla completa, **los 93 clics uno por uno**, con captura después de cada clic (122 imágenes), y las revisé todas. PowerPoint cuenta 93 clics, igual que lo que genera `anim3.py` (119 pasos menos 26 automáticos). Ningún clic sale de su slide antes de tiempo.
   - Zoom de la matriz (3, 6, 7, 8), imágenes dentro del grupo, riel (5, 8, 15) y cierres: se comportan como se diseñó.

## Defectos encontrados en PowerPoint y corregidos
| Dónde | Defecto | Arreglo |
|---|---|---|
| Comprimida 19 (larga 84) | El texto naranja se montaba sobre la última fila de la tabla. El arreglo de v20 no funcionaba en PowerPoint real | La imagen de la slide 83 no entra al riel (`railSkip`), así que la tabla va a ancho completo; filas de 0,40 in y dos celdas más cortas |
| Larga 15, 17, 38, 91; comprimida 5 | Raíces y fracciones más altas que su recuadro; Vp invadía el recuadro de Vs | E_vp y E_vs a 23 pt; E_vsc y E_tin a 24 pt |
| Larga 54, 93 | Título partido en «SM-» / «24» y «ESP-» / «NOW» | Títulos reformulados |
| Larga 89, 91 | «1» / «s» y «±1» / «%» en renglones distintos | Espacio no separable |

## Hallazgo nuevo para la defensa: el reloj del ADC no tiene cristal
`src/firmware/psoc/AcondicionamientoAnalogico.cydsn/AcondicionamientoAnalogico.cydwr`: `ADC:theACLK` (1,024 MHz, divisor 23) ← MASTER_CLK ← PLL_OUT ← **IMO**. El bloque XTAL está `enabled=False`. PSoC Creator le asigna a ese reloj **±1 %**.
- Es una cota, no una medición, pero es unas 200 veces peor que los 50 ppm ilustrativos de la slide 91. Con 1 %, dos nodos pueden separarse hasta 10 ms en 1 s.
- Para la campaña (un solo GEO) el error es común a todas las trazas y escala el eje de tiempo (≈1 % en velocidad); no desordena la fase. **Inferencia propia.**
- Para varios nodos simultáneos dominaría sobre el jitter de inicio. Quedó en la slide 91 (fila nueva de la tabla, viñeta y nota). Brunetti lo va a preguntar.

## Verificación contra los PDF (hecha a mano; puesta en citas y notas)
| Slide larga | Dato | Fuente |
|---|---|---|
| 10 | Fig. 1.1 = radiación de Rayleigh desde fuente puntual vertical (no P ni S) | Foti 2014, cap. 1, p. 5 |
| 11–12, 15 | Navier (2.15), div/rotor (2.16), Helmholtz como alternativa, Vp y Vs (2.17) | cap. 2, pp. 44–45 |
| 16 | Lineal a deformación muy pequeña. Umbral ≈10⁻⁴ en arcillas NC con IP 50; el 10⁻⁵ de la slide es una cota propia | cap. 1, p. 2; cap. 2, nota 22, p. 102 |
| 19–22 | Crosshole y downhole; crosshole «el más confiable»; pozos entubados caros. **La imagen de crosshole no es de Foti: falta su fuente** | cap. 1, p. 4 |
| 25, 27 | Refracción: inversiones de velocidad y capas ocultas. Reflexión: procesamiento complejo, sobre todo profunda | cap. 1, pp. 5 y 18 |
| 33 | Existencia de Love | cap. 2, sec. 2.3, pp. 60–61 |
| 36 | 67/26/7: **no está en Foti**; fuentes secundarias lo atribuyen a Miller y Pursey (1955); original no consultado | — |
| 37 | Rayleigh 1/√r; ondas de cuerpo 1/r² en superficie | cap. 1, pp. 5–6; cap. 2, p. 52 |
| 38 | VR/VS de 0,862 a 0,955 (0,92 con ν = 1/4). La autoría de la fórmula aproximada sigue por confirmar | cap. 2, fig. 2.15, pp. 58–59 |
| 39, 43 | ρ y ν supuestos por su débil sensibilidad; inversión mal planteada y no única; la información previa acota | cap. 6, pp. 277–279 |
| 40 | Fig. 2.13; regla λ/3–λ/2 | Foti 2014, p. 53; Foti 2018, tabla 1, p. 2383 |
| 48, 100 | MSOR equivale al MASW a fines prácticos | Lin y Ashlock 2016 |
| 99 | L ≥ λmáx (p. 2380); ejemplo de 1,5·λmáx (p. 2382); offset de 3–5·Δx (los 10 m cumplen); se piden disparos desde los dos extremos (la campaña usó uno) | Foti 2018 |

`VERIFICACION_FOTI.csv` y `VERIFICACION_COMPLETA.md` los hizo un subagente y **tienen errores** (Fig. 1.1, cR/Vs). Esta tabla los reemplaza.

## Humanizador
Leí las 116 slides y sus notas (texto completo en el toolkit). El texto ya estaba en buen registro. Se corrigieron: una frase rota (91), un relleno (60), un título que empezaba con «Además,» (37) y las comillas inglesas (106, 115).

## Otros entregables de esta noche
- `PROPUESTA_parche_04_arquitectura.md`: corrección de `04_arquitectura.tex` (EEPROM por ganancia, verificado en `psoc_nv.h:11` y `psoc_nv.c:64`). **No aplicada.**

## Abierto
1. Ver la comprimida en tu monitor y a velocidad real: yo revisé el estado final de cada clic, no la animación en movimiento.
2. Referencias sin cerrar: Kramer (página), Comina 2011, Ma et al. (+1,5/+21,3 dB), Hakimitoroghi, Zhang, documento de TI, fuente de la imagen de crosshole y fórmula de la slide 38.
3. Figuras en inglés: 71, 72, 74, 94. La fecha de la portada.
4. Medir la tasa real del IMO entre placas (por ejemplo, contar muestras contra una referencia GPS/PPS o contra un único generador). Es la pregunta de reloj más probable del tribunal.
5. **Videos:** quedaron en un anexo aparte, `Presentacion_v24_ANEXO_VIDEOS_ondas_4_slides.pptx` (14,9 MiB), con los cuatro MP4 Full HD redibujados (P, S, Rayleigh, Love). En PowerPoint los cuatro se reconocen como video de 8,8 s, y Rayleigh se reprodujo en presentación (el cuadro avanza). No los metí en la comprimida: suman 12,4 MB y la llevarían a unos 40 MiB; tampoco hay ffmpeg para recodificarlos. Revisá vos que la animación de Love muestre movimiento horizontal (no lo pude juzgar en una imagen fija) y la fuente de la animación original.
6. Nada commiteado.
