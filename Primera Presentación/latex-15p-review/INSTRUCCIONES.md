# Primera Presentación — instrucciones y estado del trabajo

> **Documento de traspaso.** Recopila **todo** lo que pidió Elías y en qué estado quedó
> cada cosa, para poder retomar en otro chat sin repetir nada.
> Última actualización: 2026-08-20.

---

## 0. Empezar acá (resumen para sesión nueva)

| | |
|---|---|
| **Carpeta entregable** | `docs/Primera Presentación/latex-15p-review/` |
| **Archivo raíz** | `main.tex` → `main.pdf` |
| **Estado hoy** | compila limpio, **17 páginas** |
| **Meta** | **15 páginas** incluida bibliografía (Art. 19 reglamento PFC) |
| **Compilar** | `pdflatex main` → `bibtex main` → `pdflatex main` ×2 |

Secciones:

| # | Archivo | Contenido | Págs |
|---|---|---|---|
| 1 | `secciones/01_problema_modelado.tex` | Utilidad, física, casos, métodos, productos, brecha | ~6 |
| 2 | `secciones/02_transductores.tex` | Transductores y SM-24 | ~4 |
| 3 | `secciones/03_acondicionamiento_digitalizacion.tex` | Analógico y digitalización | ~3 |
| 4 | `secciones/04_transmision_interfaces.tex` | Transmisión, interfaces, MASW | ~2 |

**Carpeta de contexto:** `docs/Primera Presentación/latex-nueva-estructura/` es la versión
larga (151 págs). Sirve **sólo para tener el contexto completo**, no es entregable.
⚠️ Está **desincronizada**: sólo se le copió la sección 1. La verdad vive en
`latex-15p-review/`.

---

## 1. Reglas de formato

- **Nada de saltos de página forzados.** Prohibido `\clearpage` / `\newpage`. Todo corrido.
- **Sin secciones de resumen** que ocupen páginas al pedo.
- Figuras intercaladas en el texto (`[ht]`), nunca a página completa (`[p]`).
- Nada de apéndices con bancos visuales de capturas.

## 2. Nivel técnico del texto — IMPORTANTE

**Los evaluadores son todos ingenieros electrónicos.** No sobreexplicar electrónica
general en ningún punto: lo que se ve, se entiende. Sólo llevan detalle:

- las **decisiones** de diseño (por qué esta topología y no otra), y
- la **física ajena a nuestra área** (ondas sísmicas, dispersión, inversión).

Ejemplo de lo que **NO** hay que escribir: explicar que un Sallen–Key ubica dos polos
conjugados próximos para dar una resonancia estrecha. Eso ya lo saben. Basta con decir
que el $Q$ requerido es bajo y que por eso SK/MFB no aportan.

## 3. Reglas de contenido — generales

- **No casarse con ninguna solución todavía.** Lo que aún no está probado (Kalman+RTS,
  deconvolución, cualquier técnica de *picking* nueva) **no se menciona como resultado**.
  En su lugar: describir **los problemas que se buscarán resolver de cara a la
  presentación final**.
- No presentar como validado algo que sólo funcionó sobre el conjunto con el que se ajustó.
- Mostrar **solamente la última** versión de cada cosa; las comparativas y evaluaciones
  intermedias se mencionan, no se despliegan.

## 4. Reglas de figuras

- **No usar KiCad ni el esquemático de la placa como figura.** Las figuras del circuito
  salen de las **capturas del TopDesign de PSoC Creator**.
- Las figuras de resultado (MASW) se generan **por Python**, **no** capturando la web
  (la web tiene bugs por resolver).
- **Nada de curva $c_R(f)$ todavía**: no se va a defender aún nada sobre $c_R$; queda para
  la presentación final. La imagen de dispersión va **sin picks**.
- La imagen de dispersión va **de 1 a 100 Hz, eje logarítmico**, aunque la banda útil
  termine mucho antes: la idea es que se **vea** por qué. Debajo de ~5 Hz no hay energía
  organizada (apertura de 40 m + SM-24 lejos de su $f_n$); por encima de ~20 Hz la cresta
  cruza la cota de aliasing espacial $c = 2\Delta x f$ y se fragmenta.
