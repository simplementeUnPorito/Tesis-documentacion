# Auditoría de datos de la Primera Presentación

**Fecha:** 2026-08-28
**Alcance:** `latex-reestructurado/` y su fuente `BORRADOR_PRELIMINAR_15_PAGINAS.md`.
**Método:** cada afirmación numérica o factual se contrastó contra la fuente primaria
del repositorio (dato crudo, dato procesado, script de cálculo o bitácora de commit).
No se aceptó como respaldo un documento narrativo cuando existía el dato.

Estados: **OK** verificado contra fuente primaria · **ERROR** contradice la fuente ·
**IMPRECISO** respaldado pero mal redondeado o mal atribuido · **SIN RESPALDO** no se
encontró fuente.

---

## 1. Errores confirmados

### E1 — La topología MFB no fue descartada: es la del pasa-bajos implementado

**Estado: ERROR.** `secciones/03_diseno.tex:73` afirma que «se descartaron las
topologías Sallen-Key y de realimentación múltiple porque el Q requerido es bajo y
ambas reparten cada polo entre más componentes».

La realimentación múltiple (MFB) **no** se descartó. Evidencia:

| Fuente | Qué dice |
|---|---|
| `src/calculos_modelados/matlab/AnalisisCircuito/analizar_sweeps_circuito.m:947` | `ideal.LP = makeMfbLowpassNonideal(R1,R2,R3,C1,C2,cfg.opamp);` |
| mismo archivo, líneas 1288-1292 | `R1Lp=30k, R2Lp=150k, R3Lp=12k, C1Lp=47n, C2Lp=3.3n`, juego de componentes MFB pasa-bajos clásico |
| `latex-15p-review/secciones/03_acondicionamiento_digitalizacion.tex:104` | «La sección MFB se dimensionó con f_a = 300 Hz y zeta_a = 0,691» |
| `docs/investigacion/Notes/bitacora/2026-04-30.md:25` | «Sallen key off, mfb la onda», es decir el pivote *hacia* MFB |
| `docs/investigacion/Notes/bitacora/2026-05-05.md:167` | se midieron las dos topologías (`MFB_DigitalFilterLPF.mat`, `Sallen_Key.mat`) para respaldar la decisión |

Además el propio párrafo se contradice: describe «un polo en la entrada y otro en la
realimentación de un inversor», que es exactamente la estructura que el script modela
para la rama BP (`a1 = Rin*Cin + Rf*Cf`, `a2 = Rin*Rf*Cin*Cf`, es decir dos polos
reales **desacoplados**).

**Lo que es cierto y debería decir el documento:**

1. Para la **rama pasabanda de compensación** se exploró Sallen-Key/VCVS (bitácora
   2026-04-27), se descartó el 2026-04-30, y la implementación final usa **dos polos
   desacoplados** sobre un inversor, cada uno con un único par RC.
2. El **pasa-bajos antialias sí es MFB**, dimensionado con f_a = 300 Hz y
   zeta_a = 0,691, y junto con el polo del sumador (393 Hz) forma un Bessel de tercer
   orden.

### E2 — El documento nunca dice a qué frecuencia se adquirió la campaña que reporta

**Estado: OMISIÓN, no error.** (Una versión anterior de esta auditoría daba el 2604 Hz
por equivocado. Estaba mal: se corrige acá con la fuente que zanja el punto.)

`src/interfaces/python/geophone_scope/HANDOFF_KALMAN.md:304` es explícito:

> «**fs: 2604 Hz es la nativa del firmware vigente; 2929 y 1020 son configuraciones
> históricas que quedaron en los metadatos.**»

De modo que los 2604 Hz de `secciones/03_diseno.tex:99` y de la figura
`arquitectura_vigente` **son correctos**: describen el diseño vigente, que es
precisamente lo que la sección 9 y esa figura documentan. Confirmado además en el
firmware: `psoc_adc.h:32` («2604 SPS nativos / 18 bits»), `psoc_uart.h:92` y
`geophone_scope/config.py:46`.

