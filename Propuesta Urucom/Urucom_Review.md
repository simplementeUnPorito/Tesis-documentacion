# Editorial Decision + Revision Roadmap
## "Automatic DC-Offset Calibration for a Low-Cost Geophone Front End"
### Vargas Cabral & Álvarez Martínez — Universidad Católica NSA, Asunción

Panel simulado: EIC + Metodología (R1) + Dominio (R2) + Perspectiva (R3) + Abogado del Diablo (DA).
Los cinco revisaron de forma independiente, sin verse entre sí.

---

## DECISIÓN: MAJOR REVISION (al borde de Reject-and-Resubmit)

| Revisor | Recomendación |
|---|---|
| EIC | Major Revision (*"generosa; un R&R sería defendible solo con C1"*) |
| R1 Metodología | Major Revision, rozando Reject-and-Resubmit |
| R2 Dominio | **Reject-and-Resubmit** |
| R3 Perspectiva | Major Revision |
| DA | **Reject as submitted**, invitar reenvío |

El DA encontró issues CRITICAL → por regla del panel, **Accept queda vedado**.

**El paper no es malo. El manuscrito sí.** La ingeniería es real, las tres placas existen, los registros de campo existen, y la honestidad de los autores (reportan el resultado nulo del PGA en su propio abstract) es genuinamente inusual y merece crédito. Lo que llegó a la mesa, en cambio, no está terminado.

---

## PARTE 1 — LO QUE BLOQUEA EL ENVÍO (arreglar antes de mandar nada)

### B1. Tabla II tiene 8 celdas que dicen `(falta medir)`, en rojo. **[los 5 revisores]**
Board C completo: `202 (falta medir)`, `374 (falta medir)`, `897 (falta medir)`, `342 (falta medir)`, `206 (falta medir)`, `213 (falta medir)`, `48.8 (falta medir)`, `31.9 (falta medir)`.

El abstract, la Sec. I (contribución 3) y la conclusión afirman resultados **"on three boards"**. Un tercio de la tabla principal está marcado por los propios autores como no medido. En la mayoría de las revistas esto es **desk reject sin revisión**.

Además, el caption dice *"Board C has only one run"* — o sea que el caption y las celdas se contradicen: ¿son mediciones reales de una corrida, o son placeholders? El lector no puede saberlo, y eso contamina la confianza en **toda** la tabla.

→ **Medir Board C a N=5, o borrar Board C y decir "dos placas".** Un N=2 honesto vale infinitamente más que un N=3 en rojo. No hay punto intermedio.

### B2. La Introducción afirma un experimento que la Sec. IV niega. **[EIC, R1, R2, R3, DA]**
- Sec. I, contribución 3: *"validation on three independently assembled boards **at maximum PGA gain**"*
- Abstract y Sec. IV-A: *"the PGA at a representative **mid-range** gain (×16 of a configurable range up to ×50)"*, y *"validating higher gains is **future work**"*

×16 de un rango de ×50 no es ganancia máxima. La Sec. I es el único lugar que lo dice, y reclama el experimento estrictamente más fuerte. Se lee como una frase fósil de un borrador anterior — y peor, es **exactamente el experimento que el paper necesita** (ver A1).

Agravante (R3, DA): la Fig. 4 (los registros de campo) se tomó *"using the higher PGA settings needed far-offset"* — o sea, **la única evidencia de campo se recogió en el régimen que el paper declara no validado**.

### B3. Higiene de manuscrito
- Fig. 3, caption: *"Traces are individually labeled and remain distinguishable in grayscale"* — es una nota al tipógrafo, no contenido de caption. Borrar.
- "~10 s" aparece 4 veces (abstract, IV-C, V, VI); el caption de la Fig. 3 implica ~7 s (t≈9 s → t≈16 s); los timeouts de la Tabla I suman **57.6 s** de peor caso, nunca declarado.
- Sec. II tiene una subsección "A." y ninguna "B.".
- "GEO" se usa en todo el paper y nunca se define.
- Fig. 1(b) es un screenshot de PSoC Creator donde **ningún label es legible** a ancho de columna. No aporta nada. Borrarla y poner un esquemático real con valores de componentes (que además es la figura que hace falta para responder A2).

---

## PARTE 2 — LOS TRES PROBLEMAS DE FONDO

### A1. La tesis del paper se auto-refuta en su propia Tabla II. **[DA-1, R1-C3, EIC]**

