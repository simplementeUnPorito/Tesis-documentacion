# Base de conocimiento para la reestructuración de la Primera Presentación

**Proyecto:** Diseño e implementación de un sistema electrónico multicanal del tipo IoT para caracterización geotécnica del suelo mediante ondas sísmicas  
**Fecha de consolidación:** 2026-08-27  
**Estado:** análisis previo; todavía no se autoriza la edición del TeX ni la creación/edición del PPTX  
**Documento principal a revisar posteriormente:** `docs/Primera Presentación/latex-15p-review/main.tex` y su salida `main.pdf`

Este archivo conserva las decisiones del tesista, las observaciones del tutor, las restricciones reglamentarias, la evidencia que ya existe en el repositorio y los puntos que todavía deben aclararse. Su objetivo es evitar releer toda la documentación cada vez que se retome el trabajo y, sobre todo, impedir que se confundan resultados demostrados, resultados de procesamiento, hipótesis y trabajos futuros.

---

## 1. Decisiones y aclaraciones dadas por Elías

1. El entregable inmediato es el documento de **máximo 15 páginas**.
2. En paralelo o después se preparará un **PPTX auxiliar para la presentación verbal**. Debe cumplir dos funciones:
   - guiar la exposición principal;
   - contener diapositivas auxiliares o de respaldo para responder preguntas de los evaluadores, aunque no se lleguen a mostrar durante la exposición normal.
3. Antes de editar se hará una fase de análisis y conversación. No se debe modificar todavía el TeX ni armar el PPTX.
4. Para la primera entrega se utilizará preferentemente **la evidencia que ya existe**. No se forzarán nuevas campañas ni ensayos apurados.
5. Elías continuará posteriormente con experimentos y verificaciones pendientes.
6. La medición de sincronización hecha con osciloscopio **no quedó registrada en archivos**. Debe repetirse y guardarse; por ahora no constituye evidencia metrológica reproducible.
7. No existe hoy un conjunto de varios nodos GEO operativos que permita demostrar una adquisición multicanal simultánea completa. Todas las iteraciones universales llegaron a funcionar en algún momento, pero una placa dejó de hacerlo después de modificaciones y se está desarrollando un modelo casi final.
8. La campaña Canchita se hizo cerca, pero no en el mismo punto, que los SEV del informe hidrogeológico. Elías estima una separación aproximada de 200 m al punto más cercano. El cálculo nominal realizado desde el plus code y las coordenadas UTM del informe da aproximadamente 120 m al SEV 01; como no se guardaron las coordenadas de los extremos de la línea MASW, la distancia debe tratarse como aproximada y del orden de cientos de metros, no como una coincidencia puntual demostrada.
9. Ubicación comunicada para Canchita: plus code `M9F6+Q95, Asunción 001303`.
10. Los diagramas Draw.io preparados deben conservarse como fuente visual potencial para el informe y el PPTX.
11. El arreglo sintético se adoptó por una **restricción de disponibilidad institucional**: la Facultad dispone solamente de dos geófonos. No fue una decisión de arquitectura ideal ni una afirmación de que la simultaneidad sea innecesaria.
12. Para el resultado principal se utilizará por ahora el perfil simplificado de tres capas. La justificación debe ser la separación de incertidumbre entre dato y optimizador, no solamente un CV menor.
13. La profundidad se comunicará como un resultado técnico prometedor del orden de 10–11 m; 11,83 m quedará como detalle mínimo de una configuración. Debe declararse que hacen falta más estudios y validaciones.
14. La caracterización del 21 de julio se considerará representativa de la ruta analógica usada en Canchita porque los cambios posteriores fueron digitales, de autocalibración y de ganancia; los polos y la topología de señal se mantuvieron. Esta equivalencia no convierte el barrido en una calibración E2E ni valida automáticamente cada ajuste de ganancia.
15. El contraste SEV aparecerá brevemente en el PDF y su desarrollo completo quedará para material auxiliar.
16. En Canchita se utilizó un solo nodo GEO desplazado. Existieron varias placas universales funcionales con cambios progresivos de detalles de implementación y asignación de pines, pero la campaña se realizó con un único nodo. Actualmente se trabaja en una placa por transferencia de tóner/planchado y ataque con ácido, previa a solicitar PCB fabricadas en China.
17. La geometría de Canchita se materializó con un punto de impacto fijo situado a unos metros frente al arco de fútbol. Sólo se desplazó el GEO, siguiendo una línea paralela a los laterales de la cancha. No existe todavía un relevamiento manual de coordenadas y azimut.
18. La exposición principal durará aproximadamente 30 minutos. Después se realizarán las preguntas; no se requiere demostración en vivo. Los evaluadores previstos son Fernando Brunetti, Enrique Vargas y Vicente González.
19. La portada cuenta dentro del límite de 15 páginas. Para no consumir una página completa, se mantendrá el esquema compacto actual: título y datos iniciales integrados al comienzo del documento, sin portada independiente.
20. El artículo de Guan et al. sobre Mini-Sosie se incorporó originalmente como referencia para una fuente repetitiva. La intención de Elías es explorar impactos periódicos controlados para reforzar componentes de baja frecuencia mediante la frecuencia de repetición y sus armónicos. Esta idea es una estrategia futura, no una capacidad ya demostrada por el martillete actual.
21. Elías sí realizó un ensayo exploratorio con el mazo usado hasta ahora, golpeando aproximadamente cada 1 s durante una ventana de 60 s. Sólo conservó dos capturas de pantalla, no el registro crudo. Ese ensayo originó la hipótesis de acumular energía coherente con una fuente periódica.
22. Lin y Ashlock (2016) se utilizará para justificar que la caracterización de ondas superficiales con un solo geófono es una alternativa técnicamente estudiada y de interés para campañas futuras con recursos limitados. No se presentará como validación exacta ni como protocolo idéntico al usado en Canchita.
23. La investigación bibliográfica adicional sobre acumulación coherente de impactos, Mini-Sosie, secuencias codificadas y barrido de frecuencia será realizada en paralelo por otra IA mediante un prompt preparado en esta conversación. Codex no realizará esa búsqueda en esta fase; sus resultados deberán revisarse contra fuentes primarias antes de incorporarlos.
24. En Canchita el punto de impacto permaneció fijo a unos metros frente al arco y sólo se desplazó el GEO. La campaña corresponde a un arreglo receptor secuencial con fuente repetida, no a una ejecución exacta de MSOR.
25. El ensayo manual de impactos repetidos se realizó frente al Laboratorio LED, entre el camino y el estacionamiento. La distancia fuente–GEO se estimó inicialmente en unos 20 m y una medición aproximada en Google Maps dio 26,8 m; se conservará como aproximadamente 20–27 m.
26. En ese ensayo HAMMER y `Geo1` se adquirieron juntos. El generador se trata como un esclavo más y los nodos inician el muestreo sincronizados. Esto documenta adquisición conjunta, pero no reemplaza la medición metrológica de sincronización pendiente.
27. La cadencia manual buscó aproximadamente un golpe por segundo, pero varió durante el registro. Los picos cercanos a 0,5, 1 y 2 Hz mencionados en el TeX provienen de otra medición.
28. El PPTX deberá contener un banco amplio de diapositivas auxiliares porque no habrá demostración en vivo y las preguntas se realizarán después de la exposición principal.
29. Las dos capturas preservadas del ensayo manual —señal temporal y espectro— son dos vistas del mismo registro de 60 s.
30. La medición separada en la que se observaron componentes próximas a 0,5, 1 y 2 Hz también se realizó frente al Laboratorio LED. No se conserva por ahora información suficiente para reconstruir cuantitativamente esa adquisición, por lo que se mantiene como antecedente exploratorio y no como resultado demostrable.
31. El informe crítico externo recibido el 27 de agosto confirma que una fuente repetitiva puede mejorar la detectabilidad mediante acumulación coherente, con una mejora ideal de SNR proporcional a $\sqrt{N}$ bajo hipótesis de repetibilidad y ruido no correlacionado. También advierte que una cadencia fija produce un peine espectral en la frecuencia de repetición y sus armónicos, no una banda continua ni energía nueva donde la cadena fuente–suelo–sensor–electrónica no tenga respuesta.
32. El martillete se describirá por ahora como **fuente repetitiva de impacto de cadencia controlada** o **fuente tipo Mini-Sosie en desarrollo**, no como Mini-Sosie validado. El modo fijo de 45 rpm se utilizará conceptualmente como condición de referencia; una estrategia de banda más ancha requeriría estudiar secuencias aperiódicas, pseudoaleatorias o barridas, registrar los tiempos reales de impacto y decodificar/apilar de forma coherente.

