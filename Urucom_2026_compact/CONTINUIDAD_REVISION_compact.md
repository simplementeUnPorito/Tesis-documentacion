# Continuidad — compresión a 5 páginas de Urucom_2026_compact

Última actualización: 2026-07-27.

Copia de trabajo de `docs/Urucom_2026/` para el pase de compresión a 5 páginas (límite duro URUCON, §2.2 de `Propuesta Urucom/URUCON_REQUIREMENTS.md`). El original en `Urucom_2026/` no se tocó.

## Protocolo seguido (heredado de `Propuesta Urucom/CONTINUIDAD_REVISION.md`)

- Cambios de contenido/texto: marcados con `\rev{...}` (rojo) para revisión visual.
- Cambios puramente de maquetación (espaciado, tamaño de imagen): **no** se marcan con `\rev` porque no hay texto que colorear; se documentan acá.

## Punto de partida

Tras restaurar 4 figuras y una referencia cruzada que faltaban (ver conversación previa: `fig:analog_path`, `fig:analog_response`, `fig:calibration_trace`, `fig:waterfall`, `sec:pga-note`), el paper compilaba correcto pero en **6 páginas** en vez de 5.

## Recortes aplicados, en orden

1. **Cortada la subsección "Analog Front-End Characterization"** (§IV-A): figura `fig:analog_response` (chequeo de barrido inicial) + sus dos párrafos. El propio texto la describía como *"a consistency check... rather than an end-to-end validation"* — no es evidencia de la calibración en sí. `waterfall` **no se tocó**, según pedido explícito. → seguía en 6 páginas, pero el desborde bajó a ~235 palabras en página 6 (solo cola de referencias).

2. **Cortadas dos frases genéricas** (sin contenido científico):
   - Roadmap de la Introducción ("*The remainder of this paper is organized as follows...*").
   - Lista de future-work al final de la Conclusión ("*gain calibration, thermal compensation, and adaptive bias adjustment*" → reemplazada por una cláusula corta genérica).
   → bajó a 115 palabras en página 6.

3. **Espaciado de referencias apretado** (`references/references.tex`): `\baselinestretch` local a 0.92 dentro del grupo de la bibliografía, más `\topsep`/`\partopsep` a 0. Tamaño de fuente (`\scriptsize`) sin cambios. → bajó a 86 palabras en página 6 (4 referencias colgando, ~11 líneas).

4. **Compresión global de layout** (`config/preamble.tex` + los 4 `\includegraphics` del documento):
   - `\linespread{0.97}` global (interlineado del cuerpo).
   - `\textfloatsep` 6pt→4pt, `\intextsep` 5pt→3pt, `\abovecaptionskip` 3pt→2pt.
   - Las 4 imágenes del paper (`grafico_churro`, `psoc_foreground_calibration_flow...`, `autocalibration_scope_sum`, `waterfall_wiggle_horizontal`) reducidas a 95% de su ancho de columna/página.
   → **5 páginas**, 0 `??`, 0 citas indefinidas, sin overfull hboxes (solo underfull \vbox benignos).

## Cumplimiento con URUCON_REQUIREMENTS.md

Ninguno de estos 4 pasos toca márgenes, tamaño de página, o la plantilla IEEE Conference A4 (§2.2). El tamaño de fuente del cuerpo tampoco cambió — solo interlineado, espaciado entre floats/caption, y escala de imagen al 95%. Verificado: no hay overfull hbox (nada invade márgenes).

## Pendiente / a decisión del usuario

- Si en algún momento se agrega más contenido y vuelve a desbordar, el próximo candidato en el ranking de la revisión previa es achicar `fig:analog_path` (diagrama "churro") de `figure*` a una columna, o recién ahí tocar `fig:waterfall`.
- Falta trasladar estos mismos recortes a `Urucom_2026/` (el original) si el usuario decide adoptarlos como versión final, o descartarlos si prefiere mandar la versión de 6 páginas a otro venue sin límite de 5.

## Ronda 2026-07-30: resolución de `\rev` + acrónimo AFE + tabla