- Las capturas de interfaces deben llevar **señales reales**, las que salen mejor.

---

## 5. Sección 1 — Utilidad, casos, métodos, brecha

### Física — ampliar
- ✅ Explicación de **ondas de cuerpo** (P, S) y **de superficie** (Rayleigh, Love).
- ✅ **Ecuación característica** `F(f, c_R; V_S, V_P, ρ, h) = 0` explicada bien: qué es,
  por qué es un problema de autovalores, qué son los modos, por qué $V_P$ y $\rho$ se fijan.
- ✅ **Transformada de Fourier**: estaba mal dicha, debe ser la **2D** (espacio–tiempo →
  frecuencia–número de onda). Ahora se explica que se calcula en **dos pasos separables**
  (temporal por canal + barrido espacial de desplazamiento de fase), no como FFT-2D.

### Casos de uso
- Citar más casos, **explicar en extendido** para qué se usa, sin blabla,
  **máximo un párrafo por caso**. ✅
- ⚠️ **No existe un “Park 2012”** — verificado contra masw.com. Se usaron:
  - Park (2013), *MASW for geotechnical site investigation*, TLE 32(6):656–662.
  - Park et al. (2018), *MASW applications for road construction and maintenance*,
    TLE 37(10):724–730 ← el de carreteras/pavimentos.
- ✅ Caso de carreteras del artículo CONACYT (`docs/PINV01-317.docx`). El docx habla de
  capas de pavimento (asfáltica, base, subbase, subrasante); **no** menciona “concreto”.

### Resto
- ✅ Comparación de métodos: **resumida**, se conserva la tabla, texto en un párrafo.
- ✅ Productos comerciales: **sólo a nivel párrafo**, sin capturas de manuales ni fichas.
- ✅ Método MASW: **breve**, hay pocas páginas.
- ✅ Se **pidió financiación** (propuesta PINV01-317) y **no fue aceptada**. Está dicho.

## 6. Sección 2 — Transductores

- **Mantener el detalle.** Esta sección no se recorta.
- Se concluye **lo mismo que ya se viene diciendo**: el SM-24 de 10 Hz fue una
  restricción impuesta, no una elección.
- ✅ Las alternativas y los precios se presentan en **una sola sección y una sola tabla**.
- ✅ El modelo del SM-24 referido a velocidad y aceleración quedó en **una misma
  sección** y se limita al sensor sin compensar. La explicación de Ma et al. (2023)
  sobre la respuesta plana a aceleración del sistema muy amortiguado se ubica al inicio
  de la sección de compensación, no dentro del modelo dinámico. No
  atribuir al SM-24 sin validar la banda 1–100 Hz medida por Ma con otro geófono.
- ⏳ **PENDIENTE: agregar el SM-24 de 4.5 Hz a la tabla de costos.**
  - <https://www.aliexpress.us/item/3256805089278240.html>
  - <https://www.ebay.com/itm/236043471270>
  - El de eBay se verificó: geófono 4.5 Hz, sensibilidad 28,8 V/(m/s).
    **Falta el precio** — eBay da timeout y AliExpress redirige a login.
    **Elías tiene que pasar el número que ve en pantalla.**

## 7. Sección 3 — Analógico

Narrativa correcta, en este orden:

1. **Se probaron diversas arquitecturas** hasta concluir en ésta, basada en **Ma et al.**
2. En Ma et al., para lograr `1 − BP` se usaba un **band-pass Sallen–Key** más un
   **amplificador diferencial**.
3. ⚠️ **No invertir el argumento:** acá queremos **BAJO $Q$**, porque queremos las
   frecuencias **muy separadas**. *Eso* es lo que muestra que **no vale la pena** un
   Sallen–Key ni un MFB: **no hacen falta más que polos simples**.
   *(Error cometido y corregido: decir que el problema era un SK de “alto Q” sensible a
   tolerancias. El punto real es que el alto Q **no hace falta**.)*
4. Se tomó un modelo que **desacopla ambos polos**: uno en la **rama de entrada**, otro en
   la **realimentación del opa**. Va mejor con nuestras tolerancias y con la **baja
   disponibilidad de R y C de valores finos**.
