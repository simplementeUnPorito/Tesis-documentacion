# Todo lo medido el 2026-09-04 — documento único

Para decidir con calma. Cada número dice cómo se midió y dónde está el crudo.
Lo que es **medido** y lo que es **simulado** está separado a propósito, porque
varias conclusiones viejas eran simulación disfrazada de hecho.

Crudos en `lab/planta/`, todos JSON. Banco: PSoC con firmware de autotest,
esclavo en **COM7**, PGA 1× y PGAout 1× salvo donde se aclare.

---

## 1. Resumen: qué cambia respecto de lo que creíamos

| creencia previa | qué dice la medición |
|---|---|
| «C1 se come la continua, el acople entre etapas es sólo transitorio» | **Falso.** El acople es de continua y **permanente**. C1 sólo lo demora. |
| «los abortos son de sintonía / watchdog» | **Son de autoridad.** El ADDER corre la salida del LP 4× más que el propio LP. |
| «`CAL_PI_GAIN_GEO_BP_X1000` = 101 está mal» | **No.** Era un error mío: comparé contra la ganancia de régimen y el firmware usa la **instantánea**, que es la correcta. Ver §4. |
| «la ganancia del LP es 651» | **Es 295.** Medido 524,7 µV/cód; 295 predice 553, 651 predice 1220. |
| «hay que subir `CAL_PI_SETTLE_SAMPLES`» | Ese número **siempre estuvo bien** (vacía el FIR). Faltaba otro concepto: la espera de planta. |
| «se cayeron los pull-ups del bus I2C» | **Falsa alarma mía.** Estaba midiendo el ESP maestro. Ver §7. |

**Lo que hay que decidir el fin de semana** está en §6.

---

## 2. Matriz de acople entre etapas — primera medición

**Método.** Escalón de +120 códigos en el IDAC de cada etapa, leyendo los cuatro
taps en ronda durante 150 s (~500 puntos por ensayo). A cada serie se le ajusta
`y(t) = y_inf + A·e^(−t/τ)`; el régimen permanente sale de `y_inf`, no del último
punto. Crudo: `escalon_pga0_out0_20260904_143457.json`.

### Ganancia en régimen permanente, µV en el tap por código de IDAC

| | ch0 PGA | ch1 BP | ch2 ADDER | ch3 LP |
|---|---:|---:|---:|---:|
| **Vref_PGA** | **61,2** | −0,4 | −240,3 | 1026,0 |
| **Vref_BP** | −0,3 | **90,1** | −388,3 | 1002,3 |
| **Vref_ADDER** | 2,0 | 0,5 | **740,9** | −2120,9 |
| **Vref_LP** | −1,8 | 0,1 | 0,5 | **524,7** |

### Constantes de tiempo, s (sólo donde la amplitud supera 10× el ruido)

| | ch1 | ch2 | ch3 |
|---|---:|---:|---:|
| Vref_PGA | 29,2 | 30,2 | 22,3 |
| Vref_BP | 29,1 | 26,4 | — |
| Vref_ADDER | 28,2 | 33,4 | — |

**τ es uno solo para toda la cadena: 26–33 s, media 29,5 s.** Coincide con
`R₄·C₁ = 43k × 680 µF = 29,2 s` del esquemático y con los 31,3 s medidos el
2026-09-03 por otro camino. **Tres medidas independientes.** Consecuencia
práctica: al firmware le alcanza **una** constante de espera, no cuatro.

### Lo que sale de leer la matriz

**a) El acople es permanente, no transitorio.** Mover `Vref_BP` +120 códigos deja
ch2 en 954,2 mV (venía de 1000,8) y ch3 en 1122,4 (venía de 1002,1). No vuelven.
La creencia anterior venía de una medida hecha **saturando** la cadena y mirando
sólo ch3: lo que se vio volver era la recuperación de la saturación.

**b) El acople supera la autoridad propia de la etapa afectada.**

| acople | µV/cód | veces la ganancia propia del tap |
|---|---:|---:|
| Vref_PGA → ch2 | −240,3 | 0,32 |
| Vref_BP → ch2 | −388,3 | 0,52 |
| Vref_PGA → ch3 | 1026,0 | 1,96 |
| Vref_BP → ch3 | 1002,3 | 1,91 |
| **Vref_ADDER → ch3** | **−2120,9** | **4,04** |