---

## 2. Jerarquía de fuentes y criterio de autoridad

### 2.1 Fuentes normativas y de revisión

| Prioridad | Fuente | Uso |
|---|---|---|
| 1 | `docs/Primera Presentación/Reglamento_de_PFC_noviembre_2023.pdf` | Restricciones formales del entregable y evaluación |
| 2 | `docs/Primera Presentación/Revision_estructura_trabajo_caracterizacion_suelos_v2.pdf` | Requerimientos narrativos y técnicos del tutor |
| 3 | Aclaraciones de Elías registradas en este archivo | Alcance, estado real del hardware y decisiones de presentación |

### 2.2 Fuentes técnicas principales

| Fuente | Papel |
|---|---|
| `docs/Primera Presentación/latex-15p-review/main.pdf` | Estado actual del entregable de 15 páginas |
| `docs/Primera Presentación/latex-15p-review/` | Fuente TeX que se editará cuando termine la fase de discusión |
| `src/calculos_modelados/python/masw_bench/informe/INFORME_COMPLETO.pdf` | Benchmark MASW consolidado posterior al PDF actual |
| `src/calculos_modelados/python/masw_bench/informe/md/00_INFORME_PRINCIPAL.md` | Síntesis trazable de los resultados del benchmark |
| `src/calculos_modelados/python/masw_bench/HALLAZGOS.md` | Auditorías, correcciones y límites de interpretación del benchmark |
| `src/calculos_modelados/python/masw_bench/FINAL_MEASUREMENTS.md` | Estado cuantitativo del dataset y planificación de mediciones futuras |
| `src/calculos_modelados/python/masw_bench/10_CONTRASTE_HIDROGEOLOGICO.md` | Contraste explícito MASW–SEV y sus cautelas |
| `docs/investigacion/sources/INFOR_HIDROGEO_CYT_UC_AS_JUL_2023.pdf` | Fuente primaria hidrogeológica de julio de 2023 |
| `data/processed/Canchita_procesado/manifest.json` | Inventario de la campaña procesada |
| `src/interfaces/python/geophone_scope/kalman_deconv/reports/velocity_model_fix_2026-08-17/velocity_fix_metrics.json` | Métricas espectrales del procesamiento del 17 de agosto |
| `src/calculos_modelados/matlab/AnalisisCircuito/resultados_verificacion_calibracion_2026-07-21/` | Barridos y ajuste de la cadena analógica |

### 2.3 Artículos candidatos aportados el 27 de agosto

| Fuente | Aporte defendible | Límite de uso |
|---|---|---|
| Lin y Ashlock (2016), `lin2016.pdf`, DOI `10.1016/j.soildyn.2016.04.013` | Demuestra que la simulación multicanal con un solo receptor (MSOR) es una alternativa técnicamente estudiada. Incluye simulaciones y casos de campo, compara MASW con MSOR y resulta especialmente pertinente cuando el costo, la portabilidad o la disponibilidad de sensores son restricciones. Se usará como motivación para campañas futuras con un solo GEO. | Su MSOR fija el receptor y desplaza el impacto; no es el mismo protocolo que Canchita. No debe presentarse como validación exacta de nuestro gather. Exige impactos repetibles, trigger consistente y posiciones precisas. |
| Gao y Pan (2018), `ggy063.PDF`, DOI `10.1093/gji/ggy063` | Propone estimar la firma de fuente mediante una fuente real virtual con separación modal. Es pertinente para explicar por qué conocer la wavelet/firma del martillo mejora la trazabilidad y puede ayudar a una futura inversión de forma de onda. | No justifica el nodo virtual desplazado ni el martillete periódico. Requiere dos shot gathers, geometría específica, condición de campo lejano y separación de modos; además recupera una firma escalada, no su magnitud absoluta. |
| Guan et al. (2022), `ggac169.PDF`, DOI `10.1093/gji/ggac169` | Describe Mini-Sosie de impactos periódicos y su combinación con un arreglo lineal. Los impactos a frecuencia fija concentran energía en la frecuencia de repetición y sus múltiplos; el artículo usa esas líneas como referencias de velocidad de fase para corregir una imagen pasiva sesgada. | No demuestra que nuestro martillete ya produzca esa secuencia ni que la energía baja observada se propague. Una cadencia periódica refuerza líneas discretas y distorsiona/suprime el resto del espectro; para cubrir una banda continua haría falta barrer la tasa de impacto o usar una secuencia codificada apropiada. |

Los tres artículos son útiles, pero no cumplen la misma función. Lin justifica la factibilidad y el interés de métodos con un solo geófono para campañas futuras; Guan sustenta la estrategia futura de excitación periódica; Gao y Pan es material secundario para caracterización de la firma de fuente y posiblemente quede mejor en el PPTX auxiliar o en trabajo futuro si falta espacio en las 15 páginas.

`Guan2022` y `Park1996SIST` ya existen en `latex-15p-review/referencias.bib`. Lin y Ashlock (2016) y Gao y Pan (2018) todavía no tienen entrada bibliográfica en esa fuente. No agregarlas hasta iniciar la fase autorizada de edición.

### 2.4 Fuentes visuales disponibles

| Fuente | Contenido relevante |
|---|---|
| `docs/Primera Presentación/Diagramas_operativos_y_calibracion.drawio` | Arquitectura completa, flujo operativo, nodos, sincronización, almacenamiento, fuente–geófono–AFE, calibración, PSoC y servidor |
| `docs/Primera Presentación/SuperMaquina_hardware_digital_y_fsm.drawio` | Hardware digital interno y FSM detallada |

### 2.5 Carpetas históricas

`latex`, `latex-historial` y `latex-nueva-estructura` contienen material útil y figuras reutilizables, pero la fuente de verdad del entregable actual es `latex-15p-review`. No deben editarse variantes históricas por accidente.

---

## 3. Restricciones del Reglamento de PFC

Fuente: `docs/Primera Presentación/Reglamento_de_PFC_noviembre_2023.pdf`, revisión de noviembre de 2023.

### 3.1 Artículo 19: Primera Presentación

El artículo 19 exige presentar:

- una solicitud para realizar la Primera Presentación, con visto bueno del Director del PFC;
- una copia electrónica del documento del **Estado del Arte previamente aprobado por el Director del PFC**;
- un documento de **máximo 15 páginas incluyendo la bibliografía**.

Consecuencia operativa: el PDF actual ya tiene 15 páginas, por lo que toda incorporación exige sustituir, condensar o retirar contenido. No hay margen para agregar páginas.

### 3.2 Artículo 23: evaluación de la Primera Presentación

La Primera Presentación vale 25 puntos. De esos 25 puntos, **5 puntos evalúan el orden, la calidad y la claridad de la exposición**.

Consecuencia: el informe y el PPTX deben coordinarse, pero no duplicarse literalmente. El PDF sostiene el argumento académico y la trazabilidad; el PPTX debe optimizar la explicación oral, el ritmo y la respuesta a preguntas.

### 3.3 Artículo 3: naturaleza del PFC

El reglamento admite trabajo de investigación, implementación o combinación de ambos. Para las dos modalidades exige fases de:

- compilación y análisis de información;
- formulación del problema o tecnología;
- especificación de metodología;
- diseño de la solución;
- implementación;
- validación de resultados.

Esto es consistente con el pedido del tutor: el centro puede seguir siendo la ingeniería electrónica, pero las decisiones de diseño deben derivarse del problema físico y culminar en una validación explícita.

### 3.4 Tratamiento de la portada