La tesis, textual: *"Unlike an ADDER-only patch, the method addresses offsets **before and after** the summing node."* Toda la justificación de 4 VDACs sobre el parche solo-ADDER que ya tenían descansa en la palabra **"before"**.

La única etapa "before" es el PGA. Y el PGA no mejora en ninguna placa:

| Placa | Default | Proposed | Factor |
|---|---|---|---|
| A | 110.8 ± 136.8 | 106.9 ± 63.0 | **1.04×** (nada) |
| B | 151.3 ± 86.5 | 132.8 ± **101.8** | 1.14× (y la SD **empeora**) |
| C | 202 | **206** | **0.98×** (peor) |

R1 corrió los tests: Welch **p = 0.96** (A) y **p = 0.77** (B); Cohen's d = 0.037 y 0.196. **Cero evidencia de que la calibración del PGA haga algo.**

**Y la explicación del paper ("correction granularity") no es la correcta.** R1 hizo la aritmética que el paper nunca hizo:

- 1 código VDAC = 4080/255 = **16.0 mV** exactos.
- $K_{PGA}$ a ×16 ≈ 16 → banda muerta $\Delta = \lceil 1.2 \times 16 \rceil = 20$ códigos = **±320 mV** en el nodo.
- Offsets iniciales del PGA: 110.8, 151.3, 202 mV → **6.9, 9.5, 12.6 códigos**.

**Los tres arrancan DENTRO de su propia banda muerta.** El lazo ve $|\varepsilon| < \Delta$, declara convergencia, y **nunca mueve el DAC**. No es una limitación de granularidad del hardware: **el controlador nunca corrió.**

Esto importa mucho porque el remedio que propone el paper (un DAC más fino, ref. [8]) ataca el término equivocado, mientras que el 1.2 de la fórmula es **una constante de firmware, gratis de cambiar.**

→ **Experimento decisivo, una tarde, sin hardware nuevo:** re-correr con $\Delta_i = 1$ forzado y loguear los códigos finales. Si el residuo se estanca en ±128 mV (medio paso de 256 mV), la granularidad *sí* era el límite y la historia del paper queda vindicada. Si baja, **la banda muerta era el límite y la historia del paper es falsa.**

→ Mientras tanto, **quitar** *"identifying correction granularity as the limiting factor on the PGA"* de la lista de contribuciones. Una *identificación* exige excluir las alternativas, y la alternativa principal no solo no está excluida: los propios números la respaldan.

### A2. El paper nunca justifica por qué la cadena está acoplada en DC — y ahí muere si no lo hace. **[DA-2, R2-C2/C3]**

La cadena es PGA → **filtro pasabanda** → ADDER → pasabajos. Un pasabanda con corner inferior no nulo tiene **ganancia DC = 0**. El SM-24 no tiene contenido en DC. Entonces: **¿por qué el offset del PGA llega al ADDER?**

Palabras que **no aparecen** en el manuscrito: *AC coupling, coupling capacitor, high-pass corner, chopper, auto-zero, DC-coupled.*

El único "¿por qué no X?" del paper (Sec. V) es contra la **resta por software** — y eso es un hombre de paja. No dice nada sobre:
- un **capacitor de acoplamiento** entre etapas (centavos, cero calibración, cero 10 s de boot, cero piso de cuantización de 16 mV), ni
- un **amplificador chopper/zero-drift** (offset en µV, < US$1, y corrige offset *y* ruido 1/f simultáneamente).

**Pero probablemente ustedes TIENEN la respuesta y no la escribieron.** La ref. [6] (Ma et al., *"An effective method for improving low-frequency response of geophone"*) es de donde sacan la topología, y es un paper sobre **extender la respuesta en baja frecuencia por debajo del corner del geófono** — lo cual *exige* acoplamiento DC. Si esa es la razón, es la justificación más fuerte que el paper podría dar, y responde la objeción entera.

Ahora mismo [6] se cita en **una sola frase** y no se usa más. No hay un solo Bode, ni una función de transferencia, ni una frecuencia de corte en todo el paper.

→ **Escribir el párrafo "¿Por qué DC-coupled?".** Es la revisión más importante del paper. Un revisor no puede conceder una defensa que los autores no formularon.

### A3. Cero comparaciones medidas contra cualquier alternativa. **[DA-7, EIC-C4, R2-M4]**