- Resueltos los 3 `\rev{...}` del abstract y el de §II (`02_Digitally Assisted Front_End.tex`), que eran notas del usuario, no marcas de cambio:
  - Se definió el acrónimo **AFE** (Digitally Assisted Analog Front-End) en el abstract y de nuevo en la Introducción (primer uso formal, `\emph{...} (AFE)`); todas las menciones posteriores a "the proposed Digitally Assisted Analog Front-End architecture" / "the proposed architecture" en abstract, intro, §II, §III, §IV y discusión pasaron a "the proposed AFE". Se dejaron sin tocar los usos genéricos de "analog front end" (no específicos del sistema propuesto) y "DC-servo architectures" (arquitecturas de la competencia, no la propia).
  - "temporary/temporarily" (describiendo la asistencia digital) → "non-intrusive/non-intrusively" en todos los lugares donde describía la propuesta, por pedido explícito del usuario en el `\rev` de §II.
  - Abstract: bajó de 4 a 0 apariciones de "architecture"/"architectural" (quedó "AFE" + "feasibility").
  - `title_authors.tex` conserva su `\rev{...IEEEmembership{Student Member, IEEE}}` sin tocar — es una marca de cambio de contenido (agregado de credencial), no una pregunta a resolver; y de todos modos `\rev` no está definido en el preambel compacto (error benigno preexistente, no bloquea la compilación).
- §IV (`04_experimental_validation.tex`): se amplió la explicación de `Table~\ref{tab:results}` en el cuerpo (qué es cada columna/fila, por qué el valor de arriba es el fijo y el de abajo el calibrado, qué marcan $^\dagger$/$^\ddagger$) — antes solo estaba en el `\caption`.
- Recompilado con `pdflatex` (MiKTeX) tras cada ajuste de texto para no volver a desbordar a 6 páginas: la primera versión de la explicación de tabla + un párrafo extra en la sección de resultados empujó el documento a 6 páginas (cola de referencias en pág. 6); se acortó el texto hasta volver a **5 páginas, sin overfull hbox, sin citas/refs indefinidas**.

## Ronda 2026-07-30: notas del PDF `Urucom.pdf`

- Las cuatro marcas sin comentario sobre “architecture” quedaron resueltas con el acrónimo **AFE**.
- En el abstract: “hardware” se sustituyó por “front-end”, “DAC” por “VDACs” y “temporary” por “non-intrusive”.
- En §II: “temporary” se sustituyó por “non-intrusive”.
- Fig. 1 usa la exportación sin el borde rojo punteado.
- Fig. 3 se recortó al núcleo relevante del hardware de calibración (controlador, filtro, DMA, registros y EEPROM), se amplió al 95% de la columna y se condensó el caption. El pase inicial a dos columnas mejoraba la lectura, pero empujaba las referencias a una sexta página.

## Ronda 2026-07-30 (b): figuras finales + 2 fuentes 2025

### Imágenes nuevas (del usuario)
- `imagenes/AnalogPathFinal.png` y `imagenes/DigramaDigitalFinal.png` son los originales entregados (14 y 18 MB, con márgenes en blanco enormes).
- Derivados usados por el paper (recorte de bordes blancos + downsample, generados con PIL):
  - `AnalogPathFinal_trim.png` (3000×1518, 1.4 MB) — reemplaza `Grafico churro.drawio.png` en `fig:analog_path`. Además se colapsó la banda blanca interna de 193 px entre la fila del front-end y la fila VDACs/ADC (a 40 px), lo que bajó la altura de la figura sin tocar el contenido.
  - `DigitalPathFinal_trim.png` (2600×1296, 1.1 MB) — reemplaza el recorte con `trim=...1175bp` de `Diagrama blocks_topDesign-Page-5.drawio.png` en `fig:digital_hardware`.
- **`fig:digital_hardware` pasó de `figure` (1 columna) a `figure*` (2 columnas)**: es la respuesta directa a la nota del tutor “Esta figura sigue siendo muy pequeña”. Queda a `0.89\textwidth` (≈2× lineal, ≈4× de área respecto de la versión de una columna).
- `fig:analog_path` quedó a `0.83\textwidth` — es el precio de agrandar la Fig. 3 dentro del límite de 5 páginas. La combinación 0.86/0.86 (analógico/digital) desborda a 6 páginas; 0.83/0.89 es un óptimo local verificado.
- Se probó ampliar el caption de la Fig. 3 explicando las flechas azules (`Sample`/`MuxSelect`/`Vref`): una línea más de caption en un float de doble columna desborda a 6 páginas. Descartado.
- El PDF bajó de 13.6 MB a 3.3 MB (imágenes originales de 20k px reemplazadas por versiones a ~400 dpi efectivos).