Elías confirmó que la portada cuenta dentro de las 15 páginas. No se utilizará una portada independiente: se conservará el esquema compacto del documento existente, con título y datos iniciales integrados al comienzo.

### 3.5 Objetivo formal aprobado y profundidad de 50 m

La propuesta de PFC localizada en `docs/Propuesta Tesis UCA/propuesta_tesis_geofonos_iot_final_2paginas.tex` establece como objetivo general:

> Diseñar, implementar y evaluar experimentalmente un sistema electrónico multicanal [...] orientado a la caracterización geotécnica del suelo en profundidades máximas de hasta 50 metros.

Por tanto, los 50 m no pueden eliminarse como si nunca hubieran formado parte del proyecto. Deben diferenciarse tres niveles:

- **objetivo formal de diseño:** hasta 50 m;
- **alcance demostrado con la campaña y cadena actuales:** aproximadamente 10–11 m;
- **brecha y hoja de ruta:** aumentar energía coherente en baja frecuencia, validar la respuesta real sub-10 Hz, adaptar fuente/geometría y repetir la adquisición.

Este objetivo formal del PFC no debe confundirse con la propuesta anterior de financiación PINV mencionada en el PDF actual, que no fue aceptada. Son antecedentes distintos.

---

## 4. Qué pide el tutor

Fuente: `Revision_estructura_trabajo_caracterizacion_suelos_v2.pdf`.

### 4.1 Diagnóstico general

El tutor considera que el contenido técnico y el desarrollo de ingeniería son buenos, pero que la organización está demasiado orientada a componentes y etapas de construcción. El cambio requerido no es cosmético ni consiste solamente en renombrar secciones: debe cambiar la lógica causal del trabajo.

### 4.2 Hilo narrativo solicitado

> Problema geotécnico → propiedades mecánicas → propagación de ondas → ondas superficiales y dispersión → selección de MASW → requerimientos instrumentales → diseño electrónico → caracterización del instrumento → validación controlada/campo → resultados → limitaciones.

### 4.3 Estructura recomendada

1. Importancia de la caracterización geotécnica y significado de Vs.
2. Métodos tradicionales: SPT, CPT/CPTu, downhole, crosshole y otros pertinentes.
3. Métodos basados en ondas mecánicas.
4. Fundamentos de propagación estrictamente necesarios para la medición.
5. Ondas P, S, Rayleigh y Love; relación `lambda = c/f` y profundidad.
6. Dispersión de ondas superficiales y cadena registros → dispersión → inversión → `Vs(z)`.
7. Comparación y selección de SASW/MASW y otros métodos.
8. Derivación de requerimientos: banda, canales, separación, sincronización, SNR, rango dinámico y fase.
9. Diseño e implementación: transductor, AFE, ADC, sincronización, comunicaciones, adquisición y procesamiento.
10. Validación experimental: electrónica/metrológica, adquisición controlada y una campaña MASW representativa.
11. Resultados preliminares diferenciando demostración e interpretación.
12. Limitaciones y trabajos futuros.

### 4.4 Criterio sobre casos de aplicación

- Los casos no deben ocupar un bloque autónomo y extenso.
- El caso de campo debe validar el instrumento, no convertir el documento en un estudio geofísico independiente.
- Debe priorizarse una caracterización electrónica rigurosa sobre una gran cantidad de campañas.
- La interpretación geológica debe limitarse a lo necesario para evaluar plausibilidad.

### 4.5 Aspectos que el tutor pide reforzar

- magnitud y fase extremo a extremo;
- ruido y ENOB;
- repetibilidad;
- dispersión entre canales;
- referencia geofísica independiente;
- profundidad efectivamente defendible con el SM-24 y la energía medida;
- separación explícita entre demostrado, preliminar y futuro;
- relación visible entre cada especificación electrónica y el requerimiento físico/geofísico que la origina.

---

## 5. Diagnóstico del PDF actual de 15 páginas

Fuente revisada visualmente: `latex-15p-review/main.pdf`, 15 páginas, formato A4 a dos columnas.

### 5.1 Fortalezas existentes

- El título deja claro que el proyecto es un sistema electrónico multicanal IoT aplicado a caracterización geotécnica.
- Ya se explica la utilidad del modelado del subsuelo, las ondas de cuerpo y superficie, dispersión, inversión y no unicidad.
- Existe una comparación funcional de métodos.
- Se explican el SM-24, su modelo dinámico y la necesidad de compensación.
- Se muestran el AFE, ADC, memoria, arquitectura digital, interfaces y servidor.
- Se incluyen datos reales de Canchita, un registro sintetizado, una imagen de dispersión y análisis espectral.
- El texto actual ya contiene cautelas correctas: no presenta la compensación como validación sísmica extremo a extremo y distingue algunas propuestas aún no medidas.

### 5.2 Problemas narrativos

- Los casos de aplicación aparecen pronto y consumen espacio antes de cerrar la derivación del problema instrumental.
- Los requerimientos MASW están dispersos; falta una sección puente compacta y explícita que conecte física con electrónica.
- La excitación aparece antes de que se consoliden los requerimientos instrumentales.
- Los capítulos electrónicos comienzan principalmente desde componentes y bloques, no desde las magnitudes que deben preservarse.
- La validación, los resultados y las limitaciones aparecen mezclados dentro de las secciones de implementación.
- No existe una tabla o mapa único del tipo **requerimiento geofísico → especificación electrónica → evidencia disponible → estado**.
- La parte matemática es técnicamente rica, pero puede condensarse para liberar espacio a la cadena causal y a los resultados ahora disponibles.

### 5.3 Estado del resultado geofísico en el PDF actual

Las páginas 13–14 muestran el registro de Canchita, dispersión y energía espectral, pero declaran que antes de aceptar un perfil `Vs(z)` faltan selección, incertidumbre, repetibilidad, geometría y comparación independiente. Esta afirmación era razonable al generar el PDF del 20 de agosto.

El benchmark consolidado del 23 de agosto es posterior y completa una parte sustancial de esos pendientes. Por tanto, el PDF actual quedó técnicamente desactualizado en ese punto y puede incorporar un resultado geofísico preliminar mejor defendido, con sus límites.

---

## 6. Inventario de evidencia existente

## 6.1 Campaña Canchita y naturaleza del arreglo

Fuentes: `data/processed/Canchita_procesado/manifest.json`, metadatos de `data/raw/Canchita` y benchmark MASW.

| Magnitud | Evidencia |
|---|---|
| Geometría | 21 posiciones entre 10 y 50 m, paso nominal de 2 m, apertura de 40 m |
| Construcción del arreglo | Arreglo sintético construido moviendo un solo geófono GEO entre posiciones |
| Disponibilidad institucional | Solo dos geófonos disponibles en la Facultad; esta restricción motivó el protocolo secuencial |
| Fuente/trigger | Un nodo HAMMER y un nodo GEO activos por registro |
| Registros/golpes candidatos | 607 en la auditoría del benchmark |
| Incluidos en el manifest procesado | 598 |
| Omitidos | 9 |
| Golpes por distancia | 20–37; mediana aproximada 30 |
| Frecuencias de muestreo presentes | 1020 Hz y 2929 Hz |

### Consecuencia epistemológica

La campaña sí permite:

- demostrar adquisición de señales de campo con el nodo GEO;
- construir un gather activo equivalente porque la fuente impulsiva puede repetirse y cada traza se referencia al golpe;
- calcular una imagen/curva de dispersión;
- ejecutar una inversión preliminar;
- evaluar sensibilidad a offsets, golpes, transformada, picker y semilla.

La campaña **no permite**:

- demostrar 21 canales físicos simultáneos;
- demostrar sincronización entre 21 nodos GEO;
- medir dispersión metrológica entre canales;
- demostrar igualdad de ganancia/fase entre múltiples placas;
- aplicar correctamente métodos pasivos como ReMi, ESAC o SPAC clásico, porque el ruido ambiental no puede repetirse al mover un solo sensor.

La expresión recomendada es **“registro multicanal sintetizado por posiciones con fuente activa repetible”**, no “adquisición simultánea de 21 canales”.

