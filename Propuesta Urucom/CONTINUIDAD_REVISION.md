# Continuidad de la revisión del paper URUCON

Última actualización: 2026-07-22.

Este archivo conserva las decisiones, verificaciones y tareas del proceso de revisión para poder continuar en otra conversación sin reconstruir el contexto.

## Protocolo de revisión acordado

- Todo texto nuevo o modificado durante la iteración activa se marca en rojo mediante `\rev{...}`.
- La referencia al datasheet del PSoC `[7]` también permanece roja porque el autor pidió revisarla visualmente.
- Una vez que Elías apruebe una modificación, se retirará `\rev{...}` para devolverla a negro.
- Los cambios puramente de maquetación o de una imagen no admiten el mismo marcado tipográfico; se documentan aquí.
- Por ahora no se prioriza reducir páginas. Primero se busca corrección, claridad y cumplimiento de todos los comentarios; la compresión se hará después.

## Objetivo y alcance científico

- El paper trata del método de calibración automática de offset del circuito de acondicionamiento, no del diseño exhaustivo del circuito analógico.
- La validación del circuito analógico debe ser breve y presentarse como un chequeo inicial de consistencia.
- El estudio es una prueba de concepto experimental y exploratoria.
- No se afirma significancia estadística ni validación a nivel poblacional.
- El ensayo de campo demuestra integración/operación multicanal, pero no es una comparación controlada ni una validación del método.
- Los ensayos estadísticos confirmatorios, más placas, orden aleatorizado, sensibilidad de parámetros y pruebas controladas de campo quedan para trabajos futuros.
- El subsistema de calibración pertenece a un sistema IoT mayor. La formulación adoptada evita prometer un paper concreto: “This study addresses the analog calibration subsystem within a broader IoT acquisition system; distributed acquisition and communication are reserved for future work.”

## Autoría

- Orden: Elías D. Álvarez Martínez; Vicente González; Enrique A. Vargas Cabral.
- Elías es autor principal.
- Enrique es tutor principal.
- Correo de Vicente: `vgonzalez@uc.edu.py`.
- Correos presentados en el paper: `{elias.alvarez, vgonzalez, evargas}@uc.edu.py`.

## Introducción e hipótesis

- La hipótesis debe aparecer explícitamente en la introducción.
- Hipótesis actual: el recentrado secuencial por etapa, seguido por códigos DAC congelados durante adquisición, reduce el offset entregado al ADC frente a una referencia fija compartida en las condiciones que requieren corrección, sin insertar polos ni retocar el controlador por placa/ganancia.
- La justificación para no resolver la deriva con capacitores de acople es preservar la transferencia de baja frecuencia usada para recuperar dispersión de velocidades de ondas superficiales.
- Uno o varios capacitores de acople añadirían polos pasaaltos; para situarlos muy por debajo de la banda se requerirían capacitores grandes, externos y sensibles a tolerancia.
- Autozero/chopper se menciona como alternativa, pero no está disponible en los bloques analógicos seleccionados y exigiría circuito externo, debilitando la motivación de una implementación PSoC de un solo chip.
- La frase “This paper is organized as follows” aparece una sola vez, al final de la introducción, no en el abstract.

## Abstract

- Debe decir que es un “experimental proof of concept” y mantener el carácter exploratorio.
- La magnitud principal se nombra como offset medio de la etapa LP entregada al ADC, para dejar claro que se mide el estado que entra al convertidor.
- Se evita presentar el ensayo de campo como validatorio.
- No se incluye en el abstract el párrafo de organización del paper.

## Arquitectura y trabajo previo

- El circuito deriva del front end de baja frecuencia de Ma et al.; debe reiterarse al explicar la topología PGA–BP–SUM–LP.
- No es una cascada estricta de una sola entrada: SUM combina una rama directa desde PGA con la rama que pasa por BP.
- La formulación general usa “most stages remain DC-coupled” en vez de enumerar ramas innecesariamente.
- Para PGA, la suma de contribuciones aguas arriba está vacía, pero el término local incluye offset de entrada y desbalance de resistencias; por eso no debe insinuarse que el primer stage carece de offset.
- La ecuación de equilibrio no se refiere a capacitores entre etapas. Solo se aclara que no describe el asentamiento finito de amplificadores y estados de filtros analógicos/digitales después de conmutar etapa o coeficientes.
- Los trabajos previos de PSoC se describen como métodos anteriores que calculan/guardan correcciones numéricas; el presente trabajo, en cambio, modifica físicamente la referencia de nodos accesibles mediante VDAC.
- En modo calibración, multiplexer, ADC, filtro digital y control DAC se “repurpose” temporalmente como lazo mixto. El camino del sensor no se modifica.
- Los coeficientes del filtro digital se cambian explícitamente entre modos: respuesta del geófono en adquisición y FIR pasa-bajos de 128 taps para estimar DC en calibración.

