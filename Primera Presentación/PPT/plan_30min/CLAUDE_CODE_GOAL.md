# CLAUDE_CODE_GOAL.md: última pincelada de la presentación de la primera defensa

Este archivo es el brief completo para que Claude Code termine la presentación sin más contexto. Léelo entero antes de tocar nada.

## 0. Objetivo (para /goal)

Dejar lista para defender la presentación PowerPoint de la primera defensa de tesis (30 min, diciembre de 2026). Está lista cuando se cumplen TODAS estas condiciones:

1. Existe una versión comprimida de entre 20 y 50 slides en la línea principal (hoy son 29), más un anexo opcional. Nada de lo construido queda fuera: lo tangencial va al anexo.
2. Cada afirmación factual de cada slide está verificada contra el PDF fuente (sección 5) o marcada como inferencia propia o pendiente.
3. Toda cita de la lista de pendientes (sección 6) quedó resuelta o explícitamente marcada "por confirmar" en el slide y en `PENDIENTES_DEFENSA.md`.
4. El texto de slides y notas del orador pasó por el humanizador (sección 7).
5. El .pptx abre sin reparación en PowerPoint (validado con `validate.py` y revisión visual de cada paso de animación) y pesa menos de 30 MiB.
6. Se entregan: la versión comprimida (segura) y su variante INLINE, la versión larga intacta como respaldo, y `ESTADO.md` actualizado.

No inventes datos, páginas, DOI ni resultados. Si una fuente no se puede abrir, déjalo marcado "por confirmar".

## 1. Contexto del proyecto

- Autor: Elías David Álvarez (estudiante de Ingeniería Electrónica, Universidad Católica "Nuestra Señora de la Asunción"). Tutor: Dr. Enrique A. Vargas Cabral (cita: Vargas E. A.).
- Tesis: sistema de adquisición sísmica multinodo para MASW con geófonos SM-24, PSoC 5LP, ESP32 (ESP-NOW) y ADC delta-sigma de 18 bits. Nodos GEO, nodo HAMMER (martillo con sensor ICP PCB 086D20) y un ESP32 maestro con interfaz web.
- Narrativa base: `Primera Presentación/Resumen_1ra_fimado.pdf` (resumen firmado, VoBo 29/09/2026). Es la fuente de mayor jerarquía. El resto: `latex/`, `latex-15p-review/`, `latex-reestructurado/`, `Diagramas_operativos_y_calibracion.drawio` (29 páginas; útiles 1, 2, 5, 10, 11, 12, 17, 18, 20).
- Tribunal: Fernando Brunetti (WSN, sincronización, ESP-NOW, latencia, jitter, deriva, confiabilidad, escalabilidad); Vicente González Ayala (física de ondas, G=ρVs², dispersión, límites de la inversión); Enrique Vargas Cabral (AFE, modelo del geófono, ruido, rango dinámico, offset, ADC; distingue modelo / simulación / medición eléctrica / caracterización del AFE / validación extremo a extremo). Vicente y Enrique son coautores del paper URUCON DA-AFE.
- Preferencias del autor: ser directo, sin adular, cuestionar supuestos, enfoque científico y práctico, español. Si el razonamiento del autor es incorrecto, decirlo y explicar por qué.

## 2. Reglas del proyecto (no negociables)

- Al usar un PDF: indicar PDF, capítulo o sección y página. Si dos fuentes discrepan, señalar la discrepancia explícitamente. Lo que sea inferencia o hipótesis, marcarlo como tal.
- Prioridad de fuentes: PDFs divididos por capítulo (por ejemplo `Sebastiano Foti Chapter 2.pdf`) antes que el libro completo.
- Ecuaciones: OMML nativas en el .pptx (ver sección 3). En notas Markdown, MathJax (`$...$`, `$$...$$`).
- Cita de fuente en cada slide. Cuando no se pueda verificar, "por confirmar".
- Figuras en inglés: se traducen sobre la original. Figuras propias o provisionales llevan una marca roja `FIGURA ...` en el slide.
- Diseño: 10 × 5,625 in, Arial, azul marino 1F4E79, azul 2E75B6, alerta C55A11, claro EAF1F8, gris 6B6B6B. Títulos 24 pt (22 pt en la comprimida), cita a y = 5,0.
- No afirmar nada que no esté respaldado por un documento, literatura estándar o física verificable.

## 3. Cómo está construido (toolkit)