La razón del protocolo debe explicarse con naturalidad: el sistema objetivo es multicanal, pero la validación de campo disponible tuvo que sintetizar el arreglo debido a que la Facultad cuenta con solo dos geófonos. Esto justifica el método experimental sin convertirlo en evidencia de simultaneidad. En una defensa oral conviene separar explícitamente:

- **capacidad arquitectónica buscada:** varios nodos GEO sincronizados;
- **validación realizada con los recursos disponibles:** un GEO desplazado entre 21 posiciones y una fuente activa repetible;
- **validación futura:** varios GEO operativos adquiriendo simultáneamente.

### Fundamento bibliográfico y selección posterior del subarreglo

Lin y Ashlock (2016) demuestran la factibilidad práctica de un método de ondas superficiales con un solo receptor mediante reciprocidad. Su comparación de campo empleó un geófono fijo con impactos desplazados sobre offsets de 3 a 49 m y `dx = 2 m`, y obtuvo imágenes de dispersión MSOR y MASW comparables. El artículo también advierte que la equivalencia práctica depende de la repetibilidad del impacto, del trigger y de la posición; recomienda registrar varios impactos por offset, seleccionar el subconjunto más repetible y apilarlo.

En el documento de 15 páginas esta referencia no se usará para afirmar que Canchita replicó MSOR ni para validar retroactivamente el gather. Su función será más acotada: mostrar que **trabajar con un solo geófono no es una improvisación sin antecedentes** y proponer MSOR como una alternativa interesante para próximas campañas condicionadas por la disponibilidad institucional. La geometría real de Canchita se explicará por separado a partir de los metadatos y de la descripción de Elías.

Canchita no se adquirió solamente en el subarreglo final. Se relevaron **21 posiciones entre 10 y 50 m** para preservar una geometría amplia y permitir evaluar posteriormente qué parte del tendido aportaba una curva más consistente. El benchmark barrió **26 subarreglos contiguos**. Los medio-lejanos, que comienzan aproximadamente entre 18 y 26 m, superaron al arreglo completo y al cercano en ajuste y soporte de longitudes de onda.

La interpretación física registrada en el benchmark es que los offsets bajos presentan mayor contaminación compatible con campo cercano y modos superiores, mientras que los muy lejanos sufren atenuación, menor SNR y mayor sensibilidad a puntos individuales. Esta explicación debe formularse como **interpretación consistente con los resultados**, no como una separación de campo cercano demostrada mediante un ensayo independiente. El resultado cuantitativo es:

- `10–50 m` completo: misfit aproximado de 2,28 %, soporte cercano a 8,81 m en el score corregido;
- `18–46 m`: misfit aproximado de 1,85 %, soporte cercano a 10,06 m en el score corregido; en el ranking anterior alcanzó 11,83 m con ambas convenciones;
- `22–42 m`: misfit aproximado de 1,36 %, soporte cercano a 10,75 m y base del estudio de tres capas;
- `30–50 m`: descalificado por misfit de aproximadamente 16,5 %;
- `22–38 m`: descalificado porque 38 % de la curva quedó sobre el límite de aliasing.

La selección fue **posterior a la adquisición** y debe declararse así. Para evitar apariencia de selección oportunista se mostrarán el rango completo medido, el criterio aplicado a todos los subarreglos y la limitación más fuerte: quitar sólo los offsets de 32 y 40 m desplaza `c(f)` unos 29,76 m/s RMS. La geometría sigue siendo frágil y exige repetición independiente.

## 6.2 Energía y SNR de campo

Fuente: `velocity_fix_metrics.json`, 21 posiciones.

| Banda | SNR mediana | Observación |
|---|---:|---|
| 1–10 Hz | 8,27 dB | Muy variable; mínimo aproximado −4,26 dB, máximo 17,51 dB |
| 10–50 Hz | 27,23 dB | Banda de mejor desempeño; mínimo 8,36 dB, máximo 40,77 dB |
| 50–80 Hz | 15,69 dB | Utilidad menor y más expuesta a aliasing espacial |
| 80–200 Hz | 3,29 dB | Poco útil para el objetivo MASW actual |

Otros indicadores:

- coherencia adyacente mediana en 10–50 Hz: aproximadamente 0,732;
- fracción mediana de energía en 10–50 Hz: aproximadamente 97,1 %;
- fracción mediana de energía en 1–10 Hz: aproximadamente 0,74 %.

Interpretación defendible: el cuello de botella de profundidad es la energía/coherencia de baja frecuencia, no la frecuencia de muestreo del ADC. Estas métricas son de campo y no sustituyen una medición de ruido referido a entrada, ENOB o rango dinámico del instrumento.

### 6.2.1 Mini-Sosie y martillete como estrategia para baja frecuencia

Guan et al. (2022) no usan los impactos periódicos para generar una banda baja continua. Con un intervalo fijo `T`, la secuencia concentra energía coherente en `f_0 = 1/T` y en múltiplos enteros de `f_0`. En el artículo estas líneas se usan como referencias de velocidad de fase para corregir la desviación de una imagen obtenida con ruido pasivo direccional.

Aplicado al proyecto, el concepto permite plantear un modo futuro del martillete:

1. imponer una cadencia controlada y registrar cada impacto;
2. elegir o barrer la cadencia para colocar energía coherente dentro de la banda que hoy falta;
3. apilar/correlacionar muchos impactos para aumentar la energía coherente frente al ruido;
4. verificar propagación con varios receptores o distancias, no solamente presencia de líneas espectrales.

El modelo mecánico de leva existente usa por defecto 45 rpm, equivalente a un impacto cada 1,33 s y una fundamental de aproximadamente 0,75 Hz si hay un golpe por vuelta. Sus armónicos atraviesan la banda de interés, pero esto todavía es una consecuencia teórica del régimen de giro. No existe validación experimental del martillete como Mini-Sosie.

El TeX actual contiene dos afirmaciones que deben auditarse antes de conservarlas:

- llama a Guan “la configuración empleada en este trabajo”, aunque el martillete periódico todavía no fue validado;
- declara un ensayo manual con picos alrededor de 0,5, 1 y 2 Hz. Elías confirmó que el ensayo existió, pero sólo quedaron capturas de pantalla. Sin el archivo crudo no se pueden verificar de nuevo esos picos ni cuantificar la mejora.

#### Evidencia conservada del ensayo manual

- `docs/Primera Presentación/evidencia/ensayo_impactos_periodicos_manual/01_senal_geo1_60s_impactos_aprox_1Hz.png`: captura de `Geo1 (S1)`, señal cruda durante 60 s, con una sucesión de impactos manuales de cadencia y amplitud no perfectamente uniformes.
- `docs/Primera Presentación/evidencia/ensayo_impactos_periodicos_manual/02_espectro_geo1_60s_impactos_aprox_1Hz.png`: vista espectral conservada junto con la señal, mostrada aproximadamente entre 0,1 Hz y algo más de 1 kHz.

El contexto y las limitaciones quedaron documentados junto a las imágenes en `docs/Primera Presentación/evidencia/ensayo_impactos_periodicos_manual/README.md`.

La segunda captura presenta una envolvente con caída marcada en alta frecuencia, especialmente a partir de algunos cientos de hertz, y una estructura de líneas compatible con una excitación repetida. No basta para identificar una función pasa-bajos de la fuente: el espectro observado es el producto de la firma del impacto, acoplamiento, propagación por el suelo, respuesta del geófono, AFE, ADC y procesamiento de visualización. Tampoco prueba que haya aumentado la energía propagante en baja frecuencia frente a igual número de golpes no periódicos.

Clasificación correcta para la primera entrega: **observación exploratoria cualitativa que motivó el diseño de la fuente periódica**. Puede aparecer en una diapositiva auxiliar. Para convertirla en resultado cuantitativo deben repetirse y conservarse al menos: señal GEO cruda, referencia HAMMER/trigger, cadencia real de cada impacto, distancia, configuración de ganancia, espectro calculable y comparación A/B con golpes aislados o secuencia no periódica usando el mismo número de impactos.

