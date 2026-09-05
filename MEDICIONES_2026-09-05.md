# Registro del 2026-09-05

Continuación de `MEDICIONES_2026-09-04.md`. Banco: **ESP esclavo en COM8**
(cambió de COM7; sólo hay un ESP conectado, el maestro está desenchufado por
pedido de Elías), PSoC con firmware de autotest, **geófono conectado a la
entrada** desde el mediodía.

---

## 1. El grabado del PSoC por PPCLI funciona — queda cerrado

Estaba mal diagnosticado desde el 2026-09-02. `program_psoc.ps1` **graba y el
chip arranca**.

**Cómo se comprobó.** Se grabó el mismo HEX que ya estaba en el chip (proyecto
de autotest, `-SkipBuild`), o sea sin cambio funcional, para que el experimento
midiera sólo el camino de grabado:

| paso | resultado |
|---|---|
| `PSoC3_EraseAll` | `0 OK` |
| 272 filas `ProgramRowFromHex`/`VerifyRowFromHex` con ECC (`0x01`) | todas `0 OK`, `verResult = 1` |
| `ProtectAll`, `VerifyProtect`, `DAP_ReleaseChip`, `ClosePort` | `0 OK` |
| **después**: `taps` por I2C | 1001,3 / 1001,5 / 1001,5 / 1000,8 mV |
| **después**: autotest completo | 22 PASS, 3 FAIL conocidos, 1 WARN, 83,9 s — idéntico a antes |

**Qué era en realidad.** Lo que dejaba el chip muerto era grabar las **1024
filas** (`-AllRows`), no la ausencia de PSoC Creator. El culpable era grabar de
más, no de menos.

**Por qué alcanza con las filas ocupadas.** El `.cydwr` tiene
`CYDEV_CONFIGURATION_ECC=True` con `CYDEV_ECC_ENABLE=False`: la configuración
del fabric va al espacio ECC. Parseando el HEX, esa configuración es no nula
**sólo en las filas 0..150** (región `0x80000000`, 32 B por fila). El código
ocupa 264 filas y el script graba 272: cubre las dos cosas con margen.

**Hipótesis descartada.** Se sospechaba que faltaba escribir las NV latches.
No es eso: `EraseAll` no las borra, `PSoC3_GetEccStatus` sobre el chip da `0`,
coherente con el HEX (`nvlUserSize=4`, user `00 00 40 05`) y con
`CYDEV_ECC_ENABLE=False`. `PSoC3_ReadNvlArray` falla con `0x80004005` y por eso
no se pueden comparar de frente, pero `PSoC3_WriteNvlArray` existe si alguna vez
hiciera falta.

**Control adicional:** `DAP_Acquire` + `DAP_ReleaseChip` **sin** grabar no
perturba al PSoC — sigue contestando. O sea que el problema nunca estuvo en
adquirir el chip.

**Consecuencia:** se puede iterar firmware sin intervención de Elías.

**Trampa:** el nombre del KitProg cambia entre sesiones (`CMSIS-DAP/236111` el
2026-07, `CMSIS-DAP/246475` hoy). El script lo autodetecta.

---

## 2. Temperatura por ubicación: sirve, y el rango es peor de lo supuesto