### Compresión adicional (solo maquetación) para volver a 5 páginas
- `\linespread` 0.97 → 0.94.
- `\abovecaptionskip` 2pt → 1pt; nuevo `\dbltextfloatsep` 6pt (por defecto ~20pt, y hay 3 floats de doble columna).
- Nuevo bloque `\AtBeginDocument` con `\abovedisplayskip`/`\belowdisplayskip` a 3pt (hay 5 ecuaciones desplegadas; era el ahorro más invisible).
- `references.tex`: `\baselinestretch` 0.92 → 0.85.
- Fig. 2 (flujo) a `0.88\columnwidth`; Tabla I `\resizebox` 0.98 → 0.92; Tabla II `\arraystretch` 0.82 → 0.76.
- Resultado: **5 páginas, 0 overfull hbox, 0 citas/refs indefinidas**. Márgenes, tamaño de página y tamaño de fuente del cuerpo siguen sin tocarse (URUCON §2.2).

### Fuentes más modernas añadidas (2025) — `docs/references.bib`
- `Deng2025` — Z. Deng *et al.*, “Design of low-frequency extended signal conditioning circuit for coal mine geophone”, *Sensors* 25(19):5946, 2025, doi 10.3390/s25195946. Citada en la Introducción junto a `Kafadar2020,Wijayaraja2024` (interfaces de geófono de bajo costo). Metadatos verificados vía Crossref.
- `Antoniadis2025` — D. Antoniadis y T. G. Constandinou, “A mixed-signal analogue front-end for brain-implantable neural interfaces using a digital fixed-point IIR filter and bulk offset cancellation”, arXiv:2511.12540, 2025 (aceptado para MWSCAS 2026). Citada en la Discusión junto a `Liu2020` como ejemplo actual de lazo digital **permanentemente cerrado**, que es justo el contraste con la calibración de foreground propuesta. Metadatos verificados en arXiv.
- Ambas se agregaron sin texto nuevo (solo se sumaron las claves a `\cite{...}` existentes) porque no había margen de página; aun así costaron ~5 líneas de bibliografía, que se recuperaron con la compresión de arriba.

### Estado de las notas del PDF del tutor (`D:\Downloads\Urucom.pdf`, autor `evargas`)
Las 9 anotaciones extraídas del PDF están todas resueltas:
1-4. Cuatro resaltados sin comentario sobre “architecture” → acrónimo **AFE** (ronda anterior).
5. “Cambiar ADC por VDACs” (abstract) → dice “VDACs”.
6. “cambiar por hardware por Front_End” (abstract) → “configurable analog front end”.
7. “Cambiar por non-intrusive” (abstract) → “non-intrusive”.
8. “non-intrusive” (§II) → aplicado.
9. p3: “quitar el borde rojo de la figura” (Fig. 1) → la exportación nueva no tiene el recuadro rojo punteado.
10. p3: “Esta figura sigue siendo muy pequeña” (Fig. 3) → ahora es `figure*` a doble columna.

## Ronda 2026-07-30 (c): revisión ARS aplicada + figuras a `\textwidth`

Revisión con `academic-paper-reviewer` (panel de 5). Cambios aplicados a pedido del usuario:

### Texto
- **Acrónimo `AFE` → `DA-AFE`** (21 apariciones). Motivo: "AFE" es el nombre genérico de cualquier analog front end, y el paper lo usaba a la vez como nombre propio de la arquitectura propuesta (§V llegaba a decir "the proposed AFE differs from... precision analog front ends"). `DA-AFE` = Digitally Assisted AFE. Definido en abstract e Introducción.
- **§II**: agregado el argumento de ruido de los VDAC (dato del usuario): red de desacople 1 µF ∥ 100 nF + 16 kΩ de impedancia de salida del VDAC ⇒ polo simple ≈9 Hz que limita en banda la densidad de ruido de 750 nV/√Hz. Cierra la objeción "las referencias VDAC quedan en el path durante la adquisición".
- **§III-B**: se explicita de dónde salen los $|K_i|$ (relaciones de resistencias que fijan la transferencia DC de cada nodo de referencia a su salida). **Pendiente del usuario**: si quiere, poner los números exactos de $K_{\rm SUM}=7{,}89$ y $K_{\rm LP}=6$.
- **§IV-A**: se declara que el baseline compartido *no* es óptimo por configuración, así que las reducciones reportadas son cota superior respecto de un trim fijo por placa. (Era la objeción más fuerte del panel.)
- **§IV-B**: el sign test ahora menciona que sobrevive a corrección de Bonferroni sobre las 8 configuraciones; y se aclara que las etapas cuyo residual ya cae dentro del deadband quedan sin tocar por diseño (fila BP de Board B).
- **§V**: (a) camino rápido cuantificado — con calibración válida solo se ejecutan los settles, 2560 muestras ≈1.0 s a 2604 Hz; (b) limitaciones ampliadas con *inter-channel matching*; (c) alcance de la evidencia acotado explícitamente + argumento de pérdida de rango (21.8 %FS en SUM ya consume más de un quinto del rango de amplificador y ADC antes de aplicar señal).
- **§I**: la cita `Deng2025` se re-encuadró — ya no se agrupa como "interfaz embebida de bajo costo" sino como circuito de acondicionamiento de baja frecuencia (que es lo que realmente es).
- **Deduplicaciones** (para financiar lo anterior sin perder páginas): se eliminó la repetición literal del argumento "asistencia digital solo en foreground, después path convencional" en 4 lugares — última frase del §I ¶5, §II ¶1 (condensado), §III ¶1 (reescrito como frase de enlace), §IV ¶1 (condensado) y **§V ¶1 completo** (era idéntico al ¶3 y al cierre). El argumento sigue estando, dicho una vez por sección en vez de dos.

### Figuras
- Figuras de doble columna maximizadas con un barrido automatizado (fijar ancho → compilar → contar páginas). Valores finales tras la ronda (d): `fig:analog_path` 0.88\textwidth, `fig:digital_hardware` 0.91\textwidth.
- ⚠️ **Corrección de un hallazgo falso de esta misma sesión**: se reportó que el conteo de páginas "no era monótono" con el tamaño de figura. **Era un artefacto del script**: el barrido usaba `re.sub` con `\\textwidth` dentro de un string no-raw, el patrón nunca matcheaba, los anchos jamás cambiaban y el PDF se recompilaba idéntico. Con el reemplazo arreglado la relación es monótona (más grande ⇒ más páginas). Moraleja: verificar con `grep` que el archivo realmente cambió antes de creerle al resultado del barrido.
- `references.tex`: `\baselinestretch` 0.85 → 0.80.

### Bug corregido
En un script de edición, `\ref` se escribió como retorno de carro (escape de Python sin raw string) y quedó `(Fig.~<CR>ef{fig:analog_path})` en §III-B. Detectado y reparado. Chequeo útil: `grep -rn "^ef{" sections/` + buscar `??` en el texto extraído del PDF.

### Estado
5 páginas, 0 overfull hbox, 0 refs/citas indefinidas, 20 referencias, PDF 3.3 MB.

### No aplicado (a decisión del usuario)
- Statement de disponibilidad de datos/código (cuesta ~1 línea).
- Reemplazar la Fig. 4 por logs internos del controlador: **no existen** (confirmado por el usuario), queda como reconstrucción declarada.
- Medición de ruido con geófono conectado/desconectado: descartada por tiempo; se cubre con el argumento del polo RC.
- "informal bench observations" (~10 s) sigue como está.

## Ronda 2026-07-30 (d): cita de método + ajuste del texto del VDAC

- **Nueva referencia `Conover1999`** (W. J. Conover, *Practical Nonparametric Statistics*, 3rd ed., Wiley, 1999) citada en §IV-B junto al sign test. Cierra la observación del panel de que §IV no tenía ninguna cita de método.
- **§II, ruido del VDAC**: se aclara que los 16 kΩ son la **resistencia interna de salida del VDAC** y se eliminó toda referencia a la banda útil (el circuito busca extender el ancho de banda hasta 1 Hz, así que hablar de "banda sísmica" habría sido engañoso). El texto ahora solo da los datos: 1 µF ∥ 100 nF + 16 kΩ internos ⇒ polo simple ≈9 Hz que atenúa la densidad de 750 nV/√Hz por encima de esa frecuencia.
- Espacio recuperado para que entre la referencia nueva: `\linespread` 0.94 → 0.93, bibliografía `\baselinestretch` 0.78 → 0.76, Tabla II `\arraystretch` 0.76 → 0.72, Fig. 2 a 0.82 col, Fig. 4 a 0.88 col.
- Estado: **5 páginas, 0 overfull, 0 `??`, 21 referencias**.

