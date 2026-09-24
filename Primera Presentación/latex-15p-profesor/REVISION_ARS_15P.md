# Revisión ARS y versión de 15 páginas — 23 de septiembre de 2026

## Resultado

Se trabajó sobre `latex-15p-profesor`, la carpeta más reciente de la primera presentación. El PDF final tiene **15 páginas, incluida la bibliografía**, conserva las 19 ecuaciones y las 17 figuras, y marca en rojo los pasajes modificados mediante `\revision{...}`.

La edición distingue los comentarios del tutor contenidos en `annotations_20260923_113929.md` de las instrucciones posteriores del autor. Cuando ambos difieren, prevalecen las indicaciones posteriores del autor; ARS se utilizó para controlar coherencia y trazabilidad, no para reemplazar esas decisiones.

## Cambios aplicados

1. Se mantuvieron el resumen y la introducción sin presentar resultados de campo como si se tratara de un artículo; la motivación queda centrada en el problema, los métodos superficiales no invasivos y la propuesta.
2. Se evitó anticipar el comportamiento dispersivo antes de definirlo y se conectó la penetración requerida con el tipo de onda estudiado y el interés por los métodos superficiales.
3. La comparación económica se mantuvo en miles de dólares y las plataformas alternativas se mencionan brevemente, siguiendo el tono sugerido por el tutor.
4. Se retiró de Metodología el párrafo que mezclaba prematuramente arquitectura y evaluación; se reemplazó por requisitos propios de la adquisición secuencial. La cita de Lin y Ashlock se precisó: emplearon receptor fijo y fuente móvil, cuya geometría recíproca sirve como antecedente del receptor desplazado utilizado aquí.
5. Se sustituyó «caracterizar el SM-24» por «aprovechar el SM-24 disponible» y se conservó el argumento de costo por canal.
6. La caracterización en frecuencia se reescribió como análisis espectral de magnitud y fase por etapa, limitado a regiones con coherencia suficiente. También se precisó que la rama pasabanda se combina sustractivamente con el camino directo.
7. Se aclaró que la respuesta sensor–electrónica es una predicción basada en el modelo nominal del SM-24, no una calibración mecánica extremo a extremo.
8. La etapa digital se describió desde la señal acondicionada hasta la digitalización, filtrado, diezmado, ventana de captura y almacenamiento de muestras y metadatos.
9. Se corrigió el flujo de datos: una captura puede descargarse localmente o enviarse al servidor usando datos móviles o Wi-Fi y la red privada de Tailscale.
10. Los metadatos se justifican por la trazabilidad y reutilización de la base de datos de campo; los originales se preservan y el procesamiento utiliza copias derivadas.
11. Se eliminó la redundancia de la descripción de ampliación multicanal.
12. La adquisición con un receptor fijo y otro desplazado se justificó mediante el antecedente recíproco de Lin y Ashlock, aclarando que sintetiza la dimensión espacial con eventos sucesivos y no equivale al MASW simultáneo.
13. Los resultados de los barridos se expresaron como caracterización eléctrica de la trayectoria PGA–ADC y contraste con el modelo del circuito.
14. La ampliación con más nodos GEO quedó condicionada explícitamente a la disponibilidad de financiamiento.
15. Se explicitó el orden de agregación de la SNR aparente: mediana espectral por distancia, mediana en frecuencia dentro de cada banda y mediana final entre las 15 distancias.
16. Se precisó que las 21 trazas del registro espacio–tiempo son promedios de capturas aceptadas y revisadas, alineadas mediante HAMMER y llevadas a una frecuencia de muestreo común.
17. Se conservó la advertencia de que la normalización individual de las trazas impide comparar amplitudes absolutas entre posiciones.
18. La subsección de arquitectura multicanal se trasladó antes del excitador instrumentado: la explicación queda en la página 11 y sus diagramas juntos en la página 12.
19. Se compactó únicamente la tipografía de la bibliografía a 7,2/7,5 pt para conservar las 15 páginas sin eliminar referencias ni contenido técnico.

## Verificación

- Compilación final con dos pasadas de pdfLaTeX.
- 15 páginas confirmadas mediante `pdfinfo`.
- Sin citas ni referencias cruzadas indefinidas y sin cajas desbordadas.
- Inspección visual de las páginas finales: sin recortes ni superposiciones.
- La advertencia de página 10 compuesta solo por figuras es intencional y no produce una página vacía.
- Cierre ARS: PASS metodológico, PASS disciplinar y PASS adversarial; no quedaron hallazgos bloqueantes ni mayores. Las observaciones residuales son de proximidad de algunos flotantes bajo la restricción de 15 páginas.