Open-Meteo con las coordenadas del nodo (25°20'19,4"S 57°36'57,8"W), sin API key
ni credenciales. Al mediodía del 2026-09-05: **19,0 °C**, 58 % HR.

| día | mín | máx |
|---|---:|---:|
| 2026-09-05 | 16,2 | 19,0 |
| 2026-09-06 | 11,5 | 17,6 |
| **2026-09-07** | **8,1** | 19,3 |
| 2026-09-08 | 10,9 | 24,8 |
| 2026-09-09 | 16,5 | 25,1 |
| 2026-09-10 | 18,6 | 25,1 |
| **2026-09-11** | 17,1 | **31,6** |

**De 8,1 a 31,6 °C en la misma semana**, sobre un electrolítico de 680 µF. Una
espera de planta fija dimensionada con el τ de banco (29,5 s a ~19 °C) no cubre
eso. Decisión de Elías, y es la correcta: **no corregir por temperatura**, sino
**medir τ en el propio nodo** y dimensionar la espera con lo medido. La
temperatura queda como explicación del fenómeno, no como entrada del algoritmo.

---

## 3. El geófono está conectado, y a ×1 eso es indetectable

El indicador D6b del autotest (RMS de ch0 a ganancia ×1) **no sirve** para
decidir si hay geófono: con la entrada abierta daba RMS 19 µV / pp 228 µV, y con
el geófono puesto da RMS 19 µV / pp 171 µV. Es el piso del ADC en los dos casos.

Subiendo la ganancia del PGA de entrada aparece la diferencia (n_sel=3):

| código | ganancia | media ch0 | RMS | pp |
|---:|---|---:|---:|---:|
| 0 | ×1 | 1000,69 mV | 19 µV | 171 µV |
| 3 | ×8 | 994,63 mV | 114 µV | 801 µV |
| 6 | ×32 | 973,24 mV | 1163 µV | 5607 µV |
| 8 | ×50 | 951,16 mV | 4024 µV | 18539 µV |

El RMS crece **más rápido que la ganancia** (de ×8 a ×32 la ganancia sube 4× y
el RMS sube 10,2×), o sea que a partir de ×8 deja de mandar el piso del ADC y
empieza a mandar el ruido de la entrada. Referido a la entrada, a ×50 son 80 µV
RMS: eso es varios órdenes por encima del ruido térmico de una bobina de 375 Ω,
así que **es movimiento del terreno real**, no ruido eléctrico. El geófono
está y está midiendo.

**Corolario para el autotest:** D6b hay que medirlo a ganancia alta, no a ×1.
Como está hoy da lo mismo con y sin geófono y da una falsa sensación de control.

---

## 4. PRIMER RESULTADO DURO: el PGA de entrada no se puede autocorregir por encima de ~×16

La media de ch0 baja monótonamente con la ganancia. Referida a la entrada, es
una sola constante:

| ganancia | corrimiento de ch0 | referido a la entrada |
|---|---:|---:|
| ×8 | −6,06 mV | 0,76 mV |
| ×32 | −27,45 mV | 0,86 mV |
| ×50 | −49,53 mV | 0,99 mV |

O sea un **offset referido a la entrada de ~0,9 mV**, que es del PGA (con el
geófono la entrada es un corto en continua). Ese offset se multiplica por la
ganancia antes de que ninguna etapa pueda tocarlo.

### CUIDADO: la conclusión de esta sección depende de un dato que todavía no está medido

Escribí primero que esto probaba que el PGA no se puede autocorregir arriba de
×16, razonando contra los **±15,6 mV** de autoridad medidos el 2026-09-04
(61,2 µV/código × 255). **Ese razonamiento puede ser falso**, y la falla es mía:
la matriz del 2026-09-04 se tomó **entera a PGA ×1**, así que no puede distinguir
dónde inyecta el IDAC de la etapa 0.

Hay dos posibilidades y dan conclusiones **opuestas**:

| dónde inyecta el IDAC del PGA | pendiente esperada en ch0 | autoridad a ×50 | ¿se autocorrige? |
|---|---|---:|---|
| **después** de la amplificación | 61,2 µV/cód, constante | ±15,6 mV | **no**, por 3,2× |
| **antes** (o sea en la entrada) | 61,2·g µV/cód | ±780 mV | **sí**, con 17× de margen |

Y hay un indicio fuerte a favor de la segunda: `cal_pi_stage_gain_x1000()` del
firmware **multiplica** la ganancia de la etapa 0 por la del PGA, o sea que
quien escribió el lazo asumió que la autoridad escala. Si eso está bien, el
offset y la autoridad crecen juntos y su razón es **constante**, así que ×50 no
tiene ningún problema de autoridad.

**Lo decide una sola medición**, que ya está encolada (EXP1): barrer el IDAC de
la etapa 0 a varias ganancias del PGA y mirar la pendiente de ch0. `ch0` está
antes de C1 y su propio tap no tiene transitorio (`G_TRANS[0][0] = 0` medido),
así que sale rápido.

**Lo que sí queda establecido sin depender de eso**, porque es medición directa:
el PGA tiene ~1,0 mV de offset referido a la entrada, y a ×50 eso son 49,5 mV de
corrimiento en su tap. Si ese corrimiento se puede anular o no es lo que decide
EXP1.

### EXP1: medido, y la respuesta es la segunda — mi conclusión era falsa

**Método.** Barrido del IDAC de la etapa 0 en todo su rango, midiendo ch0, a
cinco ganancias del PGA. Once puntos por ganancia. `ch0` está antes de C1 y su
propio tap no tiene transitorio (`G_TRANS[0][0] = 0`), así que no necesita
espera de planta. Crudos: `lab/planta/curva_e0_pga*_out0_2026090514*.json`

Pendiente en la zona lineal:

| ganancia del PGA | µV por código | razón contra ×1 |
|---|---:|---:|
| ×1 | 61,97 | 1,0 |
| ×8 | 460,5 | 7,4 |
| ×16 | 927,5 | 15,0 |
| ×32 | 1774 | 28,6 |
| ×50 | 2688 | 43,4 |

**La autoridad escala con la ganancia.** El IDAC de la etapa 0 inyecta **antes**
de la amplificación, y por lo tanto el offset de entrada y la autoridad para
corregirlo crecen **juntos**: su razón es constante.

**Consecuencias:**

1. **Mi conclusión anterior era falsa** y la retiro. El PGA se puede
   autocorregir a cualquier ganancia. En números: a ×50 el offset a anular son
   49,5 mV, que a 2688 µV/código son **16 códigos**. Y de hecho se ve directo en
   el dato: a ×50 el código 0 deja ch0 en 957,6 mV, y hacen falta ~16 códigos
   para llevarlo a 1000.
2. **El firmware tenía razón.** `cal_pi_stage_gain_x1000()` multiplica la
   ganancia de la etapa 0 por la del PGA, y eso es correcto. No hay que tocarlo.
3. **El plan de Elías de fijar la entrada en ×50 es viable** desde el punto de
   vista de la autoridad de calibración.

### Pero aparece el límite verdadero: el riel, no la autoridad

Los mismos barridos muestran dónde se termina el rango útil, y no es donde se
acaban los códigos:

| ganancia | riel bajo | riel alto | códigos útiles (de ±255) |
|---|---:|---:|---:|
| ×1 | no llega | no llega | **los 510** |
| ×8 | ~−230 | no llega | ~480 |
| ×16 | −153 | +204 | ~355 |
| ×32 | −51 | +102 | ~150 |
| ×50 | −51 | +102 | **~140** |

A ×50 el tap se pega en **759,4 mV** por abajo y **1114,4 mV** por arriba, y
entre esos dos rieles hay 355 mV, o sea unos 132 códigos a 2688 µV cada uno. Las
otras dos terceras partes del rango del IDAC **no existen**: son riel.

Como el offset a corregir son 16 códigos y hay ~66 de cada lado, **alcanza con
holgura**. Pero el lazo tiene que saber que no puede pasar de ahí: contra el
riel la pendiente es cero, el control empuja sin efecto y la integral se enrolla
hasta el extremo. **El clamp del IDAC de la etapa 0 tiene que escalar con
1/ganancia**, y hoy es fijo en ±255.

### Un dato de hardware que sale de acá y sirve para todo lo demás

Los tres taps medidos coinciden: la excursión útil es de **371 a 376 mV**,
centrada en **~935 mV y no en los 1000 mV del objetivo**.

| tap | riel bajo | riel alto | excursión |
|---|---:|---:|---:|
| ch0 PGA | 759,4 | 1114,4 | 355,0 mV |
| ch2 ADDER | 750,8 | 1121,6 | 370,8 mV |
| ch3 LP | 746,4 | 1122,3 | 375,9 mV |

O sea que la cadena tiene **250 mV de margen para abajo y sólo 122 mV para
arriba**. Es **asimétrica**, y eso importa: un offset positivo choca contra el
riel al doble de velocidad que uno negativo. El objetivo de 1000 mV está mal
centrado respecto de la excursión real; centrarlo en ~935 mV daría **±186 mV
simétricos en vez de +122/−250**, o sea 52 % más de margen del lado que hoy es
crítico. Es un cambio de una constante y hay que evaluarlo.

**Ojo, esto NO significa que ×50 sea inviable.** El requisito real es que la
cadena no sature y que LPo quede chico, no que todos los taps estén en cero: con
±2,5 V de excursión, 49,5 mV de corrimiento en el PGA no satura nada. Lo que
significa es que **la corrección hay que delegarla aguas abajo**, que es
justamente lo que habilita la matriz de acople (PGA→LP son 1026 µV/código, o
sea que el LP tiene autoridad de sobra sobre el desvío que dejó el PGA). Es
exactamente la optimización conjunta ponderada que pidió Elías: no minimizar
cada etapa por separado, sino el conjunto.

**Falta medir:** si a ×50 el PGA de entrada, más el PGAout, dejan el ADDER o el
LP fuera de su rango útil. Ése es el límite que decide la configuración de campo.

---

## 5. Estrategias de calibración comparadas en el modelo

**Advertencia de alcance.** Esto es **simulación**, no medición. El modelo está
calibrado contra la placa (matriz de acople del 2026-09-04, ruido de 1,5
cuentas, offsets medidos), pero sus predicciones **a ganancia alta dependen de
un dato que todavía no está medido** — dónde inyecta el IDAC del PGA, ver el
recuadro de §4. Las conclusiones de ganancia baja y media sí son de fiar; las de
ganancia alta hay que releerlas cuando esté EXP1.

### El problema del lazo actual

El lazo secuencial cierra una etapa por vez, en orden, llevando cada tap a cero.
Eso sería óptimo si las etapas fueran independientes, y **no lo son**: mover el
ADDER corre la salida del LP 4,04 veces más que la referencia del propio LP.
Llevar el ADDER exactamente a cero puede ser la peor decisión posible para el
LP, que es el tap que se captura. Aceptar unos milivoltios en el ADDER para que
al LP le sobre autoridad es un intercambio que el lazo secuencial **no puede
hacer**, porque cuando cierra el ADDER todavía no sabe qué le va a pasar al LP.

Y encima paga **una espera de planta por etapa**: con 2 τ son cuatro esperas,
236 s sólo de espera.

### La idea de Elías, formalizada

Su pedido fue: minimizar todas las etapas a la vez, "dando más peso a las que
tengan más ganancia acumulada porque son las que más probablemente saturen".
Eso es exactamente un problema de mínimos cuadrados ponderado con cajón:

> minimizar `J(d) = Σ_j w_j · ( off_j + Σ_k G[k][j]·d_k )²` con `|d_k| ≤ límite_k`

donde `G` es la matriz de acople **medida** y `w_j` el cuadrado de la ganancia
acumulada hasta el tap `j`. El peso al cuadrado no es arbitrario: lo que decide
si un tap satura es `offset + excursión de señal` contra el riel, y la excursión
en el tap `j` es proporcional a su ganancia acumulada, así que el presupuesto de
offset tiene que ser inversamente proporcional a ella. Penalizar con el cuadrado
es exactamente eso en mínimos cuadrados.

Son cuatro variables enteras y una forma cuadrática convexa: se resuelve con
descenso por coordenadas en unas pocas pasadas, con enteros de 64 bits, sin
matrices ni divisiones raras. Entra en el PSoC sin drama.

### Resultado, promediando 12 semillas por celda

Espera de planta 2 τ, Ki = 1/16. `LP` es el error asentado del tap que se
captura; `peor` es el peor de los cuatro taps; `t` el tiempo total.

| PGA × out | secuencial (hoy) | conjunta 1 iter | conjunta 3 iter, esperas cortas |
|---|---|---|---|
| | LP / peor / t | LP / peor / t | LP / peor / t |
| 1×1 | 0,21 / 0,6 / **237 s** | 0,47 / 1,2 / 118 s | **0,10 / 1,2 / 104 s** |
| 8×8 | **20,66** / 20,7 / 257 s | 6,08 / 15,4 / 118 s | **9,65 / 14,0 / 104 s** |
| 50×1 | 214,1 / 214,1 / 76 s | 4,01 / 51,7 / 118 s | 16,63 / 52,2 / 104 s |
| 1×50 | 91,3 / 91,3 / 256 s | 7,75 / 26,7 / 118 s | 10,68 / 28,8 / 104 s |

**Dos cosas que importan:**

1. **El lazo de hoy no cumple el criterio en 8×8**: da 20,66 mV contra el techo
   de 20 mV que fijó Elías, y tarda 257 s en no cumplirlo. La conjunta da
   9,65 mV en 104 s. **Menos de la mitad del tiempo y menos de la mitad del
   error.**
2. **El tiempo sale de hacer menos esperas de planta, no de esperar menos.** El
   secuencial paga cuatro esperas porque cada etapa perturba a la siguiente. La
   conjunta mueve las cuatro juntas y paga una por iteración; y como a partir de
   la segunda las correcciones son chicas —y la amplitud del transitorio es
   proporcional al salto del DAC— esas iteraciones se pueden pagar con 0,5 τ en
   vez de 2 τ. De ahí salen los 104 s.

### Resultado NEGATIVO, que también hay que registrar

Probé la variante más conservadora, que es la que más se parecía al pedido de
Elías de "preprocesar un valor y después hacer correcciones pequeñas": aplicar
el óptimo conjunto como **feed-forward** y después dejar correr el lazo
secuencial de siempre para refinar. **No funciona.** En 50×1 da 241 mV, contra
los 4,01 mV de la conjunta sola, o sea que queda **peor que no hacer nada**.

La razón es clara y conviene tenerla escrita: **el lazo deshace la
optimización**. Su objetivo es llevar cada tap a cero de a uno, y eso contradice
punto por punto el compromiso ponderado que acababa de calcularse. No se puede
anteponer el optimizador al lazo existente: hay que **cambiarle el objetivo al
lazo**, de "cada tap a cero" a "cada tap a su valor del óptimo conjunto".

Es un buen ejemplo de por qué convenía simularlo antes de escribirlo en C: la
versión intuitivamente más segura era la peor de las tres.

---

## 6. EL ADDER: contestado, y de paso una corrección a la matriz del 2026-09-04

**Método.** Barrido del IDAC del ADDER en todo su rango (−255…+255, paso 24)
midiendo **los cuatro taps** con **60 s de espera de planta por punto**. Ésa es
la diferencia con la medición del 04, que miraba sólo el tap propio: para saber
si la zona plana es recorte del tap o muerte del camino de señal hay que mirar
**aguas abajo**. Crudo: `lab/planta/curva_e2_pga0_out0_20260905_133508.json`

### 6.1 La respuesta: es saturación real, y la tabla no sirve

| código ADDER | ch2 (tap propio) | ch3 (LP) |
|---:|---:|---:|
| −255 … −183 | **750,8 mV, fijo** | **1122,3 mV, fijo** |
| −159 | 757,5 | 1122,4 |
| −135 | 805,8 | 1122,4 |
| −87 | 898,4 | 1122,4 |
| −39 | 971,4 | 1122,4 |
| −15 | 989,8 | 1054,6 |
| +9 | 1007,9 | 962,8 |
| +33 | 1026,0 | **746,4** |
| +57 | 1043,9 | 746,3 |
| +153 | 1115,2 | 746,4 |
| +177 … +249 | **1121,6, fijo** | 746,4 |

**En los extremos las DOS etapas están contra el riel al mismo tiempo.** Con el
IDAC en −255, ch2 está pegado en 750,8 mV y ch3 en 1122,3 mV, y ninguno de los
dos se mueve al cambiar el código. Eso no es una no linealidad —una pendiente
que varía pero no se anula, como la del LP— sino **saturación**: el camino de
señal está muerto ahí.

**Conclusión, y contesta la pregunta 3 de Elías:** la propuesta de modelar el
ADDER con tablas para usar el rango completo **hay que descartarla**. Una tabla
puede invertir una función monótona de pendiente variable; no puede devolver
autoridad donde la pendiente es cero. Y peor: al invertir una zona plana, la
ganancia estimada del lazo se va a infinito, o sea que la tabla no sólo no
ayudaría sino que **rompería** el control.

Excursión medida de cada tap, que es el dato de hardware que hay detrás:
**ch2 = 370,8 mV** (750,8 a 1121,6) y **ch3 = 375,9 mV** (746,4 a 1122,3).

### 6.2 Lo que sí importa, y es mucho peor de lo que creíamos

Mirando **ch3** en vez de ch2 aparece el problema real:

> **Para códigos del ADDER de −255 a −15, la salida del LP está pegada al
> riel.** El LP sólo está dentro de rango en una ventana de unos **48 códigos**,
> aproximadamente −15 … +33.

O sea que el rango útil del IDAC del ADDER **no es ±178 ni ±128: es ±25 códigos
alrededor del punto donde el LP queda centrado**. Todo lo demás es riel del LP,
aunque el propio ADDER siga respondiendo perfectamente en su tap.

El IDAC del LP puede correr esa ventana, pero poco: su autoridad es
525 µV/cód × 255 = ±134 mV, y el ADDER le mete 3825 µV/cód. O sea que el LP
compensa **±35 códigos de ADDER**, y la ventana útil total queda en unos
**−50 … +68**.

### 6.3 La corrección: el acople ADDER→LP estaba subestimado por 1,8×

En la zona donde el LP **no** está saturado hay dos puntos limpios:

| código | ch3 |
|---:|---:|
| −15 | 1054,611 mV |
| +9 | 962,848 mV |

Pendiente: **3823 µV/código**. La matriz del 2026-09-04 dice **2120,9**.

**Por qué el número viejo estaba mal, y es un error instructivo.** Aquella
medición usó un escalón de **+120 códigos** desde 0. Con la pendiente real,
120 códigos son 459 mV, y el LP sólo tiene 376 mV de excursión: **el escalón
metió al LP contra el riel**. La exponencial se ajustó entonces sobre una
respuesta recortada, y el `y_inf` que salió es el riel, no el régimen. De ahí
sale un 2121 que es un promedio entre la parte lineal y la parte muerta.

Es el mismo error que se cometió el 2026-09-03 midiendo con la cadena saturada,
y vuelve a aparecer por la misma causa: **el escalón de prueba era más grande
que el rango lineal de la etapa afectada.**

**Consecuencia sobre la conclusión de fondo:** el acople ADDER→LP no es 4,04
veces la autoridad propia del LP, es **7,3 veces** (3823/525). El problema que
Elías identificó como "la decisión de fondo" es todavía más severo de lo que
decía el documento del 04.

**Pendiente:** volver a medir la fila del ADDER con un escalón **chico** (±10
códigos), que es el único que se queda dentro del rango lineal del LP. Lo mismo
vale para revisar si otras filas de la matriz están contaminadas por el mismo
efecto.

### 6.4 Dos fallas de instrumentación que hay que arreglar

- **`FALLO set_idac` en los códigos −111 y +105**, o sea 2 de 22 puntos
  perdidos. No es aleatorio en el valor: hay que ver si es un plazo corto en el
  enlace o un caso de borde del comando.
- **En el código +81, ch3 informó `0,000 mV`**, que es físicamente imposible con
  el resto de la curva pegada al riel. Es una medida fallida que se guardó como
  si fuera válida. Un cero silencioso es la peor forma de fallar, porque un
  ajuste posterior lo toma como dato bueno. Hay que hacer que se descarte.

---

## 7. Automedición de τ: el estimador barato sirve, pero sólo en un par bien elegido

**Por qué hace falta.** Elías decidió que el nodo no corrija por temperatura sino
que **mida su propio τ** y dimensione la espera con eso. Ese estimador tiene que
correr en el PSoC, en enteros, sin guardar cientos de muestras.

**El estimador.** Con `y(t) = y_inf + A·e^(−t/τ)`, tres muestras alcanzan:

```
r = ( y(2t₁) − y(0) ) / ( y(t₁) − y(0) )  =  1 + e^(−t₁/τ)
τ = t₁ / ( −ln(r − 1) )
```

Lo valioso es que **`y_inf` se cancela**: no hay que esperar a que la planta se
asiente para estimar cuánto tarda en asentarse. En el PSoC el logaritmo sale de
una tabla de 16 entradas.

**Validación.** Se aplicó a las series del escalón del 2026-09-04, que tienen
~500 puntos y un ajuste exponencial completo por mínimos cuadrados como
referencia. Programa: `src/interfaces/python/validar_estimador_tau.py`

Error relativo contra el ajuste completo, sobre **todos** los pares:

| t₁ | n | error medio | peor |
|---:|---:|---:|---:|
| 7,5 s | 11 | 90,0 % | 275 % |
| 15 s | 16 | 68,2 % | 303 % |
| 20 s | 15 | 34,8 % | 94 % |
| 30 s | 16 | 45,8 % | 247 % |
| 45 s | 16 | 22,5 % | 283 % |

**Visto así, el estimador parece inservible. No lo es: lo que pasa es que el
promedio mezcla pares con señal fuerte y pares con señal despreciable.**

Separando, con t₁ = 45 s:

| par (etapa → tap) | τ del ajuste | τ del estimador | error |
|---|---:|---:|---:|
| **1 → ch2** (ida) | 26,4 s | 27,1 s | **2,7 %** |
| **1 → ch2** (vuelta) | 29,1 s | 29,3 s | **0,7 %** |
| 2 → ch1 | 28,2 s | 28,1 s | 0,4 % |
| 1 → ch1 | 29,1 s | 33,1 s | 14 % |
| 2 → ch3 | 32,2 s | 35,6 s | 11 % |

**Decisión: medir τ con el par etapa 1 (Vref_BP) → ch2 (tap del ADDER) y
t₁ = 45 s.** Es el par con mayor relación señal-ruido de la matriz —su respuesta
tiene `G_TRANS = −861` contra `G_DC = −388`, o sea que el transitorio es más
grande que el régimen— y da 0,7 % y 2,7 % en dos ensayos independientes. La
medición completa tarda 90 s y se hace una vez por sesión, no en cada
calibración.

**Lo que NO hay que hacer:** promediar el estimador sobre varios pares. Los pares
de señal débil no aportan información y ensucian el resultado; el promedio de las
tablas de arriba es la prueba.

**Pendiente:** verificar el estimador contra una medición hecha hoy, a la
temperatura de hoy, y no sólo contra los datos del 04.

---

## 8. La calibración conjunta contra la placa real: falla, y por una razón concreta

**Método.** `src/interfaces/python/calibrar_pc.py` corre el algoritmo completo
desde la PC contra la placa: mide los cuatro taps, resuelve el óptimo ponderado,
aplica los cuatro IDAC, espera y repite. Es exactamente lo que haría el firmware,
pero observable paso a paso y sin regrabar nada.

**Primera corrida, PGA ×8 y PGAout ×8** (`* ` marca tap contra el riel):

| iteración | ch0 | ch1 | ch2 | ch3 | DAC aplicado |
|---|---:|---:|---:|---:|---|
| 0 (reposo) | 994,8 | 1001,3 | **1121,5\*** | **746,4\*** | [0, 0, 0, 0] |
| 1 | 1011,1 | 995,8 | **1121,2\*** | **746,0\*** | [35, 32, 11, −20] |
| 2 | 1024,1 | 991,8 | **750,0\*** | **1121,7\*** | [64, 40, 7, −22] |
| final | — | — | — | — | LP +122,1 mV, **NO CUMPLE** |

**El algoritmo saltó de un riel al otro.** Entre la iteración 1 y la 2, ch2 pasó
de 1121 a 750, o sea **371 mV**, cuando la matriz predecía **59 mV** para ese
cambio de códigos. Un factor de **6,3×**.

### La causa: la matriz está mal escalada, y el error es mío

La matriz de acople se midió el 2026-09-04 **entera con PGA ×1 y PGAout ×1**. Al
corregirla con EXP1 escalé la fila 0 por la ganancia del PGA, que es lo que EXP1
demostró. Pero **no escalé nada por PGAout**, y la placa dice que hay que
hacerlo: los IDAC de las etapas de aguas arriba inyectan **antes** de PGAout, así
que su efecto sobre ch2 y ch3 se amplifica también por esa ganancia.

Con PGAout ×8 el factor que falta es del orden de 8, y el observado es 6,3. Es
consistente.

### Y hay un hecho más duro todavía

**Con PGAout en ×2 o más, la cadena arranca contra el riel con los IDAC en cero.**
Esto sí está medido con espera de planta correcta (60 s), en la campaña:

| PGA | PGAout | ch0 | ch1 | ch2 | ch3 |
|---|---|---:|---:|---:|---:|
| ×1 | ×1 | 1000,7 | 999,9 | 1004,1 | 984,6 |
| ×1 | **×2** | 1001,1 | 996,4 | **1121,5 riel** | **746,4 riel** |
| ×2 | ×1 | 999,7 | 1000,8 | 1003,7 | 985,7 |
| ×50 | ×1 | 958,4 | 1010,1 | **1121,8 riel** | **746,6 riel** |

O sea que **PGAout ×2 rieliza y PGA ×2 no**. De las 12 combinaciones de la
campaña, 10 arrancan en riel.

### AVISO: las mediciones rápidas que siguieron a esto NO son válidas

Después de lo anterior corrí varios barridos con 2,5–3 s de espera por punto para
ir rápido, y **hay que descartarlos**. La prueba es directa: en el mismo código
del IDAC del ADDER (130) y la misma ganancia (PGAout ×2), un barrido que venía
desde −255 daba ch2 = 750 mV (riel bajo) y otro que arrancaba desde 0 daba
ch2 = 1121 mV (riel alto). **El mismo código, dos estados opuestos, según de
dónde se viniera.**

No es histéresis del circuito: es que con τ ≈ 30 s una espera de 3 s son 0,1 τ, o
sea que cada lectura es un transitorio y el resultado depende del camino. La
etapa 2 tiene τ = 33,4 s medido sobre su propio tap, así que era previsible.

**Es la tercera vez que el mismo error de método arruina una medición** —el
2026-09-03 midiendo con la cadena saturada, el 2026-09-04 con un escalón que
saturaba el LP, y ahora con espera insuficiente—. Queda como regla: **ninguna
medida de continua de esta cadena vale con menos de 1 τ de espera**, y para
pendientes hacen falta 2 τ.

Lo que sí queda en pie de esta tanda, porque se midió con 60 s: el reposo de la
tabla de arriba. Lo que NO queda establecido: si existe algún código del IDAC del
ADDER que devuelva la cadena al rango con PGAout ≥ ×2. Eso lo está midiendo
`medir_matriz_vs_ganancia.py`, que espera 1 τ en la búsqueda y 2 τ en cada
pendiente.

Esto **no significa** todavía que PGAout > ×1 sea inusable: la corrida de (8,8)
demostró que los IDAC **sí** pueden mover ch2 de un riel al otro, así que la
autoridad para recuperarlo existe. Lo que significa es que **la calibración no
puede arrancar de códigos cero** en esas combinaciones, y que el optimizador
necesita la matriz bien escalada para no pasarse de largo.

### Lo que se está midiendo ahora para cerrarlo

Barrido del IDAC del ADDER en todo su rango, con PGAout en ×1, ×2 y ×8, mirando
ch2 y ch3. Da tres cosas de una:

1. **cómo escala el acople con PGAout**, que es lo que le falta a la matriz;
2. **dónde está la ventana útil** en cada ganancia, que es de dónde tiene que
   arrancar la calibración en vez de arrancar de cero;
3. si la ventana existe en todas las ganancias, o si a partir de cierto PGAout
   **no hay ningún código que devuelva la cadena al rango** — que sería el
   límite de hardware definitivo para las combinaciones altas.

### La lección de método, que vale más que el número

La matriz se midió a **una sola combinación de ganancias** y después se usó para
razonar sobre **las 81**. Eso es exactamente el mismo error que ya cometimos dos
veces: el 2026-09-03 midiendo con la cadena saturada, y el 2026-09-04 con un
escalón de +120 códigos que metía al LP contra el riel. **Una matriz medida en un
punto de operación no vale en otro punto de operación**, y hay que medir la
dependencia en vez de suponer que no existe.

---

## 9. Cómo hay que centrar la cadena, y dos errores de procedimiento propios

### 9.1 El emparejamiento etapa↔tap no es la diagonal

Con el PGA de entrada en ×50, el tap del LP queda contra el riel y **ni −255 ni
+255 de su propio IDAC lo sacan de ahí**. Los números lo explican solos:

| quién mueve ch3 | µV por código | autoridad total |
|---|---:|---:|
| el propio LP | 525 | ±134 mV |
| **el ADDER** | **3823** | **±975 mV** |

El ADDER tiene **7,3 veces** más autoridad sobre la salida del LP que el propio
LP. Entonces el tap del LP **hay que centrarlo desde el ADDER**, y dejarle a su
propio IDAC el ajuste fino, que es donde su resolución sirve y la del ADDER —con
un escalón de 3,8 mV— no alcanzaría.

El ADDER paga quedando descentrado, y puede pagarlo: su tap **no es el que se
captura**, así que alcanza con que no llegue al riel.

Esto probablemente explique buena parte del historial de calibraciones que "no
se sostenían": el lazo estaba usando el actuador equivocado para el tap que
importa.

### 9.2 Error propio: centrar aguas arriba puede ser lo que rompe aguas abajo

La primera versión de la búsqueda centraba las etapas 0 y 1 siempre que
estuvieran a más de 60 mV del centro de su excursión. Con PGA ×50 eso llevó la
etapa 1 al código **−252**, y como esa etapa mueve el tap del LP unos
1002 µV/código, esos 252 códigos le metieron al LP **~252 mV**.

**O sea que la propia corrección metió al LP contra el riel**, y el programa
concluyó "no hay punto válido" cuando el que lo había arruinado era él. El tap 1
estaba en 1016,5 mV, a 106 mV de su riel: perfectamente sano, no había nada que
corregir.

**Regla que queda**, y sale de la estructura triangular de la cadena: *aguas
arriba sólo se toca lo que está por saturar, y sólo lo justo para alejarlo.* Todo
el margen que sobre se reserva para el LP, que es el tap que se captura y el
único que entra en el criterio de aceptación.

### 9.3 Extrapolar el valor asentado en vez de esperarlo

Cada medida de continua cuesta una espera de planta, y ése es el cuello de
botella de todo el trabajo. Con tres muestras igualmente espaciadas de una
exponencial se puede saltear la espera:

```
y_inf = ( y0·y2 − y1² ) / ( y0 + y2 − 2·y1 )
```

Validado contra las series del escalón del 04, que tienen ~500 puntos y ajuste
completo como referencia (`src/interfaces/python/validar_extrapolacion.py`):

| t | n | error medio | peor |
|---:|---:|---:|---:|
| 7,5 s | 11 | 4703 µV | 12276 µV |
| 15 s | 11 | 3212 µV | 14186 µV |
| 20 s | 12 | 1136 µV | 3341 µV |
| **30 s** | 12 | **488 µV** | **2718 µV** |

Con t = 30 s —o sea 60 s de espera total, lo mismo que cuesta 2 τ— el error es de
**medio milivoltio**, contra el ~13,5 % de la amplitud del transitorio que queda
como residuo al esperar 2 τ sin extrapolar. **No ahorra tiempo: compra
precisión.**

**Pero hay que filtrar, y esto es lo importante.** Sin filtro el error medio sale
de 20 a 33 mV y el peor caso llega a **300 mV**. Mirando fila por fila, los
fallos son todos series **que terminan cerca del riel**: ahí la respuesta no es
una exponencial sino una exponencial **recortada**, y se le está pidiendo al
estimador que ajuste algo que no es lo que supone. El filtro —descartar cuando el
valor cae cerca del riel— es **observable en el momento de medir** y no depende
del resultado, así que se puede aplicar sin hacer trampa.

---

## 10. La conclusión de diseño: la calibración necesita DOS actuadores, no cuatro

Después de romperlo tres veces y arreglarlo, el procedimiento que queda es mucho
más simple que el que había, y no por elegancia: cada simplificación salió de un
fracaso concreto.

### El procedimiento

1. **Los cuatro IDAC en cero, esperar, leer.**
2. **Aguas arriba, no tocar nada** salvo que un tap esté a menos de 60 mV de su
   riel, y en ese caso sólo alejarlo.
3. **Bisección del IDAC del ADDER** hasta que el tap del LP dé el objetivo. Sin
   usar la matriz: la bisección sólo necesita saber que los dos extremos caen a
   lados opuestos, y eso se comprueba probándolos.
4. **Newton sobre el IDAC del LP**, con la pendiente medida en el punto, para
   recortar los últimos milivoltios.
5. **Verificar** después de esperar.

### Por qué sólo dos actuadores

| actuador | µV/código sobre ch3 | para qué sirve |
|---|---:|---|
| IDAC del ADDER | 3823 | **grueso**: recorre los 376 mV de excursión en 98 códigos |
| IDAC del LP | 525 | **fino**: 0,525 mV de escalón, para los últimos milivoltios |
| IDAC del PGA | 1026 × ganancia | **inutilizable**: a ×50 son 51 mV *por código* |
| IDAC del BP | 1002 | inutilizable por la misma razón |

Los de aguas arriba no son actuadores del LP: son **perturbaciones**. A ×50, un
solo código del IDAC del PGA corre la salida del LP **51 mV**, o sea dos veces y
media el criterio de aceptación entero. No hay forma de usar eso para ajustar
nada; lo único sensato es no moverlo.

### Los tres fracasos que llevaron acá, porque el patrón vale más que los casos

Los tres tienen la misma forma: **una conclusión negativa que salía de mi
procedimiento y no del circuito.**

1. **"El LP no se puede recuperar."** Mi búsqueda "centraba" la etapa 1, la
   llevó al código −252, y con ~1002 µV/código sobre ch3 eso le metió al LP
   252 mV. *Mi corrección* fue la que lo mandó al riel.
2. **"El ADDER no saca al LP del riel."** Los dos extremos del ADDER dejaban al
   LP en rieles **opuestos** —1122,5 mV con −255 y 746,4 mV con +255—, que es
   exactamente la señal de que **sí** hay autoridad y el punto útil está en el
   medio. Mi test rechazaba por ver "riel" en los dos sin mirar en cuál.
3. **"×50 no cumple."** El refinamiento persiguió el objetivo nominal en ch0,
   movió la etapa 0 catorce códigos, y esos catorce códigos le metieron al LP
   **718 mV**. Destruyó lo que la búsqueda había logrado, para corregir un tap
   que estaba a 155 mV de su riel y no molestaba a nadie.

En los tres casos la conclusión contradecía un dato de campo de Elías —que ×50
funciona— y en los tres el que estaba mal era yo.

**Regla que queda escrita:** cuando la medición dice "no se puede", sospechar del
procedimiento antes que del hardware, **sobre todo si contradice algo que ya se
observó funcionando**. Y en una cadena con acoples de este tamaño, cualquier
corrección aguas arriba hay que evaluarla por lo que le hace al tap de abajo,
nunca por lo que le hace al suyo.

---

## 11. RESULTADO PRINCIPAL: con PGA ×50, el PGAout máximo estable es ×1

Es la pregunta que Elías planteó como objetivo de campo. Medido con
`buscar_max_pgaout.py`, procedimiento de dos actuadores (§10), espera de
búsqueda 1 τ y de medición 2 τ.

| PGA | PGAout | ganancia total | error del LP | peor tap | tiempo | veredicto |
|---|---|---|---:|---:|---:|---|
| ×50 | **×1** | ×50 | **−0,21 mV** | 42,4 mV | 484 s | **CUMPLE** |
| ×50 | ×2 | ×100 | — | — | 92 s | sin punto válido |
| ×50 | ×4 | ×200 | — | — | 92 s | sin punto válido |
| ×50 | ×8 | ×400 | — | — | 304 s | sin punto válido |
| ×50 | ×16 | ×800 | — | — | 305 s | sin punto válido |
| ×50 | ×24 | ×1200 | — | — | 92 s | sin punto válido |
| ×50 | ×32 | ×1600 | — | — | 304 s | sin punto válido |
| ×50 | ×48 | ×2400 | — | — | 307 s | sin punto válido |
| ×50 | ×50 | ×2500 | — | — | 94 s | sin punto válido |

**Los −0,21 mV son el número que importa:** el criterio de Elías es 20 mV y esto
queda **cien veces por debajo**, en 484 s, dentro del techo de 2 τ que él fijó.
La configuración que ya validó en campo no sólo funciona: calibra con un margen
enorme.

### El diagnóstico del fallo es limpio, y esta vez no es un error de método

Para PGAout ≥ ×2 el mensaje es *"los dos extremos del ADDER dejan al LP en el
riel bajo"*. Eso es cualitativamente distinto del caso de ×1, donde los extremos
caían en rieles **opuestos** —1122,5 y 746,4 mV— y por eso existía un punto en el
medio. Cuando los dos extremos caen del **mismo** lado, no hay ningún código que
cruce: la autoridad del ADDER, con todo su recorrido, no alcanza para compensar
lo que PGAout amplifica.

### Qué significa para el nodo

**La red de seguridad se cumple.** El peor resultado posible de esta búsqueda era
PGAout ×1, y ×1 reproduce exactamente la placa que Elías ya validó en campo. No
hay riesgo de quedarse sin configuración usable.

**Y hay una recomendación de hardware que sale sola.** El límite no es de
resolución ni de sintonía: es que **la autoridad del ADDER no alcanza**. Con
3823 µV/código sobre el LP y 255 códigos, su recorrido es de ±975 mV, y aún así
no compensa lo que PGAout ×2 le mete. O sea que el offset que entra **antes de
PGAout** es el problema, y hay dos caminos:

1. **Anularlo donde entra**, con un ajuste propio antes de PGAout. Es lo correcto:
   corrige la causa en vez de pelearla amplificada.
2. **Más autoridad en el ADDER**, subiendo su resistencia. Pero eso empeora la
   resolución justo donde ya es gruesa (su escalón sobre el LP es de 3,8 mV), así
   que es el peor de los dos.

Falta el dato que decide cuál: si el offset entra antes o después del primer PGA.
Lo separa la tanda de reparto de ganancia (§12), que está corriendo.

---

## 12. El origen de coordenadas: qué se descartó y qué quedó

Elías marcó a la tarde que el criterio con el que se venía midiendo todo el día
estaba mal planteado, y tenía razón. Lo que sigue es el rastro completo, porque
hubo **dos hipótesis mías refutadas** y la forma en que cayeron es lo útil.

### 12.1 El error de partida

Todo el día se informó el error del LP como desvío respecto de **1000 mV**. Ese
número **no era un objetivo elegido**: era lo que el banco lee en reposo, y se
tomó por objetivo sin verificarlo. El objetivo real de GEO es **0**:

    CAL_TARGET_GEO_PGA_MV = ... = CAL_TARGET_GEO_LP_MV = 0

Los 1000/1024/3500 mV son de **HAMMER**, que es single-ended porque el martillo
no tiene lado positivo y negativo. GEO es diferencial y se compara **contra
Vref**, así que un tap balanceado tiene que leer cero.

### 12.2 Primera hipótesis mía, refutada: "hay un volt de desbalance"

Si el objetivo es 0 y el banco lee ~1000, parecía que la cadena estaba a un volt
de Vref. Elías señaló que eso ni siquiera era imposible: con `polarity_reg` el
recorrido del IDAC es ±255 × 1875 µV = **±478 mV en la referencia**, y por la
ganancia referencia→tap del ADDER (3823/1875 = 2,04) eso da **±975 mV en ch3**.
Había autoridad para casi un volt.

**Refutada por medición directa:** con el banco marcando 1000,32 mV, el tester
mide **LPo = 2,388 V** contra un Vref de **2,415 V**. El LP está a **27 mV** de
Vref, no a un volt. La cadena está sana.

### 12.3 Segunda hipótesis mía, también refutada: "las etapas saturan contra la alimentación"

Idea de Elías para fijar la escala sin osciloscopio, que es un método correcto:
*"si satura hacia arriba sabés que es 5 V y si satura hacia abajo es 0"*. Los
rieles de alimentación son los dos únicos puntos conocidos del sistema, y
saturar contra ellos los vuelve observables desde adentro.

Se midió, llevando cada etapa a ±255 con 2 τ de espera por punto:

| tap | mínimo | máximo | span |
|---|---:|---:|---:|
| ch0 PGA | 756,49 | 1116,10 | 359,6 |
| ch1 BP | 960,65 | 1016,85 | **56,2** |
| ch2 ADDER | 749,21 | 1123,24 | 374,0 |
| ch3 LP | 746,40 | 1123,01 | 376,6 |

Tres de los cuatro taps se detienen en el **mismo par de valores** —dispersión de
10 mV abajo y 7 mV arriba— con punto medio en **935,7 mV**, que coincidía con el
centro obtenido por otro camino y otro día. Con Vdda = 4,826 V y Vref = 2,415 V
medidos con el tester, la escala salía 13,04 mV reales por mV de banco y Vref
caía en 935,9 — **a 0,2 mV del centro medido**. Parecía cerrado.

**Refutada también por el tester.** Esa escala predice que con el banco en
1000,32 el LP tiene que estar en **3,255 V**. Mide **2,388 V**.

**Conclusión: las etapas NO saturan contra la alimentación.** Se detienen en
~750 y ~1122 de banco por otro motivo —la etapa siguiente, el buffer del AMux, o
el rango de entrada del ADC— y eso queda como pregunta abierta.

### 12.4 Lo que sí quedó, y es un hallazgo aparte

**ch1 no se puede saturar con ningún actuador**: su recorrido total es de 56 mV.
El IDAC del BP mueve su propio tap sólo 90 µV/código —23 mV en todo el rango—
pero mueve **ch3 unos 1002 µV/código**. Es una relación de **11 a 1 a favor** de
usarlo como actuador de aguas abajo.

Eso refuerza mucho la idea de Elías de descentrar el BP para habilitar más
ganancia en PGAout: **es el actuador más barato de la cadena**, porque casi no
desordena su propio tap y además ch1 no puede saturar ni queriendo.

### 12.5 Por qué el problema es del IDAC y no del ADC

Pregunta de Elías: *"no entiendo bien por qué me decís que tienen menor
resolución, el ADC en teoría tiene 18 bits en 5 V de rango"*.

El ADC nunca fue el problema. Con 18 bits sobre ±2,5 V el LSB es **19,1 µV**. El
límite es el **IDAC, que tiene 8 bits**, y lo que importa es cuánto vale un paso
suyo **en el tap**:

| actuador | paso sobre ch3 | veces el LSB del ADC |
|---|---:|---:|
| LSB del ADC | 19,1 µV | 1 |
| IDAC del LP | 525 µV | 27× |
| IDAC del BP | 1002 µV | 52× |
| IDAC del ADDER | 3823 µV | **200×** |

**El ADC ve 200 veces más fino de lo que el ADDER puede corregir.** El cuello de
botella es el actuador, no el sensor. Por eso mejorar el ADC no compra nada, y
por eso la resistencia tampoco resuelve: fija la **escala** del paso, no la
**cantidad** de pasos, que siguen siendo 255. Al subir PGAout hace falta más
autoridad *y a la vez* más finura —rango dinámico ∝ Go²— y eso sólo lo da
encadenar dos etapas, una gruesa y una fina.

### 12.6 Puntos de prueba en la placa

Aportados por Elías: **LPo = P0[1]**, **PGAgain = P2[7]**.
Alimentación medida: **Vdda = 4,823–4,830 V**, **Vref = 2,415 V** (≈ Vdda/2 ✓).

---

## 13. La escala, medida con tester — y lo que corrige

Elías midió con tester (no hay osciloscopio) dos puntos del mismo tap, separados
a propósito, más las referencias:

| qué | valor |
|---|---|
| LPo (P0[1]) con el banco en 1000,32 | **2,388 V** |
| LPo con el banco en 1099,94 | **4,372 V** |
| PGAgain (P2[7]) con el banco en 1000,90 | 2,419 V |
| Vdda | 4,823–4,830 V |
| Vref | 2,415 V |

De los dos puntos de LPo sale la recta:

```
LPo[mV] = 19,9157 × banco[mV] − 17533,5
```

**Un milivoltio del banco son 19,92 mV reales.**

| punto | banco | real |
|---|---:|---:|
| 0 V (masa) | **880,4** | 0 |
| **Vref, que es el objetivo** | **1001,5** | 2,412 V |
| Vdda | **1122,7** | 4,826 V |

### Tres verificaciones independientes

1. La recta predice Vdda en banco **1122,7**. La saturación alta medida por
   barrido —otro experimento, otro día, sin conocer esta recta— dio **1123,01**
   en ch3 y **1123,24** en ch2.
2. El punto medio entre 0 V y Vdda cae en banco **1001,55**, que es exactamente
   donde se sienta la cadena en reposo con los cuatro IDAC en cero. **La cadena
   está centrada en Vref**, como Elías sostenía.
3. Para ch0 en banco 1000,90 la recta predice 2,400 V y el tester dio 2,419:
   difieren 19 mV, o sea **1 mV de banco**.

### Lo que esto DERRIBA

- **El "riel bajo" de 746.** Equivale a **−2,6 V**, imposible. Por debajo de
  banco 880,4 el ADC está fuera de rango y devuelve basura. La conclusión "está
  saturado abajo" era correcta; el número no.
- **El "centro" en 936 mV** y todo lo derivado: la supuesta excursión de 372 mV,
  la asimetría del objetivo, y el argumento de que centrar daba 52 % más margen.
  Salían de promediar ese valor inválido.
- **El criterio de riel usado todo el día.** Un tap leyendo 900 se daba por
  "sano, a 154 mV del riel" cuando está en **0,39 V**, casi contra masa. Varias
  combinaciones se declararon válidas estando railadas.

### Lo que CONFIRMA

- El criterio original de "error contra 1000 mV", que se venía usando sin
  justificar, **estaba bien por casualidad**: banco 1000 es Vref con 1,5 mV de
  error, o sea 30 mV reales.
- Todas las **relaciones entre etapas** (pendientes relativas, el factor 7,3
  entre ADDER y LP, el 11 a 1 del BP) son cocientes y no cambian.
- La excursión útil de cada etapa son **los 4,83 V completos**, no 372 mV.

---

## 14. RESPUESTA A LA PREGUNTA DE LAS RESISTENCIAS

Elías: *"si finetuneamos los valores de resistencia para cada etapa, ¿sería
posible controlar mejor los desbalances y así permitirnos mayores ganancias?"*

**Sí, y es el cuello de botella principal.** Con la escala real:

| actuador | paso real | recorrido (±255) |
|---|---:|---:|
| **ADDER → ch3** | **76,1 mV/cód** | **±19,4 V** |
| BP → ch3 | 20,0 mV/cód | ±5,09 V |
| LP → ch3 | 10,5 mV/cód | ±2,67 V |
| PGA → ch0 (×1) | 1,22 mV/cód | ±0,31 V |
| PGA → ch0 (×50) | 61,0 mV/cód | ±15,5 V |

La alimentación son **4,83 V**. El ADDER tiene **cuatro veces más recorrido que
toda la alimentación**: de sus 510 códigos, sólo **63 caben** antes de que el
tap toque el riel. Los otros 447 no existen.

### La recomendación

| etapa | R hoy | paso hoy | útiles | **R sugerida** | paso nuevo | **útiles** |
|---|---:|---:|---:|---:|---:|---:|
| **ADDER** | 15 k | 76,1 mV | **63** | **2,0 k** | 10,2 mV | **475** |
| **PGA** | 15 k | 61,0 mV (×50) | **79** | **2,2 k** | 8,9 mV | **510** |
| **BP** | 15 k | 20,0 mV | 242 | **6,8 k** | 9,1 mV | **510** |
| **LP** | 15 k | 10,5 mV | 462 | **dejar en 15 k** | — | 462 |

Criterio: que ±255 códigos cubran ~±2,5 V, o sea media alimentación a cada lado.
Más que eso es rango que el riel no deja usar. Los valores son comerciales de
la serie E24.

**El LP no hay que tocarlo**: ya está bien dimensionado, y es el único donde el
rango es resolución de señal y no sólo margen de continua.

### Una corrección a lo que dije antes

Primero afirmé que la resistencia *no* ayudaba, con el argumento de que "fija la
escala, no la cantidad de pasos: siguen siendo 255". La frase es cierta y la
conclusión estaba mal. **Los pasos utilizables hoy no son 255, son 63**,
justamente porque la escala está mal elegida. Bajar la resistencia cambia rango
sobrante por resolución faltante, uno a uno, y hay rango de sobra para vender.

### Por qué esto debería destrabar PGAout

El modo de fallo dominante medido fue *"la ventana útil es más angosta que un
código"*. Con el ADDER 7,5 veces más fino, esa ventana pasa a tener 7,5 códigos
donde tenía uno. **Es exactamente el cuello de botella**, y se destraba con dos
resistencias.

No está demostrado —hay que cambiarlas y medir— pero la cadena causal está
completa y cada eslabón está medido.

### Y el ADC no es el problema

| | resolución |
|---|---:|
| LSB del ADC | **380 µV reales** |
| paso del IDAC del LP | 10,5 mV (**27×** el LSB) |
| paso del IDAC del ADDER | 76,1 mV (**200×** el LSB) |

El ADC ve 200 veces más fino de lo que el ADDER puede corregir. Mejorarlo no
compra nada. *(Nota: la resolución efectiva del ADC es 380 µV y no los 19 µV que
darían 18 bits sobre 5 V — sobre los 4,83 V útiles entran unas 12.700 cuentas,
o sea ~13,6 bits. Por qué se pierden esos 4,4 bits es la misma incógnita del
factor 19,92, y queda abierta.)*

---

## 15. ¿Vale la autocalibración lo que cuesta? — el apartado para la tesis

Elías pidió medir esto explícitamente: *"principalmente con esto buscamos medir
su utilidad y justificar su complejidad. Si no se cumple esto no vale la pena y
necesito que lo justifiques en mi tesis"*.

**El experimento es el más simple posible:** poner los cuatro IDAC en cero —o
sea, sólo la tensión de base, sin ninguna corrección— y medir dónde queda la
cadena en cada combinación de ganancia. Es exactamente lo que sería el nodo si
no existiera el sistema de calibración.

### Resultado

Sobre 12 combinaciones medidas con espera de planta correcta (60 s):

| | combinaciones |
|---|---:|
| **Arrancan con al menos un tap CONTRA EL RIEL** | **10 de 12** |
| Arrancan dentro de rango | 2 de 12 |

Un tap contra el riel significa que **esa etapa no transmite señal**: el nodo no
captura nada. No es que capture peor, es que no captura.

Y las dos que sí arrancan en rango, tampoco están bien:

| PGA × out | peor tap sin calibrar | error del LP tras calibrar | mejora |
|---|---:|---:|---:|
| ×1 × ×1 | **336 mV** | **6,6 mV** | **51×** |
| ×2 × ×1 | 315 mV | 14,1 mV | 22× |

*(valores en voltios reales, con la escala verificada con tester)*

### El argumento

**La autocalibración no es un refinamiento que mejora un número: es lo que hace
que la mayoría de las configuraciones existan.** En 10 de 12 casos, la
diferencia es entre un nodo que funciona y uno que no captura absolutamente
nada. Y en los 2 casos que arrancan en rango, mejora el punto de operación entre
**22 y 51 veces**.

Eso incluye la configuración que Elías validó en campo por dar mejor señal
—PGA ×50—, que **sin calibrar tiene el ADDER y el LP contra el riel**.

### Por qué tiene que ser AUTOMÁTICA y no un ajuste de fábrica

Es la otra mitad del argumento, y todavía falta medirla:

- **τ depende de la temperatura**, porque C1 es un electrolítico. En la ubicación
  del nodo la temperatura va de **8,1 a 31,6 °C en la misma semana** (Open-Meteo,
  2026-09-05). Un ajuste fijo dimensionado en banco a 19 °C no cubre eso.
- Si además el **punto de operación** deriva con la temperatura, un trim de
  fábrica directamente no sirve. **Ésa es la medición que falta** (EXP4c): dejar
  el nodo calibrado y registrar los cuatro taps durante horas, de madrugada, que
  es cuando la casa está quieta y además la temperatura baja de ~19 a ~11 °C.
  La excursión térmica viene de regalo.

### Lo que falta para cerrar el apartado

- **EXP4b — excursión útil perdida.** Cuantificar en bits del ADC lo que se
  pierde por el offset sin corregir. Es el argumento en términos de rango
  dinámico.
- **EXP4c — deriva del punto calibrado.** El que justifica lo *automático*.
- **EXP4d — que la calibración no empeora el ruido.** Barato, y cierra la
  objeción obvia.


---

## 16. CORRECCIÓN a §14: la resistencia se dimensiona por lo que hay que compensar, no por llenar el rango

Elías, después de leer §14: *"la resistencia no debería elegirse tanto por
llenar el rango sino por cuánto hace falta compensar de normal, ¿no creés?"*.

**Tiene razón, y §14 estaba mal.** La recomendación de ahí habría inutilizado la
única configuración que funciona.

### Lo que faltaba medir: cuánto se inyecta de verdad

Sale de los códigos que la calibración efectivamente aplicó en las corridas que
cerraron, multiplicados por el paso real de cada etapa:

| etapa | **máximo inyectado** | autoridad actual | margen |
|---|---:|---:|---:|
| **ADDER** | **−14,62 V** | ±19,42 V | 33 % |
| **PGA (a ×50)** | **+14,30 V** | ±15,54 V | **9 %** |
| LP | 0,29 V | ±2,67 V | 9× |
| BP | 0,00 V | ±5,09 V | sin usar |

§14 proponía bajar el ADDER de 15 kΩ a 2,0 kΩ, dejándolo con **±2,59 V para un
trabajo que exige 14,6 V**. Y bajar el PGA a 2,2 kΩ, cuando el PGA es **el más
ajustado de los cuatro**: usa el 91 % de su autoridad.

### El error de razonamiento, que conviene tener escrito

§14 decía que el ADDER usa "63 de 510 códigos útiles" y que los otros 447 "no
existen". **Es falso.** Esos 447 códigos no están desperdiciados: **son los que
recorren el offset**. Producen una salida recortada mientras se los atraviesa,
pero son exactamente los que traen la cadena de vuelta desde el recorte.

Se confundió *"el tap está fuera de rango mientras paso por ahí"* con *"ese
código no sirve"*. Son cosas distintas: de un actuador no importa que todos sus
puntos sean estados operativos válidos, sino que **alcance** el punto que hay
que alcanzar.

### La recomendación correcta

| etapa | necesita / tiene | **qué hacer** | por qué |
|---|---|---|---|
| **PGA** | 14,3 / 15,5 V | **no tocar, o subir** | 9 % de margen: el más ajustado |
| **ADDER** | 14,6 / 19,4 V | **no tocar** | es el actuador grueso; necesita el alcance |
| **LP** | 0,29 / 2,67 V | **bajar a ~1,8 kΩ** | es el fino: le sobra 9× de rango y le falta resolución |
| BP | 0 / 5,09 V | dejar | no se usó en ninguna calibración que cerró |

Bajando **sólo el LP** a 1,8 kΩ:

| | hoy | con 1,8 kΩ |
|---|---:|---:|
| paso del LP sobre ch3 | 10,5 mV | **1,18 mV** |
| recorrido del LP | ±2,67 V | ±300 mV |
| escalones del ADDER que cubre | 35 | **4** |

Sigue cubriendo más de un escalón del ADDER, así que el par grueso+fino
encadena sin huecos, y la **precisión final mejora 9×** sin perder alcance.

Y no contradice el criterio de Elías de *"si perdemos rango en LP perdemos
resolución"*: eso era sobre el rango de **señal** en LPo, que no cambia. Acá se
achica el rango del **IDAC de corrección**, que está 9 veces sobredimensionado.

### La lección de método

Dimensionar un actuador por "que su recorrido coincida con el riel" suena
razonable y es **el criterio equivocado**. El correcto es *cuánto hay que
corregir*, y eso hay que **medirlo**, no deducirlo del circuito. En este caso
los dos criterios daban recomendaciones **opuestas** para la misma etapa.