El paper rechaza **tres** alternativas y **no midió ninguna**:
1. El parche solo-ADDER: *"is not a separate measured condition"* — y la razón que dan (*"would not expose drift before/after it"*) **es petición de principio**: la hipótesis bajo test es precisamente que el baseline falla. Y en el mismo párrafo admiten que es *"equivalent to calibrating that stage in isolation"* — **o sea que el firmware ya puede hacerlo. Están a un flag de distancia.**
2. El DC servo continuo: rechazado narrativamente, sin un solo número (ni corner, ni settling, ni distorsión medida).
3. AC coupling / chopper: ni mencionados.

La única comparación medida es contra **"Default"** — códigos VDAC nominales fijos, una condición nula que nadie enviaría a producción.

→ **Agregar una tercera columna a la Tabla II: "ADDER-only".** Mismas placas, mismo ×16, mismo N. Un flag de firmware y una sesión de osciloscopio. Es el cambio de mayor valor de toda esta revisión: convierte el *"architectural, not quantitative"* que ustedes mismos confiesan en un resultado cuantitativo duro.

---

## PARTE 3 — REGALOS QUE ESTÁN DEJANDO EN LA MESA

### G1. El titular del paper está en la Tabla II y no lo escribieron. **[DA, EIC-M3]** — **cero trabajo de laboratorio**
Board A, LP, sin calibrar: **−1.99 V** sobre un rango ADC de **±2.5 V**. Quedan 0.51 V de headroom: el nodo estaba al 80% del clipping.
Calibrado: **133.8 mV** → ~2.37 V de headroom.

Eso es **~4.6× (≈2.2 bits) de rango dinámico recuperado**, y la eliminación de un riesgo real de saturación.

Ustedes usaron el −1.99 V **para tranquilizar al lector de que el rango del osciloscopio alcanzaba** (Sec. IV-B). Es el mejor número del paper y lo gastaron en una nota al pie.

→ Columna nueva en la Tabla II: *"% del fondo de escala del ADC consumido por DC, antes → después"*. Y el número al abstract. Es aritmética sobre datos que ya tienen.

### G2. La ecuación (1) es triangular. La escribieron y no la invirtieron. **[R3-O1, DA-11, R1-M2]**
$y_i^{DC} = A_i y_{i-1}^{DC} + b_i + K_i u_i$ — la etapa $i$ depende solo de la $i-1$. Es un **sistema lineal triangular inferior** con solución cerrada. No hacen falta cuatro lazos PI corriendo 10 s; hace falta identificar $A_i, b_i, K_i$ y resolver (dos lecturas de ADC por etapa, < 1 s en total).

Y eso cura de paso el problema que ustedes mismos confiesan: *"$K_i$ is a nominal design value... **not individually measured per board**"* — y después reportan la variación placa-a-placa como hallazgo. **Están usando un modelo nominal de la planta y luego pidiendo disculpas por la varianza que eso produce.** Medir $K_i$ por placa cuesta menos de un segundo.

Corolario que tampoco escribieron: **como Eq. 1 es triangular, corregir en orden de flujo de señal (PGA→BP→ADDER→LP) significa que cuando trimean la etapa $i$, su entrada ya está en cero — el trim es final, sin iteración.** Un barrido greedy hacia adelante es demostrablemente suficiente y óptimo en una pasada. Eso es un resultado transferible a cualquiera con una cascada, en cualquier campo, y lo presentan como si fuera una elección arbitraria de implementación.

### G3. El controlador no es un PI. Es un integrador. **[R1-M2]**
Contribución máxima del término proporcional, para el **mayor error que el ADC puede representar** ($\varepsilon_{max}$ = 156 códigos):

| Etapa | $k_p/|K_i|$ | Aporte P máximo |
|---|---|---|
| BP | 5.0e-5 | **0.0078 códigos** |
| ADDER | 1.27e-5 | **0.0020 códigos** |
| LP | 1.67e-5 | **0.0026 códigos** |
| PGA | 6.25e-5 | **0.0098 códigos** |

**El término P nunca puede aportar ni el 1% de un LSB del DAC, en ninguna etapa, para ningún error físicamente alcanzable.** El lazo es un integrador puro con $\tau = 1/(k_i f_s) = 0.77$ s.

Describirlo como *"a gain-aware PI controller using deadband, anti-windup, slew limiting, stability detection, and one-LSB refinement"* sobrevende lo que realmente corre. → O arreglan $k_p$ (un valor plausible es 0.1–1) y re-miden, o lo llaman por su nombre.