5. Se **aprovecha ese mismo opa para la inversión de fase**, lo que permite un **sumador
   inversor** en vez de un **diferenciador**: menos componentes, sin depender del
   **pareamiento**, y con un **polo simple en la realimentación** que arranca el filtrado.
6. **Potenciómetro** a la entrada del sumador, en la **rama BP**, para **calibrar la
   proporción `1 − BP`**.
7. **Selección de pasivos:** se registraron **todos los disponibles en el laboratorio** y,
   con el **modelo no ideal del operacional del PSoC**, se resolvieron las ecuaciones con
   `src/calculos_modelados/python/Calculos rapidos/calculoCompensadorOptimo.py`.
   - Geófono: `f0_des = 10 Hz`, `ZETA_GEO = 0.25`, `ZETA_TARGET = 1000`,
     `M_GEOPHONE = 0.011 kg`.
   - Opamp: A0 = 90 dB, f_t = 8 MHz, R_in = 35 MΩ, **R_out = 10 Ω**.
8. ⚠️ **Fórmula del compensador — la correcta es:**

   $$H_{comp}(s)=\frac{s^2+2\zeta_0\omega_n s+\omega_n^2}{s^2+2\zeta_1\omega_n s+\omega_n^2}
   = 1-\frac{2(\zeta_1-\zeta_0)\,\omega_n s}{s^2+2\zeta_1\omega_n s+\omega_n^2}$$

   con **$\zeta_0 = 0{,}25$** (amortiguamiento propio del SM-24) y
   **$\zeta_1 \approx 1000$** (objetivo).
   *Error cometido y corregido: haber escrito $(\zeta_{geo}-\zeta_0)$ en el numerador.
   Va $(\zeta_1-\zeta_0)$.*
9. **Compensador elegido — es el `rank 14` de `compensador_optimo.csv`**
   (NO de `compensador_resultados_todos.csv`, que es la lista de pruebas).
   Verificado contra los componentes realmente poblados en la placa:

   | Bloque | Valor | Polo |
   |---|---|---|
   | Rama de entrada | 43 kΩ + 680 µF | 5,4 mHz |
   | Realimentación | 47 kΩ ∥ (27 pF + 150 pF = **177 pF**) | 19 kHz |
   | Sumador | directa 6,8 kΩ; rama BP por el potenciómetro; realim. 27 kΩ ∥ 15 nF | 393 Hz |
   | Pasa-bajos MFB | 12 kΩ, 150 kΩ, 47 nF, 3,3 nF | par complejo |

   Desempeño: `f0 = 10,21 Hz` (error 2,1 %), `ζ1 = 938` efectivo,
   error RMS **0,457 dB** nominal → **0,195 dB** tras ajustar el potenciómetro.
   *El par 27 pF ∥ 150 pF identifica unívocamente al rank 14.*
   ⚠️ *El sumador quedó poblado con valores distintos de los que proponía esa fila del CSV
   (sugería 7,5 k / 6,8 k / 53,9 nF). Se documentan los reales. **Confirmar con Elías si
   fue un cambio deliberado.***
10. **Antialias:** se puso un **MFB** que, **junto con el polo del sumador**, forma un
    **Bessel de tercer orden** (`calculoMFB_LPF.py`, ζ = 0,691, f0 = 300 Hz).
    *Acá sí se justifica un MFB: hace falta un par de polos complejos conjugados.*
11. **Límite práctico:** la idea era **expandir para llegar bien a 1 Hz**. Falló porque el
    **acople DC era grande** y **en la etapa del sumador el drift era inusable**.
12. **Calibrador:** por eso se implementó.
    ⚠️ **NO mencionar “URUCOM” en el documento.** Explicarlo en base al material de
    `docs/Propuesta Urucom`: calibración *foreground* secuencial PGA→BP→SUM→LP, FIR de
    128 taps para estimar el offset, control PI con banda muerta y anti-windup, códigos en
    EEPROM indexados por ganancia con CRC, lazo inactivo durante la captura.

## 8. Sección 4 — Transmisión, ingesta e interfaces

- **Resumida.** Explica **principalmente la arquitectura**.
- Debe hablar de **lo que se probó y por qué se cambió**.
- Nada de resultados no validados (§3).