Con números: la autoridad total del LP son **133,8 mV**, y el ADDER moviéndose
120 códigos le mete **254,5 mV**. Lo saca de rango antes de que el LP intente
nada. **Ése es el mecanismo de aborto por riel, ahora medido.**

**c) La cadena es triangular.** Aguas abajo no afecta aguas arriba: la fila de
`Vref_LP` es cero salvo su diagonal, la columna de ch0 también. Eso **valida el
orden de calibración actual (0,1,2,3)** y descarta invertirlo.

**c-bis) Control de calidad: ida contra vuelta.** Cada etapa se midió yendo a
+120 y volviendo a 0. Las dos ramas dan la misma ganancia dentro del **1–1,5 %**:

| par | ida | vuelta | acuerdo |
|---|---:|---:|---:|
| PGA→ch0 | 61,2 | 62,0 | 1,3 % |
| PGA→ch2 | −240,3 | −236,7 | 1,5 % |
| PGA→ch3 | 1026,0 | 1013,6 | 1,2 % |
| BP→ch1 | 90,1 | 91,4 | 1,4 % |
| BP→ch2 | −388,3 | −390,1 | 0,5 % |

Valida la matriz entera y **descarta histéresis** en el rango medido.

**d) Hay dos caminos, uno rápido y uno lento.** El ajuste separa `G_DC` de la
amplitud transitoria `A`. Según el par eso es un sobrepico (`BP→ADDER`: salta a
−150 mV y sube a −46,6) o una subida lenta desde casi cero (`PGA→LP`: arranca en
−4 mV y trepa a +123). Las dos matrices están en
`calculos_modelados/python/calibracion_pi/modelo_cadena.py`.

---

## 3. Curvas propias, sin suponer linealidad

**Método.** Barrido del IDAC de cada etapa sobre todo su rango, midiendo su
propio tap. Se calcula la pendiente **local** entre puntos consecutivos, que es
lo que delata la no linealidad, y se separa del **recorte** (pendiente que se da
vuelta). Crudos: `curva_e*_pga0_out0_*.json`.

| etapa | pendiente global | razón p90/p10 | residuo vs recta | veredicto |
|---|---:|---:|---:|---|
| **PGA** | 61,57 µV/cód | 1,06 | 0,034 mV | **lineal** — la constante alcanza |
| **BP** | 96,54 µV/cód | 1,13 | 1,14 mV | **lineal** |
| **ADDER** | 916,5 µV/cód | ∞ | 35,2 mV | **RECORTA** — pendientes locales negativas |
| **LP** | 733,0 µV/cód | 2,63 | 25,6 mV | **NO lineal** |

- **PGA y BP son lineales.** Una constante de ganancia es correcta para las dos.
  No hace falta curva a trozos.
- **El LP no es lineal, razón 2,63.** Confirma de forma **independiente** el 2,6
  que ya estaba documentado (29 cuentas/cód cerca de Vref contra 75,6 en −224).
  La curva a trozos que ya tiene es la solución correcta.
- **El ADDER recorta**, y eso **no es lo mismo** que no ser lineal. Aparecen
  pendientes locales negativas, o sea que la cadena pega contra un tope. Más
  allá de ese tope el lazo no ve efecto y sigue empujando hasta el riel. **Hay
  que acotar el rango útil del IDAC del ADDER**, no darle una curva.

*(Las pendientes globales del ADDER y del LP salen infladas porque el ajuste
incluye las zonas recortada y no lineal. Para la ganancia del lazo valen las del
escalón, §2.)*

### Rango útil de cada IDAC — y el ADDER pierde el 40 %

La curva en S es **real**. En el handoff de anoche quedó escrito que «la curva en
S del barrido es recorte de la etapa — NO, era un limitador propio del firmware».
Eran **dos efectos distintos**: el limitador existía y se sacó, y debajo estaba
la saturación de verdad, que el limitador tapaba.

Midiendo dónde la pendiente local cae por debajo del 30 % de su mediana:

| etapa | rango útil | recorrido útil | pendiente mediana | rango perdido |
|---|---|---:|---:|---:|
| PGA | −230 … +230 | 25,3 mV | 62,1 µV/cód | 10 % |
| BP | −230 … +230 | 38,0 mV | 93,5 µV/cód | 10 % |
| **ADDER** | **−178 … +128** | 307,3 mV | 739,0 µV/cód | **40 %** |
| LP | −248 … +218 | 357,4 mV | 535,3 µV/cód | 9 % |

Tres etapas pierden apenas los extremos (~10 %, que es el redondeo del criterio).
**El ADDER pierde el 40 % y encima asimétrico**: su pendiente local va de
1963 µV/cód en el centro a **0,4 µV/cód** en los extremos, un factor 5000. Ahí el
lazo empuja sin efecto y termina contra el riel.

**Acción concreta:** acotar el IDAC del ADDER a **−178 … +128**. Fuera de eso no
hay autoridad, sólo hay riel.

Las pendientes medianas confirman por **cuarta vía** las ganancias del escalón:
62,1/61,2 · 93,5/90,1 · 739,0/740,9 · 535,3/524,7.

### ¿Cuánto sesga medir sobre transitorios?

La primera tanda de curvas se tomó con 500 ms por punto, o sea sobre
transitorios. Se repitió con **60 s de espera de planta** por punto para
cuantificar el sesgo. En la etapa 0:

| | pendiente | razón | residuo |
|---|---:|---:|---:|
| sin espera (500 ms) | 61,57 µV/cód | 1,06 | 0,034 mV |
| con 60 s | 61,90 µV/cód | 1,04 | 0,043 mV |
| escalón (régimen, ajuste exponencial) | 61,2 µV/cód | — | — |

**Coinciden al 1 %**, y es lo que hay que esperar: el PGA tiene `G_TRANS = 0`, o
sea que **su propio tap no tiene transitorio**, así que esperar no cambia nada.
Tres medidas independientes del mismo número por tres caminos distintos.

Donde la espera sí importa es en las etapas con transitorio propio —el BP, que
tiene `G_TRANS = 98` contra `G_DC = 90`— y sobre todo en los **taps ajenos**.

---

## 4. Ganancias y autoridad: medido contra lo que usa el firmware

**Primero me equivoqué acá, y la corrección es la parte interesante.** Comparé
las constantes del firmware contra la ganancia de **régimen permanente** y
concluí que la del BP estaba al doble. Es la comparación equivocada: el lazo
reacciona en 49 ms, muchísimo antes de τ, así que la que corresponde es la
**instantánea**, `G_DC + G_TRANS`. Con ésa, las cuatro coinciden:

| etapa | G_DC | G_TRANS | **instantánea** | firmware | error |
|---|---:|---:|---:|---:|---:|
| PGA | 61,2 | 0,0 | 61,2 | 58,1 | +5,3 % |
| **BP** | 90,1 | **98,0** | **188,1** | **189,4** | **−0,7 %** |
| ADDER | 740,9 | 21,4 | 762,3 | 770,6 | −1,1 % |
| LP | 524,7 | 0,0 | 524,7 | 553,1 | −5,1 % |

El BP es la **única** etapa donde el transitorio es comparable a la continua, por
eso parecía mal sólo ésa. **Las cuatro constantes están bien y no hay que
tocarlas.**

Lo detecté porque el "arreglo" **rompe el lazo**. Con la ganancia de régimen (48)
el deadbeat sobrecorrige por 2 en la escala de tiempo en la que trabaja, y el DAC
oscila con amplitud **creciente** hasta el riel:

```
trayectoria del DAC del BP:  0, -17, 2, -19, 4, -21, 6, -23, 9, -28, 14, -33, 20, -40
éxito: 0 %
```

`Kp = 1/2` lo estabiliza (1,586 mV en 1τ, 100 %), pero no hace falta: la
constante ya era la correcta.

**La consecuencia real, que sí importa.** Usando la ganancia instantánea el lazo
es estable, pero el valor **final** del BP queda en `G_DC/G_inst = 0,48` de lo que
hacía falta. O sea: **converge y después se va.** Ése es exactamente el síntoma
«no se sostiene» que se venía observando, y ahora tiene explicación cuantitativa.
El arreglo no es tocar ganancias sino **esperar a la planta**, para que la medida
sobre la que corrige sea la asentada.

