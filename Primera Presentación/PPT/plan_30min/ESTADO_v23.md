> **OBSOLETO (2026-10-13, mañana).** Ver `ESTADO_v24.md`. Este documento tiene datos superados o incorrectos y se conserva solo como historial.

# Estado v23 (2026-10-13, noche)

Este archivo reemplaza a los documentos v22 (RESUMEN_ENTREGA_V22, README_V22_FINAL, CHANGELOG_V22, CUMPLIMIENTO_*, ENTREGA_V22_MANIFEST). No se borró nada.

## Archivos vigentes
- `Presentacion_v23_COMPRIMIDA_INLINE_29_slides.pptx` (28,7 MiB): 29 slides, 26 animadas, 119 pasos.
- `Presentacion_v23_LARGA_INLINE_116_slides.pptx` (27,6 MiB): 116 slides.
- `toolkit/tesis_toolkit_codigo_v23.zip`: código con los arreglos (`g6mod`/`g7mod` con rutas relativas, `img/attrib.json` recuperado, `apply_v23_edits.py` con las 41 ediciones, módulos originales en `_orig_modules/`, `TEXTO_COMPLETO.md` con el texto de las 116 slides). Las imágenes siguen en los zips `tesis_toolkit_imagenes_*`.

Validación de ambos archivos: `validate.py` PASA; `check_anim.py` en la comprimida da 26 slides y 0 problemas. **No se abrieron en PowerPoint** (no hay PowerPoint en este entorno).

## Errores de la v22 (no usar)
- `Presentacion_v22_LARGA_…` tiene **114 slides**: faltan la 2 y la 3. Faltaba `img/attrib.json` en los zips y esas slides son condicionales.
- `Presentacion_v22_COMPRIMIDA_…` es una copia de la v21; `comp3_build.js` fallaba por la misma causa (los números de slide quedaban corridos en 2).
- Los documentos v22 dicen que la v21 está "confirmada OK": es falso, nunca se probó en PowerPoint.
- `VERIFICACION_FOTI.csv` (lo hizo un subagente) tiene errores. La fila de la Fig. 1.1 es falsa: esa figura muestra solo la radiación de Rayleigh. También marcó como no encontrados los valores de cR/Vs, que sí están en Foti (fig. 2.15). Usar la tabla de abajo.

## Antes de la edición, la regeneración es fiel
El texto de la regeneración sin editar coincidía slide por slide con v19 (larga) y v21 (comprimida): 0 diferencias.

## Verificado a mano contra los PDF (y ya puesto en citas y notas)
| Slide larga | Dato | Fuente |
|---|---|---|
| 10 | Fig. 1.1 = radiación 2D de Rayleigh desde fuente puntual vertical (no P ni S) | Foti 2014, cap. 1, p. 5 |
| 11–12, 15 | Navier (2.15), div/rotor (2.16), Helmholtz como alternativa, Vp y Vs (2.17) | Foti 2014, cap. 2, pp. 44–45 |
| 16 | Linealidad a deformación muy pequeña. Umbral ≈10⁻⁴ en arcillas NC con IP 50; el 10⁻⁵ de la slide es una cota propia | cap. 1, p. 2; cap. 2, nota 22, p. 102 |
| 19–22 | Crosshole y downhole; crosshole "el más confiable y preciso"; 2–3 pozos entubados. **La imagen de crosshole no viene del cap. 1 de Foti: falta su fuente** | cap. 1, p. 4 |
| 25, 27 | Refracción: inversiones de velocidad y capas ocultas. Reflexión: procesamiento complejo, sobre todo profunda, las ondas superficiales son ruido | cap. 1, pp. 5 y 18 |
| 33 | Existencia de Love | cap. 2, sec. 2.3, pp. 60–61 |
| 36 | 67/26/7: **no está en Foti**. Fuentes secundarias lo atribuyen a Miller y Pursey (1955); original no consultado (403) | — |
| 37 | Rayleigh 1/√r; ondas de cuerpo 1/r² en superficie (Ewing 1957) | cap. 1, pp. 5–6; cap. 2, p. 52 |
| 38 | VR/VS de 0,862 a 0,955, y 0,92 con ν = 1/4 (ecuación exacta). La fórmula aproximada no está en Foti y su autor (Viktorov o Bergmann) queda por confirmar | cap. 2, fig. 2.15, pp. 58–59 |
| 39, 43 | ρ y ν se suponen por su débil sensibilidad; inversión mal planteada y no única; la información previa acota | cap. 6, pp. 277–279 |
| 40 | Fig. 2.13; regla λ/3–λ/2 | Foti 2014, p. 53; Foti 2018, tabla 1, p. 2383 |
| 48, 100 | MSOR equivale al MASW a fines prácticos (FEM y campo con Δx = 2 m y offsets de 3–49 m) | Lin y Ashlock 2016, pp. 82 ss. |
| 99 | L ≥ λmáx (p. 2380), ejemplo de 1,5·λmáx (p. 2382), aliasing con λ < 2Δx. **Offset sugerido de 3–5·Δx: los 10 m cumplen**, pero recomiendan disparos desde los dos extremos y la campaña usó uno | Foti 2018, pp. 2380–2382 |

## Humanizador
Lectura completa de las 116 slides y sus notas (`TEXTO_COMPLETO.md`). El texto ya estaba en buen registro. Se corrigieron:
- una frase rota (slide 91);
- el relleno "de la mejor manera posible" (slide 60);
- el título de la slide 37, que empezaba con "Además,";
- las comillas inglesas, cambiadas por « » (slides 106 y 115).

## Abierto
1. **Recorrer las dos versiones en PowerPoint**, primero las slides comprimidas 3, 6, 7, 8, 15, 18 y 19. Ver si piden reparación.
2. Las citas nuevas son más largas: revisar que la cita (y = 5,0) no choque con el número de slide en 12, 16, 20 y 38.
3. Pendiente sin cambios: Kramer (página), Comina 2011, Ma et al. (+1,5/+21,3 dB), Hakimitoroghi y Zhang, documento de TI, reloj del ADC, ENOB, percentiles de jitter, figuras en inglés (71, 72, 74, 94), fecha de la portada.
4. Corregir `latex/secciones/04_arquitectura.tex` (líneas ~251 y ~296: rango del ADC y EEPROM). No se tocó.
5. Los videos de `Ondas_sismicas_REMASTER_FHD_COMPLETO` no se incorporaron.
6. Nada commiteado.
