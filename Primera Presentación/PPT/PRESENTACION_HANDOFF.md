# Handoff — Presentación 1 de tesis (v04)

## Cambios de v04

- Se creó `Presentacion_1ra_Borrador_v04.pptx`, preservando la v03.
- Slide 22: se reemplazó el placeholder por la Fig. 1 original de Lin & Ashlock (2016), recortada desde el PDF local del paper.
- Slide 43: se incorporó la imagen del martillo instrumentado / PCB 086D20 disponible en el proyecto.
- Slide 44: se incorporó una captura real de Geophone Scope con señales HAMMER y GEO.
- Slide 45: se incorporó una adquisición real alineada HAMMER–GEO usada en el flujo de análisis.
- Slide 50: se reemplazó el placeholder final por el resultado MASW del proyecto (registro sintetizado + imagen de dispersión).
- Validación estructural del PPTX: aprobada contra la v03.

## Archivos principales

- `Presentacion_1ra_Borrador_v04.pptx` — deck editable actual.
- `Presentacion_1ra_Borrador_v03.pdf` — último render completo disponible para revisión rápida.
- `Presentacion_1ra_Borrador_v03.pptx` — versión anterior preservada.
- Carpeta de recursos generados durante esta iteración:
  - `generated_slide_art/methods_direct.png`
  - `generated_slide_art/methods_inhole.png`
  - `generated_slide_art/methods_surface_body.png`
  - `generated_slide_art/methods_surface_waves.png`
  - `generated_slide_art/love_diagram.png`
  - `generated_slide_art/rayleigh_diagram.png`
  - `generated_slide_art/homogeneous_semispace.png`
  - `generated_slide_art/depth_sensitivity.png`
  - `generated_slide_art/dispersion_curve.png`

## Objetivo de la presentación

Primera presentación / mid-term del Proyecto Final de Carrera.  
Duración objetivo: **27–28 min netos**, aunque Elías tiende a hablar rápido.  
No hay formato burocrático obligatorio: priorizar narrativa técnica y visual.

La idea no es vender la tesis como terminada. Hay que mostrar:

1. por qué interesa caracterizar el suelo;
2. cómo se llega racionalmente a Rayleigh/MASW;
3. qué requisitos electrónicos impone MASW;
4. cómo se diseñó GEO;
5. cómo se coordinan MASTER y HAMMER;
6. qué ya fue validado;
7. qué falta cerrar para la presentación final de diciembre.

---

# Narrativa acordada

## A. De la necesidad geotécnica a MASW

### 1. Motivación
Empezar por **para qué queremos conocer el suelo**, no por “qué queremos medir”.

Ejemplos visuales:
- fundaciones;
- grietas / asentamientos;
- rutas / pavimentos / rellenos;
- taludes;
- evaluación durante y después de una obra.

### 2. Estado del arte dividido por invasividad

La clasificación que se quiere mostrar es:

### Métodos invasivos / penetrativos
**A. Medición directa del terreno**
- SPT
- CPT / CPTu

Ventajas:
- muy usados;
- valiosos para diseño;
- SPT puede recuperar muestra;
- CPT da perfil continuo.

Limitaciones:
- intervención física;
- costo;
- logística;
- cobertura espacial localizada.

**B. Medición de ondas dentro del terreno**
- downhole
- crosshole

Ventaja:
- velocidades dinámicas, incluida `Vs`, de forma bastante directa.

Limitación:
- uno o varios pozos;
- geometría conocida;
- logística / costo.

### Métodos no invasivos desde superficie
**C. Ondas de cuerpo**
- refracción;
- reflexión;
- P/S desde superficie.

**D. Ondas superficiales**
- Love;
- Rayleigh;
- SASW / MASW.

Importante: **refracción superficial no significa “ondas superficiales”**. La sísmica de refracción near-surface clásica usa ondas de cuerpo, principalmente P.

No presentar estos métodos como excluyentes. La información de SPT/CPT, downhole/crosshole, H/V, refracción, geología, etc. puede complementar y restringir la inversión de ondas superficiales.

---

## B. Física mínima antes de Rayleigh

### 3. Medio elástico
Introducir P y S:

`Vp = sqrt((lambda + 2mu)/rho)`  
`Vs = sqrt(mu/rho)`

Luego:

`Gmax = rho * Vs^2`

Objetivo narrativo: **Vs se vuelve una variable muy atractiva porque está ligada directamente a la rigidez inicial del terreno**.

