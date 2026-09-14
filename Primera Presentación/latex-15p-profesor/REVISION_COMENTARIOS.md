# Cierre de revisión

Entregable: `main.pdf`. Se conservaron las versiones anteriores; esta revisión sólo afecta al documento y sus figuras.

## Cambios contrastados con los comentarios

| Comentario o decisión | Ubicación y cambio |
|---|---|
| Inicio directo desde una obra civil | Resumen e introducción reescritos; necesidad previa al diseño y seguimiento posterior. |
| No introducir velocidades ni tipos de onda antes de explicarlos | Introducción general; definiciones físicas en sección 2. |
| Métodos invasivos y superficiales complementarios | Introducción: reconocimiento preliminar, sondeos y repetición de observaciones. |
| Explicar la restricción económica y propuesta instrumental | Introducción: plataforma PSoC 5LP–ESP32 y nodo de impacto. |
| Medio continuo antes de fórmulas P/S | 2.1: parámetros del medio, equilibrio, descomposición y tipos de onda antes de sus velocidades. |
| Diferenciar propagación y movimiento material | 2.1: velocidad del patrón frente a oscilación local. No se identifica VP/VS con velocidad de partículas. |
| Interfaces antes de ondas superficiales | 2.2–2.3: reflexión, transmisión, conversión P–SV y familias superficiales. |
| Love, Rayleigh y selección causal | 2.3–2.5: polarización, movimiento vertical, estratificación y dispersión. |
| Utilizar los tres gráficos aportados | Figuras 1–3, sin sustituirlas por diagramas generados. |
| Eliminar tabla Love–Rayleigh y polinomio innecesario | Eliminados. |
| SASW breve; MASW como extensión | Sección 3: dos receptores, observación espacial y antecedente de receptor desplazado. |
| Llegar al sensor desde lo que debe medirse | Secciones 3–4.1: requisitos y SM-24 disponible. |
| Compensación de Ma en orden causal | 4.2: respuesta bajo resonancia, amortiguamiento efectivo, atenuación y recuperación de ganancia. |
| Potenciómetro analógico | Corregido en texto y tabla del frente. |
| Conservar esquemático completo | Figura 6, sin recorte del circuito. |
| Calibración por derivas del PSoC | 4.3: FIR, conversión de error ADC a códigos DAC, PI posicional, banda muerta y códigos constantes al adquirir. |
| Coherencia con el controlador documentado | Ecuaciones contrastadas con la propuesta Urucom; no se presenta una media móvil uniforme como FIR implementado. |
| Evidencias eléctricas y respuesta combinada | 4.4 y figura 8: transferencia medida combinada con modelo nominal del SM-24. No se atribuye una calibración mecánica al producto. |
| No repetir gráficos de caracterización | Una figura de calibración y una de respuesta geófono–ADC, con finalidades diferentes. |
| Diagramas digitales reales del proyecto | Figuras 9 y 11: versiones de los diagramas operativos, con rótulos de publicación. |
| Precisar DMA y asistencia del procesador | 4.5: traslados DMA y formación de lotes por CPU diferenciados. |
| Fuente e interfaz como subsecciones independientes | 4.6 y 4.7; principio ICP e interfaz real en figura 10. |
| Descarga local, envío automático y descarte | 4.7: opciones del operador y conservación del original. |
| Mayor detalle del inicio multinodo | 4.8: ARM, PRESTART, confirmaciones, START por difusión y disparo local. |
| Incluir prueba de tres esclavos | 4.9: 128 órdenes y separación aproximada de 200–400 µs entre marcadores GPIO. |
| No confundir arranque con cadencia ni validación ADC | 4.5, 4.8 y 4.9 distinguen esas magnitudes. |
| Quitar la antigua frontera e integración repetitiva | Sustituidas por 4.9 Resultados parciales; capítulo 5 Trabajo futuro. |
| Análisis espectral que motive mejorar excitación | 4.9.1: procedimiento, SNR aparente y resultados por banda; sin atribuir causa exclusiva a la fuente. |
| No equivalencia no validada de profundidad | Figura espectral rotulada «banda baja de interés». |
| Waterfall recortado y secuencial | Figura 13: primeros 4 s, 21 posiciones con un receptor desplazado. |
| Sin nombres de campañas, scripts ni proyecto interno | Retirados del recorrido del documento y sus pies. |
| No resultados de dispersión o inversión | Reservados a la segunda presentación. |
| Validación futura para decidir con el profesor | No se impone un protocolo en el texto; reserva indicada sólo como comentario del LaTeX. |

## Procedencia de los gráficos aportados

- P/S: referencia a Kearey, Brooks y Hill, con crédito a Bolt recogido allí.
- Rayleigh: ejemplo de concreto de Sun et al. (2024), identificado como ilustración cualitativa, no ensayo del terreno del proyecto.
- Interfaz P/S: se conserva el gráfico aportado. Su origen editorial exacto no quedó establecido; el pie no inventa una atribución y cita por separado el fundamento físico.

## Verificación

Compilación mediante pdflatex, BibTeX y dos pasadas adicionales de pdflatex. Revisión técnica independiente de método, dominio y coherencia argumental, con corrección de los hallazgos mayores. Las pruebas nuevas propuestas no se presentan como ejecutadas ni se altera el código del instrumento.
