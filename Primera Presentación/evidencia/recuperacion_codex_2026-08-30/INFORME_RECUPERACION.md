# Recuperación de contenido — 30 de agosto de 2026

Se comparó el manuscrito con imágenes con la última revisión de Codex. Esa revisión
se reconstruyó en una carpeta temporal a partir del respaldo y del script de
edición conservados, incorporando la última supresión de un párrafo redundante.
No se reemplazó el documento completo ni se revirtió el trabajo de figuras.

## Contenido recuperado

- **9 ecuaciones:** dos del circuito RC, dos de calibración FIR/PI, dos de
  cuantificación y diezmado, dos de temporización y deriva, y una de apilamiento.
- Calibración por etapa: FIR de 128 coeficientes, ganancias PI diferenciadas,
  permanencias de 512/1024 muestras, verificación al arranque y almacenamiento
  válido por ganancia. Se retiró la descripción antigua que unificaba parámetros.
- Interpretación de la identificación eléctrica, incluidos sus residuos de
  0,200 dB y 1,16°, sin afirmar que se descartó la electrónica como limitación.
- Ubicación de la campaña, alcance de la comprobación temporal y comparación
  de 26 subarreglos, incluida la tabla que había desaparecido.
- Extremo inferior de 8 Hz y apertura efectiva de 20 m para el subarreglo
  22–42 m. Se retiró la frase reaparecida que atribuía fragmentación al aliasing.
- Etiquetas y referencias internas que habían vuelto a números escritos a mano.

## Comentario del autor y contenido conservado

Se atendió el comentario `\rev` sobre la relación de rigidez de la introducción:
se retiró esa ecuación redundante y se mantuvo la formulación de fundamentos.
Por eso el total final es **31**, no 32.

Se preservaron las figuras y los nuevos apartados de interfaz de campo y servidor.
Se retiró únicamente la segunda copia idéntica de la figura de interfaz web, que
también repetía la etiqueta `fig:interfazcampo`. Quedan **24 figuras**.
Los 52 archivos de imagen locales coinciden byte a byte con el respaldo previo.

Sólo se ajustó en LaTeX la escala de dos figuras para evitar desbordes verticales;
no se recortaron ni editaron sus archivos. La imagen de contenido espectral aún
contiene el rótulo histórico de 50 m: su pie aclara que esa meta fue retirada y
mantiene el resultado actual desde 8 Hz. El gráfico original queda conservado.

Se retiraron los envoltorios verdes anteriores conservando su texto. Las nuevas
marcas verdes identifican la recuperación y la corrección del comentario actual.
No quedan comentarios `\rev` pendientes.

## Verificación y respaldo

- PDF: **28 páginas**, 31 ecuaciones y 24 figuras.
- Compilación con BibTeX y dos pasadas de pdfLaTeX: sin errores, sin desbordes
  y sin referencias sin resolver ni etiquetas duplicadas.
- Revisión visual de las páginas y revisión detallada de ecuaciones y resultados.
- El total de páginas supera el límite de 15 mencionado en el contexto previo;
  no se recortó contenido para resolver ese asunto durante esta recuperación.
- `respaldo_fuentes_recuperadas.zip`: fuentes LaTeX, bibliografía y contexto de
  continuación. Las imágenes siguen en la carpeta de trabajo y no se duplican.
- `cambios_recuperacion.diff`: comparación exacta con el estado encontrado.
- `verificacion.json`: recuentos y huellas SHA-256 de las secciones recuperadas.

El respaldo anterior a la recuperación permanece también en
`C:/Users/elias/AppData/Local/Temp/tesis_recuperacion_67y1xazj/antes`.