### 4. Interfaces
Hablar brevemente de:
- Snell;
- reflexión;
- transmisión;
- conversión P ↔ SV;
- superficie libre.

---

## C. Love primero, luego Rayleigh

Orden obligatorio:

1. Love
2. Rayleigh
3. recién después explicar por qué Rayleigh nos interesa más.

### Love
- movimiento SH;
- horizontal y transversal a la propagación;
- útiles, pero una fuente vertical no es la configuración activa más natural.

No decir que Love “es mala” ni que siempre se atenúa más rápido.

### Rayleigh
- acoplamiento P–SV;
- trayectoria aproximadamente elíptica en plano vertical;
- componente vertical fácil de generar y medir;
- velocidad relacionada con `Vs`;
- menor decaimiento geométrico ideal que ondas de cuerpo.

### Energía superficial
Se dejó una slide con el resultado clásico aproximado para una carga vertical en un semiespacio homogéneo, isótropo y elástico:

- ~67 % Rayleigh
- ~26 % S
- ~7 % P

**No usar 90 % como regla universal.**

---

# Dispersión e inversión

## 5. Suelo homogéneo
Primero mostrar un semiespacio homogéneo:

- mismas `rho`, `Vs`, `Vp` / `nu`;
- para un modo dado, `cR` no depende de `f`.

## 6. Relación Rayleigh–Vs
Mostrar que `cR` es ligeramente menor y estrechamente relacionada con `Vs`, dependiendo de `nu`.

## 7. Estratificación
Agregar capas con distintos:
- `Vs`;
- `Vp` o `nu`;
- `rho`;
- espesores.

## 8. Sensibilidad con profundidad
Usar:

`lambda_R(f) = c_R(f) / f`

Idea visual:
- alta f → lambda corta → sensibilidad más superficial;
- baja f → lambda larga → sensibilidad generalmente más profunda.

Evitar afirmar una equivalencia rígida “frecuencia = profundidad”.
Hablar de **sensibilidad distribuida**.

## 9. Dispersión
Al agregar estratificación:

`cR = cR(f)`

La curva de dispersión contiene información sobre la estructura vertical.

## 10. Inversión
Modelo directo:

`modelo de capas -> curva de dispersión`

Problema inverso:

`curva medida -> modelo compatible`

Parámetros posibles:
- espesores;
- `Vs`;
- `Vp` / `nu`;
- `rho`.

Importante:
- la inversión no es única;
- información independiente puede enriquecer/restringir la solución.

---

# SASW / MASW

## 11. SASW
- 2 receptores;
- diferencia de fase;
- ambigüedad de ciclos completos;
- repetir separaciones;
- menor redundancia espacial.

## 12. MASW
- múltiples posiciones;
- registro espacio-tiempo;
- patrones coherentes;
- mejor separación modal / redundancia.

## 13. Prototipo con dimensión espacial sintetizada
Usar Lin & Ashlock 2016 como justificación conceptual:
- se puede sintetizar la dimensión espacial mediante adquisiciones sucesivas;
- fuente/receptor desplazados de forma recíproca;
- requiere geometría, excitación y referencia temporal bien controladas.

Objetivo de adquisición:

`U[m,n] = uz(x_m, t_n)`

---

# Requisitos electrónicos

MASW impone:
- banda útil;
- fase;
- rango dinámico;
- antialias;
- frecuencia de muestreo;
- geometría;
- referencia temporal;
- excitación;
- almacenamiento;
- operación de campo.

---

# Arquitectura general

Primero presentar solo los tres roles:

## GEO
Mide respuesta del suelo.

## MASTER
Coordina nodos y sirve de interfaz.

## HAMMER
Mide la excitación.

**No explicar todavía aquí que la red no transporta las muestras.**
Eso se explica recién en la sección MASTER, después de terminar GEO.

Orden narrativo obligatorio:

`Arquitectura general -> GEO completo -> MASTER -> HAMMER`

---

# GEO

## Sensor
SM-24:
- geófono vertical;
- `fn ≈ 10 Hz`;
- sensibilidad nominal ~28.8 V·s/m.

Modelo mecánico:

`m u¨ + c u˙ + k u = -m xg¨`

Transferencia de velocidad:

`Hv(s) = G0 s^2 / (s^2 + 2 zeta wn s + wn^2)`