---

## PARTE 4 — EL PROBLEMA QUE NADIE ESPERABA (y que puede ser un hallazgo)

**Cinco celdas de la Tabla II están FUERA de la banda muerta del propio lazo.** [R1-C2, DA-8]

Un lazo convergido **no puede** dejar un residuo mayor que su banda muerta. Sin embargo:

| Celda | Proposed | Banda muerta | |
|---|---|---|---|
| A BP | +107.1 mV | ±48 mV | **2.2× afuera** |
| B BP | +87.6 mV | ±48 mV | 1.8× afuera |
| C BP | +213 mV | ±48 mV | **4.4× afuera** |
| B LP | +289.0 mV | ±128 mV | **2.3× afuera** |

Y hay una segunda pista: **todos** los residuos de BP y LP, en las tres placas, son **positivos**.

La explicación más probable (y la señaló el DA independientemente): **el lazo lleva a cero lo que el ADC VE, no lo que la etapa ES.** El camino de observación (MOSFET del mux, capacitor conmutado, offset del ADC) es común a las cuatro etapas y se resta de todas por igual. Por construcción, el lazo deja cada nodo en −(offset del camino de observación).

Lo irónico: **la ref. [7] que ustedes citan (AN68403) "measures the system offset with grounded inputs"** — el procedimiento exacto que acotaría este término. **Citan el remedio y no lo aplican.**

→ Aterrizar la entrada del mux, medir el offset del camino de observación, restarlo de $r_i$. **30 minutos.** Si es ~60 mV, esto explica la tabla entera y **deja de ser un defecto para convertirse en un hallazgo publicable.**

---

## ROADMAP DE REVISIÓN — ordenado por (valor / esfuerzo)

### Cero laboratorio (una tarde de escritorio)
1. **Borrar todos los `(falta medir)`** y el rojo. Decidir: Board C completo, o dos placas. *(bloqueante)*
2. **Arreglar la contradicción "maximum PGA gain" ↔ ×16.** Después hacer grep de las 4 apariciones de la ganancia y verificar que coinciden. *(bloqueante)*
3. **Escribir el párrafo "¿Por qué DC-coupled?"**, anclado en [6]. *(la revisión más importante del paper)*
4. **Poner $\Delta_i$ y el paso de corrección en mV en la Tabla I.** Ahora mismo *ninguna* afirmación de granularidad del paper es verificable. Esto las hace falsables — que es el punto.
5. **Columna de headroom recuperado en la Tabla II** + el número al abstract (G1).
6. **Correr los tests estadísticos** que R1 ya corrió: 5 de 6 comparaciones BP/ADDER/LP dan p < 0.05 con d de 1 a 28. **El resultado central del paper es defendible estadísticamente y ustedes no lo defendieron.**
7. Citar el canon: **Enz & Temes (Proc. IEEE, 1996)** sobre autozero/CDS/chopper; la literatura de *digitally-assisted analog* (titulan una sección con el término de arte del subcampo y no citan nada de él); y las alternativas AC-coupling / zero-drift op-amp.
8. Reconciliar los tiempos: típico (~7 s, de la Fig. 3) **y** peor caso (57.6 s, suma de la Tabla I), por separado.
9. Quitar *"controller-independent"* de las contribuciones (un solo controlador probado) o degradarlo a propiedad de diseño.
10. Borrar Fig. 1(b). Reemplazar Fig. 2 por pseudocódigo de 12 líneas (más chico, legible y más reproducible).

### Una tarde de banco
11. **Medir la condición ADDER-only** → tercera columna de la Tabla II. *(la que convierte "architectural" en "quantitative")*
12. **Medir el offset del camino de observación** con la entrada aterrizada (Parte 4). 30 minutos.
13. **Re-correr con $\Delta_i = 1$** forzado → resuelve de una vez si el PGA falla por granularidad o por banda muerta (A1).
14. **Medir $K_i$ por placa** (un paso de DAC, una lectura de ADC, por etapa). Elimina el confounder del que ustedes mismos se disculpan.
15. **Correr a ×50**, calibrado vs. sin calibrar. Si un nodo intermedio satura sin calibración y no satura con ella, **la tesis del paper queda probada en una figura**. Es la piedra angular que falta.
16. **Piso de ruido**: reemplazar el geófono por una resistencia de ~375 Ω, loguear 60 s, FFT. Reportar con VDACs activos vs. apagados. **Están inyectando cuatro salidas de DAC delante de ganancias grandes y nunca miraron si eso empeora el SNR.** Es lo primero que pregunta cualquier revisor analógico, y decide si yo desplegaría esto.