El problema real es otro y es de lectura: la campaña que el documento reporta en las
secciones 10 y 11 **no se adquirió a esa tasa**.

| Fuente | Valor |
|---|---|
| `data/raw/Canchita/metadata.json` | `"fs": 2929` |
| `data/processed/Canchita_procesado/manifest.json` | 455 registros a **1020 Hz** y 143 a **2929 Hz** |

Tal como está, un lector supone razonablemente que los registros de campo salieron a
2604 Hz. **Falta una cláusula en la sección 10.3** que diga que la campaña se adquirió
con una configuración anterior, a 2929 Hz nativos, y que el conjunto procesado mezcla
2929 y 1020 Hz. No hay que cambiar el 2604 de la sección 9.

### E3 — f_0 está mal redondeado

**Estado: IMPRECISO.** El documento dice f_0 = 10,21 Hz.
`resultados_tanda_calibrada/05_tablas_reportes/parametros_compensador.csv` da
`f0 = 10,2045976372255 Hz`, cuyo redondeo correcto a dos decimales es **10,20 Hz**.
El error se hereda de `latex-15p-review`, que ya decía 10.21.

### E4 — zeta_1 y el factor de atenuación

**Estado: IMPRECISO.** El mismo CSV da `zeta1_denominador_BP = 937,396332177499`.
El documento usa zeta_1 ≈ 938 y de ahí deriva «1876 veces». Con el valor exacto,
2·zeta_1 = 1874,8. La cifra redonda es defendible, pero conviene escribir
zeta_1 ≈ 937 y «cerca de 1875 veces», o declarar explícitamente el redondeo.
En cambio 1/(2·zeta_1) = 5,33e-4 sí es correcto.

### E5 — Las dos figuras del resultado geofísico muestran la inversión que el texto descarta

**Estado: ERROR, y es el más visible de todos.**

`masw_resultado.png` (sección 11.3) y `vs_vs_sev.png` (sección 11.3) se generan desde
`data/processed/Canchita_procesado/masw_perfil_vs.csv`, que es la **exportación de
julio**: 9 capas hasta 82,575 m, desajuste 2,554 %, $V_S$ de 62,9 a 1011,5 m/s, con la
curva de dispersión llegando a $\lambda = 130{,}6$ m a 5,11 Hz.

El texto de la sección 11.3 presenta otra cosa: un modelo de **tres capas**, con
78 m/s hasta 2,4 m y 178 m/s por debajo, desajuste 1,36 %, soporte de longitud de onda
de 20 a 22 m y profundidad defendible de 10 a 11 m. El mismo párrafo declara que
$V_{S,30}$ **no puede calcularse** porque la profundidad sustentada no llega a 30 m.

Verificado abriendo las imágenes: `masw_resultado.png` rotula literalmente
«Perfil $V_S(z)$ · **9 capas + semiespacio**» y dibuja el eje de profundidad **hasta
100 m**. Es decir, la figura contradice de frente la cautela central del texto.

Hay que regenerar ambas figuras desde el resultado del benchmark (tres capas, park,
sub-arreglo 22-42, picker dp) o retirarlas. El perfil correcto está en
`src/calculos_modelados/python/masw_bench/informe/md/10_CONTRASTE_HIDROGEOLOGICO.md`
§3 y en `HALLAZGOS.md` §16.1.

### E6 — El pie de figura promete una banda de incertidumbre que no existe

**Estado: ERROR.** El pie de `masw_resultado` dice «Derecha: perfil $V_S(z)$ **con su
banda de incertidumbre**». La figura **no tiene ninguna banda de incertidumbre**: es
una línea escalonada sola. El pie describe algo que no está dibujado.

### E7 — «21 posiciones» contra «15 distancias» en la misma página