Problema:
la tesis necesita información LF y el sensor pierde sensibilidad bajo resonancia.

### Idea importante
A 1 Hz con `fn = 10 Hz`, lejos de resonancia:

`|H| ~ (f/fn)^2 ~ 0.01`

aprox. **-40 dB** respecto a banda alta.

Por eso **no basta “amplificar más”**:
las componentes alrededor y por encima de resonancia consumen antes el rango dinámico del AFE / ADC.

---

# Estado del arte de extensión LF del geófono

Mostrar alternativas como decisión de ingeniería, no como “las demás están mal”.

## 1. Medición directa + ganancia
+ simple  
- banda alta domina / rango dinámico insuficiente para LF.

## 2. Carga / impedancia / compensación pasiva
Ej. Pazos.
+ simple  
- extensión limitada.

## 3. Inversión / zero-pole
Compensa directamente la dinámica.

Problemas:
- alta ganancia LF / DC;
- bias / offset;
- amplificación de ruido LF;
- sensibilidad al modelo.

### Matiz importante
Ma et al. **también** termina necesitando mucha ganancia y por tanto también amplifica offsets del AFE.
La diferencia es que no usa una inversión LF agresiva cuyo compensador ideal diverge al acercarse a DC.

## 4. Force balance
Usar la bobina también como actuador:

`I_coil -> F_Lorentz`

Puede modificar el comportamiento electromecánico y extender la banda.

Ventajas:
- extensión real de la dinámica mecánica;
- buena linealidad/banda.

Costo:
- lazo activo;
- estabilidad;
- consumo;
- complejidad;
- tolerancias / ruido.

## 5. Ma et al.
Idea elegida:
**no levantar agresivamente el fondo; atenuar primero la región dominante y después recuperar nivel global con ganancia.**

Conceptualmente:

`Hcomp(s) ≈ 1 - Hbp(s)`

Implementación:
- camino directo;
- BP inversor;
- suma/resta;
- ganancia global;
- LP antialias.

Esto conecta directamente con el siguiente problema:
**alta ganancia -> offset acumulado -> DA-AFE.**

---

# AFE implementado

Cadena:

`entrada diferencial -> PGA -> directo + BP -> SUM -> LP -> ADC`

Objetivos:
- rechazo modo común;
- ganancia programable;
- compensación LF;
- antialias;
- adaptación al ADC.

Mostrar:
- modelo vs medición;
- magnitud;
- fase;
- tolerancias.

Advertencia:
la extensión SM-24 + AFE en LF es por ahora una **predicción en cascada** con el modelo nominal del geófono, no una calibración mecánica extremo a extremo.

---

# DA-AFE / calibración de offset

Problema:
alta ganancia + offsets pequeños -> consumo de margen dinámico / saturación intermedia.

Filosofía:

`CALIBRAR -> CONGELAR -> MEDIR`

Recursos:
- MUX;
- ADC;
- FIR;
- PI;
- VDAC por etapa.

Orden secuencial:

`PGA -> BP -> SUM -> LP`

porque las etapas posteriores heredan el residual anterior.

Ecuaciones principales:
- error ADC;
- conversión a códigos VDAC;
- deadband;
- PI;
- saturación;
- anti-windup.

Resultado importante del paper:
LP residual:

`2.9–45.8 %FS -> 0.4–3.9 %FS`

en las configuraciones probadas con una única configuración de controlador.

---

# Captura digital GEO

PSoC 5LP:
- ADC ΔΣ;
- 18 bit;
- ~2604 Sa/s;
- DMA;
- DFB;
- RAM;
- SignalController;
- almacenamiento local / metadatos.

Idea oral:
una vez disparada la captura, el timing crítico queda en hardware/local.

---

# MASTER

Recién aquí explicar:

- ESP-NOW;
- ARM;
- PRESTART;
- START por broadcast;
- reloj local;
- captura local;
- store-and-forward;
- descarga posterior.

**La red no transporta muestras durante la adquisición.**
Coordina la captura y luego transfiere los datos.

Sincronización preliminar:
- separación observada GPIO ~200–400 us;
- esto todavía **no** equivale a medir sincronización ADC–ADC;
- falta caracterizar deriva de reloj.

Error de fase:

`Delta_phi(f) = 360° f Delta_t`

Para `Delta_t = 400 us`:
- ~3° @ 20 Hz;
- ~7° @ 50 Hz.

---

# HAMMER

