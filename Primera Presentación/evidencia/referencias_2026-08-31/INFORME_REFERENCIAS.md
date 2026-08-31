# Referencias y atribuciones — 31 de agosto de 2026

Se revisó `latex-reestructurado`; no se modificaron las versiones congeladas ni los archivos de imagen o Draw.io.

## Resultado

- 29 referencias citadas e impresas, frente a las 10 anteriores. No se utilizó `nocite{*}`: las entradas conservadas pero no pertinentes no se incorporaron artificialmente al PDF.
- Se conservaron, sin modificar sus expresiones, las 31 ecuaciones y las 24 imágenes. Se mantiene el extremo de 8 Hz, la limitación por apertura y las capturas en modo claro.
- Se retiraron las marcas verdes de la ronda anterior, conservando su contenido. Las incorporaciones y correcciones de esta ronda usan `revsolution`. No había comentarios `rev` pendientes.
- PDF: 29 páginas. Compilación con pdflatex/BibTeX y pasadas hasta estabilizar las referencias: sin errores, citas indefinidas, referencias cruzadas pendientes ni overfull. Las advertencias menores y la comprobación visual se detallan en `verificacion.json`.

## Cobertura

| Contenido | Fuentes incorporadas o completadas |
| --- | --- |
| Reconocimiento, penetración, ensayos en pozo y rigidez | Samtani y Nowatzki (FHWA, 2006), Kramer (1996) |
| Ondas, atenuación, dispersión, SASW y MASW | Foti et al. (2014, 2018), Park et al. (1998, 1999, 2007, 2018) |
| No unicidad de inversión e interpretación | Xia et al. (1999), Foti et al. (2009) |
| Geófono y compensador | Ficha SM-24, Ma et al. (2023), con autores y DOI corregidos |
| Alternativas de transductor y precios | Analog Devices, Güralp, SparkFun, R. T. Clark y DigiKey; enlaces y valores verificados |
| PSoC, entrada instrumental y calibración | Hoja CY8C58LP Rev. O, AN60319, AN68403; el controlador concreto sigue declarado como implementación del proyecto |
| Filtrado analógico | Karki / Texas Instruments, SLOA049D |
| Muestreo, cuantificación, FIR, promedio, fase y periodicidad | Smith (1997) |
| ESP-NOW | Guía oficial Espressif |
| Remuestreo | Efron (1979), sin atribuirle los parámetros propios del experimento |
| Contraste con sondeos eléctricos | Informe de Víctor González & Asoc. S.S. (julio de 2023) |

Los DOI de los trabajos citados quedaron visibles y enlazados conservando el estilo apalike. Se agregó xurl para partir enlaces largos dentro de las columnas.

## Figuras

Dos ilustraciones ya estaban atribuidas a Foti et al. (2014). El dibujo interno del geófono se identificó visualmente en la diapositiva 10 de Breslin (2020), que acredita a DESY: se hizo explícita esa procedencia indirecta. La página original de DESY no pudo consultarse directamente; no se le atribuyó una consulta inexistente. Las otras 21 figuras se identificaron como diagramas, capturas o resultados propios del proyecto. La atribución bibliográfica no implica una declaración de licencia o permiso de reproducción.

## Correcciones que exigió contrastar las fuentes

- Los ensayos de penetración no miden directamente Gmax; pueden estimar rigidez por correlación. Se retiró la afirmación absoluta y se distinguió la rigidez inicial de su reducción con la deformación.
- La ficha 3ESPC respalda 0,017–100 Hz estándar y 0,0083 Hz en la opción de 120 s; no respalda «fracciones de milihertz» ni que un sensor resuelva por completo todas las limitaciones del ensayo.
- Los precios publicados corresponden a productos con distinto nivel de integración. Se eliminaron costos no verificados y se indicó «por cotización» donde no se dispone de precio público. El ruido del MEMS se informa como especificación, no como comparación experimental del proyecto.
- No se presenta la menor sensibilidad de MFB a tolerancias como una regla universal.
- ESP-NOW utiliza direcciones MAC; lo que no requiere es asociación a punto de acceso ni configuración IP.

El informe hidrogeológico consultado permanece en `docs/investigacion/sources/INFOR_HIDROGEO_CYT_UC_AS_JUL_2023.pdf`; AN60319, en `docs/Propuesta Urucom/sources/AN60319_Instrumentation_Amplifier_Using_PSoC3.pdf`. No se inventaron enlaces públicos para esas copias.

El ZIP contiene fuentes y PDF antes/después; `cambios.diff` permite revisar los cambios sin perder las incorporaciones anteriores. No se hizo una reducción editorial a 15 páginas.