Los archivos están en `tesis_toolkit_codigo.zip` (código y scripts de figuras) y `tesis_toolkit_imagenes_{1,2,3}.zip` (carpeta `img/final`). Descomprime todo en una misma carpeta de trabajo con la estructura:

```
trabajo/
  build/   (código: g1mod.js ... g10mod.js, lib.js, build_all.js, comp2_build.js, anim2.py, qa2.py, qa2run.sh, comp_*.js/py (v1, obsoleto), inject_eq.py, inline_eq.py, shrink.py, dedupe.py, qa_steps.py, comp_spec.json)
  fig/     (scripts matplotlib de figuras propias y PNG)
  img/final/ (todas las imágenes que usan los slides)
```

Requisitos: Node con `pptxgenjs`, Python 3 con `Pillow`, LibreOffice (solo para renderizar a PDF), el skill `pptx` de Anthropic para `validate.py` y `soffice.py`. Las rutas son relativas al directorio del código.

### Versión LARGA (respaldo, 116 slides)

```
cd build
node build_all.js g1mod,g2mod,g3mod,g4mod,g5mod,g6mod,g7mod,g8mod,g9mod,g10mod LARGA_raw.pptx
python3 inject_eq.py LARGA_raw.pptx LARGA.pptx                       # ecuaciones OMML nativas (marcadores §E_xxx§)
python3 inline_eq.py LARGA_raw.pptx LARGA_inl_raw.pptx && python3 inject_eq.py LARGA_inl_raw.pptx LARGA_inl.pptx   # variante INLINE
python3 shrink.py LARGA.pptx LARGA_s.pptx && python3 dedupe.py LARGA_s.pptx LARGA_final.pptx
```

`shrink.py` tarda unos 100 s por archivo. `dedupe.py` elimina medios duplicados. El tope de PowerPoint/entrega es 30 MiB.

Cada módulo `gNmod.js` define slides con `pres.addSlide()` en orden. El orden global de las llamadas es el número de slide largo (1 a 116). Los helpers (`txt, bullets, img, box, eq, eqbox, card, tag, strip, hd, cell`) se repiten en cada módulo. El texto del orador va en `s.addNotes(...)`; las notas que empiezan con "Nota para mí" son avisos al autor que deben conservarse o resolverse.

### Versión COMPRIMIDA (principal, 29 slides): motor v3 "coreografía con instancias"

Solo se mantiene la variante **INLINE** (símbolos en línea como OMML dentro del párrafo). El autor decidió que es la final; la variante SIMPLE ya no se genera.

Reglas del motor v3 (surgieron de los fallos de v19: SPT y downhole salían de la escena; imágenes del riel quedaban detrás de otras):
- **Cada objeto sufre como máximo UN movimiento/escala** (`animMotion`/`animScale` relativos a su posición base). Hipótesis: PowerPoint no encadena bien dos movimientos relativos sobre el mismo objeto. Si un objeto debe moverse otra vez, se dibuja una **copia idéntica** (instancia nueva) en el rect actual: la anterior sale al instante y la nueva aparece (`appear`) y hace su único movimiento. `anim3.py` tiene una aserción que impide el doble movimiento.
- **Riel con 4 casillas fijas** (x = 8,25 in, 1,35 × 0,78 in, paso 0,84 in); una casilla nunca se desplaza; la más vieja se desaloja con fade. Entran a la riel las 2 imágenes principales de cada panel (área ≥ 0,9 in²), así queda el hilo visual de cada tema.
- **Rótulos e imágenes estáticos** después de su primera aparición (SPT, CPT/CPTu, Downhole, Crosshole): mismo key y mismo rect = sin efecto. Solo cambia el texto.
- **Matriz 2×2** (slide 3 comprimida, y de nuevo en 6, 7 y 8): grupo nativo `Obj [oN]` creado por `group.py` a partir de formas `MX<tag>:<i>`. Zoom in = salida con `p:anim` de `ppt_x/ppt_y/ppt_w/ppt_h` al rect ampliado + fade; zoom out = instancia nueva con `p:anim` desde el rect ampliado al natural. La matriz reposa en su rect natural en el editor. Factor Z = min(6.4/fw, 2.7/fh, 6), centro de foco (5.0, 3.25).
- Pares (`"kind":"pair"`, slides 3 y 6 comprimidas): matriz → zoom a SPT/CPT (o downhole/crosshole) → imagen 1 → imagen 2 → solo cambia el texto (intro, ventajas, limitaciones, nota) → zoom out: el texto de la celda se reemplaza por las dos imágenes (v21; ya no van al riel). Las slides siguientes arrancan con la matriz que ya trae esas imágenes dentro del grupo (`prior`/`fill` en `matrixDesc`, `CELL_IMGS` en `comp3_build.js`).
- Spec extra por slide: `"pin":[[slide,idx]]` deja una imagen fija en el riel desde el inicio (slide 5: excitación); `"railSkip":[[slide,idx],...]` impide que una imagen entre al riel (slide 15: Sallen-Key y diferencial de Ma et al.). `"kind":"mauto"` (slides 7 y 8): matriz con cabecera, zoom a la celda, escenas automáticas, y opcionalmente cierre con zoom out.
- Velocidad: `SPEED` (por defecto 0,5 = animaciones al doble de rápido). Duraciones `D(ms)`, retardos `L(ms)` en `anim3.py`.
- `check_anim.py` debe pasar siempre; `normalize_ids` evita el aviso de reparación (ids duplicados).