**Estado: ERROR.** La sección 11.2 afirma que las métricas de energía y SNR se calculan
«sobre las 21 posiciones», y la tabla de síntesis repite «Métricas de energía y SNR
sobre 21 posiciones». Pero la figura que las sostiene,
`contenido_baja_frecuencia.png`, lleva impreso en su propio título:
**«Contenido espectral real del canal de geófono en campo (265 golpes, 15 distancias)»**.

O se corrige el texto a 15 distancias y 265 golpes, o se regenera la figura sobre las
21 posiciones. Como está, el documento se contradice a sí mismo.

### E8 — El pie del SM-24 describe mal la figura

**Estado: ERROR.** El pie dice que las respuestas referidas a velocidad y a aceleración
están «**sobre los mismos ejes**». No lo están: la figura tiene **dos paneles
separados** con escalas verticales distintas (de −120 a 0 dB el izquierdo, de −60 a
+10 dB el derecho). Las pendientes de 40 y 20 dB por década que el pie menciona sí se
verifican en el dibujo.

### E9 — La figura de la sección 10.1 lleva impresa una ruta local del disco

**Estado: ERROR de presentación.** `mosaico_normalizados.png` no es una figura sino una
**hoja de contacto** de cinco figuras MATLAB, cada una con tres subgráficos apilados, y
tiene rotulada dentro de la imagen la ruta absoluta
`C:/Github/Tesis/src/calculos_modelados/matlab/AnalisisCircuito/resultados_tanda_calibrada/06_graficos_normalizados`.
Eso no puede ir en un documento entregable, y además al 27 % de escala es ilegible.

Reemplazo recomendado: usar el gráfico individual
`resultados_tanda_calibrada/06_graficos_normalizados/normalizado_cadena_pga_adc.png`,
que es justamente la fila central de la Tabla 2, a ancho de página completa.

### E10 — La distancia a los sondeos eléctricos está mal acotada

**Estado: ERROR.** La sección 11.3 dice que los sondeos «se ubican en el mismo predio, a
una distancia del orden de **120 a 200 m** de la línea de adquisición».
`10_CONTRASTE_HIDROGEOLOGICO.md` §3.1 da las tres distancias reales:

| Sondeo | Distancia a la línea |
|---|---|
| SEV 01 | ≈ 120 m |
| SEV 02 | ≈ 258 m |
| SEV 03 | ≈ 340 m |

El rango correcto es **120 a 340 m**. El texto sí acierta al usar el SEV 01 como el más
próximo.

### E11 — La figura de geometría muestra un segundo grupo que el pie no menciona

**Estado: MENOR.** `geometria_campanas.png` dibuja dos grupos: «Grupo 1, 21 posiciones,
L=40 m, activo» y «Grupo 2, 14 posiciones, L=26 m, peso 0». El pie sólo habla de las
21 posiciones. El JSON de estado actual ya tiene un solo grupo, así que **al regenerar
la figura el problema se corrige solo**.

---

## 2. Verificado correcto contra fuente primaria

### Geometría y campaña, desde `data/processed/Canchita_procesado/manifest.json`

| Afirmación del documento | Valor hallado | Estado |
|---|---|---|
| 21 posiciones | 21 exactas: 10, 12, ..., 50 m | **OK** |
| Paso de 2 m | paso uniforme de 2 m | **OK** |
| Apertura L = 40 m | 50 − 10 = 40 m | **OK** |
| 607 registros candidatos | `sample_count` 598 + `skipped_count` 9 = **607** | **OK** |
| 598 incorporados | `sample_count = 598` | **OK** |
| Mediana cercana a 30 golpes por posición | mediana **30,0** (media 28,5) | **OK** |
| Entre veinte y treinta y siete golpes por posición | mínimo **20**, máximo **37** | **OK** |
| Separación y apertura persistidas | `geophone_spacing_m` 2,0 y `array_length_m` 40,0 en `field_review_masw_state.json` | **OK** |

Corroborado además por `src/calculos_modelados/python/masw_bench/FINAL_MEASUREMENTS.md`
§1.1: «golpes totales 607 (≈28,9 por offset)», «offsets 10 a 50 m, 21 posiciones»,
«apertura L 40 m».