## Convenciones del controlador

- `\hat y_i[n]`: cuenta ADC con signo y filtrada, proporcional a `V_stage - V_ref`.
- `r_i`: referencia deseada; vale cero porque el objetivo es `V_stage = V_ref`.
- `e_i[n] = \hat y_i[n] - r_i`; con `r_i=0`, queda `e_i[n]=\hat y_i[n]`.
- Los valores de resolución ADC/VDAC y spans son nominales del datasheet del PSoC.
- `q_DAC = 16 mV/code` es nominal.
- Los 4096 mV usados en el escalado representan el span ideal de 256 bins de cuantización (`256 × 16 mV`), no la salida máxima realizable del código 255.
- Explicación directa de la limitación de actualización: aunque el PI pida una corrección grande, el firmware mueve el VDAC de una etapa como máximo un código por cada nueva muestra filtrada procesada; además recorta el comando a los límites configurados de esa etapa, siempre dentro de 0–255.
- Si se alcanza un límite, se suspende la integración cuando el error intentaría empujar el comando todavía más afuera; esto evita windup.
- No se publica el vector numérico feo de inicialización; se llama `c_base`.

## Chequeo inicial del circuito y Figura 3

- No hubo fuente sísmica calibrada.
- Se usó un generador Agilent 33220A para barrer el front end con senoidales en tandas solapadas de 0.01 Hz a 200 kHz.
- Un Tektronix TDS 2004B registró entradas y salidas.
- La transferencia experimental de electrónica se definió como LP output / monitored PGA output (CH4/CH1), es decir, el camino desde la salida PGA monitoreada hasta la entrada del ADC.
- Para aproximar la cadena sensor–ADC, la respuesta experimental de electrónica se cascada en frecuencia con el modelo nominal de aceleración del SM-24. No debe describirse como una simple multiplicación de datos sin contexto.
- La figura no valida el sensor completo ni el método de calibración; es una comprobación inicial de forma. Una medición end-to-end con fuente sísmica calibrada queda como trabajo futuro.
- Verificación de normalización:
  - todas las curvas de magnitud mostradas están normalizadas;
  - el compuesto medido se fija a 0 dB en su máximo;
  - la cadena ideal y el sobre de potenciómetro 0–2 kΩ usan esa misma referencia;
  - las curvas aisladas de aceleración y velocidad del geófono se normalizan cada una a su propio máximo.
- Se eliminó la frase redundante que decía que la comparación solo enfatiza forma.
- La coherencia local de la medición cae por debajo de 0.9 aproximadamente a 0.84 kHz. El cuerpo del paper declara ahora ese criterio y usa una frontera gráfica redondeada de aproximadamente 1 kHz.
- La coherencia local se calcula como el término cruzado normalizado al cuadrado entre las señales analíticas de entrada y salida dentro de bins logarítmicos del sweep.
- La línea vertical dash-dotted de la Fig. 3 marca el inicio redondeado de la degradación. Por encima, la combinación de fuerte atenuación y coherencia no monótona impide una comparación de amplitud confiable con el modelo; la discrepancia se interpreta como limitada por la medición, no como transferencia comprobada del circuito.
- Script local del paper para regenerar la figura: `scripts/refine_analog_response_figure.m`.
- Artefacto usado por LaTeX: `Imagenes/analog_path_check.png`.

## Datos de calibración y Tabla II

- Placas: dos prototipos ensamblados independientemente, A y B.
- Conjunto principal real: ocho celdas placa–ganancia, todas con diez reinicios pareados:
  - Board A: ×1, ×4, ×16, ×32 y ×50;
  - Board B: ×16, ×32 y ×50.
- `N=10` significa reinicios repetidos de la misma placa/configuración, no diez dispositivos independientes.
- `c_base` se seleccionó empíricamente en Board B a ×50 y se reutilizó sin cambios en Board A y las demás ganancias.
- Para las mediciones del paper se deshabilitaron escrituras EEPROM posteriores a la calibración, de modo que cada reinicio estacionario volvió a cargar `c_base`.
- Board B ×1: existe un único registro baseline y no una corrida calibrada completa; se excluye.
- Board B ×4: con las bandas normales el estado baseline ya estaba dentro de banda y el algoritmo no hacía correcciones, por lo que no existe una condición “after” normal distinta. Se excluye de las métricas principales.
- Diagnóstico separado Board B ×4: tres pares con bandas más estrechas; LP antes 148/142/157 mV y después 34.4/38.5/53.5 mV. Se informa en la nota de la Tabla II, pero no se mezcla con las ocho celdas principales.
- La Tabla II usa líneas punteadas gris claro para separar ganancias y una línea vertical discontinua entre Board A y Board B.
- No se reclama significancia estadística. Los valores son media y desviación estándar muestral descriptivas.