Archivos: `comp_spec.json` (qué escenas), `comp3_build.js` (planificador, escribe `choreo.json`), `group.py`, `anim3.py`, `check_anim.py`, `qa2.py`+`qa2run.sh`. Los `comp2_build.js`/`anim2.py` son el motor anterior (obsoletos).

```
export NODE_PATH=/opt/npm-tools/node_modules
node comp3_build.js COMP3_raw.pptx                       # escribe choreo.json
python3 inline_eq.py COMP3_raw.pptx COMP3_inl_raw.pptx
SCALE_EQ=1 python3 inject_eq.py COMP3_inl_raw.pptx COMP3_eq.pptx
python3 group.py COMP3_eq.pptx COMP3_grp.pptx choreo.json
python3 anim3.py COMP3_grp.pptx COMP3_anim.pptx choreo.json
python3 check_anim.py COMP3_anim.pptx
python3 shrink.py COMP3_anim.pptx COMP3_s.pptx && python3 dedupe.py COMP3_s.pptx COMP3_final.pptx   # ~100 s + ; correr con nohup
QSRC=COMP3_grp.pptx ./qa2run.sh 3,6,7,8                  # montajes qa2/mNN.jpg (solo layout)
```
(`qa2run.sh` usa su propia carpeta como directorio de trabajo; la ruta del skill pptx para `soffice.py` hay que ajustarla.)

**Supuestos NO verificados en PowerPoint (no hay PowerPoint en el entorno de construcción):**
1. Regla de un solo movimiento por objeto (explicación probable de los fallos de v19; evidencia fuerte, no probada).
2. Zoom de la matriz con `p:anim` sobre `ppt_x/y/w/h` aplicado a un grupo.
3. Build por párrafo con `bldLst` (`PARA=0` lo desactiva) y arranque automático de la primera escena.
4. `validate.py` y `check_anim.py` pasan, pero no prueban comportamiento.
Tarea de Claude Code: abrir en PowerPoint, recorrer TODOS los clics (26 slides animadas, ~119 pasos) y anotar cada escena con un objeto fuera de lugar o detrás de otro. Casos a mirar primero: slides comprimidas 3 y 6 (zooms), 7 y 8 (matriz), 8 (riel SV/SH), 15 (riel vs AFE final), 18 (caja t_max, D ≤ 10), 19 (texto naranja vs tabla).

## 4. Trabajo pendiente (en orden)

### 4.1 Mejorar la compresión (la parte creativa)

Hoy la compresión es "pila con reemplazo": cada clic reemplaza el panel anterior. El autor pidió más dinamismo: cosas que se achican y se combinan, de modo que varias entren en una slide. Objetivos:

- Mantener 20 a 50 slides en la línea principal. Hoy 29. Se puede subir un poco si mejora la legibilidad.
- Más pasos "acumulativos" (sin `x`): un panel grande que se encoge a una esquina y deja lugar al siguiente. Hoy solo hay pares lado a lado (6+7, 13+14, 19+20). Probar tríos y 2×2 donde el texto aguante. Mínimo legible: texto de 9 pt; si no aguanta, volver a pila.
- Usar efectos de énfasis (agrandar/achicar con movimiento) además de fade y wipe. Cuidado: la inyección XML no se probó en PowerPoint; validar siempre con `validate.py` y abriendo el archivo.
- Revisar títulos de grupo y encabezados de panel (son los títulos largos de las slides originales; algunos conviene acortar).
- Mover al anexo lo tangencial. Candidatos: slide larga 112 (riesgo del watchdog, viene del documento de tesis y no del resumen), 104 (error de posición), 91 (deriva ilustrativa), 93 (escalabilidad ESP-IDF), 88 (broadcast vs unicast), 80-82 (memoria, duración, metadatos), 56-58 (técnicas alternativas de baja frecuencia), 23-27 (refracción y reflexión). Decidirlo con el tutor; no borrar nada.
- Presupuesto de tiempo: 30 min. Con 29 slides y unos 116 pasos son 15 s por paso: demasiado. Marcar los pasos que se omiten en la defensa (por ejemplo ocultar paneles) o llevarlos al anexo.

