# Contexto y encargo para continuar la Primera Presentación

> Este archivo es el prompt de continuación. Se le pasa completo a codex.

---

## 1. Qué es esto

Documento de **Primera Presentación** de un proyecto de fin de grado de
**Ingeniería Electrónica** (UCA, Paraguay). Autor: Elías David Álvarez Martínez,
matrícula Y24127. Tutor: Enrique A. Vargas Cabral, Ph.D.

El proyecto es un **sistema electrónico multicanal tipo IoT para caracterización
geotécnica del suelo mediante ondas sísmicas** (método MASW). El foco del
documento es **la electrónica**: el instrumento es el objeto de diseño y
validación, y la geofísica es el contexto que fija los requerimientos.

**Documento de trabajo:**

```
C:\Github\Tesis\docs\Primera Presentación\latex-reestructurado\
  main.tex
  secciones\01_contexto.tex      secciones 1 a 5
  secciones\02_requerimientos.tex sección 6
  secciones\03_diseno.tex         sección 7 (10 subsecciones)
  secciones\04_validacion.tex     secciones 8, 9 y 10
  referencias.bib
```

**Compilar** (no hay latexmk ni pandoc; MiKTeX con pdflatex + bibtex):

```
cd "docs\Primera Presentación\latex-reestructurado"
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Estado actual tras la recuperación: **28 páginas, 31 ecuaciones numeradas,
24 figuras, 0 errores, 0 overfull y 0 referencias sin resolver.** Se conservaron
las imágenes incorporadas posteriormente y se recuperó el contenido perdido.
Informe y respaldo de fuentes en `evidencia/recuperacion_codex_2026-08-30/`.
La recopilación histórica de candidatos sigue en `recopilacion_figuras/`.

---

## 2. Reglas que NO se negocian

1. **La estructura actual tiene 10 secciones.** El autor pidió reunir las
   anteriores secciones 3, 4 y 5 en una sección de fundamentos con subsecciones
   3.1 Ondas de cuerpo y ondas superficiales, 3.2 Fundamentos de propagación
   de ondas en un medio y 3.3 Métodos basados en ondas mecánicas. Esta petición
   reemplaza la restricción anterior de conservar doce secciones. No agregar
   resumen, conclusiones ni otros cambios estructurales sin una nueva petición.
2. **No tocar** `latex-historial\`, `latex-15p-review\` ni `latex\`. Son
   entregables anteriores congelados.
3. **No editar** archivos `.cyprj`, `.cydwr`, `.cysch` ni `.cyfit` del proyecto
   PSoC. Sólo `.c` y `.h`.
4. **Conservar las imágenes actualmente incorporadas.** La prohibición anterior
   de insertarlas correspondía a la etapa de recopilación. Posteriormente se
   añadieron figuras y el autor pidió recuperar los textos perdidos en esa
   edición, manteniendo el trabajo gráfico. No incorporar otras candidatas sin
   una nueva petición. Nunca recortar los esquemáticos del circuito.
5. **No comprometerse con una profundidad concreta como meta.** El objetivo se
   enuncia como «extender la caracterización hacia capas más profundas». La
   cifra de 50 m fue eliminada deliberadamente. Cuidado: los «offsets de 10 a
   50 m» son la geometría medida de la campaña y **sí** van.
6. **No inventar datos.** Si un número no está en el repositorio, decirlo. Este
   documento ya tuvo una auditoría por afirmaciones sin respaldo.

---

## 3. Cómo se marcan las revisiones

En el preámbulo de `main.tex` están definidos:

```latex
\newcommand{\rev}[1]{{\color{red}#1}}          % comentarios del autor
\newcommand{\revsolution}[1]{{\color{revverde}#1}}  % correcciones aplicadas
```

Nota: LaTeX no admite guion bajo en el nombre de un comando, por eso es
`\revsolution` y no `\rev_solution`.

**El ciclo de trabajo, confirmado por el autor el 30 de agosto de 2026, es:**

1. **Buscar siempre los `\rev{}` actuales en los cuatro archivos de secciones y
   en `main.tex` antes de modificar el documento.** El recuento de este archivo
   es una fotografía de la última sesión, no reemplaza esa búsqueda.
2. Retirar el envoltorio de las `\revsolution{...}` anteriores sin borrar su
   contenido. Si no hay un nuevo comentario asociado, ese texto se considera
   correcto por el momento; no se reabre su revisión por iniciativa propia.
3. Atender los nuevos `\rev{comentario}` y **envolver las correcciones en
   `\revsolution{...}`**. Si el comentario cuestiona una solución anterior,
   reemplazarla por la nueva corrección marcada en verde.
4. **Borrar únicamente el `\rev{}` que se atendió**, en el mismo paso. Conservar
   e informar los comentarios que no puedan resolverse. Una observación técnica
   se contrasta con la evidencia; no se incorpora una afirmación incorrecta.
5. Verde donde hubo un comentario del autor, también si lo escribió en la
   conversación: la petición general de más ecuaciones autoriza marcar sus
   incorporaciones en verde. Si un texto se cambió por
   iniciativa propia, va sin marca.

Tras cambiar las capturas a modo claro hay **0 comentarios pendientes y 33 marcas verdes**
en las secciones, más el color de la tabla recuperada. Se atendió el comentario
que pedía retirar la relación de rigidez de la introducción. Las marcas verdes
anteriores se retiraron sin borrar su contenido; las actuales corresponden a
la recuperación solicitada y a ese comentario. Las aclaraciones durante esta
pasada pertenecen a la misma revisión: no retirar sus marcas en cada seguimiento.

---

## 4. Cómo escribe el autor (respetarlo)

- Registro impersonal con «se», formal, español rioplatense académico.
- **Declarar toda variable** al presentarla.
- **Sin meta-comentarios** sobre las propias cautelas del texto.
- **Sin hombres de paja**: no plantear objeciones falsas para refutarlas.
- Profundidad **proporcional a la importancia**: la cadena analógica, el
  compensador y la temporización son el núcleo y merecen desarrollo; la
  trazabilidad y lo obvio, una línea.
- Decir «proyecto de fin de grado», nunca «Proyecto Final de Carrera».
- No culpar a la Facultad por las limitaciones: se dice «el número de
  transductores disponibles».
- Odia el relleno. Si un párrafo no agrega, se borra.

---

## 5. Trampas técnicas del entorno

1. **Los heredocs de bash se comen las barras invertidas.** Nunca usar
   `python - <<'EOF'` para escribir LaTeX. Escribir un archivo `.py` y
   ejecutarlo.
2. `rg` está disponible en el entorno de Codex verificado el 30 de agosto.
   Usarlo para localizar comentarios; PowerShell queda como alternativa.
3. Números en español con coma decimal: `\sisetup{output-decimal-marker={,}}`
   ya está puesto.
4. Los flotantes de tabla se rotulan «Tabla» (redefinido en el preámbulo).
5. Una `tabularx` dentro de `table*` debe dimensionarse contra `\textwidth`,
   no contra `\columnwidth`. Ya hubo un bug por eso.

---

## 6. Datos verificados contra fuente primaria — NO re-derivar

Todos estos números fueron auditados contra el repositorio. Detalle completo en
`docs\Primera Presentación\AUDITORIA_DATOS_2026-08-28.md`.

### Campaña de campo (Canchita)

| Dato | Valor | Fuente |
|---|---|---|
| Posiciones | 21, de 10 a 50 m, paso 2 m | `data\processed\Canchita_procesado\manifest.json` |
| Apertura | 40 m | ídem |
| Registros candidatos | 607 | 598 aceptados + 9 omitidos |
| Aceptados | 598 | `sample_count` |
| Golpes por posición | mín 20, máx 37, **mediana 30** | ídem |
| Fs de la campaña | **2929 Hz nativos**, mezclada con 1020 Hz | `data\raw\Canchita\metadata.json` |

> **TRAMPA:** existe un segundo manifiesto,
> `Canchita_grupo1_procesado\manifest.json`, con 477 muestras y mediana 21.
> **No es la campaña completa.** Citar siempre `Canchita_procesado`.

> **TRAMPA:** la tasa nativa del **firmware vigente** es **2604 Hz**
> (`psoc_adc.h:9`, `PSOC_ADC_NATIVE_FS_HZ`). Los 2929 y 1020 Hz son
> configuraciones **históricas** con que se tomó la campaña. Ambas cifras son
> correctas en su contexto. A pedido del autor se retiró del texto la explicación
> histórica de esas tasas; no «unificarlas» ni atribuir 2604 Hz a esta campaña.

### Compensador y frente analógico

| Dato | Valor | Fuente |
|---|---|---|
| `f_0` | **10,20 Hz** (exacto 10,2046) | `outputs\calculos_modelados\matlab\AnalisisCircuito\resultados_tanda_calibrada\05_tablas_reportes\parametros_compensador.csv` |
| `zeta_1` | **937** (exacto 937,396) | ídem |
| `zeta_0` | 0,25 | ídem |
| Atenuación central | 1/(2·zeta_1) = 5,3e-4, unas **1875 veces** | ídem |
| Ganancias | ×2 instrumental, ×1–50 PGA, ×3,6 sumador (rama BP), ×5 LP, producto ×1800 | el ×3,6 es 27k/7434 Ω |
| Potenciómetro | recorrido 2 kΩ; cancelación nula a 632,556 Ω; objetivo a 634,539 Ω → **1,98 Ω de separación** | ídem |
| Pasa-bajos antialias | **MFB**, 30k/150k/12k, 47 nF, 3,3 nF, f_a=300 Hz, zeta_a=0,691 | `analizar_sweeps_circuito.m:947` |

### Identificación del acondicionamiento

Fuente: `outputs\calculos_modelados\matlab\AnalisisCircuito\resultados_tanda_calibrada\05_tablas_reportes\resumen_identificacion.csv`

| Ruta | Puntos | Banda | Coherencia | Dentro de tolerancias | Dentro del recorrido del pot. |
|---|---:|---|---:|---|---|
| BP | 85 | 0,21 Hz – 47,5 kHz | 0,9684 | 32 % / 6 % | 32 % / 6 % |
| COMP | 71 | 0,21 Hz – 4,74 kHz | 0,9643 | 37 % / 11 % | **92 % / 94 %** |
| LP | 33 | 11,75 Hz – 1,11 kHz | 0,9454 | 82 % / 94 % | 82 % / 94 % |
| PGA→ADC | 61 | 0,21 Hz – 1,11 kHz | 0,9946 | 41 % / 15 % | **100 % / 100 %** |

Otros, de `data\raw\Osciloscopio_verificacion_calibracion_2026-07-21\RESULTADO.md`:
calibración manual llevó el error del compensador de **26,707 dB a 10,707 dB**;
BP dispersión mediana 2,257 dB y p90 21,454 dB entre campañas históricas;
barridos desde **10 mHz hasta 200 kHz**.

### Resultados geofísicos

Fuente: `src\calculos_modelados\python\masw_bench\informe\md\`

| Dato | Valor |
|---|---|
| Perfil adoptado | 3 capas: 78 m/s hasta **2,4 m**, 178 m/s debajo |
| Sub-arreglo | 22–42 m, desajuste 1,36 %, soporte 10,75 m |
| Profundidad defendible | **10 a 11 m** (λ soportada 20–22 m) |
| Criterio de capas | con 3 capas el 100 % de la varianza es del dato; con 4, el 52 % viene del optimizador |
| Bootstrap | 24 remuestreos × 5 semillas = 120 inversiones |
| SEV 01 | a ≈120 m; interfaces a 1,00 / 2,06 / 4,15 m. SEV 02 a 258 m, SEV 03 a 340 m |
| Banda de mayor energía | **10–50 Hz**; bajo 10 Hz la energía es 0,74 % del total |
| Extremo inferior de la curva utilizada | **8 Hz**, no es un corte físico del instrumento |
| Coherencia adyacente | 0,732 en 10–50 Hz, sobre **265 golpes en 15 distancias** |
| Sensibilidad | transformada 2,28 m/s; picker 1,89 m/s; quitar offsets 32 y 40 m → 29,76 m/s |
| Jitter de alineación | 1,46 ms |
| Tolerancia de sincronización | **unos 670 µs** (5 % de error, c=150 m/s, dx=2 m) |

> **TRAMPA:** el documento decía antes 130 µs (1 % de error). El autor lo cambió
> a 5 %. No quedan 130 µs en ningún lado y no deben volver.

---

## 7. Errores que ya se corrigieron y no deben reaparecer

1. **La topología MFB no se descartó.** Es la del pasa-bajos antialias. La rama
   de compensación se parametriza mediante `f_low` y `f_high`, con un par RC
   de entrada y otro de realimentación. En el modelo ideal cada par fija un
   quiebre; `f_0` y `Q` se calculan a partir de ambos y no son independientes.
   Esta es la explicación corregida a pedido del autor el 30 de agosto.
2. **El compensador sí busca convertir al SM-24 en un sensor de banda más
   ancha.** Lo que no puede hacer es crear señal bajo el piso de ruido.
3. **La caracterización del acondicionamiento no es un «error del circuito»**:
   el desvío se explica por la posición del potenciómetro, y la medición cae
   dentro de la envolvente que el potenciómetro puede alcanzar.
4. **Las métricas de banda útil son sobre 265 golpes en 15 distancias**, no
   sobre las 21 posiciones.
5. El criterio de apertura **estricto de diseño** considerado aquí pide
   `L ≳ 2·λ_max`. No atribuir esa cifra a Foti: la fuente primaria presenta
   `L ≳ λ_max` como orientación y un ejemplo de `1,5·λ_max`. Debe usarse la
   apertura de cada subarreglo: 22–42 m tiene 20 m, no los 40 m del tendido
   completo. El soporte de 20–22 m de longitud de onda no satisface el criterio
   estricto en ese subarreglo; los resultados se mantienen como preliminares.
6. **Shannon–Nyquist no demuestra `z ≈ λ/2`.** Fija el límite de muestreo
   espacial `λ_min ≳ 2·Δx`. La profundidad se estima a partir de la sensibilidad
   de las ondas Rayleigh. Verificación: Foti et al., sección 2.1.2,
   https://doi.org/10.1007/s10518-017-0206-7.
7. **Conservar 8 Hz como extremo inferior de la curva utilizada.** En el
   subarreglo 22–42 m, de apertura efectiva 20 m, ese punto tiene velocidad
   172 m/s y longitud de onda 21,5 m. Cumple el límite de muestreo espacial
   (2·Δx = 4 m) y el criterio de análisis que admite hasta 1,5 veces la apertura;
   no cumple el criterio estricto de diseño del punto 5. El punto de 8,5 Hz
   tiene longitud de onda 19,76 m. No presentar 5 Hz como resultado respaldado.
   El ensayo fundamenta evaluar una mayor apertura efectiva para frecuencias
   menores y capas más profundas, junto con energía coherente suficiente.
   No afirmar que los 40 m completos fueron el único límite diagnosticado.

---

## 8. Lo que queda por hacer

### 8.1 Prioridad alta

1. **Secciones actuales 8, 9 y 10 revisadas parcialmente.** En la segunda
   pasada se atendieron los comentarios sobre caracterización eléctrica,
   ubicación de campaña, tasas históricas, interpretación de resultados y
   límite inferior de la curva. En la tercera se resumió el alcance geofísico
   y se separaron el perfil, la sensibilidad al procesamiento y el contraste
   con sondeos eléctricos en apartados propios. En la cuarta se redujo la
   sección 10 a las líneas expresamente pedidas por el autor; no reponer
   explicaciones extensas, promesas de ensayo mecánico completo ni cadencia
   fija de 0,75 Hz. Si se pide continuar sin comentarios nuevos,
   completar la revisión de estilo y cohesión sin reabrir lo ya aceptado.

2. **28 páginas contra un límite de 15.** La incorporación posterior de
   figuras y la recuperación del contenido dejaron el documento en 28 páginas.
   No se recortaron textos ni figuras para forzar el límite de 15 páginas que
   incluye bibliografía. El autor había reservado esa decisión para tratarla
   con el tutor; no confundir la recuperación con una autorización de recorte.

3. **Verificar la bibliografía contra fuente primaria.** Sin verificar todavía:
   `Ma2023` (la referencia central del compensador), `LinAshlock2016`,
   `Barbier1976` y `Park1996SIST`. El criterio de apertura, el límite de
   muestreo espacial y los datos de publicación de `Foti2018` se contrastaron
   con la fuente primaria el 30 de agosto.

### 8.2 Prioridad media

4. Si vuelven las figuras del resultado MASW: **no usar**
   `data\processed\Canchita_procesado\masw_perfil_vs.csv`. Es la exportación de
   julio, con 9 capas hasta 82,6 m y desajuste 2,554 %, que **contradice** el
   texto (3 capas, soporte 10–11 m). El resultado correcto está en `masw_bench`.

5. **La presentación en PowerPoint no está empezada.** Necesita una exposición
   principal de unos 30 minutos y un banco amplio de diapositivas auxiliares,
   porque las preguntas son posteriores y no hay demostración en vivo.

---

## 9. Encargo inmediato

Salvo que el autor indique otra cosa:

1. Leer los cuatro `.tex` y **buscar comentarios `\rev{}` nuevos**. Si los hay,
   atenderlos siguiendo el ciclo de la sección 3 de este documento.
2. Si no hay comentarios nuevos, hacer una **pasada de estilo y cohesión sobre
   las secciones 8, 9 y 10**, con los mismos criterios de la sección 4:
   eliminar relleno, no repetir lo que ya dice otra sección, declarar toda
   variable, y mantener la separación entre lo demostrado y lo interpretado.
3. Después de cualquier cambio: recompilar y verificar que siguen en **0
   errores, 0 overfull y 0 referencias sin resolver**.
4. Informar al final, en pocas líneas: qué se cambió, qué número se movió y qué
   quedó sin resolver. **No pegar el contenido de los archivos en la respuesta.**

---

## 10. Historial: primera pasada del 30 de agosto de 2026

- Se conservaron los doce títulos de sección. La sección 3 resume las familias
  de métodos; las definiciones de polarización se concentran en la 5. Se
  definieron los parámetros de Lamé y se trasladaron a instrumentación las
  observaciones sobre ruido y orientación del geófono.
- La sección 8 referencia la relación frecuencia–longitud de onda mediante
  etiqueta LaTeX, distingue Shannon de profundidad y explicita los criterios
  de apertura y su aplicación al subarreglo.
- La sección 9.3 explica los dos pares RC con sus frecuencias de quiebre. La
  9.4 se reescribió usando `Urucom_2026_compact/sections/03_Foreground Calibration.tex`:
  verificación de códigos guardados, ajuste secuencial, estimador FIR, PI por
  etapa, refinamiento, protección ante saturación, persistencia por ganancia
  y restauración de la ruta de adquisición.
- Se corrigió la generalización de parámetros: `k_P=10^-3`, `k_I=3·10^-4`
  corresponden a PGA; en BP, SUM y LP son `10^-4` y `5·10^-4`. La permanencia
  es de 512 muestras en PGA/SUM y 1024 en BP/LP. Esos valores coinciden en el
  documento compacto y las tablas del firmware consultadas. No se modificaron
  datos de campaña ni resultados experimentales.
- Cuidado al trasladar tablas completas: el artículo compacto usa banda muerta
  PGA de 18 códigos y asentamiento LP de 1024 muestras; los encabezados actuales
  del firmware indican 3 y 512, respectivamente. La presentación describe esos
  aspectos sin asignarles un valor único. No mezclar parámetros de los ensayos
  del artículo con los de otra configuración del firmware.
- En las secciones 10–12 sólo se retiraron los envoltorios verdes anteriores:
  su contenido no se reescribió en esta sesión, porque había comentarios nuevos
  prioritarios en las secciones 1–9. La reducción a 15 páginas sigue pendiente.
- Compilación final con pdflatex, BibTeX y pasadas de resolución de referencias:
  17 páginas, 12 secciones, 0 errores, 0 overfull y 0 referencias sin resolver.
  Se inspeccionó el PDF renderizado, incluidas las páginas con correcciones.

## 11. Segunda pasada y acuerdo sobre 8 Hz, 30 de agosto de 2026

- Se aplicó la reorganización 3.1–3.3 solicitada por el autor, se añadieron
  etiquetas semánticas y se actualizaron las referencias internas mediante
  comandos LaTeX. Los capítulos posteriores quedan numerados de 4 a 10.
- Se incorporó el decaimiento geométrico ideal de amplitud: 1/r para ondas de
  cuerpo y 1/raíz(r) para superficiales. Se retiró de requerimientos el análisis
  experimental de subarreglos, manteniéndolo en validación y resultados.
- Se reescribió la caracterización eléctrica: objetivo de ampliar la banda
  del sensor, excitación eléctrica y modelo del geófono frente a una validación
  mecánica pendiente por falta de equipo, sensibilidad del potenciómetro y
  necesidad de menor recorrido y ajuste multivuelta para reproducibilidad
  entre canales. Los 0,200 dB y 1,16 grados son residuos del modelo identificado
  frente a la medición, no errores respecto del diseño nominal.
- Se sustituyó el código de ubicación por la sede Santa Librada de la
  Universidad Católica, en las proximidades de la cancha, y se retiró la
  explicación de las tasas históricas de firmware a pedido del autor.
- El autor confirmó conservar 8 Hz. Se revisó el archivo
  src/calculos_modelados/python/masw_bench/cache/curvas_boot_43dd0a39ad0f.npz:
  transformada Park, subarreglo 22–42 m, 24 remuestreos, dx = 2 m, L = 20 m;
  los campos fg, base y m_inv respaldan el punto de 8 Hz, 172 m/s y 21,5 m.
  La grilla exploratoria comienza en 6 Hz y la máscara de inversión utilizada
  comienza en 8 Hz; esto no demuestra un corte físico del instrumento.
- El punto de 5,1141 Hz de la exportación antigua masw_curva_dispersion.csv
  corresponde a 668 m/s y 130,62 m de longitud de onda, sin soporte de apertura
  suficiente en esta campaña. Se eliminaron las propuestas de 5 Hz del texto.
- Resultados y trabajos futuros explican que se requiere evaluar una mayor
  apertura efectiva para investigar frecuencias menores y capas más profundas,
  acompañada de señal coherente y ajuste reproducible del compensador. No se
  fijó una profundidad futura ni se afirmó que aumentar la apertura sea suficiente.
- Se preservaron las supresiones del autor y se mantuvieron verdes las nuevas
  correcciones durante los mensajes de seguimiento de esta misma pasada.
- Se desactivaron los comandos de color en los marcadores PDF. Compilación
  con pdflatex, BibTeX y dos pasadas adicionales: 16 páginas, 10 secciones,
  0 errores, 0 overfull y 0 referencias sin resolver. Se inspeccionaron las
  16 páginas renderizadas y, en detalle, los párrafos de resultados y trabajos
  futuros sobre 8 Hz y apertura; no se observaron superposiciones ni recortes.

## 12. Tercera pasada, 30 de agosto de 2026

- Se encontraron y resolvieron dos comentarios nuevos en los resultados
  geofísicos. Se retiraron los 61 envoltorios verdes de la pasada anterior,
  conservando su contenido; las once marcas actuales corresponden a esta revisión
  y a la aclaración posterior sobre apertura.
- Se reemplazó la comparación extensa con el procesamiento anterior por una
  frase: el análisis y la selección de subconjuntos permitieron identificar
  longitudes de onda de 20 a 22 m, con alcance preliminar de 10 a 11 m según
  la relación z ≈ λ/2. No reintroducir las cifras históricas de 5,42 m.
- La sección 9.3 distingue 9.3.1 Curva de dispersión y alcance y 9.3.2 Perfil
  e incertidumbre de la inversión. Se resumió la selección de tres capas sin
  retirar los 24 remuestreos, cinco semillas y 120 inversiones, ni los valores
  de velocidad e interfaz, ni los supuestos y límites de interpretación.
- La nueva sección 9.4 reúne la sensibilidad al procesamiento y a la selección
  de posiciones; la 9.5 contiene el contraste con sondeos eléctricos. La
  síntesis queda en 9.6. Se actualizó la referencia desde trabajos futuros a 9.4.
- Se conservaron las métricas de 2,28 m/s, 1,89 m/s y 29,76 m/s; se retiró la
  comparación retórica de trece veces, sin convertir la mediana y la diferencia
  cuadrática media en una misma estadística. La evidencia consultada está en
  masw_bench/informe/md/00_INFORME_PRINCIPAL.md, apartados 2.5 y 4.
- Se mantienen sin cambios el extremo inferior de 8 Hz y la necesidad de
  mayor apertura efectiva junto con señal coherente a menor frecuencia.
- El título de la síntesis se mantuvo unido a su tabla de ancho completo para
  evitar que quedara aislado en la página anterior. No se suprimieron filas,
  figuras ni contenido adicional para forzar una reducción de páginas.
- PDF final: 16 páginas, 10 secciones, 0 errores, 0 overfull y 0 referencias
  sin resolver. Se inspeccionaron las páginas renderizadas y los apartados
  modificados. Las tablas de ancho completo todavía dejan espacios libres;
  la reducción a 15 páginas no se abordó en esta revisión.
- Aclaración posterior del autor: en 9.3.1 se sustituyó la descripción de una
  cresta que se debilita y fragmenta por una explicación de la limitación de
  apertura efectiva para interpretar frecuencias menores y longitudes de onda
  grandes. Se distingue del aliasing espacial, que afecta longitudes de onda
  cortas. Se mantiene la necesidad de señal coherente a menor frecuencia.
  No se atribuyó a la apertura una fragmentación observada ni una caída de energía.
- No reintroducir la descripción visual anterior: la imagen está normalizada
  por frecuencia y no demuestra una pérdida de energía entre bandas. Además,
  figuras_finales.py dibuja la frontera lambda = 1,5 L, correspondiente al
  criterio de análisis, no al criterio estricto de diseño de la sección 6.

## 13. Cuarta pasada: ecuaciones y recopilación de figuras

- Petición del autor: incorporar más ecuaciones y recopilar imágenes por
  sección, incluidas las del Draw.io, sin insertarlas hasta que las elija.
- Se atendieron los dos nuevos comentarios de la sección 10. Quedaron cuatro
  líneas de trabajo: ruido, operación multicanal, geometría y protocolo, y
  ensayo de una fuente periódica con período variable. La relación f_k = k/T
  explica cómo se desplazan la fundamental y sus armónicos al variar el
  período entre ensayos. No se fija 0,75 Hz ni se promete una solución validada.
- Se eliminó la promesa de caracterización mecánica completa y se ajustaron
  las menciones relacionadas en validación y en la tabla de síntesis.
- Se pasó de 13 a 32 ecuaciones numeradas. Las diez secciones principales
  incluyen formulación matemática: rigidez, tránsito, atenuación, imagen de
  dispersión e inversión, SASW, geometría y fase, circuito RC, FIR y PI,
  cuantificación, diezmado, temporización, transferencia y coherencia,
  apilamiento, alcance medido y frecuencia de repetición.
- La ley de calibración se contrastó con el artículo compacto. La ecuación
  de transferencia corresponde al estimador realmente implementado en
  analizar_sweeps_circuito.m: señales analíticas por Hilbert y sumas dentro de
  intervalos del barrido. No describirlo como una estimación Welch convencional.
- El desajuste relativo coincide con inversion.py para predicciones completas;
  se declara la penalización de puntos faltantes. El promedio y diezmado
  adicional se distingue del filtrado interno del convertidor delta-sigma.
- Se exportaron las 14 páginas de Diagramas_operativos_y_calibracion.drawio
  sin modificar el archivo. La recopilación tiene 37 candidatos: 14 diagramas,
  20 imágenes y 3 páginas del libro de Foti ya disponible en docs.
- Entregables en recopilacion_figuras: Catalogo_figuras.pdf (38 páginas),
  catalogo_figuras.html (filtro por sección y selección de identificadores),
  RECOPILACION_FIGURAS.md, inventario.json y Diagramas_operativos_exportados.pdf.
  generar_catalogo.py permite reconstruir la galería y el catálogo.
- Las notas distinguen figuras prioritarias, de apoyo, bibliográficas y las
  que deben rehacerse. F06 no respalda el requisito temporal vigente, F17 no
  representa directamente el perfil adoptado, F03 contiene datos ilustrativos
  y F02 es un análisis histórico con ajustes medidos, no sólo un esquema teórico.
- Los esquemáticos se conservaron íntegros y no se insertó ninguna imagen en
  el manuscrito. El autor debe indicar los identificadores elegidos.
- Compilación y revisión visual: 16 páginas, 32 ecuaciones, 0 errores,
  0 overfull y 0 referencias sin resolver. Se revisaron también las 38 páginas
  del catálogo visual. La reducción independiente a 15 páginas sigue pendiente.


## 14. Recuperación después de incorporar imágenes

- Se contrastaron las cuatro secciones con la revisión anterior reconstruida
  desde respaldo y script, sin sobrescribir las figuras ni los apartados nuevos
  de interfaz de campo y servidor de ingesta.
- Habían desaparecido 9 ecuaciones, la tabla de subarreglos y correcciones de
  calibración, caracterización, ubicación de campaña y alcance. Se repusieron.
- Se restauró la explicación de apertura efectiva y 8 Hz; no reintroducir la
  descripción de fragmentación por aliasing ni afirmar que la medición eléctrica
  descarta por sí sola limitaciones electrónicas a baja frecuencia.
- Se atendió el nuevo comentario sobre la relación de rigidez en la introducción:
  se retiró esa ecuación redundante. Quedan 31 ecuaciones, no 32.
- Se preservan 24 figuras. Se retiró una única duplicación exacta de la interfaz
  web. Los archivos de imagen no se editaron. El pie del espectro de campo aclara
  que su rótulo de 50 m es histórico y ya no constituye una meta del proyecto.
- Se conservan las cuatro líneas breves de trabajos futuros. No reponer la
  cadencia fija de 0,75 Hz ni promesas de calibración mecánica completa.
- Informe, diferencias, verificaciones y respaldo de fuentes en
  evidencia/recuperacion_codex_2026-08-30/. Usar ese ZIP como referencia de esta
  revisión si futuras ediciones vuelven a perder contenido.

## 15. Capturas de interfaz en modo claro

- El autor pidió sustituir las imágenes oscuras por capturas en modo claro.
- La figura de interfaz web usa `figuras/i_web_maestro_claro.png`, copiada sin
  editar de `latex-15p-review/figuras/interfaces/geophone_scope_captura_real_claro.png`.
  Muestra la web del maestro con controles de captura y señales HAMMER/GEO;
  se ajustó el pie para describir esa pantalla.
- El osciloscopio usa `figuras/i_scope_stream_claro.png`, copiada sin editar de
  `latex-15p-review/figuras/interfaces/qt_scope_06_stream_tema_claro.png`.
- La pantalla de análisis ya estaba en modo claro y se conservó. También se
  conservaron todos los textos y ecuaciones recuperados. Las capturas oscuras
  originales siguen en la carpeta, pero ya no están referenciadas en el documento.
- Para futuras sustituciones de capturas, usar modo claro y conservar los datos
  reales de la interfaz; no recolorear ni reconstruir artificialmente las señales.


## 16. Referencias y atribuciones (31 de agosto de 2026)

- A pedido del autor se completaron las citas del manuscrito: ahora se imprimen
  29 referencias (antes 10). No usar nocite{*} para incorporar entradas sin uso.
- Se verificaron fuentes geotécnicas, DSP, Ma (compensador), PSoC, filtros,
  ESP-NOW, transductores, bootstrap y el informe hidrogeológico de julio de 2023.
- Las 24 figuras tienen procedencia explícita: dos de Foti, el geófono de DESY
  reproducido en Breslin (2020), y 21 elaboraciones/capturas/resultados propios.
- Se corrigieron la banda del Güralp, los costos no respaldados, las afirmaciones
  absolutas sobre penetración y tolerancias MFB, y la descripción de direcciones
  de ESP-NOW. No reponer esos enunciados sin evidencia adicional.
- Las marcas de la ronda anterior se retiraron conservando su contenido. Esta
  ronda usa revsolution para los agregados y correcciones; no había rev pendientes.
- Se preservan exactamente 31 ecuaciones y 24 imágenes, los 8 Hz, la limitación
  por apertura, los resultados recuperados y las capturas en modo claro.
- PDF final de 29 páginas, sin errores, overfull ni referencias sin resolver;
  se verificó visualmente. No se hizo la reducción editorial a 15 páginas.
- Respaldo antes/después, informe, diferencias y verificación en
  evidencia/referencias_2026-08-31/.