## 6.3 Resultado MASW: por qué 5,4 m no es el límite de todo lo conseguido

### Resultado del pipeline del 17 de agosto

El informe `acceleration_kalman_inversion_2026-08-17/INFORME_AMEDIDA_KALMAN_INVERSION.md` trabajó con 25 puntos entre 8,00 y 21,71 Hz. Su longitud de onda máxima fue aproximadamente 10,84 m y, usando `z ≈ lambda/2`, dio una profundidad aproximada de **5,42 m**.

Ese número describe ese pipeline y esa banda. No es una cota global del dataset.

### Resultado del benchmark consolidado del 23 de agosto

El benchmark evaluó 1640 corridas en total:

- 1051 experimentos de pipeline completo;
- 276 configuraciones de picker contra verdad conocida;
- 52 configuraciones de inversión con bandas de incertidumbre;
- 261 casos adversariales.

Conclusiones relevantes:

1. La curva de dispersión de campo contiene soporte de longitud de onda del orden de **20–22 m**, que lleva a una profundidad de investigación del orden de **10–11 m** mediante `z ≈ lambda/2`.
2. La configuración `park | 18-46 | dp | mean` alcanza **11,83 m** con las convenciones permisiva y conservadora en la tabla de ranking. Es una cifra específica de configuración, no una resolución uniforme de 11,83 m.
3. Las inversiones con bandas posteriores sitúan el soporte típico de los finalistas entre aproximadamente **10,06 y 11,0 m**.
4. Por eso, el titular más robusto para la primera entrega es: **“la campaña proporciona soporte de investigación de aproximadamente 10–11 m”**.
5. Puede mencionarse que una configuración alcanza 11,83 m, siempre que se la identifique y no se redondee el resultado como “12 m resueltos”.
6. Los rankings que declaran 15 m exactos se apoyan en el borde de la máscara de resolución y fueron identificados como una trampa métrica. No deben citarse como profundidad medida.

No se debe unir en una misma leyenda, como si provinieran del mismo resultado, el perfil principal `park | 22-42 | dp | 3 capas` y el máximo de **11,83 m** del ranking `park | 18-46 | dp | mean`. La presentación más limpia es usar el perfil `22-42` como resultado principal, cuyo soporte informativo es del orden de **10,8 m**, y dejar 11,83 m como detalle de que otra ventana finalista alcanzó un poco más de profundidad. El titular común sigue siendo **aproximadamente 10–11 m**.
7. Los perfiles antiguos que se extienden a decenas de metros, incluido el CSV procesado con profundidades del orden de 80 m, no son defendibles con la banda y geometría actuales.
8. `Vs30` no es alcanzable con el dataset actual.

### Diferencia entre profundidad de soporte y detalle estratigráfico

Llegar a un soporte de 10–11 m no significa resolver cada interfaz hasta 11 m con la misma exactitud. La resolución disminuye con la profundidad y la incertidumbre se concentra en interfaces y en el tramo profundo.

## 6.4 Perfil `Vs(z)` defendible y sus cautelas

El benchmark concluye que el dato no sostiene más de tres capas de manera estable. La decisión se obtuvo sobre 24 curvas bootstrap del dato real y 5 semillas de inversión, es decir **120 inversiones por configuración**. Con tres capas, prácticamente el 100 % de la variación se atribuyó al remuestreo del dato; a partir de la cuarta capa, aproximadamente la mitad de la dispersión de `Vs(z)` provino del optimizador.

Por tanto, el recuerdo de que “variaba menos con el bootstrap” apunta en la dirección correcta, pero la formulación rigurosa es más precisa:

> Se adopta provisionalmente el modelo de tres capas porque es el modelo más complejo cuya incertidumbre sigue estando dominada por el dato. Las capas adicionales no quedan determinadas independientemente por la medición y trasladan aproximadamente la mitad de la variabilidad al optimizador.

No debe justificarse la elección diciendo solamente que el CV fue 3,0 % frente a 8,1 % con cinco capas. `HALLAZGOS.md` corrigió explícitamente esa lectura: el CV mediano está sesgado a favor de modelos con menos parámetros y no es comparable entre distintos números de capas. El criterio válido es la fracción de varianza atribuible al dato (`%dato`).

El resumen de tres capas se comporta prácticamente como un escalón:

- `Vs` somera del orden de **78 m/s**;
- interfaz efectiva alrededor de **2,4 m**;
- `Vs` mayor por debajo, del orden de **178 m/s** dentro de buena parte del soporte;
- el semiespacio y el tramo profundo son mucho más sensibles a la parametrización y al coeficiente de Poisson.

Precauciones obligatorias:

- la interfaz de 2,4 m debe presentarse como **interfaz efectiva**, no como estrato geológico identificado;
- los primeros 1–2 m son reproducibles bajo el modelo, pero el paso espacial de 2 m limita su resolución real; reproducibilidad no equivale a resolución;
- la inversión impone monotonía creciente de `Vs`;
- en sintéticos, la monotonía ocultó el 100 % de una inversión de velocidad conocida y produjo 39,5 % de error en ese caso;
- liberar la monotonía con el dato real no restringe un perfil útil;
- el coeficiente de Poisson no fue medido. Variarlo por capas cambia poco la `Vs` superficial, pero ensancha fuertemente la incertidumbre profunda;
- un misfit bajo demuestra consistencia con el modelo impuesto, no unicidad geológica.

### Resultado recomendado para el cuerpo principal

Mostrar como resultado preliminar de validación del instrumento:

1. gather activo sintetizado;
2. imagen y curva de dispersión con límites de aliasing/apertura;
3. perfil simplificado de tres capas o escalón, con banda de incertidumbre;
4. soporte de aproximadamente 10–11 m;
5. una frase explícita sobre monotonía, `nu` no medido y falta de validación puntual.

Los detalles de rankings, ataques adversariales, pickers y sensibilidad de `nu` son mejores candidatos para diapositivas auxiliares del PPTX.

## 6.5 Robustez del procesamiento MASW

Resultados útiles para justificar que se hizo más que “obtener una curva bonita”:

| Prueba | Resultado |
|---|---|
| Cambiar transformada | Dispersión mediana de `c(f)` de 2,28 m/s en 12–30 Hz |
| Cambiar picker | Dispersión de 1,89 m/s |
| Quitar offsets de 32 y 40 m | Cambio RMS de 29,76 m/s |
| Quitar 75 % de golpes | Cambio de 29,7 % en profundidad de soporte |
| Cambiar semilla de inversión | CV de 17,2 % |
| Perturbar `c(f)` | Cambios importantes, hasta 39,4 % en `Vs` |

Conclusión: `c(f)` es mucho más robusta que `Vs(z)`. La geometría pesa aproximadamente trece veces más que cambiar de transformada. El instrumento y la campaña deben priorizar geometría, banda baja y trazabilidad; no conviene centrar el relato en sofisticación algorítmica.

## 6.6 Caracterización analógica existente

Fuente: `resultados_verificacion_calibracion_2026-07-21/05_tablas_reportes/resumen_identificacion.csv`.

| Ruta medida | Puntos | Banda aproximada | Coherencia | Error de identificación en magnitud | Error de fase |
|---|---:|---:|---:|---:|---:|
| BP | 55 | 11,63 Hz–47,45 kHz | 0,9986 | 0,874 dB | 12,10° |
| COMP | 41 | 11,58 Hz–4,74 kHz | 0,9694 | 0,617 dB | 4,11° |
| LP | 32 | 11,56 Hz–1,18 kHz | 0,9475 | 0,329 dB | 1,96° |
| LP_PGA, ruta analógica hasta entrada del ADC | 30 | 11,58–862,7 Hz | 0,9938 | 0,416 dB | 1,88° |

Lo que sí demuestra:

- existe una caracterización de magnitud y fase de partes relevantes del AFE;
- la ruta analógica hasta la entrada del ADC fue barrida con alta coherencia;
- el margen de potenciómetros cubrió los puntos medidos;
- la calibración manual mejoró la coincidencia.

Lo que no demuestra:

- cadena extremo a extremo desde excitación mecánica/geófono hasta códigos ADC almacenados;
- comportamiento por debajo de aproximadamente 11,6 Hz, justamente donde está el objetivo de profundidad;
- todas las ganancias y rangos;
- repetibilidad temporal/temperatura;
- dispersión entre varias placas;
- ruido referido a entrada o ENOB;
- desempeño de la revisión casi final que se está construyendo, si los barridos pertenecen a una revisión anterior.

El archivo `RESULTADO.md` indica además que persistía un desajuste alrededor de 10 Hz y recomendaba una calibración fina y un nuevo barrido. Por tanto, la evidencia debe denominarse **caracterización analógica parcial**, no calibración metrológica completa.

## 6.7 Sincronización y temporización

Hay tres cantidades distintas que no deben mezclarse:

1. **Alineación de golpes en procesamiento:** el benchmark reporta un jitter del orden de 1,46 ms después de alinear submuestras. Esto describe la repetibilidad/alineación del trigger en el dataset activo.
2. **Sincronización digital entre nodos:** requiere registros simultáneos y una comparación de relojes o marcas temporales entre varias placas.
3. **Medición de osciloscopio comentada por Elías:** se observó en su momento, pero no se guardaron los datos y debe repetirse.

El punto 1 no valida automáticamente los puntos 2 y 3. Para la entrega actual puede afirmarse que el procesamiento alinea los golpes y que existe una arquitectura de sincronización diseñada; no debe afirmarse una precisión inter-nodo metrológicamente demostrada.

## 6.8 Hardware multinodo

Estado comunicado:

- no existe ahora un conjunto completo de GEO operativos para una prueba multinodo;
- una placa quedó inoperativa tras modificaciones;
- se desarrolla una versión casi final;
- la operación multinodo simultánea permanece como validación futura.
- el prototipo usado se montó sobre placa universal y su construcción fue suficientemente difícil como para limitar la campaña a un solo nodo GEO funcional;
- hubo varias iteraciones universales que pueden documentarse fotográficamente;
- la siguiente revisión se está realizando por transferencia de tóner/planchado y ataque químico;
- después de validar esa revisión se prevé encargar PCB fabricadas en China.

En el informe, las fotografías y diagramas de hardware deben rotular con precisión si muestran:

- prototipo utilizado en las mediciones;
- propuesta de mejora no utilizada;
- revisión casi final en desarrollo;
- arquitectura objetivo.

Una composición fotográfica breve de la evolución **placa universal → placa planchada/ácido → PCB de fabricación externa** puede reforzar el carácter de implementación electrónica. En el PDF debería ocupar una sola figura compacta; el registro fotográfico completo es más apropiado para diapositivas auxiliares.

En la búsqueda preliminar no aparecieron fotografías físicas inequívocas de las placas. Los archivos `docs/Urucom_2026_compact/imagenes/PSoC circuit.jpg` y `Schematic-Circuit-PSoC.jpg`, pese a sus nombres, son capturas de esquemáticos. Antes de maquetar hay que localizar o incorporar las fotos reales y distinguir cuál placa fue efectivamente usada en Canchita.

### Trazabilidad de revisión de circuito pendiente

Los metadatos actuales no identifican de forma inequívoca la revisión analógica de cada placa. Se dejó un recordatorio en `src/firmware/psoc/AcondicionamientoAnalogico.cydsn/psoc_hw.h` para que una implementación futura:

- defina revisión de circuito y número de placa independientemente de la clase GEO/HAMMER y de la versión de firmware;
- los reporte al ESP mediante el protocolo;
- los persista en los metadatos de cada captura junto con ganancia y calibración;
- diferencie prototipos universales, placa planchada/ácido y futuras PCB fabricadas.

En esta fase solo se añadió el comentario `TODO`; no se modificó el protocolo.

## 6.9 Contraste hidrogeológico

Fuente primaria: `INFOR_HIDROGEO_CYT_UC_AS_JUL_2023.pdf`, 38 páginas.

### Datos principales del informe hidrogeológico

- Método: tres Sondeos Eléctricos Verticales, arreglo Schlumberger.
- Estado del terreno: seco.
- SEV 01: coordenadas UTM 21S `X=435595`, `Y=7198920`, sector “Cancha de Fútbol de la UC”, `AB/2=125 m`.
- SEV 02: `X=435698`, `Y=7199100`.
- SEV 03: `X=435872`, `Y=7199128`, paramétrico junto al pozo de Contables.
- El informe ubica el nivel freático regionalmente entre 10 y 30 m, sin dar un valor puntual por sondeo.
- En SEV 01 aparecen interfaces eléctricas a 1,00 m, 2,06 m, 4,15 m, 24,0 m y 71,8 m.
- El nivel hidrogeológico de interés de SEV 01 se modela entre 24,0 y 71,8 m; no debe confundirse con el nivel freático.
- El informe no contiene SPT, CPT, densidad, perfil litológico de pozo ni nivel estático medido por SEV.

### Distancia y estatus del contraste

La conversión nominal del plus code de Canchita y las coordenadas del SEV 01 da aproximadamente 120 m; Elías recuerda una distancia próxima a 200 m. Como no hay GPS de los extremos de la línea MASW, se conservará la formulación:

> “El SEV 01 se ubica en el mismo predio y a una distancia nominal del orden de 120–200 m de la campaña; la separación exacta y el posible solapamiento de tendidos no están documentados.”

Esto permite usar el SEV como **contraste contextual cercano o control de plausibilidad**, no como validación independiente puntual.

### Coincidencias y tensiones

- La interfaz MASW efectiva de ~2,4 m está cerca de la interfaz eléctrica de 2,06 m del SEV 01, pero el SEV tiene tres interfaces en los primeros 4,15 m y está sujeto a equivalencia. La coincidencia debe expresarse como contacto compatible en el intervalo 2–4 m, no como acuerdo de 34 cm.
- El SEV describe el suelo superficial como seco y muy compactado; `Vs ~78 m/s` indica material mecánicamente blando. No hay arbitraje porque resistividad no mide rigidez y MASW no mide compactación/densidad.
- Una caída de resistividad a 4,15 m sugiere mayor fracción arcillosa o humedad, pero no demuestra una inversión de `Vs`.
- Una prueba dirigida con interfaces del SEV dio el mismo ajuste con y sin monotonía y 0/24 perfiles prefirieron un descenso específicamente bajo 4,15 m. No hay evidencia sísmica positiva de capa lenta.
- El freático entre 10 y 30 m comienza en el borde del soporte MASW y se extiende por debajo; el dataset actual no puede localizarlo.

### Uso recomendado en la primera entrega

- Una mención breve como contraste de plausibilidad y limitación.
- No presentar el SEV como “verdad de terreno”.
- No dedicarle un caso de estudio autónomo.
- Reservar tablas, coordenadas y comparación detallada para una diapositiva auxiliar del PPTX.

---

## 7. Matriz de cumplimiento del pedido del tutor

| Pedido | Evidencia actual | Estado para primera entrega | Tratamiento recomendado |
|---|---|---|---|
| Problema → física → MASW | Contenido ya existente | Disponible pero desordenado | Reordenar y condensar |
| Requerimientos derivados | Datos dispersos en sensor, AFE, geometría y adquisición | Parcial | Crear tabla puente explícita |
| Magnitud AFE | Barridos de BP, COMP, LP y LP_PGA | Parcialmente demostrado | Mostrar una figura compacta y límites |
| Fase AFE | Barridos con error de identificación | Parcialmente demostrado | Incluir como preservación de forma/fase, no E2E |
| Extremo a extremo | No existe cadena geófono→ADC→memoria calibrada completa | Pendiente | Declarar como futuro |
| Ruido/ENOB | No se halló medición específica | Pendiente | No inferir ENOB desde SNR de campo |
| Repetibilidad | Bootstrap de golpes y sensibilidad de procesamiento | Disponible para la campaña, no para metrología de hardware | Usar como repetibilidad del resultado de campo |
| Dispersión entre canales | Un solo GEO operativo por registro | No demostrada | Declarar pendiente |
| Sincronización | Arquitectura + alineación de trigger; osciloscopio sin datos guardados | Parcial/no reproducible | Separar diseño de verificación |
| Campaña MASW representativa | Canchita, 21 posiciones, 598 aceptadas | Disponible | Caso único de validación |
| Curva e inversión | Benchmark amplio posterior al PDF actual | Disponible con cautelas | Incorporar resultado 10–11 m y perfil simple |
| Referencia independiente | SEV cercano, distinto punto y distinta magnitud | Contextual | No llamarlo validación puntual |
| Profundidad crítica | Benchmark y análisis de banda baja | Disponible | Reemplazar 5,4 m global por 10–11 m; Vs30 no alcanzable |
| Multinodo completo | No disponible | Pendiente | Futuro |