> **Trampa a evitar.** Existe un segundo manifiesto,
> `Canchita_grupo1_procesado/manifest.json`, con 477 muestras y mediana 21. **No es el
> de la campaña completa** y no debe citarse. Es un subconjunto.

### Caracterización del acondicionamiento, desde `resumen_identificacion.csv`

Las cuatro filas de la Tabla 2 reproducen exactamente el CSV:

| Ruta | Puntos | Banda | Coherencia | Magnitud | Fase |
|---|---:|---|---:|---:|---:|
| BP | 85 | 0,2112 – 47 476,9 Hz | 0,96835 | 6,4851 dB | 27,770° |
| COMP | 71 | 0,2113 – 4 735,79 Hz | 0,96428 | 0,37936 dB | 2,4438° |
| LP | 33 | 11,749 – 1 113,98 Hz | 0,94543 | 0,59598 dB | 2,4810° |
| LP_PGA | 61 | 0,2113 – 1 112,38 Hz | 0,99457 | 0,19977 dB | 1,1612° |

**OK** en los cuatro casos. También verificado: el potenciómetro objetivo de 634,539 Ω
y el error complejo de 20,749 coinciden con `parametros_compensador.csv`
(`pot_requerido_para_zeta0 = 634,5388`, `error_relativo_estimacion_pot = 20,7491`).

### Cadena de ganancia

**OK, con una precisión que conviene incorporar al texto.** El ×3,6 del sumador no es
el camino directo (−27k/6,8k = 3,97) sino la **rama BP** (−27k/7434,5 Ω = 3,632). Con
ese valor 2 × 50 × 3,632 × 5 = **1816 ≈ 1800**, de modo que la cifra es internamente
coherente. El ×5 del pasa-bajos queda confirmado por componentes
(`R2Lp/R1Lp = 150k/30k = 5`). Conviene aclarar de qué rama se trata.

### Aritmética verificada de forma independiente

| Afirmación | Comprobación | Estado |
|---|---|---|
| El SM-24 cae 27,6 dB a 2 Hz | con zeta_0 = 0,25 da −27,65 dB | **OK** |
| El SM-24 cae 40 dB a 1 Hz | −39,92 dB | **OK** |
| f_min = c/2z da 7,5 Hz para 10 m | 150/20 = 7,5 | **OK** |
| f_min da 1,5 Hz para 50 m | 150/100 = 1,5 | **OK** |
| Tolerancia de sincronización de 130 µs | 0,01·2/150 = 133 µs | **OK** |
| L ≥ 1,5·lambda_max da 27 m | 40/1,5 = 26,7 m | **OK** |
| 45 impactos por minuto dan 0,75 Hz | 45/60 | **OK** |
| Doce líneas en 1–10 Hz, la primera a 1,50 Hz | armónicos n = 2 a 13 | **OK** |
| sigma_t ≤ 0,051/f para 5 % de pérdida | sqrt(−2·ln0,95)/2pi = 0,0510 | **OK** |
| 5,1 ms a 10 Hz y 1,02 ms a 50 Hz | exacto | **OK** |
| 1,46 ms da 0,4 % a 10 Hz y cerca de 10 % a 50 Hz | 0,42 % y 10,0 % | **OK** |
| La geometría pesa unas trece veces más que el algoritmo | 29,76/2,28 = 13,05 | **OK** |
| Profundidad de 5,42 m desde lambda = 10,84 m | 10,84/2 | **OK** |
| Modelo de op-amp: GBW 8 MHz, A0 90 dB, Rin 35 MΩ | `modelo_operacional_psoc.csv` | **OK** |

### Interfaces del SEV

`fig_dos_inversiones.py:36` codifica `SEV = [(1186, 1.00), (15, 2.06), (105, 4.15), ...]`.
Las tres profundidades citadas (1,00 / 2,06 / 4,15 m) son **OK**.

### Soporte de profundidad de 10 a 11 m