### Capturas con señal real — hecho
`serve_demo.py` (en `esp-web-historicos/`) acepta ahora **`--datos <captura>`** y
transmite una captura real en vez de la señal sintética:

```powershell
cd C:\Github\Tesis\esp-web-historicos
python .\serve_demo.py --version 07_2026-08-03_pga-pgaout --port 8010 `
  --datos C:\Github\Tesis\data\raw\Canchita\muestras10_20260703_181007
```

Lee `metadata.json` (fs, `adc_counts_per_volt`), convierte volts → cuentas, arma los nodos
según los subdirectorios `geo*`/`hammer*` y emite la captura entera en lotes.
→ `figuras/interfaces/spa_captura_real.jpg`

Captura elegida: `muestras10_20260703_181007` (fs 2929 Hz, SNR ≈ 45, golpe a 0,78 s,
dura exactamente los 3 s de la ventana de la interfaz).

### MASW — generar por Python, no por la web
Script: `figuras/generar_masw_campo.py` → `figuras/interfaces/masw_campo.png` y
`figuras/interfaces/autopotencia_normalizada_multicanal.png`

- Lee `data/processed/Canchita/field_review_masw_state.npz` (21 trazas promediadas,
  10–50 m, dx 2 m, L 40 m) y calcula la dispersión por desplazamiento de fase.
- Panel (a) gather real; panel (b) imagen de dispersión 1–100 Hz log, **sin picks**,
  con las cotas $c=2\Delta x f$ y $\lambda=L$; panel (c), detalle lineal de
  **5–50 Hz**. El gather usa estilo **wiggle** con sombreado de los lóbulos positivos
  y muestra 2 s. La dispersión conserva la escala azul `turbo`; las cotas se distinguen
  en violeta y azul con contorno blanco.
- El mismo script calcula la **autopotencia unilateral normalizada** de las 21 trazas
  sobre una ventana común de 2 s: quita la media, aplica Hann y representa
  $10\log_{10}(P_{xx}/P_{xx,\max})$ como curvas y mapa frecuencia–distancia. La
  normalización es por traza: compara forma espectral, no amplitud absoluta.
- **Trampa:** la matriz viene **rellenada con NaN** (las trazas no cubren el mismo
  intervalo) → hay que quedarse con la ventana común.
- **Trampa:** acotar a ~1,6 s; incluir los 9 s entierra la cresta en ruido.

---

## 9. Trampas y avisos operativos

- ⚠️ **El servidor de post-procesamiento modifica datos.** Corrido sin `--read-only`,
  reescribió `alignment_offsets.json`, `dispersion_groups.json` y
  `field_review_masw_state.json` de `data/processed/Canchita/`. Se hizo backup y se
  restauró. **Usar siempre `--read-only`:**
  ```powershell
  cd C:\Github\Tesis\src\interfaces\python
  python -m server --port 8000 --read-only
  ```
- ⚠️ **La web de post-procesamiento tiene bugs** que Elías va a resolver. Mientras tanto,
  las figuras se generan por Python.
- ⚠️ Al hacer scroll sobre la página, el cursor sobre un `<select>` **cambia la campaña**
  sin querer. Recargar si pasa.
- Babel español rompe con `\%` dentro de `tabularx` (*Incompatible glue units*).
  Usar `\SI{2.1}{\percent}` en vez de `$2{,}1\,\%$`.

## 10. Pendientes abiertos

| # | Pendiente | Bloqueado por |
|---|---|---|
| 1 | **Precio del SM-24 de 4.5 Hz** en la tabla de costos | Elías debe pasar el precio |
| 2 | **Bajar de 17 a 15 páginas** | No buscar todavía: priorizar claridad compacta |
| 3 | Confirmar si el sumador poblado ≠ CSV fue deliberado | Confirmación de Elías |
| 4 | Bugs de la web de post-procesamiento | Los ve Elías |

### Sobre las 17 páginas

El 20 de agosto se hizo una pasada general de redacción: se eliminaron repeticiones entre
tablas y párrafos, se mantuvieron las ecuaciones y decisiones técnicas, y se redujo el
documento de 25 a 17 páginas. Elías pidió no perseguir todavía las 15 páginas: primero
debe quedar mejor explicado y compacto. La física y el detalle del SM-24 se conservan.