## Medición con osciloscopio y Figura 4

- Equipo: Tektronix TDS 2004B, cuatro canales, 8 bits, 60 MHz.
- Ventana documentada por las fuentes primarias: 100 ms después de esperar el asentamiento del transitorio. El autor había escrito 1 s en un comentario posterior, pero `mediciones osciloscopio.txt` y ambos CSV de mediciones indican 100 ms; el manuscrito conserva 100 ms hasta que se confirme y se corrijan también los metadatos crudos si estos estuvieran equivocados.
- Los cuatro ground clips se conectaron a `V_ref = V_DDA/2`; cada canal midió `V_stage - V_ref`.
- Como el PC alimentado por USB estaba sin tierra y el osciloscopio sí estaba unido a protective earth, esa conexión fijó `V_ref` a tierra durante la medición. No se caracterizaron otros caminos de fuga.
- En cada reinicio se midió primero fixed-reference y después calibrated. Esto preserva el pareo, pero el orden nunca aleatorizado deja la deriva lenta como posible confusor.
- La Fig. 4 aplica a los registros del osciloscopio exactamente los coeficientes FIR de 128 taps cargados durante calibración.
- Las líneas grises claras son datos del osciloscopio; las curvas de color son reconstrucciones externas de lo que aproximadamente ve el controlador.
- No son logs internos y no reproducen muestreo ADC nativo, conmutación de etapas, resets ni aritmética fixed-point.
- Se eliminó “aggressive FIR”; se describe simplemente como el FIR pasa-bajos empleado para estimar DC.

## Campo, limitaciones y futuro

- Entre laboratorio y campo, el único evento observado que produjo timeout fue energizar una placa mientras el geófono estaba en movimiento; el transitorio AC saturó la cadena y violó la hipótesis cuasiestática.
- El registro 10–50 m solo demuestra operación e integración multicanal.
- Resolución finita del DAC, ruido/distorsión, vibración sostenida, deriva térmica y transitorios lentos de estado del filtro se presentan como aspectos por estudiar o mejorar, no como una lista cerrada de defectos.
- El sistema IoT completo, incluyendo adquisición distribuida y comunicación, queda para trabajos futuros.

## Referencias y acknowledgments

- Es razonable citar el datasheet del PSoC para especificaciones del dispositivo: CPU, DMA, ADC, VDAC, rangos y resolución nominal. No debe usarse como sustituto de literatura científica para justificar novedad o eficacia.
- La cita `[7]` está roja para que Elías decida si conservarla y/o dividir el respaldo entre datasheet y application notes.
- Se eliminó por completo el acknowledgment sobre uso de Claude/Codex.

## Maquetación actual

- La Fig. 1 se adelantó en el código para aparecer en la cabecera de la página 2.
- El flowchart usa prioridad de flotante superior y aparece en la cabecera de la página 3.
- La Fig. 3 contiene la línea vertical próxima a 1 kHz y la leyenda textual se explica en el caption y en el cuerpo.
- La compilación actual produce seis páginas. No se ha intentado todavía comprimir el paper.

## Chat compartido con el tutor

- Se leyó completo el enlace compartido “Análisis metodología trabajo” el 2026-07-22.
- Sus cambios considerados necesarios ya están cubiertos en el manuscrito actual:
  - proof of concept explícito en abstract, introducción y conclusión;
  - `N=10` definido como reinicios y no dispositivos;
  - condición de geófono estacionario;
  - LP identificado como resultado principal que alimenta al ADC;
  - ensayo de campo presentado solo como demostración funcional;
  - parámetros seleccionados empíricamente y mantenidos fijos;
  - “Default” sustituido por “Fixed-reference baseline”;
  - Board B ×1/×4 explicado junto con los guiones de la Tabla II;
  - Fig. 4 distingue mediciones de osciloscopio y estimaciones FIR reconstruidas, sin presentarlas falsamente como logs internos.
- Recomendaciones opcionales del tutor todavía no forzadas:
  - reorganizar la discusión en tres subsecciones: desempeño/deadbands, tiempos/restricciones operativas y alcance/limitaciones;
  - añadir marcadores visuales de inicio/cambio de etapa/final en la Fig. 4;
  - ampliar para una futura versión de revista con más placas, temperatura, deriva, ablación, comparación de técnicas, estadística confirmatoria y campo antes/después.