### 4.2 Validación académica de todo el contenido

Para cada slide larga (y por tanto cada panel), contrastar con la fuente. Dejar el resultado en `PENDIENTES_DEFENSA.md`: slide, afirmación, fuente (PDF, capítulo, página), estado (verificado, inferencia propia, por confirmar). Los citados "a confirmar" son principalmente de Foti et al. (2014) y de figuras sin fuente exacta. Ver sección 6.

### 4.3 Humanizador

Pasar por el humanizador (skill `humanizer`) el texto de todos los slides y todas las notas, en español. Reglas: sin frases infladas, sin tríadas forzadas, sin guiones largos, sin "no solo... sino", sin vocabulario de relleno; conservar los números, símbolos y cada marca "por confirmar" o "inferencia propia". Después regenerar todo (sección 3) y volver a revisar el layout, porque cambiar el largo del texto puede desbordar cajas.

### 4.4 Figuras a regenerar en el repo (el autor lo pidió)

Marcadas con una etiqueta roja en el slide. Regenerar en alta resolución y en español, y quitar la etiqueta:

- Largas 59 y 68: figuras mías (scripts `fig/fig_comp_curvas.py`, `fig/fig_recorte.py`).
- Larga 71 (diagrama de flujo de calibración, en inglés, 608×389 px) y 72 (eje "Time (s)" en inglés).
- Larga 76 (esquema delta-sigma de Texas Instruments traducido; documento exacto y licencia por confirmar. El filtro que muestra es Sinc3 y no se afirma que sea el del PSoC).
- Larga 74 (captura de PSoC Creator con etiquetas en inglés), 94 (figuras con etiquetas en inglés), 98 y 99 (mías: `fig/fig_geometria.py`, `fig/fig_cuna.py`), 81 y 78 (mías).
- Las fotos de campo del IIT no tienen fuente en los CSV.
- En el zip de la biblioteca v11, `A_electronic_compensation_geophone.png` es en realidad MicDAC Fig. 1 (mal rotulada).

## 5. Fuentes y cómo citarlas

- `Resumen_1ra_fimado.pdf`: secciones 3, 4.1 a 4.10, 5, ecuaciones 5 a 19, figuras 1 a 17.
- Foti et al. (2014), *Surface Wave Methods for Near-Surface Site Characterization* (capítulos y figuras citados "a confirmar" en las slides 10-12, 15, 17, 20, 25, 27, 33, 36-38, 43, 45).
- Foti et al. (2018), Bull. Earthquake Eng. 16(6): criterios de apertura L ≳ λmáx y L ≳ 1,5·λmáx (la tesis lo atribuye a ese artículo: confirmar capítulo y página).
- Ma et al. (2023), Sensors 23(6), 3082: compensador (ζ1 ≈ 938, +17,5 dB a 10 Hz verificado en el abstract).
- Lin y Ashlock (2016), Soil Dyn. Earthquake Eng. 87:82-92: receptor único.
- Paper URUCON DA-AFE (Álvarez, González y Vargas): offset residual y calibración.
- Korsimaa et al. (2025) HardwareX 24:e00713; Xue et al. (2021) Measurement 183:109760; Pérez-Solano et al. (2022) Comput. Commun. 186:80-89 (UWB).
- Espressif ESP-IDF v5.5, API ESP-NOW: máx. 20 pares, cifrados hasta 17 (7 por defecto), payload 250 B (v1.0) o 1470 B (v2.0); no especifica alcance ni throughput.
- Libro completo de Foti solo si hace falta.

## 6. Lista de dudas y errores conocidos (resolver o dejar marcados)

Hechos que el autor corrigió:
- Cambiar el rango del ADC NO invalida la calibración de offset, y la EEPROM se indexa solo por ganancia (no por ganancia y rango). Está ya corregido en los slides, pero `latex/secciones/04_arquitectura.tex` (líneas ~251 y ~296) dice lo contrario y hay que corregirlo.
- No se habla de límites de tiempo con SD (depende del tamaño de la tarjeta). Sin SD el límite es fijo: 512 lotes de 30 muestras.