`FINAL_MEASUREMENTS.md` §1.1 y §1.2: «mejor z confiable ≈ 11 m», con longitud de onda
realmente invertida de **20 a 22 m** en los tres finalistas. **OK.**

### Resultados geofísicos, desde `masw_bench/informe/md/`

Todo el contenido cuantitativo de la sección 11.3 se verificó y es **OK**:

| Afirmación | Fuente | Estado |
|---|---|---|
| Perfil en escalón: 78 m/s hasta 2,4 m, 178 m/s debajo | `10_CONTRASTE_HIDROGEOLOGICO.md:249-251` (cita `HALLAZGOS.md` §16.1) | **OK** |
| Una sola interfaz resuelta, en 2,4 m | ídem | **OK** |
| Tres capas: 100 % de la varianza es del dato | `00_INFORME_PRINCIPAL.md` §2.5 | **OK** |
| Con cuatro capas cerca de la mitad viene del optimizador | mismo §2.5: **52 %** | **OK** |
| SEV 01 es el más próximo, a ≈120 m | `10_CONTRASTE_HIDROGEOLOGICO.md` §3.1 | **OK** |
| Interfaz MASW de 2,4 m contra la de 2,06 m del SEV: 0,34 m | ídem | **OK** |

Tabla de subarreglos (`00_INFORME_PRINCIPAL.md` §2.4), reproducida exactamente:

| Ventana | Desajuste | z(1,5L) | Estado |
|---|---:|---:|---|
| 10-50 (completo) | 2,28 % | 8,81 m | **OK** |
| 18-46 | 1,85 % | 10,06 m | **OK** |
| 22-42 | 1,36 % | 10,75 m | **OK** |
| 30-50 | 16,5 % | — | descalificado por desajuste, **OK** |
| 22-38 | — | — | descalificado, 38 % de la curva sobre aliasing, **OK** |

### Las cifras que más sospecha levantaban, y que resultaron correctas

Se rastrearon a fondo porque no aparecían en los CSV de resumen. Todas tienen fuente
primaria:

| Afirmación | Fuente | Valor exacto | Estado |
|---|---|---|---|
| «la calibración manual redujo el error de 26,7 dB a 10,7 dB» | `data/raw/Osciloscopio_verificacion_calibracion_2026-07-21/RESULTADO.md` | «Error RMS de magnitud CH3/PGA contra PSoC High: `26.707 dB` → `10.707 dB`» | **OK** |
| «deja un desajuste remanente en torno a 10 Hz» | mismo archivo, primera línea | «todavía no coincide con el ajuste objetivo alrededor de 10 Hz» | **OK** |
| BP: dispersión mediana 2,26 dB y p90 21,45 dB | mismo archivo, línea 29 | `2.257 dB` y p90 `21.454 dB` | **OK** |
| «la fila BP mezcla campañas históricas mutuamente inconsistentes» | `resultados_tanda_calibrada/RESULTADO.md` líneas 6 y 48 | «las campañas no coinciden bien entre sí en ganancia de BP» | **OK** |
| «el estimador del potenciómetro no resulta confiable» | mismo, sección Potenciómetro | «ninguna posición fija del modelo reproduce toda la forma observada» | **OK** |
| «bandas superpuestas desde los 10 mHz hasta los 200 kHz» | carpetas `10mHzto50mHz_400s_50s_div` y `20kHzto200kHz_1ms_100us_div` en `data/raw/Osciloscopio_verificacion_calibracion_2026-07-21/` | ambos extremos existen | **OK** |
| «la dinámica subsónica no resulta observable» | `resultados_tanda_calibrada/RESULTADO.md` | «tfest conserva su límite inferior de 0,2 Hz» | **OK** |
| jitter de alineación 1,46 ms | base de conocimiento §466, del benchmark | 1,46 ms | **OK** |
| coherencia adyacente 0,732 en 10–50 Hz | `latex-historial/secciones/24_banda_util_real.tex` | 0,732 | **OK** |
| energía bajo 10 Hz «menos del uno por ciento» | misma fuente | 0,74 % | **OK** |
| plus code `M9F6+Q95` | base de conocimiento §24 | ídem | **OK** |
| Laboratorio LED, 20–27 m | base de conocimiento §40 | estimado 20 m, medido ≈26,8 m | **OK** |
| 26 subarreglos contiguos | base de conocimiento §284 | 26 | **OK** |
| 24 bootstrap × 5 semillas = 120 inversiones | base de conocimiento §380 | ídem | **OK** |
| sensibilidad 2,28 / 1,89 / 29,76 m/s | base de conocimiento §423-425 | ídem | **OK** |
| 8,00–21,71 Hz, λ 10,84 m, z 5,42 m | base de conocimiento §348 | ídem | **OK** |
| 11,83 m «con otra convención» | base de conocimiento §289 | ídem | **OK** |