### Autoridad de cada etapa sobre su propio tap (ganancia × 255 códigos)

| etapa | autoridad |
|---|---:|
| PGA | **±15,6 mV** |
| BP | **±23,0 mV** |
| ADDER | ±188,9 mV |
| LP | ±133,8 mV |

**Las dos primeras tienen muy poco margen.** Es el número que decide tu requisito
de que la cadena calibre con cualquier par de ganancias: si a ganancia alta el
offset amplificado supera esto, no hay firmware que lo arregle.

### Offsets naturales, con los cuatro IDAC en código 0

Taps en **1001,0 / 1001,1 / 1001,1 / 1001,5 mV** contra un objetivo de 1000 mV.
O sea que en 1×/1× **la cadena está naturalmente centrada a ~1 mV** y la
calibración casi no tiene que hacer nada. El caso difícil es a ganancia alta, y
eso es lo que falta medir (§8).

---

## 5. Simulación — ahora sí calibrada contra la placa

`calculos_modelados/python/calibracion_pi/modelo_cadena.py`. **Todos los
parámetros inventados fueron reemplazados por los medidos.** Lo que se corrigió:

- acoples y offsets: ahora la matriz de §2 y los ~1 mV de §4;
- ruido: **1,5 cuentas**, no 8. Con 8 la banda muerta del PGA —que son 5— quedaba
  tapada y el lazo no podía lockear ni convergiendo perfecto;
- los offsets viejos (12 / −35 / 60 / −95 mV) eran además **imposibles**: con
  ±23 mV de autoridad, el BP no corrige −35 mV ni con el lazo perfecto. El
  modelo abortaba por razones que no existen en la placa.

**Validación:** con los parámetros medidos y **sin espera**, el modelo da
**17,5 mV**. En la placa se observó `GEO_LP` en **−18 mV**. Antes, con
parámetros inventados, daba 34 mV. El modelo reproduce el defecto real.

| espera por etapa | error asentado | tiempo total | éxito |
|---|---:|---:|---:|
| sin esperar (firmware de hoy) | 17,5 mV | 2 s | 100 % |
| **1 τ** | **2,09 mV** | 119 s | 100 % |
| 2 τ | 0,47 mV | 237 s | 100 % |
| 3 τ | 0,56 mV | 355 s | 100 % |

**1τ ya cumple tu objetivo de 20 mV con margen de 10×**, en 2 minutos. 2τ da
0,47 mV en 4 minutos. De 2τ en adelante no mejora.

**Precompensación:** implementada (`calibrar_precomp`), cancela el acople usando
la matriz al cerrar cada etapa. **No mejora en 1×/1×** —mismo resultado a 0 y 1τ,
algo peor a 2τ— porque con offsets de 1 mV las correcciones son chicas y el
acople que inducen también. Queda escrita para el caso que sí importa, que es
ganancia alta.

**Ki:** el barrido sale **plano** (4,44–4,59 mV para todo el rango) y agrega
inversiones del DAC. No es un bug: el integrador corrige lo que el lazo
**observa**, y acá el lazo mide, anula, declara lock y se va — el error aparece
después. Recomendación: **1/32 o 1/64**, como red de seguridad contra lo que el
modelo no captura, no porque la simulación lo pida.

---

## 6. Lo que hay que decidir

1. **NO tocar `CAL_PI_GAIN_GEO_BP_X1000`.** Verificado: el 101 es correcto,
   corresponde a la ganancia instantánea. Cambiarlo rompe el lazo (§4).
2. **Dejar la ganancia del LP en 295** y corregir el 651 del proyecto de test.
   Vos dijiste 651; la medición dice 295 y por tu regla manda lo medido.
3. **Fijar `CAL_PI_PLANT_SETTLE_TAU_X10`.** Hoy vale 0 a propósito. Con τ=29,5 s
   medido: **10 (=1τ) da 2,09 mV en 119 s**, 20 (=2τ) da 0,47 mV en 237 s. Como
   la recalibración es por umbral y no en cada arranque, 2τ es asequible.
   Para campo, τ de peor caso con 5–45 °C es **~40 s**, no 29,5.