Discrepancias entre fuentes (señalarlas si se tocan):
- Jitter de sincronización: `latex-15p-review` dice 100-200 µs; el resumen firmado dice 200-400 µs (128 órdenes START, 3 nodos). Se usa el firmado.
- Criterio de apertura: Foti et al. (2018) L ≳ λmáx (y 1,5·λmáx) frente a Comina et al. (2011) λmáx > 60 m para Vs,30; con 40 m el segundo no se cumple (según `08_trabajos_futuros.tex`, sin verificar en el artículo).
- SNR aparente: el resumen da bandas (0,5 / 2,1 / 16,7 / 24,4 dB; 265 impactos, 15 distancias); el documento de tesis da 18,9 dB (10-26 m) y 4,9 dB (30-50 m). Son agrupaciones distintas; no mezclar.
- Registros: la tesis habla de 607 candidatos y 598 procesados (mediana de ~30 golpes por posición); el resumen habla de 265 impactos solo para el análisis de SNR.
- Alcance de 13,7 dB (repo) frente a 13,8 dB = 20·log10(5/1,024) (cálculo propio).
- La figura de repetibilidad del repo menciona fs = 2929 Hz, mientras el ADC opera a 2604 SPS: aclarar de qué configuración viene.

Cosas que salen solo de las notas del autor o de mi inferencia (marcar "por confirmar"):
- Hakimitoroghi et al. (2017), Zhang (2025): año y página pendientes. Pazos, Alguacil y Davila (2005), BSSA 95(5):1940-1946, según la introducción de Ma et al.
- "Estable / no amplifica ruido" para el compensador de Ma (slide larga 60) es inferencia mía.
- La imagen 3 de la slide 63 (entrada con dos operacionales) se asumió como la entrada instrumental ×2 del autor.
- "El BP inversor es menos sensible a tolerancias": argumento analítico; hace falta análisis de Monte Carlo o de sensibilidad.
- Los números 21,8 %, 2,9-45,8 % → 0,4-3,9 % del fondo de escala y +1,5/+21,3 dB vienen del paper y de la tesis, no del resumen firmado.
- Decimación: se asume que el límite de 512 lotes cuenta muestras ya diezmadas (confirmar en el firmware). La decimación por promedio no es un antialias ideal: -3,9 dB en Nyquist; un alias de 150 Hz sobre 50 Hz con D = 13 se atenúa solo ~10 dB (estimación propia, está en notas).
- El nivel intermedio "RAM del PSoC encadenada" aparece en el repo y no en el drawio.
- ENOB y ruido referido a la entrada del ADC: sin medir (solo en notas, no en slides).
- Reloj del ADC: ¿cristal u oscilador interno? La tabla de deriva usa ε = 10 y 50 ppm como ILUSTRATIVO; ε no está medido. El retardo de grupo fijo del arranque del ADC nunca se calibró.
- Jitter: solo hay flancos GPIO de ESP32 con 3 nodos; no hay percentiles, ni comparación medida unicast vs broadcast, ni la versión de ESP-NOW usada, ni si el peer broadcast cuenta para el límite de 20.
- Slide larga 84: lo dicho de Wi-Fi, LoRa y GPS es conocimiento general; pide fuente si se dan cifras.
- Slide larga 112 (watchdog START_NOW tras captura + 2,5 s) viene del documento de tesis, no del resumen.
- Slide larga 99: la sugerencia de campo cercano con offset mínimo de 10 m es inferencia mía.
- Slide larga 104: δc/c ≈ δ(Δx)/Δx es derivación propia a partir de c = 2πfΔx/Δφ.
- Referencias: faltan Pazos 2005, Hakimitoroghi 2017, Zhang 2025, URUCON, Texas Instruments, Wood y Cox 2012, Comina 2011, Socco y Strobbia 2004, Xia 1999 (están en `latex/*.bib`, `referencias.bib` y `ampliacion.bib` del repo; completar las entradas de las slides 115-116).
- Fecha de la presentación en la portada y nombres: confirmar con el autor.

## 6 bis. Cosas que el tribunal probablemente preguntará