### Valores de componente, confirmados por el esquemático

El esquemático `AnalogPathFinal_trim.png` muestra, legibles a tamaño nativo, los
mismos valores que usa `analizar_sweeps_circuito.m`: rama BP con 43k de entrada,
680 µF, 43k de realimentación y 150 pF + 27 pF; `Ru` y `R_BP` de 6,8 k con
potenciómetro de 2 k; sumador de 27 k con 15 nF; y pasa-bajos de **30k / 150k / 12k /
47 nF / 3,3 nF**, que es la disposición **MFB clásica**. Es evidencia visual
independiente de E1.

El esquemático muestra VDACs, no fuentes de corriente, lo cual es **correcto** y
coherente con la sección 9.3, que declara que la revisión con IDAC no participó de la
campaña.

---

## 3. Figuras: todas ilegibles en la maqueta a dos columnas

El documento es `article` a **dos columnas** con `margin=2,5 cm` y `columnsep=0,7 cm`,
de modo que `\textwidth` = 6,30 pulgadas y **`\columnwidth` = 3,01 pulgadas**.

Las figuras provienen de `latex-historial`, que es un documento **a una columna**. Sus
scripts las generan con `figsize` de 7,4 a 11 pulgadas y fuentes de 8 a 10 pt. Al
insertarlas en una columna de 3,01 pulgadas el factor de escala cae a 0,27–0,62 y el
texto queda entre **3,4 y 5,6 pt**. El piso de legibilidad impresa es 6 pt. **Ninguna
figura lo alcanza.**

| Figura | Ancho nativo | Destino | Escala | Fuente efectiva |
|---|---:|---:|---:|---:|
| `AnalogPathFinal_trim` | 41,67" | 3,01" | **0,07** | ilegible |
| `DigitalPathFinal_trim` | 36,11" | 3,01" | **0,08** | ilegible |
| `mosaico_normalizados` | 19,72" | 5,42" | 0,27 | ilegible |
| `respuesta_sm24_modelo` | 10,40" | 3,01" | 0,29 | ilegible |
| `repetibilidad_fuente` | 9,64" | 3,01" | 0,31 | ilegible |
| `gather_sintetizado` | 8,84" | 3,01" | 0,34 | ilegible |
| `geometria_campanas` | 8,34" | 3,01" | 0,36 | **3,4 pt** |
| `flujo_calibracion_horizontal_usuario` | 8,44" | 3,01" | 0,36 | 202 dpi efectivos |
| `sincronizacion_fase` | 7,30" | 3,01" | 0,41 | **3,7 pt** |
| `extension_banda` | 7,30" | 3,01" | 0,41 | **3,7 pt** |
| `roadmap_validacion` | 10,70" | 5,42" | 0,51 | ilegible |
| `vs_vs_sev` | 10,32" | 5,42" | 0,52 | ilegible |
| `arquitectura_vigente` | 10,50" | 5,42" | 0,52 | **3,7 pt** |
| `masw_resultado` | 10,30" | 5,42" | 0,53 | ilegible |
| `contenido_baja_frecuencia` | 8,73" | 5,42" | 0,62 | **5,6 pt** |