## Ronda 2026-07-30 (e): cierre de la re-revisión ARS

- **§III-B**: los $|K_i|$ ahora declaran su procedencia — *"obtained by symbolic DC analysis of each stage in MATLAB, from the nominal component values of Fig. 1"*. Cierra el ítem S6 del roadmap.
- **§I**: se bajó la única sobre-afirmación que quedaba — *"Improving the effective operating conditions... therefore **directly benefits the overall measurement system**"* → *"...is therefore a **precondition for exploiting the available acquisition range**"*. Era el resto del issue CRITICAL del abogado del diablo (DA-1); el resto ya estaba cubierto en §V.
- **§V**: se agregó la frase de apertura que faltaba tras eliminar el párrafo redundante en la ronda (c) — la sección abría en frío con "From an instrumentation perspective...".
- Reajuste de anchos tras el texto nuevo: `fig:analog_path` 0.86\textwidth, `fig:digital_hardware` 0.89\textwidth (barrido automatizado).

### Trade-off vigente (a decisión del usuario)
Para maximizar las dos figuras grandes y meter la cita de método, quedaron reducidas **Fig. 2 (flujo) a 0.82\columnwidth** y **Tabla I a `resizebox 0.92\columnwidth`**. La Tabla I quedó chica en el render. Si el tutor vuelve a objetar tamaño, la palanca más barata para revertirlo es sacar `Conover1999` (2 líneas de bibliografía) o el statement de rango en §V.

### Pendientes no aplicados
- Valores numéricos explícitos de $K_{\rm SUM}=7{,}89$ y $K_{\rm LP}=6$ (ahora al menos está declarado el método).
- Confirmar que los 750 nV/√Hz del VDAC salen del datasheet citado `[9]` y no de medición propia (si es medición, hay que decirlo).
- Data/code availability statement (~1 línea).
- Reemplazo de la Fig. 4 por logs internos: descartado, no existen.

### Estado final del día
**5 páginas, 0 overfull hbox, 0 `??`, 0 citas indefinidas, 21 referencias, PDF 3.3 MB.**

## Ronda 2026-07-30 (f): ajustes finales del usuario

- **"microvolt-level" eliminado** (§I): la amplitud de la señal sísmica depende de la distancia a la fuente y de la fuente misma — puede ser de milivolts. Ahora dice *"before the low-amplitude seismic signal reaches the acquisition converter"*.
- **Reparto de tamaño entre las dos figuras de doble columna invertido** a pedido del usuario: la analógica tiene más letras y componentes, así que se le dio prioridad. Final: `fig:analog_path` **1.00\textwidth** (máximo posible) y `fig:digital_hardware` **0.76\textwidth**. Verificado en render: la digital sigue perfectamente legible a 0.76 (muy por encima de la versión de una columna que el tutor objetó). Combinaciones intermedias probadas (1.00/0.80, 0.98/0.82, 0.96/0.84, 1.00/0.78) desbordan a 6 páginas; 1.00/0.76 es el máximo que entra.
- **750 nV/√Hz**: confirmado por el usuario que es dato de datasheet, no medición propia ⇒ la cita `\cite{InfineonPSoC}` en §II es correcta y no hay que declarar medición.
- **Data availability statement: descartado.** URUCON_REQUIREMENTS.md §"no embedded Internet hyperlinks" (líneas 62-63, 166, 176) prohíbe links embebidos y anotaciones clicables. Nota técnica: el preámbulo **no carga `hyperref`**, así que una URL en texto plano no generaría anotación clicable y sería admisible — pero no hay ningún requisito de URUCON que pida disponibilidad de datos, así que no se agrega.

### Estado final
**5 páginas, 0 overfull hbox, 0 `??`, 0 citas indefinidas, 21 referencias.**