4. **Acotar el IDAC del ADDER a −178 … +128.** Medido: fuera de ahí su pendiente
   cae a 0,4 µV/cód (factor 5000 contra el centro) y el lazo sólo puede railar.
5. **Ki en 1/32.**
6. **Decidir qué hacer con el acople ADDER→LP (4,04×).** Es el problema de fondo
   y no se arregla con sintonía. Opciones: precompensar por firmware, o subir la
   autoridad del LP por hardware.

---

## 7. Un error mío de diagnóstico, para que no se repita

Pasé la tarde concluyendo que se habían caído los pull-ups de 3V3 del bus I2C, a
partir de una regresión medida contra tres días anteriores, reproducible tres
veces. **Era falso: estaba midiendo el ESP maestro**, que no tiene ningún PSoC
del otro lado. El esclavo real estaba en COM7.

Lo que lo hizo posible:
- me confié del handoff que decía «el esclavo en COM8» y **nunca lo verifiqué**;
- `platformio.ini` tiene `upload_port = COM8` fijo en el entorno `slaveTest`, así
  que además le grabé ese firmware **al maestro**, pisándole el suyo;
- el ESP contestaba consola y perfil perfectamente, porque era un ESP sano.

Dos lecciones que valen más que la conclusión: **reproducibilidad no es validez**
—repetir una medida sobre el objeto equivocado la confirma igual de bien—, y
cuando el usuario afirma un hecho físico que contradice la conclusión (Elías dijo
dos veces que la placa no se había tocado), **lo primero que hay que revisar es
la conclusión**. Detalle completo en `hardware_pullups_caidos_2026-09-04.txt`.

**Pendiente de revertir:** el maestro (COM8) quedó con `slaveTest` y el esclavo
(COM7) también; hay que devolverles master y slave2 cuando se termine de medir.

**Dato útil:** los pines I2C reales, del `.cydwr`, porque el netlist usa los
nombres del símbolo del kit (P12.0/P12.1) y **no** son los del firmware:
`I2Cp[0] SDA = P2[1] pin 63`, `I2Cp[1] SCL = P2[3] pin 65`.

---

## 8. Lo que falta medir

- **Las 81 combinaciones PGA × PGAout.** Es lo que decide tu requisito de que
  calibre con cualquier ganancia. El programa (`medir_planta.py campana`) recorre
  primero las cuatro esquinas y después cierra hacia el centro, y es reanudable.
- **Las curvas con espera de planta.** Las de §3 se tomaron con 500 ms por punto,
  o sea sobre transitorios. Sesga la pendiente global; la **forma** —que es lo
  que decide linealidad— se mantiene. Está corriendo la versión con 60 s.
- **Verificar en placa** que subir la espera efectivamente sostiene la
  calibración: calibrar, esperar diez minutos, pedir snapshot.
- **El sentido físico de la polaridad** con DMM en LPo, que quedó abierto de
  antes.

---

## 9. Cambios de firmware ya hechos hoy

**`c62186b` — el techo de 16 bits.** `settle_samples`, `timeout_samples`,
`refine_settle_samples`, `samples_taken`, `settle_remaining`,
`control_hold_remaining` y `sample_index` eran `uint16`. Con τ≈29,5 s a 2604 Hz,
un τ son ~77.000 muestras y el techo de 16 bits es 65.535 = **25,2 s**: no entra
ni un τ. Y falla **en silencio**: 5τ truncan a 5,5 s. Todos a `uint32`.

**`c62186b` — el concepto que faltaba.** `CAL_PI_SETTLE_SAMPLES_*` vacía el FIR y
para eso 128 muestras es *exacto*. Se agregó `plant_settle_samples`, que es otra
cosa. El multiplicador queda en **0** —sin cambio de comportamiento— hasta
decidir el punto 3 de §6.

**`53041b7` — firma de arranque por LED.** No sirve en esta placa: el pin del LED
está desactivado en el TopDesign. Queda inerte y documentada.

Programas nuevos: `medir_planta.py` (escalón / curva / campaña),
`analizar_planta.py` (tablas y figuras), `registrar_calibracion.py` (evolución
temporal de una calibración).