Los dos esquemáticos son un caso aparte: aun ocupando el ancho completo de página
quedarían al 15 % de su tamaño nativo. No se arreglan reescalando.

**Restricción:** no deben regenerarse dentro de `latex-historial/figuras/` ni editarse
sus scripts en el lugar, porque ese es un entregable histórico cuyo PDF depende de esos
PNG exactos.

### 3.1 Qué se hizo

Se copiaron los scripts a `latex-reestructurado/scripts/` y se regeneraron las figuras
en `latex-reestructurado/figuras/`, que ahora va primero en `\graphicspath`.
`latex-historial/` quedó intacto.

1. **Cada figura se regeneró al ancho de su destino**, de modo que entra a escala
   próxima a 1 y las fuentes conservan su tamaño en puntos. Todas las figuras del
   documento pasaron a `figure*` a ancho de página, porque una columna de 3 pulgadas
   no puede alojar un diagrama de Bode rotulado a un tamaño legible.
2. **Los dos esquemáticos se partieron en bloques funcionales.** El analógico va en dos
   láminas apiladas a ancho completo (entrada y ganancia; compensación, sumador y
   pasa-bajos) a unos 240 dpi efectivos: ahora se leen todos los valores de componente.
   El digital va en dos paneles (control y DMA) a unos 200 dpi.
3. **`arquitectura_vigente` se rehízo como diagrama TikZ** dentro del documento. Al
   reescalar el PNG el texto desbordaba las cajas y quedaba ilegible, porque las cajas
   están en coordenadas de datos y el texto no. El TikZ además usa la tipografía del
   documento.
4. **Se quitaron los títulos incrustados** que duplicaban el pie de figura y venían en
   una tipografía ajena (`respuesta_sm24_modelo`, `contenido_baja_frecuencia`,
   `geometria_campanas`, `roadmap_validacion`).
5. **`mosaico_normalizados` se reemplazó** por `normalizado_cadena_pga_adc.png`, que es
   la fila destacada de la tabla de identificación. Desaparece la ruta local impresa.
6. Se corrigieron tres defectos de maqueta que aparecieron al revisar: la tabla de
   identificación estaba en un `table*` pero dimensionada a `\columnwidth`, de modo que
   se comprimía a media página; las tablas de requerimientos, subarreglos y síntesis
   quedaban con una palabra por línea; y el documento **no tenía ni un solo `\label`**,
   con cuatro referencias cruzadas escritas a mano que la renumeración dejó apuntando
   al flotante equivocado. Ahora usan `\label`/`\ref`. Los flotantes de tabla se
   rotulan «Tabla» y no «Cuadro», que es lo que dice el cuerpo del texto.

Estado del PDF: **25 páginas, cero errores, cero referencias sin resolver, tres
`Overfull` menores** (eran trece).

---

## 4. Advertencia sobre el estado MASW persistido

`data/processed/Canchita/field_review_masw_state.json` fue **modificado el 2026-08-20**,
después de que se generaran las figuras (12 y 13 de agosto). Su estado actual tiene sólo
2 picks en el modo 0, `regions_by_mode` vacío y **no contiene la clave `edited_profile`**
que `fig_estado_actual.py` necesita. Las figuras derivadas de ese JSON provienen de un
estado anterior y el script fallaría si se lo volviera a correr tal cual.

Lo que sí se conserva sin cambios y respalda al documento: `geophone_spacing_m = 2,0`,
`array_length_m = 40,0`, `inversion_params.nlayers = 7` y `inv_scalars.misfit = 7,106`.

---

## 5. Estado de cada hallazgo