Motivación:
si se sintetiza la dimensión espacial con eventos sucesivos, no se puede asumir que todos los golpes son idénticos.

HAMMER permite:
- instante de impacto;
- forma de excitación;
- repetibilidad;
- detección de rebote;
- alineación;
- aceptar/rechazar captura.

Cadena:
`PCB 086D20 -> excitación/corriente -> desacople/protección -> PGA -> LP -> ADC`

La lógica digital / comunicación / almacenamiento reutiliza la filosofía de GEO.

---

# Flujo de campo

Secuencia:

`configurar -> calibrar -> ARM -> impacto -> revisar -> aceptar/repetir -> mover -> siguiente posición`

Interfaz:
- configuración;
- adquisición;
- revisión;
- después interfaz de análisis.

---

# Resultados preliminares

## Sincronización
Preliminar, no definitiva.

## SNR aparente por banda
Medianas:

- 1–5 Hz: 0.5 dB
- 5–10 Hz: 2.1 dB
- 10–20 Hz: 16.7 dB
- 20–50 Hz: 24.4 dB

No atribuir la mala SNR <10 Hz solamente al geófono o AFE:
incluye fuente + acoplamiento + terreno + sensor + electrónica.

## Registro espacio–tiempo
Resultado central actual:
- 21 posiciones;
- 10–50 m;
- `Delta x = 2 m`;
- alineadas con HAMMER;
- remuestreo/promedio;
- construcción de `U(x,t)`.

Frase útil:
> “Todo el sistema presentado hasta acá fue construido para poder obtener esta matriz.”

---

# Qué está demostrado y qué falta para diciembre

## Ya demostrado / avanzado
- AFE funcional;
- compensación implementada;
- caracterización eléctrica;
- DA-AFE;
- captura digital local;
- arquitectura distribuida;
- HAMMER;
- flujo de campo;
- registro espacio-tiempo secuencial.

## Pendiente
- calibración mecánica extremo a extremo;
- mejorar excitación LF;
- medir sincronización ADC–ADC;
- deriva de relojes;
- varios GEO simultáneos;
- curva de dispersión;
- identificación de modos;
- inversión;
- perfil `Vs(z)`.

---

# Estado actual del deck

- **78 slides totales**
- **50 principales**
- **28 auxiliares / backup**

## Slides principales actuales

1. Portada
2. ¿Para qué necesitamos caracterizar el suelo?
3. Métodos invasivos: medición directa del terreno
4. Métodos invasivos: medición de ondas dentro del terreno
5. Métodos no invasivos: ondas de cuerpo desde superficie
6. Métodos no invasivos: ondas superficiales
7. Modelo mínimo: un medio elástico admite ondas P y S
8. Vₛ nos interesa porque está directamente ligada a la rigidez
9. Las interfaces cambian la propagación
10. ¿Por qué mirar ondas superficiales? Porque dominan una fuente vertical de superficie
11. Ondas Love
12. Ondas Rayleigh
13. Rayleigh encaja con el problema
14. Suelo homogéneo
15. Relación cR–Vs
16. Agregamos estratificación
17. Longitud de onda y sensibilidad con profundidad
18. Dispersión
19. Curva de dispersión -> modelo
20. SASW
21. MASW
22. MASW sintetizado
23. Objetivo U(x,t)
24. Requisitos
25. Arquitectura: GEO / MASTER / HAMMER
26–40. GEO: SM-24, alternativas LF, Ma, AFE, DA-AFE, captura digital
41–42. MASTER / sincronización
43. HAMMER
44–45. Campo / análisis
46–47. Resultados
48–49. Qué está demostrado / roadmap
50. Preguntas

## Backup actual (51–78)

- A1 Elastodinámica + Helmholtz
- A2 Relaciones elásticas
- A3 Snell + conversión modal
- A4 cR/Vs vs Poisson
- A5 Modos Rayleigh / kernels
- A6 No unicidad + información complementaria
- A7 SASW fase
- A8 MASW U(x,t) -> dispersión
- A9 Aliasing temporal/espacial
- A10 MASW sintetizado
- A11 Modelo SM-24
- A12 Carga y amortiguamiento
- A13 Cálculo de ganancia sub-resonante
- A14 Comparativa LF
- A15 Ma et al.
- A16 Esquemático AFE
- A17 Barridos AFE
- A18 Cuantización ADC/VDAC
- A19 PI/deadband/anti-windup
- A20 Parámetros DA-AFE
- A21 SignalController/DMA
- A22 Error de reloj
- A23 Error de fase
- A24 HAMMER AFE
- A25 SNR aparente
- A26 BOM/costo
- A27 Metadatos
- A28 Referencias