- Brunetti: por qué ESP-NOW broadcast, qué jitter hay realmente en el inicio del ADC, deriva de relojes, cuántos nodos escala, qué pasa si se pierde un paquete.
- Vicente: si bajo 10 Hz se mide suelo o ruido, límites de apertura, incertidumbre de la inversión, qué onda es la dominante.
- Enrique: ruido del AFE referido a la entrada, estabilidad del compensador, nivel de evidencia de cada afirmación (modelo / simulación / medición eléctrica / caracterización / extremo a extremo).
Cada una tiene respuesta en las notas del orador de las slides 85-93, 106-112 y 54-60; revisar que sigan siendo coherentes tras la compresión.

## 7. Protocolo de entrega y verificación

1. Regenerar versión larga y comprimida (sección 3).
2. `python3 <skill-pptx>/scripts/office/validate.py archivo.pptx` en los dos archivos (larga INLINE y comprimida INLINE) y `check_anim.py` en la comprimida. Debe decir "All validations PASSED!".
3. Revisión visual: PDF de la larga (116 slides) y `qa2run.sh` de la comprimida (cada escena), más recorrido completo en PowerPoint. Sin texto desbordado, sin superposiciones con la cita ni con el número de slide, imágenes sin cortar, ecuaciones dentro de su caja.
4. Las variantes INLINE (`inline_eq.py`) no se probaron en PowerPoint: si fallan al abrir, quedarse con la segura.
5. Peso menor a 30 MiB con `shrink.py` y `dedupe.py`.
6. Nombres: `Presentacion_v20_COMPRIMIDA_INLINE_29_slides.pptx`, `Presentacion_v18_LARGA_INLINE_116_slides.pptx` (solo INLINE). Guardar en `docs/Primera Presentación/PPT/plan_30min/`.
7. Actualizar `ESTADO.md` (qué cambió, qué quedó abierto) y `PENDIENTES_DEFENSA.md`.
8. No hacer push ni commit sin que el autor lo pida.

## 8. Estado de la entrega actual (v17, previa a esta tarea)

- `Presentacion_v17_LARGA_116_slides.pptx` y su variante INLINE: versión larga completa (G1 a G10, cierre y referencias). Sin compresión, con progresión de slides.
- `Presentacion_v17_COMPRIMIDA_29_slides.pptx` (motor v1, RECHAZADO por el autor: copias repetidas con fade/wipe). Reemplazada por `Presentacion_v18_COMPRIMIDA_29_slides.pptx` (motor v2, coreografía con objetos persistentes) y su INLINE.
- Mapa de grupos: ver `comp_spec.json`. Resumen: portada; motivación; ensayos de penetración; ondas; P y S; downhole/crosshole; refracción y reflexión; interfaces; Love y Rayleigh; estratificación; SASW/MASW; requerimientos y plataforma; SM-24; técnicas de baja frecuencia; AFE; ruta PGA-ADC y offset; sistema digital; ADC, diezmado, FSM y memoria; ESP-NOW y presupuesto de fase; disparo y jitter; descarga, escalabilidad y HAMMER; flujo y operación de campo; geometría; captura y registro espacio-tiempo; SNR; evidencia, futuro y riesgos; conclusiones; preguntas; referencias.
- Historial detallado de decisiones y banderas abiertas: `ESTADO.md`.

## 9. Entrega v20 (motor v3, solo INLINE)

- `Presentacion_v20_COMPRIMIDA_INLINE_29_slides.pptx`: animaciones al doble de rápido, slide 3 con matriz 2×2 + zoom, pares SPT/CPT y downhole/crosshole con rótulos estáticos, métodos con ondas desde la matriz (7 y 8), riel de hasta 4 miniaturas fijas; arreglos en 8, 15, 18, 19.
- `Presentacion_v18_LARGA_INLINE_116_slides.pptx`: respaldo largo; slide 80 con D hasta 10 y caja t_max más grande.
- Abierto: confirmar con el tutor que D = 10 es el máximo razonable (Nota para mí en la slide 80).

## 10. Entrega v21 (solo INLINE)

- `Presentacion_v21_COMPRIMIDA_INLINE_29_slides.pptx` y `Presentacion_v19_LARGA_INLINE_116_slides.pptx`.
- Cambios: matriz con imágenes en las celdas (3, 6, 7, 8), imagen de excitación fija en el riel de la slide 5, riel del AFE solo con esquemas propios (15), f_low y f_high lado a lado (larga 64, comprimida 15).
- Por revisar en PowerPoint: grupo con imágenes haciendo zoom (slides 6, 7, 8), fracciones OMML de la slide 15, z-order de las imágenes sobre la celda.
- Ideas para Claude Code: Morph entre slides; revisar si el orador debe aclarar que la miniatura fija de la slide 5 muestra Rayleigh.