---

## 8. Puente propuesto: requerimiento geofísico → decisión electrónica

Esta tabla debe guiar la reescritura. No necesariamente debe entrar completa en el PDF; puede condensarse visualmente.

| Necesidad física/MASW | Especificación o decisión electrónica | Evidencia actual | Límite |
|---|---|---|---|
| Observar longitudes de onda largas | Banda baja útil; respuesta del SM-24 y AFE | Señal organizada aproximadamente desde 6–8 Hz; soporte 10–11 m | Muy poca energía bajo 5–8 Hz; compensación sub-10 Hz no validada |
| Evitar aliasing espacial | Separación de receptores y apertura registradas | `dx=2 m`, `L=40 m` | Alta frecuencia útil limitada; primer metro pobremente resuelto |
| Preservar `c(f)` | Fase estable entre rutas/canales | Caracterización parcial de fase del AFE | Sin dispersión entre múltiples placas |
| Mantener SNR | Sensor, ganancia, AFE, ADC y fuente | SNR de campo fuerte en 10–50 Hz | No hay ruido referido a entrada ni ENOB |
| Capturar golpes repetibles | Trigger HAMMER y ventana de adquisición | 598 registros aceptados; alineación submuestra en procesamiento | No equivale a sincronización inter-nodo |
| Formar un arreglo simultáneo | Relojes, sincronización, buffer y comunicaciones | Arquitectura diseñada | Solo un GEO activo por registro |
| Conservar trazabilidad | Metadatos, almacenamiento local, servidor | Manifest, respaldos y pipeline reproducible | Falta prueba completa con todos los nodos |
| Operar en campo | Interfaces y servidor web | Capturas reales e interfaces existentes | Acceso remoto y tolerancia a fallas parcialmente pendientes |

---

## 9. Uso recomendado de los diagramas Draw.io

## 9.1 Para el documento de 15 páginas

Por el límite de espacio, conviene usar como máximo una o dos composiciones derivadas:

1. **“Sistema completo – impacto a Vs(z)”**: mejor candidato para mostrar el hilo causal desde fuente, sensor y electrónica hasta `Vs(z)`. Puede reemplazar varias explicaciones fragmentadas.
2. **“Fuente/geófono/AFE”** o un recorte del flujo de calibración: candidato para la sección de diseño/validación.

Los diagramas completos de lógica digital, almacenamiento y servidor son demasiado densos para el cuerpo principal salvo que se simplifiquen de forma importante.

## 9.2 Para el PPTX principal

- sistema completo y flujo operativo;
- arquitectura maestro–esclavo;
- sincronización y captura;
- cadena fuente–geófono–AFE;
- flujo de calibración;
- pipeline de procesamiento del servidor.

## 9.3 Para diapositivas auxiliares

- hardware digital interno;
- FSM detallada;
- almacenamiento y volcado;
- modelo UML de nodos;
- arquitectura completa de SuperMáquina/PSoC;
- recuperación ante fallos y trazabilidad.

---

## 10. Propuesta preliminar de distribución de las 15 páginas

Esta es una hipótesis de trabajo para discutir, no una edición autorizada.

| Página | Función narrativa |
|---:|---|
| 1 | Título, problema, objetivo y magnitud `Vs` |
| 2 | Métodos tradicionales y motivación de métodos no invasivos |
| 3 | Propagación, ondas P/S/Rayleigh/Love y `lambda=c/f` |
| 4 | Dispersión, cadena de inferencia y comparación SASW/MASW |
| 5 | Selección de MASW y tabla puente de requerimientos instrumentales |
| 6 | Arquitectura global del sistema y fuente/trigger |
| 7 | Transductor SM-24, banda, limitaciones y criterio de compensación |
| 8 | AFE, ganancia, rango dinámico y preservación de fase |
| 9 | ADC, memoria, temporización y arquitectura digital |
| 10 | Comunicaciones, interfaces y trazabilidad de datos |
| 11 | Caracterización analógica parcial y qué falta medir |
| 12 | Campaña Canchita como validación del flujo de adquisición |
| 13 | Dispersión, inversión preliminar, perfil y profundidad 10–11 m |
| 14 | Síntesis de resultados, limitaciones y trabajo futuro |
| 15 | Referencias; probablemente será necesario que comiencen al final de la página 14 |

Principios de compresión:

- reducir casos de aplicación a uno o dos párrafos de motivación;
- conservar solo la matemática que alimenta directamente un requerimiento o una interpretación;
- sustituir descripciones repetidas de componentes por una figura causal y una tabla de trazabilidad;
- mover detalles de algoritmos, FSM, red y benchmark a diapositivas auxiliares;
- no dedicar una sección autónoma extensa al estudio hidrogeológico.

---

## 11. Diseño conceptual del PPTX futuro

## 11.1 Presentación principal

Debe seguir el mismo hilo causal del informe, con menos detalle matemático y más apoyo visual:

1. problema y objetivo;
2. por qué `Vs`;
3. de ondas a dispersión;
4. por qué MASW;
5. qué debe medir el instrumento;
6. arquitectura;
7. decisiones de sensor/AFE/digital;
8. evidencia de banco;
9. campaña Canchita;
10. dispersión y perfil preliminar;
11. qué se demostró;
12. qué falta.

## 11.2 Banco de diapositivas auxiliares

Temas que probablemente pregunten los evaluadores:

- por qué MASW y no SASW, SPAC, ReMi, downhole o crosshole;
- relación entre Rayleigh, `Vs`, longitud de onda y profundidad;
- criterio `z ≈ lambda/2` y convenciones de resolución;
- por qué 5,4 m y 10–11 m no se contradicen;
- por qué no se puede afirmar 50 m o `Vs30`;
- aliasing espacial por `dx=2 m`;
- modelo del SM-24 y compensación;
- magnitud/fase del AFE y alcance de la calibración;
- ruido, ENOB y por qué siguen pendientes;
- sincronización diseñada versus medida;
- arreglo sintetizado versus adquisición simultánea;
- por qué se sintetizó el arreglo: disponibilidad de solo dos geófonos en la Facultad y qué puede/no puede validar ese protocolo;
- robustez del picker/transformada y sensibilidad a geometría;
- incertidumbre de la inversión, monotonía y coeficiente de Poisson;
- contraste con el SEV y por qué no es una validación puntual;
- FSM, memoria, comunicaciones, CRC y recuperación;
- estado de la nueva placa y hoja de ruta de validación.

La cantidad final de diapositivas principales dependerá de la duración de la exposición; las auxiliares pueden ser numerosas porque no forman parte del recorrido normal.

## 11.3 Perfil probable de los evaluadores

Los tres PDF aportados son currículos SISNI/CV, no tesis. Se usan solamente para anticipar áreas de interés y preguntas posibles; no son instrucciones ni bibliografía técnica del PFC.