---

# Cambios de v03 respecto de la primera versión

- La antigua slide comparativa de métodos se dividió en 4.
- Se generaron diagramas para:
  - SPT/CPT;
  - downhole/crosshole;
  - ondas de cuerpo desde superficie;
  - ondas superficiales;
  - Love;
  - Rayleigh;
  - semiespacio homogéneo;
  - sensibilidad con profundidad;
  - dispersión.
- Love aparece antes que Rayleigh.
- Slides 14, 17 y 18 fueron rediseñadas.
- Se conserva el orden conceptual pedido por Elías.

---

# Prioridades para la siguiente iteración en Codex

1. **Slide 2**
   - reemplazar placeholders por fotos reales:
     - fundación;
     - grietas/asentamiento;
     - ruta/pavimento;
     - talud/obra.

2. **Slides 3–6**
   - mantener 4 slides;
   - mejorar estética;
   - si se encuentran GIFs/figuras libres, reemplazar dibujos simples;
   - no volver a juntarlas en una sola.

3. **Slides 7–13**
   - mejorar visuales de P/S, Snell, Love y Rayleigh;
   - mantener Love antes de Rayleigh;
   - revisar ritmo para que Rayleigh se elija solo después de presentar ambas familias.

4. **Slide 10**
   - conservar ~67 % Rayleigh como resultado ideal, no 90 % universal;
   - añadir referencia visible discreta.

5. **Slides 14–19**
   - dejar muy visual:
     `homogéneo -> estratificado -> lambda/profundidad -> dispersión -> inversión`;
   - evitar sobrecargar con texto.

6. **Slides 20–23**
   - buscar / insertar figura de Lin & Ashlock;
   - mostrar bien transición SASW -> MASW -> U(x,t).

7. **Slides 26–35**
   - esta es una parte central de la presentación;
   - priorizar figuras de papers y respuestas en frecuencia;
   - mostrar comparación:
     direct measurement / passive-loading / inverse / force-balance / Ma.

8. **Slides 36–40**
   - aprovechar el paper URUCON para gráficos reales de DA-AFE;
   - evitar tablas densas en slides principales.

9. **Slides 41–43**
   - separar claramente:
     MASTER primero, HAMMER después;
   - recién en MASTER explicar store-and-forward / no streaming durante captura.

10. **Slides 46–47**
    - preservar datos reales;
    - el waterfall `U(x,t)` debe ser uno de los visuales más grandes e importantes del deck.

11. **Slides auxiliares**
    - mantener fórmulas/detalles fuera del flujo principal;
    - cualquier fórmula eliminada de la presentación principal debería migrar al backup, no desaparecer.

12. **Timing**
    - objetivo 27–28 min;
    - la mayoría de slides deberían ser 20–40 s;
    - slides clave pueden tomar 60–90 s:
      - `Gmax = rho Vs^2`
      - inversión
      - `U(x,t)`
      - Ma et al.
      - resultado espacio–tiempo.

---

# Estilo visual deseado

- técnico, limpio, académico;
- no “Gamma-style” / tarjetas genéricas;
- poco texto;
- una idea por slide;
- títulos que expresen una conclusión, no solo el tema;
- mantener paleta actual:
  - azul oscuro;
  - teal;
  - naranja;
  - verde;
  - tierra para subsuelo;
- ecuaciones grandes solo si son parte de la narrativa;
- referencias discretas en pie de slide;
- figuras importantes grandes;
- usar placeholders solo donde aún falten fotos propias.

---

# Fuentes principales que deben preservarse

- Resumen / documento de tesis actual.
- Paper URUCON sobre DA-AFE.
- Foti et al. para ondas superficiales / MASW.
- Park et al. para MASW.
- Lin & Ashlock (2016) para dimensión espacial sintetizada.
- Ma et al. para compensación LF elegida.
- Pazos para extensión por carga/impedancia.
- Papers de force balance / negative resistance.
- Hakimitoroghi / zero-pole / inverse correction.
- Miller & Pursey para reparto de energía ideal de fuente vertical superficial.

No inventar detalles que no estén soportados por los papers/documentos.