- Se mantuvo una precisión más conservadora que la última sugerencia del chat para la Fig. 4: las curvas coloreadas aproximan la información filtrada usada por el controlador, pero son reconstrucciones externas de los registros del osciloscopio y no estados internos registrados.

## Archivos principales

- Documento maestro: `Urucom.tex`.
- Preamble y macro roja: `config/preamble.tex`.
- Autores: `frontmatter/title_authors.tex`.
- Abstract: `sections/00_abstract_keywords.tex`.
- Introducción: `sections/01_introduction.tex`.
- Arquitectura: `sections/02_platform_design.tex`.
- Controlador: `sections/03_self_calibrating_platform.tex`.
- Experimentos: `sections/04_experimental_validation.tex`.
- Discusión: `sections/05_discussion.tex`.
- Conclusión: `sections/06_conclusion.tex`.
- PDF compilado: `Urucom.pdf`.

## Próxima iteración sugerida

1. Elías lee únicamente el texto rojo y anota comentarios nuevos en los `.tex`.
2. Se responde uno por uno a sus comentarios y se corrigen solo los puntos rechazados.
3. Lo aprobado se convierte de rojo a negro.
4. Recién después se estudia reducción de páginas y compactación final.
5. Antes de entrega se hace una revisión estadística/metodológica final y se elimina todo el marcado rojo restante.

## Iteración 2026-07-23 — primera base de compresión (solo texto)

Objetivo nuevo del autor: **reducir de 6 a 5 páginas** (límite duro URUCON, incluye
refs), eliminar reiteraciones y usar cross-refs en vez de resúmenes recurrentes.
Alcance de esta pasada: **solo texto** (sin tocar geometría/ubicación de figuras/tablas).

Protocolo rev aplicado: se limpiaron las marcas rojas previas (dash-dotted en caption de
Fig. 3) como aceptadas; todo texto nuevo/reescrito de esta pasada va en `\rev{}`.

### Cambios marcados en rojo (`\rev`) — para revisar
- **Abstract** (`00`): reemplazado por la versión del tutor comprimida (~150 palabras).
  Añade el encuadre de rango dinámico microvolt, aclara que cada restart se midió en
  ambas condiciones, y atribuye el mayor residual al PGA (respuesta wideband sin filtrar).
- **Introducción** (`01`): reescrita integrando las mejoras del tutor comprimidas:
  encuadre microvolt/saturación y no-escalabilidad del trimming manual; prior work en
  **3 líneas** (numérico → body-bias → autozero/chopper); contribuciones + "organized as
  follows" en un solo párrafo.
- **§IV Board B ×1/×4** (`04`): párrafo de exclusión comprimido + cross-ref a §pga-note
  (donde ya viven los números del diagnóstico de bandas estrechas).
- **§V future work** (`05`): las dos listas de trabajo futuro (efectos físicos +
  metodológica) consolidadas en **una sola lista canónica**.
- **§VI Conclusión** (`06`): reescrita; ya **no repite los números** del abstract;
  cross-ref a §IV (resultado) y §V (trabajo futuro).

### Cambios NO marcables (deleciones/limpieza) — documentados aquí
- `00`: borrado el abstract comentado viejo.
- `01`: borrados todos los párrafos comentados muertos (`%...`) que inflaban el archivo.
- Nota de Tabla II (`04`): quitadas las frases de "N = restarts, no dispositivos" y de
  exclusión de Board B (ambas ya están en el cuerpo/caption → dedup).
- Captions Fig. 4 y waterfall (`04`): recortada la prosa que solo repetía el cuerpo
  (reconstrucciones-no-logs; "not a controlled comparison").
- `05`: quitada la frase "One initialization selected on Board B at ×50 transferred…"
  (repetía la selección de `c_base` de §IV).

### Estado de páginas tras esta pasada
- Compila **limpio** (0 overfull hbox, 0 refs sin resolver) pero **sigue en 6 páginas**.
- Diagnóstico preciso: el cuerpo + figuras llenan exactamente 5 páginas; **las 18
  referencias completas caen enteras en la página 6**. La página 5 está dominada por la
  **Fig. 3 full-width (`figure*`)**, que ocupa ~media página; por eso el recorte de texto
  solo no alcanza para subir las referencias a la pág. 5.
- **Palanca real para cerrar la 6ª página**: geometría de figuras (diferida por el autor)
  — p. ej. Fig. 3 (y/o Fig. 1) de `figure*` full-width a una columna, o reducir su alto.
  Queda pendiente de autorización para la próxima pasada.