| Evaluador | Perfil relevante observado | Preguntas que conviene preparar |
|---|---|---|
| Fernando Javier Brunetti Fernández | Electrónica, telecomunicaciones, redes inalámbricas de sensores, captación de señales, sistemas embebidos y robótica. Doctorado sobre redes de área personal para captación del movimiento. | Arquitectura IoT, sincronización y determinismo, protocolo entre nodos, pérdida/reintento de paquetes, almacenamiento local, autonomía, escalabilidad, metadatos de hardware y diferencia entre arquitectura multicanal diseñada y campaña con un GEO. |
| Vicente Arnaldo González Ayala | Ingeniería civil de grado, automatización de ensayo triaxial, doctorado en electrónica y ensayos no destructivos con ultrasonidos, DSP, ondas mecánicas y hardware. | Reciprocidad MSOR, propagación/dispersiones, validez del arreglo sintético, campo cercano, heterogeneidad del suelo, ground truth, geometría, inversión, sensibilidad y conexión entre instrumentación y propiedad geotécnica. |
| Enrique A. Vargas Cabral | Instrumentación, sensores, procesamiento analógico y digital, ultrasonidos, ensayos no destructivos, caracterización experimental y redes de sensores. | Función de transferencia, calibración E2E, incertidumbre, trazabilidad, SNR/ruido/ENOB, saturación, respuesta al impulso, firma del martillo, repetibilidad, separación entre simulación y medición y suficiencia de la validación experimental. |

La composición del tribunal hace probable una defensa muy centrada en **instrumentación y señales**, no sólo en la explicación geofísica. El PPTX auxiliar debe incluir evidencia y respuestas específicas sobre sincronización, calibración, geometría, reciprocidad, incertidumbre y límites de validación.

---

## 12. Lenguaje recomendado para las afirmaciones

### 12.1 Se puede afirmar ahora

- “Se adquirieron 598 registros aceptados en 21 posiciones de 10 a 50 m con una fuente activa y un geófono desplazado secuencialmente.”
- “El conjunto permite sintetizar un registro multicanal activo y obtener una curva de dispersión reproducible.”
- “La banda útil de campo se concentra principalmente en 10–50 Hz, con soporte adicional de baja frecuencia en configuraciones seleccionadas.”
- “El benchmark posterior evaluó 1640 corridas y sitúa la profundidad de soporte defendible en aproximadamente 10–11 m.”
- “El dato sostiene un perfil simplificado; la `Vs` somera es del orden de 78 m/s y aparece una interfaz efectiva cercana a 2,4 m.”
- “Se caracterizaron parcialmente magnitud y fase de la cadena analógica hasta la entrada del ADC.”
- “El estudio SEV cercano aporta contexto de plausibilidad, no una validación puntual.”

### 12.2 Debe calificarse como preliminar

- perfil `Vs(z)`;
- ubicación/naturaleza geológica de interfaces;
- profundidad exacta de 11,83 m;
- respuesta compensada sub-10 Hz;
- precisión de sincronización;
- repetibilidad entre placas;
- operación multicanal física completa.

### 12.3 No debe afirmarse con la evidencia actual

- caracterización hasta 50 m demostrada;
- `Vs30` medido;
- resolución confiable a 80 m;
- 21 geófonos adquiridos simultáneamente;
- precisión inter-nodo de 100–200 microsegundos validada, mientras no exista archivo reproducible;
- ENOB medido;
- calibración extremo a extremo completa;
- dispersión entre canales medida;
- validación independiente en el mismo punto;
- nivel freático detectado por MASW;
- identificación litológica definitiva desde `Vs` o resistividad.

---

## 13. Preguntas que todavía conviene resolver antes de editar

### Decisiones de contenido del PDF

1. **Resuelto:** usar 10–11 m como resultado técnico prometedor, 11,83 m sólo como detalle mínimo asociado a su configuración y declarar la necesidad de más estudios.
2. **Resuelto:** usar provisionalmente el perfil simplificado de tres capas; justificarlo por `%dato`, no por CV.
3. **Resuelto:** mención breve del SEV en el PDF y detalle en material auxiliar.
4. **Resuelto con supuesto declarado:** tratar los barridos del 21 de julio como representativos de la forma de la ruta analógica, porque se conservaron polos/topología; no extrapolar automáticamente ganancia, autocalibración ni E2E.
5. **Resuelto:** en Canchita se empleó un único nodo GEO desplazado; el segundo geófono disponible no formó parte simultánea del gather.
6. **Resuelto conceptualmente:** explicar primero la campaña completa de 10–50 m y después la selección posterior de subarreglos medio-lejanos. Atribuir la mejora a menor contaminación compatible con campo cercano/modos superiores y al compromiso con atenuación/SNR, dejando claro que la geometría sigue siendo sensible y requiere repetición.
7. **Resuelto:** el impacto permaneció fijo a unos metros frente al arco y sólo se desplazó el GEO. La geometría corresponde a un arreglo receptor secuencial, no a MSOR exacto.

### Decisiones del PPTX

8. **Resuelto:** la exposición principal durará aproximadamente 30 minutos y las preguntas serán posteriores.
9. **Resuelto:** los evaluadores previstos son Fernando Brunetti, Enrique Vargas y Vicente González. Sus CV muestran perfiles complementarios en redes de sensores, instrumentación, DSP, ensayos no destructivos, ondas y control.
10. **Resuelto:** no se espera demostración en vivo. La evidencia y las respuestas deberán quedar preparadas en el PPTX y sus diapositivas auxiliares.

### Datos que pueden completarse sin repetir campañas

11. **Parcialmente resuelto:** el impacto permaneció fijo a unos metros frente al arco y la línea de adquisición fue paralela a los laterales de la cancha. Si aparecen fotos o mapas, todavía conviene precisar extremos, separación respecto del arco y azimut.
12. Identificar la revisión exacta de placa/firmware asociada a cada barrido y campaña.
13. **Resuelto:** la portada cuenta dentro de las 15 páginas. No se hará una portada independiente; se conservará un encabezado compacto con título y datos, siguiendo la base existente.
14. Localizar las fotografías físicas de las iteraciones y marcar cuál corresponde al único nodo GEO usado en Canchita; las imágenes localizadas hasta ahora son esquemáticos, no fotos. Elías las incorporará posteriormente.
15. **Resuelto:** todas las placas universales funcionaron; fueron iteraciones con cambios progresivos de detalles y pines. Falta asociar cada fotografía y campaña con su revisión exacta.
16. **Resuelto parcialmente:** el ensayo manual de trenes de impactos sí se realizó frente al Laboratorio LED, a aproximadamente 20–27 m, y motivó la idea Mini-Sosie. HAMMER y GEO se adquirieron juntos, pero sólo quedaron dos vistas de pantalla y la cadencia manual varió. Mientras no se repita con datos crudos, tratarlo como observación exploratoria y no como validación cuantitativa.
17. **Resuelto:** las dos imágenes preservadas —señal temporal y espectro— son vistas del mismo registro de 60 s.
18. **Resuelto hasta el nivel recordado:** la medición separada con componentes próximas a 0,5, 1 y 2 Hz se realizó también frente al Laboratorio LED. Como no se conserva el registro crudo ni una ficha experimental completa, no se utilizará como evidencia cuantitativa.

---

## 14. Conclusión de esta fase de análisis

La reestructuración solicitada puede hacerse sin inventar resultados ni exigir nuevas campañas para la primera entrega. El repositorio ya contiene evidencia suficiente para mejorar de forma material el PDF actual:

- una narrativa física y electrónica sólida que debe reordenarse;
- caracterización analógica parcial;
- una campaña de campo representativa;
- un benchmark MASW mucho más completo que el reflejado en el PDF del 20 de agosto;
- una profundidad de soporte defendible de aproximadamente 10–11 m, no solamente 5,4 m;
- un perfil `Vs(z)` preliminar simplificado y acompañado de incertidumbre;
- un contraste hidrogeológico cercano útil como contexto;
- una lista clara y honesta de validaciones pendientes.

La clave de la versión revisada será separar cuatro niveles:

1. **Diseñado:** arquitectura, requerimientos y mejoras propuestas.
2. **Implementado:** hardware, firmware, interfaces y almacenamiento existentes.
3. **Medido/demostrado:** barridos analógicos, registros de Canchita, dispersión y benchmark.
4. **Pendiente:** E2E metrológico, ENOB, sincronización reproducible, dispersión entre placas, multinodo simultáneo y validación puntual independiente.

No se debe editar el TeX ni construir el PPTX hasta que Elías responda o cierre las preguntas de la sección 13 y autorice pasar de análisis a implementación.