### Media mañana de campo
17. **Misma línea, mismo tiro, calibración on/off, intercalado (ABABAB).** Reportar la **imagen de dispersión** de cada condición, lado a lado. Eso es el producto de MASW. A nadie en geofísica le importan los milivoltios; les importa si pueden pickear una curva de dispersión. Ustedes tienen las placas, la línea, el martillo y un flag de firmware — y escribieron una frase explicando por qué no lo hicieron.

### Cosas que hay que decidir, no medir
18. **"Low-Cost" está en el título y no hay un solo número de costo en el paper.** O ponen un BOM por canal y lo comparan contra [3] y contra un nodo comercial, o **sacan "Low-Cost" del título**. No hay tercera opción.
19. Estado de "no convergió": el flag existe y no va a ningún lado. Propagarlo al header de la traza (SEG-2/SEG-Y) y a un LED. Un canal railado en una línea de 24 no pierde una traza: **corrompe la imagen de dispersión construida con todas**.

---

## LO QUE NO HAY QUE CASTIGAR (para que no sobre-corrijan)

El DA los revisó explícitamente y los mantiene:

- **Reportaron el resultado que los perjudica** (Board C PGA 202 → 206). Muchos autores habrían borrado la fila. Eso es reporte honesto de resultado negativo y merece crédito, no castigo. **Que sobreviva a la revisión.**
- **La banda muerta $\lceil 1.2|K_i|\rceil$ es un criterio principiado**, no un fudge: es un paso de DAC referido al nodo más 20% de margen. El DA intentó llamarla arbitraria y al calcularla la retiró.
- **Congelar el lazo antes de adquirir es una ventaja estructural real** (sin polos extra, sin realimentación variante en el tiempo en la señal). No necesita medición para creerse.
- **El diseño del registro EEPROM** (hardware class, gain code, valid-stage mask, versión, CRC; *"a failed run never overwrites a valid one"*) es buena práctica defensiva de embebidos.
- **La normalización $1/|K_i|$ de la Eq. (3) es correcta y no es obvia**: hace que el ancho de banda del lazo sea idéntico en etapas de ganancias muy distintas. **No se están llevando suficiente crédito por eso.**
- **El `(falta medir)` es casi con certeza un fallo de edición, no fabricación** — el caption declara N=1 para Board C de forma independiente y correcta. Tratarlo como fallo de preparación del manuscrito, descalificante pero trivial de arreglar. **No como mala conducta.**

---

## EL PÁRRAFO QUE TIENEN QUE ESCRIBIR

El DA construyó la mejor defensa honesta que ustedes pueden dar, y su veredicto fue: **es fuerte y probablemente verdadera — y no está en el paper.**

> *"El front end está acoplado en DC deliberadamente. Deriva de Ma et al. [6], cuyo propósito declarado es extender la respuesta del geófono **por debajo** de su corner mecánico; un capacitor de acoplamiento que bloquee el offset del PGA tendría que ubicarse muy por debajo de 1 Hz para preservar esa extensión, lo que en una placa de bajo costo significa un electrolítico grande en el camino de señal — fugas, tolerancia, tempco, microfonía — precisamente la clase de componente analógico de precisión que la tesis de un-solo-chip existe para eliminar. Los op-amps internos del PSoC no son choppers y no se pueden cambiar; [5] documenta exactamente este tradeoff. Agregar un chopper externo derrota la premisa de un solo chip. Dada una cadena acoplada en DC y amplificadores no seleccionables, el trim por etapa es la única palanca que queda — y el mux, el ADC y los VDACs ya están en el die, así que es gratis."*

Escriban eso y la objeción más fuerte contra el paper queda desactivada. **Pero no rescata al manuscrito tal como está** — no responde por qué cuatro DACs cuando los datos soportan dos, ni por qué el PGA sigue en la lista de contribuciones si no corrige nada, ni por qué la Introducción afirma un experimento que los Métodos niegan, ni por qué un tercio de la tabla dice "falta medir".

**La idea sobrevive. El manuscrito no.** Todo lo que hace falta está al alcance del hardware que ya tienen sobre la mesa.