| | Hallazgo | Estado |
|---|---|---|
| E1 | MFB presentada como descartada, cuando es la topología del pasa-bajos | **corregido** en el .md y en el .tex |
| E2 | No se declaraba la frecuencia de muestreo real de la campaña | **corregido**: se agregó la cláusula en §10.3 |
| E3 | `f_0 = 10,21` mal redondeado | **corregido** a 10,20 Hz |
| E4 | `zeta_1 = 938` y factor 1876 | **corregido** a 937 y 1875 |
| E5 | Las figuras del resultado MASW muestran la inversión de julio | **ABIERTO**, requiere decisión |
| E6 | Pie que prometía una banda de incertidumbre inexistente | **corregido** |
| E7 | «21 posiciones» donde la métrica usa 265 golpes en 15 distancias | **corregido** en las dos apariciones |
| E8 | Pie del SM-24 decía «sobre los mismos ejes» | **corregido** |
| E9 | Hoja de contacto con ruta local impresa | **corregido**, reemplazada |
| E10 | Distancia a los sondeos acotada como 120–200 m | **corregido** a 120, 258 y 340 m |
| E11 | La figura de geometría mostraba un grupo no mencionado | **corregido** solo, al regenerar |

---

## 6. Lo único que queda abierto: E5

Es el más importante y **no se puede cerrar sin una decisión**.

`masw_resultado.png` y `vs_vs_sev.png` se construyen desde
`data/processed/Canchita_procesado/masw_perfil_vs.csv`, que es la exportación de julio
(9 capas hasta 82,6 m, desajuste 2,554 %). El texto de la sección 11.3 presenta el
resultado del benchmark: tres capas, 78 y 178 m/s, interfaz en 2,4 m, desajuste 1,36 %,
soporte de 10 a 11 m. **Las figuras contradicen al texto**, y de forma visible: dibujan
el perfil hasta 100 m de profundidad justo donde el texto explica que no se sostienen
más de 11 m y que por eso $V_{S,30}$ no puede calcularse.

Tres salidas posibles:

1. **Regenerar las dos figuras desde el resultado de tres capas.** Es la correcta. Hace
   falta exportar el perfil y la curva del sub-arreglo 22-42 con picker `dp` desde
   `src/calculos_modelados/python/masw_bench/` a un CSV con el mismo formato que
   `masw_perfil_vs.csv`, y volver a correr `fig_masw.py` y `fig_vs_vs_sev.py`.
2. **Mostrar las dos inversiones lado a lado** y explicar por qué se prefiere la de tres
   capas. Ya existe `fig_dos_inversiones.py` para eso, y el argumento metodológico
   (partición de la varianza) es de los más fuertes del trabajo.
3. **Retirar las dos figuras** y sostener la sección 11.3 solo con el texto y la tabla.
   Es la opción segura si no hay tiempo.

Mientras tanto, ninguna de las dos figuras debe presentarse como «el resultado» sin
aclarar de qué inversión se trata.

---

## 7. Pendientes menores, no bloqueantes

1. La caracterización de la etapa **LP por separado** sólo cubre de 11,75 Hz hacia
   arriba (33 puntos). La cadena completa PGA→ADC sí baja a 0,21 Hz, que es lo que
   sostiene el argumento, pero conviene no confundirlas al exponer.
2. `normalizado_cadena_pga_adc.png` queda a unos 300 dpi efectivos con fuentes cercanas
   a 6 pt. Es legible pero está en el piso. La mejora real exige reexportar la figura
   desde MATLAB con fuentes mayores, y eso sólo lo puede hacer quien tenga MATLAB.
3. `repetibilidad_fuente.png` queda en unos 5,8 pt efectivos, también en el piso.
4. `roadmap_validacion.png` tiene dos pares de etiquetas que se solapan levemente y
   no lleva acentos (dice «Campana», «despues», «sintesis»).
5. Verificar contra fuente primaria las referencias `Ma2023`, `Foti2018` (el criterio
   $L\ge1{,}5\lambda_{\max}$), `LinAshlock2016`, `Barbier1976` y `Park1996SIST`.
6. El estado MASW persistido cambió el 2026-08-20 y ya no contiene `edited_profile`.
   El script quedó protegido para no fallar, pero si se quiere volver a generar
   `masw_estado_actual` hay que recuperar ese estado del historial de git.
