# Diseño e implementación de un sistema electrónico multicanal del tipo IoT para caracterización geotécnica del suelo mediante ondas sísmicas

`[C01]` *Proyecto final de carrera - Primera presentación*

**Alumno:** Elías David Álvarez Martínez  **Carrera:** Ingeniería Electrónica.
**Matrícula:** Y24127  **Tutor:** Ing. Enrique A. Vargas C.,PhD

> **Nota de trabajo (no forma parte del texto final).** La estructura de este borrador reproduce, sección por sección, la *Estructura revisada recomendada* de `Revision_estructura_trabajo_caracterizacion_suelos_v2.pdf`. Los doce títulos y su orden son los del tutor; no se agregan secciones fuera de esa lista. Los rótulos `[FIGURA]`, `[TABLA]` y `[REVISAR]` son indicaciones editoriales. Las citas entre corchetes usan claves compatibles con `latex-15p-review/referencias.bib` o señalan entradas que deberán agregarse. El borrador separa deliberadamente lo demostrado, lo preliminar y lo pendiente.

---

## 1. Importancia de la caracterización geotécnica del suelo

La respuesta de una obra civil frente a cargas estáticas y dinámicas depende de propiedades mecánicas del terreno que varían con la profundidad y, en general, también lateralmente. Reconocer esa variación (espesores, contactos, rellenos y zonas de menor rigidez) es una condición previa al dimensionamiento de fundaciones, a la evaluación de asentamientos y a la estimación de la respuesta sísmica de sitio.

Entre las magnitudes que describen ese comportamiento, la velocidad de propagación de las ondas de corte, $V_S$, ocupa un lugar particular porque se vincula de forma directa con la rigidez del medio a pequeñas deformaciones. Para un medio elástico de densidad $\rho$, el módulo de corte a pequeñas deformaciones queda determinado por

$$
G_{\max}=\rho\,V_S^{2},
$$

de manera que medir $V_S$ equivale, conocida la densidad, a medir la rigidez del suelo en el rango de deformaciones en que su comportamiento puede considerarse aproximadamente elástico. Esa equivalencia explica por qué el perfil $V_S(z)$ se ha consolidado como parámetro de entrada en la clasificación sísmica de sitios y en el análisis de respuesta dinámica del terreno [Kramer1996; Foti2014].

`[R14]` Conviene fijar desde el inicio una precisión que condiciona todo lo que sigue: ninguna técnica de prospección entrega una imagen exacta del subsuelo, sino un modelo compatible con los datos, con la geometría del ensayo y con los supuestos de interpretación. Esa distinción determina qué información debe preservar el instrumento y hasta qué profundidad puede sostenerse una afirmación.

`[C02]` Se tiene como objetivo de este proyecto de fin de grado el diseño, la implementación y la evaluación experimental de un sistema electrónico multicanal del tipo IoT para la caracterización geotécnica del suelo mediante ondas sísmicas, orientado a profundidades de investigación de hasta 50 m. La contribución que se presenta en esta primera etapa es de instrumentación: la integración y la evaluación con datos reales de una cadena de medida completa, desde la fuente instrumentada y el geófono hasta el acondicionamiento analógico, la conversión analógico-digital, la temporización, el almacenamiento y el procesamiento que conduce a un perfil $V_S(z)$ preliminar. El interés de construirla en lugar de adquirirla no está en suponer que la industria carezca de soluciones, sino en disponer de una plataforma auditable en cada etapa, condición que el instrumental comercial cerrado no ofrece a un laboratorio universitario.

`[C03]` Conviene precisar el centro de gravedad del trabajo antes de continuar. Se trata de un proyecto de fin de grado de Ingeniería Electrónica, de modo que el objeto de diseño, implementación, caracterización y validación es el sistema de instrumentación. La caracterización geotécnica y el método MASW constituyen el contexto de aplicación: son los que definen los requerimientos que el instrumento debe satisfacer y el criterio con el que se juzga si los satisface. Las secciones 2 a 7 desarrollan en consecuencia únicamente la física necesaria para derivar esos requerimientos, y la interpretación geológica se mantiene en todo el documento dentro del límite estricto de verificar la plausibilidad de los resultados obtenidos.

Ese objetivo formal debe distinguirse con claridad del alcance efectivamente alcanzado hasta hoy, y el documento mantiene esa separación en todas sus secciones:

- **Objetivo de diseño.** Una plataforma multicanal orientada a investigar hasta 50 m de profundidad.
- **Alcance demostrado con la campaña y la cadena actuales.** Adquisición, procesamiento e inversión con soporte de investigación del orden de 10 a 11 m.
- **Brecha experimental.** Aumentar la energía coherente de baja frecuencia, completar el hardware multinodo y realizar las validaciones metrológicas y geofísicas independientes que todavía faltan.

`[R16]` Las secciones 2 a 7 establecen qué se desea medir y por qué mediante ondas superficiales; la sección 8 traduce esa elección en requerimientos cuantitativos; la sección 9 presenta el diseño electrónico como respuesta a ellos; las secciones 10 y 11 describen la validación y sus resultados, y la 12 delimita lo que aún no puede afirmarse.

## 2. Métodos tradicionales de caracterización del suelo

`[R17]` El reconocimiento geotécnico convencional se apoya en ensayos que establecen contacto físico con el terreno. El ensayo de penetración estándar (SPT) da una medida indirecta de resistencia y permite recuperar muestras a intervalos discretos, con la ventaja de una práctica extendida y correlaciones documentadas; el ensayo de penetración con cono (CPT y su variante piezométrica CPTu) mejora la continuidad vertical del registro y reduce la dependencia del operador, aunque pierde aplicabilidad en gravas o niveles cementados.

Cuando el objetivo es directamente una velocidad sísmica, la referencia son los ensayos en pozo: el downhole registra en profundidad las llegadas generadas en superficie y el crosshole mide el tiempo de tránsito entre perforaciones vecinas, ofreciendo la mejor resolución vertical disponible para $V_S$. Ambos comparten la limitación que motiva este trabajo, ya que exigen perforar, con el costo y el plazo asociados, y describen el suelo sólo en el entorno del pozo.

De esa comparación se desprende la motivación de los métodos no invasivos. Una obra necesita reconocer la variación lateral de la rigidez en un volumen extenso, y un conjunto de sondeos puntuales resulta costoso de densificar. Los métodos basados en la propagación de ondas mecánicas desde la superficie permiten cubrir esa extensión sin perforar, a cambio de trabajar con una magnitud que se infiere en lugar de medirse por contacto. `[C04]` A ese argumento se agrega un campo de aplicación que el carácter no invasivo habilita de manera casi exclusiva: el control de calidad y el seguimiento de obras ya construidas. Una traza vial, un terraplén o una plataforma pueden recorrerse de forma repetida y sin daño para verificar la uniformidad de la compactación durante la construcción, y para detectar posteriormente la degradación o la pérdida de rigidez que anticipa la necesidad de mantenimiento. Un ensayo destructivo no admite esa repetición sobre la misma obra.

## 3. Métodos basados en ondas mecánicas

`[R06]` La caracterización sísmica se apoya en que las propiedades mecánicas del medio gobiernan cómo se propaga una perturbación, y en que esa propagación deja magnitudes observables en superficie: tiempos de llegada, amplitudes y relaciones de fase entre puntos separados. Medirlas permite estimar las propiedades sin acceder a la profundidad de interés.

Las familias de métodos se distinguen por qué observable explotan. La refracción sísmica utiliza los tiempos de primera llegada de ondas de cuerpo refractadas críticamente y resulta apropiada cuando la velocidad crece de manera monótona con la profundidad; su punto débil conocido es la incapacidad de detectar capas de baja velocidad ocultas bajo otras más rápidas. La reflexión aprovecha los contrastes de impedancia y alcanza mayor profundidad, pero requiere fuentes de energía considerable y una relación señal a ruido difícil de obtener en el rango somero. Los métodos de ondas superficiales, en cambio, explotan la dependencia de la velocidad de fase con la frecuencia, y esa dependencia es precisamente lo que codifica la variación de rigidez con la profundidad.

Para un ensayo desde superficie orientado a $V_S$ en los primeros metros, la última familia presenta una ventaja física decisiva. Un impacto vertical aplicado en la superficie de un semiespacio destina la mayor parte de la energía elástica radiada a la onda Rayleigh [Foti2014], cuya amplitud decae con la distancia de forma considerablemente más lenta que la de las ondas de cuerpo. El método aprovecha así la componente más energética del campo de ondas en lugar de combatirla como ruido, lo que resulta determinante cuando la fuente disponible es un impacto manual y no una fuente sísmica de gran porte.

## 4. Fundamentos de propagación de ondas en un medio

En un medio elástico, homogéneo e isótropo, la propagación de perturbaciones infinitesimales queda descrita por dos velocidades independientes, asociadas a los dos modos posibles de deformación. La velocidad de las ondas de compresión y la de las ondas de corte se expresan en función de los parámetros de Lamé $\lambda$ y $\mu$ y de la densidad $\rho$ como

$$
V_P=\sqrt{\frac{\lambda+2\mu}{\rho}},
\qquad
V_S=\sqrt{\frac{\mu}{\rho}} .
$$

La segunda expresión es la que conecta la medición con el objetivo planteado en la sección 1: como $\mu$ coincide con el módulo de corte a pequeñas deformaciones, `[C05]` obtener $V_S$ equivale a obtener $G_{\max}$ salvo por el factor de densidad. Esa relación resulta especialmente conveniente porque las dos magnitudes involucradas tienen rangos de variación muy dispares. La densidad de los suelos habituales se mantiene aproximadamente entre 1,4 y 2,2 t/m³, es decir dentro de un factor menor que dos, mientras que $V_S$ recorre desde algunas decenas de metros por segundo en suelos blandos hasta varios cientos en materiales densos o cementados. Como $G_{\max}$ depende del cuadrado de la velocidad, su variación queda dominada por $V_S$, y un valor de densidad estimado con precisión moderada resulta suficiente para obtener una rigidez útil [Kramer1996; Foti2014]. Las ondas de compresión, en cambio, resultan poco informativas en el rango somero saturado: por debajo del nivel freático $V_P$ queda gobernada por la compresibilidad del agua intersticial y tiende hacia unos 1500 m/s con independencia del estado del esqueleto sólido, de modo que pierde sensibilidad justamente a la propiedad que interesa medir [Foti2014; Foti2018].

Ambas velocidades quedan vinculadas por el coeficiente de Poisson,

$$
\nu=\frac{V_P^{2}-2V_S^{2}}{2\left(V_P^{2}-V_S^{2}\right)},
$$

relación que conviene retener porque $\nu$ no fue medido en este trabajo y debió adoptarse por hipótesis en la inversión, con las consecuencias que se analizan en la sección 11.3.

`[C06]` Las expresiones anteriores suponen un medio homogéneo y perfectamente elástico, y conviene señalar que ninguna de las dos condiciones se cumple en el terreno real. El suelo es un medio estratificado, y esa estratificación no es una desviación molesta del modelo sino precisamente lo que el ensayo se propone reconstruir. El suelo tampoco es perfectamente elástico: disipa energía a medida que la onda avanza, por lo que la amplitud registrada en un receptor lejano se reduce tanto por divergencia geométrica como por atenuación material, y esta última crece con la frecuencia.

De ahí se sigue una consecuencia que condiciona el diseño del instrumento. Si la señal útil se debilita al aumentar la distancia y la frecuencia, entonces el margen entre señal y ruido de la cadena de medida deja de ser una cifra de mérito genérica y pasa a ser la variable que determina cuál es la máxima longitud de onda que todavía puede reconocerse y, por lo tanto, hasta qué profundidad puede investigarse.

## 5. Ondas de cuerpo y ondas superficiales

`[R18]` `[C07]` Las ondas de cuerpo se propagan por el volumen del medio y se distinguen por su polarización: la P desplaza las partículas en la dirección de propagación y la S lo hace transversalmente, razón por la cual es esta última la que involucra al módulo de corte. Dentro de la onda S conviene además distinguir dos polarizaciones, porque de ellas depende qué onda superficial puede formarse: la componente SV oscila en el plano vertical que contiene la dirección de propagación y la SH en el plano horizontal perpendicular a él.

Las ondas superficiales no son un tercer tipo de onda independiente, sino el resultado de la interacción de las anteriores con la superficie libre del terreno. Cuando una onda P y una onda SV inciden sobre esa frontera, la condición de tensión nula obliga a que se conviertan mutuamente al reflejarse, y para ciertas combinaciones de ángulo y frecuencia ambas quedan acopladas en una perturbación que no se propaga hacia el interior sino que viaja paralela a la superficie, con amplitud que decae exponencialmente con la profundidad. Esa perturbación es la onda Rayleigh: combina por construcción una componente vertical y una longitudinal, y describe en el semiespacio homogéneo un movimiento elíptico retrógrado. Su velocidad de fase se sitúa entre el 87 % y el 96 % de $V_S$ según el coeficiente de Poisson, lo que la convierte en un buen sustituto observable de la velocidad de corte.

La componente SH no puede acoplarse a la P por razones de polarización, y por eso no participa de la onda Rayleigh. Puede, en cambio, quedar atrapada por reflexiones múltiples dentro de una capa superficial de menor velocidad apoyada sobre un sustrato más rápido, y forma entonces la onda Love. Como su movimiento es horizontal y transversal, no produce señal apreciable en un geófono vertical; por esa razón la onda Love queda fuera del alcance de este trabajo, cuya cadena de medida registra únicamente la componente vertical.

La relación entre la Rayleigh y $V_S$ es la que convierte a la primera en un observable útil. Como la velocidad de fase Rayleigh es del orden del 90 % de la velocidad de corte del material que la onda efectivamente muestrea, una medición de $c_R$ constituye una medición aproximada de $V_S$ una vez resuelto qué volumen del terreno correspondió a cada frecuencia.

Esa correspondencia entre frecuencia y volumen muestreado la fija la longitud de onda. Para una frecuencia $f$ y una velocidad de fase $c_R(f)$,

$$
\lambda_R(f)=\frac{c_R(f)}{f},
$$

y el desplazamiento asociado a una onda Rayleigh decae con la profundidad en una escala comparable a $\lambda_R$. Las longitudes de onda cortas quedan por tanto controladas por el material somero, mientras que las largas integran un volumen mayor y alcanzan mayor profundidad. `[C08]` La regla práctica $z\approx\lambda/2$, en la que $z$ es la profundidad de investigación, entendida como la profundidad máxima hasta la cual la medición conserva sensibilidad apreciable, resume esa proporcionalidad y se emplea de forma habitual para estimar la profundidad de investigación de una campaña, pero no asigna una profundidad exacta a cada frecuencia: las funciones de sensibilidad son distribuidas y se superponen entre frecuencias vecinas. `[R08]` De ahí se sigue una advertencia que resulta decisiva al interpretar los registros: observar energía a una frecuencia baja no demuestra que exista allí una onda Rayleigh útil, criterio que la sección 12 desarrolla al discutir la fuente.

## 6. Utilización de ondas superficiales para la caracterización de suelos

En un medio homogéneo la velocidad Rayleigh no depende de la frecuencia. La dispersión aparece cuando el medio está estratificado, porque cada longitud de onda muestrea una combinación distinta de capas y se propaga con la velocidad de fase que resulta de esa combinación. La curva $c_R(f)$ deja entonces de ser una constante del material y pasa a contener, codificada, la variación de rigidez con la profundidad: ese es el fundamento del método.

`[R09]` La explotación de esa información sigue la cadena de la figura 1: se registra la respuesta del terreno en varias posiciones de una línea, se transforma el conjunto de trazas al dominio frecuencia–velocidad de fase, se extrae de esa imagen la curva de dispersión observada $c_R^{\mathrm{obs}}(f)$ y se resuelve el problema inverso buscando el modelo estratificado que la reproduzca [Park1998; Park1999; Xia1999].

`[R10]` La última etapa impone la cautela principal del método: el problema inverso no tiene solución única, de modo que un ajuste bajo demuestra consistencia entre el dato y el modelo propuesto, no que ese modelo sea el único compatible. La sección 11.3 aplica ese criterio al resultado obtenido.

`[C24]` [FIGURA 1. Diagrama de la cadena de inferencia, dibujado en TikZ dentro del propio documento y no importado como imagen: propiedad mecánica → propagación Rayleigh → registros $u(x,t)$ → imagen $f$–$c$ → curva $c_R(f)$ → inversión → perfil $V_S(z)$. Se descartó `fundamentos_dispersion.png` por llevar título y tipografía propios, fondos grises y datos ilustrativos.]

## 7. Revisión y selección del método

Dentro de la familia de ondas superficiales, la alternativa histórica a MASW es el análisis espectral de ondas superficiales (SASW), que estima la velocidad de fase a partir de la diferencia de fase entre dos receptores y repite la medición con distintas separaciones. Su exigencia instrumental es menor, pero la estimación depende del desenvolvimiento de fase y no dispone de un criterio interno para separar el modo fundamental de los modos superiores, lo que obliga a un procesamiento cuidadoso y a la repetición del ensayo. El registro simultáneo de muchos receptores que propone MASW resuelve precisamente esa debilidad: la transformación al dominio $f$–$c$ separa los modos como máximos distintos y proporciona redundancia frente a ruido local y frente a la falla de un canal individual [Park1999].

Los métodos pasivos, entre ellos ReMi, SPAC y ESAC, presentan una ventaja complementaria de peso, ya que el ruido ambiental contiene energía en frecuencias inferiores a las que alcanza un impacto manual y permite en principio extender el rango hacia mayores profundidades. Su requisito, sin embargo, resulta incompatible con los recursos disponibles: exigen registrar simultáneamente en todas las posiciones del arreglo, porque el campo de ruido no puede reproducirse a voluntad mientras se desplaza un sensor. `[C09]` Con dos geófonos disponibles en la Facultad y un único nodo receptor operativo por registro, estos métodos quedan fuera de alcance por construcción y no por decisión de diseño.

`[C25]` [TABLA 1. Comparación de métodos. Se resuelve como tabla y no como figura importada.]

| Método | Propiedad observada | Requisito de campo | Limitación dominante |
|---|---|---|---|
| SPT | Resistencia a la penetración | Perforación | Medida puntual y por correlación empírica |
| CPT / CPTu | Resistencia de punta y fricción lateral | Penetración continua | Pierde aplicabilidad en gravas y cementados |
| Downhole / Crosshole | $V_P$ y $V_S$ directas | Uno o varios pozos | Costo y plazo; describe sólo el entorno del pozo |
| Refracción sísmica | Tiempos de primera llegada | Fuente y línea en superficie | No detecta capas de baja velocidad ocultas |
| SASW | Diferencia de fase entre dos receptores | Dos receptores y ensayos repetidos | Sin criterio interno de separación modal |
| MASW activo | Dispersión $c_R(f)$ sobre varios offsets | Fuente controlada y arreglo de receptores | Depende de la energía disponible en baja frecuencia |
| Pasivos (ReMi, SPAC, ESAC) | Dispersión del ruido ambiental | Registro simultáneo en todo el arreglo | Exige simultaneidad y un campo de ruido adecuado |

La selección de MASW activo se sigue entonces de los objetivos y de la física expuesta. La fuente controlada permite referenciar temporalmente cada registro y repetir la excitación tantas veces como sea necesario; la geometría conocida convierte la diferencia de fase entre posiciones en una velocidad; y el registro de múltiples offsets ofrece la redundancia que la inversión necesita. Para el propósito de este trabajo hay además una razón instrumental: MASW ejercita simultáneamente todas las funciones que el sistema debe cumplir, esto es, sincronización, preservación de fase entre canales, margen dinámico, almacenamiento sin pérdidas y trazabilidad de la geometría, y por lo tanto sirve como banco de prueba integral de la plataforma.

## 8. Requerimientos del sistema de instrumentación

Esta sección constituye el puente entre la geofísica y el diseño electrónico. Cada requerimiento que sigue se deriva de una necesidad del método expuesta en las secciones 5 a 7 y no de una preferencia de implementación.

**Banda útil de trabajo.** La profundidad de investigación se fija por la máxima longitud de onda observable a través de $z\approx\lambda/2$, y la longitud de onda se relaciona con la frecuencia mediante $\lambda=c/f$. Combinando ambas expresiones, la frecuencia mínima necesaria para alcanzar una profundidad $z$ resulta

$$
f_{\min}\simeq\frac{c_R}{2z}.
$$

Con la velocidad de fase efectivamente observada en el sitio, del orden de 150 m/s, alcanzar 10 m exige contenido coherente en torno a 7,5 Hz, mientras que el objetivo formal de 50 m exigiría alcanzar aproximadamente 1,5 Hz. Esta única relación explica la distancia entre el objetivo de diseño y el alcance demostrado, y anticipa por qué la elección del transductor y la energía de la fuente, y no la velocidad de conversión, constituyen el cuello de botella del sistema.

**Separación entre canales y apertura del arreglo.** La separación $\Delta x$ define el muestreo espacial del frente de onda y por lo tanto un límite de aliasing, ya que sólo pueden interpretarse sin ambigüedad longitudes de onda que satisfagan $\lambda\gtrsim 2\Delta x$. La apertura total $L$ actúa en el extremo opuesto: no puede estimarse de forma confiable una longitud de onda comparable o mayor que la extensión del tendido. `[C10]` Las recomendaciones de buena práctica expresan ese límite como $L\gtrsim 1{,}5\,\lambda_{\max}$ en una estimación optimista, y con criterios más conservadores exigen $L\gtrsim 2\,\lambda_{\max}$ [Foti2018 — **verificar el criterio exacto contra la fuente antes del .bib**]. Para la apertura de 40 m efectivamente desplegada, el criterio optimista admite longitudes de onda de hasta unos 27 m, cifra que resulta consistente con el soporte de 20 a 22 m que el procesamiento identificó a posteriori y que se reporta en la sección 11.3. Ambos límites se trasladan al plano $f$–$c$ y deben dibujarse sobre la imagen de dispersión, práctica que se adopta en la sección 11.

**Sincronización entre canales.** Un desfase temporal $\Delta t$ entre dos canales introduce un error de fase $2\pi f\,\Delta t$ que el procesamiento interpreta como un tiempo de propagación adicional. En una aproximación de primer orden, el error relativo resultante sobre la velocidad de fase es

$$
\frac{\Delta c}{c}\simeq\frac{c\,\Delta t}{\Delta x},
$$

de modo que la tolerancia de sincronización queda determinada por la geometría y por la velocidad esperada, no por una cifra elegida de antemano. Para $c\approx150$ m/s, $\Delta x=2$ m y un error admisible del 1 % en la velocidad de fase, el desfase entre nodos debe mantenerse por debajo de unos 130 µs. Este número es el que justifica la arquitectura de arranque coordinado descrita en la sección 9 y el que deberá verificarse experimentalmente según se indica en la sección 12.

**Relación señal a ruido y rango dinámico.** El registro debe conservar simultáneamente el primer arribo cercano a la fuente y la llegada atenuada en el offset más lejano, cuya diferencia de amplitud abarca varios órdenes de magnitud. De allí la necesidad de ganancia programable por canal y de un convertidor con margen suficiente para evitar tanto la saturación como el enterramiento de la señal lejana en el ruido de cuantificación. La contrapartida es que ninguna ganancia recupera información que nunca superó el piso de ruido de la cadena, lo que devuelve la atención a la energía de la fuente.

**Preservación de fase.** Como la magnitud medida es una velocidad de fase, un error sistemático de fase entre canales se traduce directamente en un error de velocidad. El requerimiento no es que la respuesta del acondicionamiento sea plana, sino que sea conocida y, sobre todo, idéntica entre canales, porque una diferencia común a todos los canales se cancela al estimar la pendiente de fase mientras que una dispersión entre unidades no lo hace.

**Trazabilidad y operación en campo.** El procesamiento sólo es reproducible si cada registro conserva su geometría, su configuración de ganancia, su referencia temporal y la identificación del hardware que lo produjo. A ello se suma la exigencia operativa de trabajar sin infraestructura, con almacenamiento local y sin depender de conectividad externa durante la adquisición.

`[C11]` La tabla 1 resume esa derivación y funciona además como mapa de lectura del resto del documento: la columna de decisiones anticipa lo que la sección 9 desarrolla, y la de evidencia remite a las secciones 10 y 11, donde cada afirmación se sostiene o se declara pendiente.

[TABLA 1. Puente requerimiento → decisión → evidencia → estado. Es la tabla central del documento y no debe recortarse.]

| Necesidad derivada del método | Decisión de diseño adoptada | Evidencia disponible | Estado |
|---|---|---|---|
| `[C12]` Observar longitudes de onda largas ($f\lesssim 8$ Hz para 10 m) | Geófono SM-24 con rama de compensación $1-\mathrm{BP}$ [Ma2023] → §9.3 | Ruta PGA → ADC identificada desde 0,21 Hz → §10.1 | Electrónica verificada en la banda; el geófono entra como modelo |
| Evitar aliasing espacial y respetar la apertura | Geometría registrada: $\Delta x=2$ m, apertura 40 m, offsets de 10 a 50 m | Metadatos de la campaña | Disponible para la campaña realizada |
| Estimar $c_R(f)$ sin sesgo instrumental | Respuesta de fase conocida y homogénea entre canales | Caracterización parcial de fase del AFE | Pendiente: falta dispersión entre placas |
| Sostener el rango dinámico entre offsets | Ganancia programable, control de offset y ADC $\Delta\Sigma$ con rangos seleccionables | Arquitectura implementada y registros de campo utilizables | Pendiente: sin ruido referido a entrada ni ENOB |
| Sincronizar por debajo de ~130 µs | Arranque coordinado por radio y temporización de ventana en lógica dedicada → §9.4 | Ensayo funcional con tres nodos en laboratorio → §10.2 | Funcionalmente demostrado; sin verificación metrológica |
| Referenciar temporalmente cada impacto | Nodo HAMMER con martillo instrumentado, adquirido junto al nodo GEO | 598 registros aceptados con referencia de impacto | Operativo en campaña |
| Adquirir simultáneamente varios receptores | Nodos GEO independientes con buffer local e inicio común → §9.1 | Coordinación probada con tres nodos en laboratorio → §10.2 | No demostrado con varios GEO completos en campo |
| Evitar pérdida o corrupción de muestras | Fragmentación con numeración de secuencia, reintento, CRC y copia local | Implementación e interfaces existentes | Falta ensayo multinodo bajo interferencia |
| Conservar trazabilidad del registro | Metadatos de campaña, manifiesto y servidor de ingesta | Conjunto de datos y flujo reproducible | Falta asociar revisión de hardware y firmware a cada registro |

## 9. Diseño e implementación del sistema electrónico

### 9.1 Arquitectura general

La plataforma separa tres funciones que la sección 8 exige mantener independientes: la adquisición, que debe ser determinista y local; el transporte, que puede ser diferido y tolerante a fallos; y el análisis, que debe ser reproducible a partir de los datos almacenados. La fuente instrumentada y cada nodo receptor se comportan como esclavos de una operación coordinada por un maestro. Cada nodo GEO convierte el movimiento del terreno en tensión, acondiciona y digitaliza la señal, la conserva localmente y la entrega cuando el enlace lo permite. Una interfaz de campo configura los nodos y gobierna las capturas sin requerir conectividad externa, mientras que un servidor centraliza registros, geometría y metadatos y ejecuta el flujo de procesamiento.

Debe señalarse desde ya que la arquitectura es multicanal por diseño, pero que la validación de campo disponible no lo es físicamente: cada registro se obtuvo con un nodo HAMMER y un único nodo GEO. La sección 10 explica esa restricción y delimita qué puede y qué no puede concluirse de ella.

`[R04]` [FIGURA 2. Lámina doble a ancho de página. Panel superior: arquitectura del sistema desde el impacto hasta $V_S(z)$, compuesta de «0. Sistema completo - impacto a Vs(z)» y «2a. Arquitectura master-slaves». Panel inferior: cadena fuente–geófono–AFE con el flujo de calibración de offset, compuesto de «4a. Fuente geófono y AFE» y «4b. Calibración de offset». Ambos de `Diagramas_operativos_y_calibracion.drawio`, reducidos a los bloques imprescindibles y con tipografía unificada. Reemplaza a las antiguas figuras 2 y 3.]

### 9.2 Transductor y el conflicto de banda

El elemento sensor es un geófono vertical pasivo SM-24, de frecuencia natural nominal 10 Hz, sensibilidad 28,8 V·s/m y amortiguamiento dependiente de la carga [SM24]. Su elección respondió a la disponibilidad institucional y no a una optimización de la profundidad objetivo, y es importante presentarla así porque de ella se derivan buena parte de las limitaciones del trabajo.

El conflicto con el requerimiento de banda de la sección 8 es cuantitativo. Un geófono se comporta como un sistema de segundo orden pasa-altos respecto de la velocidad del suelo, de modo que su respuesta cae aproximadamente 27,6 dB a 2 Hz y 40 dB a 1 Hz respecto de la zona plana situada por encima de su frecuencia natural. Como la frecuencia mínima necesaria para alcanzar 10 m es del orden de 7,5 Hz, el sensor opera justo en el codo de su propia respuesta; y como alcanzar 50 m requeriría trabajar en torno a 1,5 Hz, el objetivo formal cae de lleno en la región donde el transductor atenúa la señal cuarenta decibelios antes de que ninguna etapa electrónica pueda intervenir.

### 9.3 Frente analógico y calibración

El acondicionamiento implementado en el PSoC 5LP encadena una entrada instrumental, una etapa de ganancia programable, una rama de compensación, un sumador y un filtrado pasa-bajos previo a la conversión. La etapa de compensación es la decisión de diseño central del frente analógico y merece desarrollarse con detalle.

`[C13]` El punto de partida es que una misma tensión de salida del geófono admite dos lecturas. Referida a la velocidad del suelo, la respuesta del sensor es un pasa-altos de segundo orden,

$$
H_v(s)=\frac{V_o(s)}{\dot X_g(s)}=-G_0\,\frac{s^{2}}{s^{2}+2\zeta_0\omega_n s+\omega_n^{2}},
$$

donde $G_0$ es la sensibilidad, $\omega_n=2\pi f_n$ la pulsación natural y $\zeta_0$ el amortiguamiento nominal. Como la aceleración cumple $A_g(s)=s\dot X_g(s)$, la misma salida referida a aceleración resulta

$$
H_a(s)=\frac{H_v(s)}{s}=-G_0\,\frac{s}{s^{2}+2\zeta_0\omega_n s+\omega_n^{2}},
$$

que es un pasabanda y no presenta meseta con el amortiguamiento nominal. Por debajo de $f_n$, $|H_v|$ cae a razón de 40 dB por década y $|H_a|$ a 20 dB por década. No se trata de dos modos de funcionamiento sino de dos referencias de la misma tensión, y la distinción importa porque la estrategia de compensación se formula sobre la referencia a aceleración.

La observación que aporta Ma y colaboradores es que no hace falta invertir la respuesta del sensor, operación mal condicionada porque amplificaría el ruido con la misma pendiente con que el geófono atenúa la señal. Basta con conservar $f_n$ y elevar el amortiguamiento efectivo hasta un valor $\zeta_1\gg\zeta_0$, con lo cual la respuesta referida a aceleración se aplana entre

$$
f_1\simeq\frac{f_n}{2\zeta_1},
\qquad
f_2\simeq 2\zeta_1 f_n,
$$

de modo que $\zeta_1$ se elige para llevar el quiebre inferior $f_1$ hasta la banda de interés. El quiebre superior $f_2$ no constituye un objetivo, ya que la aplicación no requiere extender la banda alta; sólo se conserva la simetría logarítmica $f_1f_2=f_n^{2}$ en torno a $f_n$.

La transferencia que realiza esa transformación es el cociente entre el denominador nominal y el deseado,

$$
H_{\mathrm{comp}}(s)=\frac{s^{2}+2\zeta_0\omega_n s+\omega_n^{2}}{s^{2}+2\zeta_1\omega_n s+\omega_n^{2}},
$$

y al separar el término constante aparece la forma que da nombre a la arquitectura y que se implementa directamente en el circuito,

$$
H_{\mathrm{comp}}(s)=1-\frac{2(\zeta_1-\zeta_0)\,\omega_n s}{s^{2}+2\zeta_1\omega_n s+\omega_n^{2}}.
$$

La estructura $1-\mathrm{BP}$ no es entonces una elección heurística sino una consecuencia algebraica: el camino directo menos un pasabanda centrado en la resonancia del sensor. Su implementación se resolvió desacoplando los dos polos, uno en la entrada y otro en la realimentación de un inversor, de manera que cada uno dependa de un único par $RC$. Esa realización se comparó experimentalmente contra una Sallen-Key y contra una de realimentación múltiple. La Sallen-Key quedó descartada porque su realimentación positiva agrava la sensibilidad del $Q$ a las tolerancias y admite oscilación si los componentes se apartan del valor nominal, mientras que la desviación medida respecto de la respuesta objetivo resultó menor en la realimentación múltiple. Conviene precisar que esta última no se abandonó: es la topología con la que está implementado el filtro pasa-bajos antialias que precede al convertidor. Los valores se resolvieron por búsqueda sobre la malla de componentes comerciales incorporando el modelo no ideal del amplificador del PSoC, y un potenciómetro en serie con la rama pasabanda permite ajustar en cada unidad la proporción de la que depende la cancelación.

El precio de la compensación es alto y conviene explicitarlo, porque condiciona todo el resto del frente analógico. Con los valores implementados se obtiene $f_0=10{,}20$ Hz y un amortiguamiento efectivo $\zeta_1\simeq 937$, que es el valor con el que se diseñó la rama pasabanda. En la zona central la respuesta compensada queda escalada por $1/(2\zeta_1)\simeq 5{,}3\times10^{-4}$, esto es, una atenuación cercana a 1875 veces que debe recuperarse íntegramente en ganancia. Esa ganancia se repartió deliberadamente entre etapas para no concentrar el margen en un solo bloque: la entrada instrumental aporta $\times 2$, la etapa programable entre $\times 1$ y $\times 50$, el sumador $\times 3{,}6$ sobre la rama de compensación y el pasa-bajos $\times 5$, con un producto máximo de $\times 1800$. El propósito de la compensación no es convertir al SM-24 en un sensor de banda ancha, objetivo inalcanzable por vía puramente electrónica, sino conservar una forma de respuesta predecible en la banda baja y aprovechar el margen del convertidor, aceptando a cambio un compromiso explícito con el ruido: toda la cadena de ganancia que restituye ese factor 1875 amplifica también el ruido propio del frente, y es esa tensión la que vuelve indispensables las mediciones de ruido referido a entrada que la sección 12 declara pendientes.

Extender la banda hacia baja frecuencia agrava el problema del offset y de la deriva, que de otro modo consumirían el rango del convertidor sin aportar señal. Para controlarlo, un multiplexor permite observar nodos internos de la cadena con el mismo convertidor, y una rutina de calibración en primer plano ajusta secuencialmente las referencias de la etapa de ganancia, de la rama de compensación, del sumador y del filtro. Durante la captura los lazos se desactivan y se aplican códigos fijos almacenados con verificación de integridad, de manera que ninguna corrección actúe sobre la señal mientras se registra. La revisión posterior del circuito, que sustituye las referencias por fuentes de corriente e incorpora una etapa de ganancia de salida, se encuentra en desarrollo y no participó de la campaña; los resultados de la sección 10 corresponden exclusivamente a la ruta anterior.

### 9.4 Digitalización y temporización determinista

La conversión emplea el convertidor delta-sigma del PSoC configurado a una frecuencia de muestreo del orden de 2604 muestras por segundo, con resolución nominal de 18 bits y rangos bipolares seleccionables que se coordinan con la ganancia programable para aprovechar la escala sin saturar. Un filtro FIR implementado en hardware y varios canales de acceso directo a memoria trasladan la señal cruda y la filtrada sin intervención del procesador.

`[C14]` La elección de una arquitectura delta-sigma frente a una de aproximaciones sucesivas responde a la forma particular del problema. La banda de interés termina por debajo de unos pocos cientos de hertz, de modo que la velocidad de conversión no es una restricción, mientras que el rango dinámico sí lo es: el mismo registro debe contener el primer arribo cercano a la fuente y la llegada atenuada del offset más lejano. Un convertidor delta-sigma explota precisamente ese desbalance, ya que sobremuestrea muy por encima de la banda útil y desplaza el ruido de cuantificación hacia frecuencias altas, donde el diezmado lo elimina; obtiene así una resolución que una arquitectura de aproximaciones sucesivas sólo alcanzaría con un comparador y una referencia considerablemente más costosos. El sobremuestreo aporta una segunda ventaja relevante en campo: relaja la exigencia sobre el filtro antialias analógico, cuyo orden y precisión de componentes habrían tenido que aumentar para proteger una conversión directa a esa velocidad. A ello se suma que el convertidor está integrado en el mismo dispositivo que aloja el acondicionamiento y la lógica de control, lo que evita una interfaz externa y sus problemas asociados de acoplamiento y de temporización.

La temporización de la ventana de captura es el punto donde la sección 8 impone su condición más estricta, y por eso no se delegó al software. Una máquina de estados descrita en lógica programable coordina el disparo, la habilitación del convertidor, el conteo de muestras y el cierre de la captura, de modo que la duración y el instante de la ventana no dependen de la latencia variable del firmware. Esta decisión es la que hace defendible el requerimiento de sincronización, aunque su verificación experimental siga pendiente. `[C15]` Queda además una decisión de diseño abierta que incide directamente sobre esa métrica: la selección de la fuente de reloj que gobierna la ventana. El oscilador interno del dispositivo resulta suficiente para fijar la duración de la captura, pero su deriva y su incertidumbre de frecuencia se acumulan sobre registros largos y entre nodos distintos, de modo que evaluar un cristal externo o una referencia compartida es parte del trabajo necesario para acercarse a la tolerancia derivada en la sección 8.

Corresponde una advertencia explícita sobre la resolución. Los 18 bits son una cifra nominal del convertidor y no un número efectivo de bits medido: faltan ensayos de ruido referido a entrada, linealidad, saturación y repetibilidad por rango y por ganancia. Que la campaña haya registrado señales utilizables demuestra que la cadena funciona, no que su desempeño esté cuantificado.

### 9.5 Sincronización, comunicaciones y trazabilidad

La coordinación entre nodos y el transporte de datos se resuelven sobre módulos ESP32 mediante un protocolo de difusión directa entre pares, que evita depender de infraestructura de red en campo. Como una captura completa excede ampliamente la carga útil de un paquete y el enlace no garantiza entrega, el protocolo fragmenta cada registro, numera las secuencias, confirma la recepción y reintenta los fragmentos faltantes, mientras cada nodo conserva además una copia local. `[C16]` El motivo de exigir la entrega íntegra, y no una reconstrucción aproximada, es que la magnitud que el método estima es una fase: un tramo de muestras faltante no degrada gradualmente el resultado sino que invalida el registro completo para el cálculo de dispersión. De ahí que la política ante una pérdida sea reintentar o descartar, y que la copia local exista precisamente para que descartar no signifique perder la posición.

La separación entre la interfaz de campo, que opera los nodos, y el servidor, que valida, agrupa y preserva los registros junto con su geometría y sus metadatos, es la que permite reconstruir a posteriori cualquier resultado a partir de los datos almacenados.

### 9.6 Fuente instrumentada

La excitación se aplica con un martillo instrumentado PCB 086D20, cuyo sensor piezoeléctrico de tipo ICP entrega una medida de la fuerza aplicada y requiere alimentación por corriente constante con desacople de la polarización [PCB086D20; PCBSignalConditioning]; el acondicionamiento correspondiente se integró en el mismo PSoC. El nodo HAMMER y el nodo GEO se adquieren de forma conjunta y con arranque coordinado, lo que permite referenciar cada respuesta al instante del impacto y, sobre todo, apilar varios golpes por posición.

La repetibilidad de la fuente adquiere una importancia particular en el protocolo empleado. Cuando el arreglo se construye desplazando un receptor, cualquier variación de amplitud, punto de golpe o acoplamiento entre posiciones sucesivas se incorpora al registro como si fuera variación espacial. Registrar entre veinte y treinta y siete golpes por posición y seleccionar el subconjunto más consistente reduce ese riesgo pero no lo elimina, y por esa razón la geometría aparece en la sección 11 como la sensibilidad dominante del resultado.

## 10. Validación experimental

La validación se organiza en los tres niveles que corresponden a un trabajo de instrumentación: la caracterización electrónica del instrumento, una prueba controlada de adquisición y una campaña de campo representativa. El caso de campo se presenta como demostración de la utilidad del instrumento y no como un estudio geofísico autónomo.

### 10.1 Caracterización electrónica del frente analógico

`[C17]` Se excitaron las rutas relevantes del acondicionamiento con barridos senoidales adquiridos por osciloscopio en cuatro canales simultáneos, identificando magnitud y fase con estimación de coherencia. La cobertura se organizó en bandas superpuestas que van desde los 10 mHz hasta los 200 kHz, de modo que la banda crítica para el objetivo de profundidad quedara efectivamente excitada y no extrapolada. La tanda utilizada aquí es la posterior a la calibración manual del compensador, que incorpora las campañas históricas únicamente a las etapas independientes del potenciómetro. La configuración medida se considera representativa de la cadena empleada en la campaña de campo, porque las modificaciones posteriores se concentraron en la lógica digital, la autocalibración y la ganancia, mientras se conservaron los polos y la topología de la señal.

[TABLA 2. Identificación de las etapas del acondicionamiento.]

| Ruta medida | Puntos | Banda identificada | Coherencia | Error de magnitud | Error de fase |
|---|---:|---:|---:|---:|---:|
| BP | 85 | 0,21 Hz – 47,5 kHz | 0,9684 | 6,485 dB | 27,77° |
| COMP | 71 | 0,21 Hz – 4,74 kHz | 0,9643 | 0,379 dB | 2,44° |
| LP | 33 | 11,75 Hz – 1,11 kHz | 0,9454 | 0,596 dB | 2,48° |
| `[C17]` **PGA → ADC (ruta completa)** | **61** | **0,21 Hz – 1,11 kHz** | **0,9946** | **0,200 dB** | **1,16°** |

El resultado central es la última fila. La ruta analógica completa, desde la salida monitoreada de la etapa de ganancia hasta la entrada del convertidor, quedó identificada sobre 61 puntos que abarcan casi cuatro décadas, con coherencia mediana de 0,9946 y errores de 0,200 dB en magnitud y 1,16° en fase. La banda cubierta se extiende hasta 0,21 Hz, es decir, contiene por completo el rango de 1 a 10 Hz del que depende el objetivo de profundidad, y satisface con holgura el requerimiento de respuesta conocida y estable en fase planteado en la sección 8. Este punto merece énfasis porque contradice la expectativa habitual: la limitación de baja frecuencia del sistema no está en el acondicionamiento, que fue medido y resultó predecible allí, sino en la energía que llega a su entrada.

El alcance de esta caracterización tiene, aun así, cuatro límites que deben declararse. El primero es que no cubre la cadena completa desde el movimiento del terreno hasta los códigos almacenados, por lo que no constituye una calibración extremo a extremo: el geófono queda descrito por su modelo nominal y no por una medición propia. El segundo es que, aunque existen puntos por debajo de 1 Hz, la dinámica subsónica del compensador no resulta observable en ellos, de modo que la banda está medida pero el comportamiento del polo inferior no queda resuelto. El tercero se concentra en el compensador: la calibración manual redujo el error de magnitud del compensador respecto del modelo de 26,7 dB a 10,7 dB, una mejora sustancial que sin embargo deja un desajuste remanente en torno a 10 Hz, y el estimador de la posición del potenciómetro no resulta confiable porque ninguna posición fija reproduce toda la forma observada. El cuarto es que la fila de BP mezcla campañas históricas mutuamente inconsistentes, con una dispersión de magnitud mediana de 2,26 dB y de 21,45 dB en el percentil 90, razón por la cual su error de ajuste es mucho mayor que el de las demás etapas y no debe leerse como una degradación del circuito.

Estas mediciones tampoco sustituyen las de ruido referido a entrada, número efectivo de bits, deriva térmica, repetibilidad de la calibración y dispersión entre unidades, ninguna de las cuales fue realizada.

[FIGURA 3. Respuesta identificada de la ruta PGA → ADC: magnitud, fase y coherencia sobre las cuatro décadas medidas, con la banda de 1 a 10 Hz destacada y el modelo nominal del SM-24 encadenado en trazo discontinuo para mostrar la forma de la cadena completa. La leyenda debe aclarar que el geófono entra como modelo y no como medición.]

### 10.2 Prueba controlada de adquisición

El segundo nivel verifica que el sistema adquiere de forma coordinada antes de exigirle un resultado geofísico. El nodo generador se trata como un esclavo más y comparte el arranque con el nodo receptor, de modo que cada respuesta queda referida al instante de su impacto. `[C19]` Para cuantificar esa referencia se midió, dentro de cada posición, la dispersión entre los instantes de disparo de los golpes individuales una vez alineados a nivel de submuestra, obteniéndose un valor del orden de 1,46 ms. Conviene precisar qué describe y qué no describe ese número. Es el residuo de repetibilidad entre golpes sucesivos de un mismo nodo, y agrupa el jitter mecánico del impacto con el del circuito de disparo. No mide, en cambio, ni la deriva entre jornadas de adquisición ni la incertidumbre de la posición del receptor, que son fuentes de error independientes y se tratan como parte del problema de geometría y repetibilidad de la campaña en las secciones 10.3 y 12.

`[C18]` La capa de coordinación entre nodos sí fue probada de forma independiente. En laboratorio se operaron tres nodos simultáneos, uno de clase HAMMER y dos de clase GEO, que ejecutaron correctamente el arranque conjunto y el reparto de la orden de captura. Este ensayo se realizó sobre los módulos de radio sin el acondicionamiento analógico ni el PSoC asociados, de modo que demuestra que el protocolo de coordinación escala más allá de dos nodos y opera como fue diseñado, pero no aporta una cifra de precisión: no hubo conversión sincrónica de señal ni registros exportados que permitan comparar marcas temporales.

Conviene por eso separar cuatro magnitudes que resulta fácil confundir. La primera es la alineación de golpes recién mencionada, que corresponde al procesamiento de un solo nodo. La segunda es la operación funcional de la coordinación multinodo, demostrada con los tres nodos de laboratorio. La tercera es la sincronización digital medida entre nodos distintos, que exige registros simultáneos y una comparación de marcas temporales entre placas completas, y que no pudo realizarse por no disponerse de un conjunto de nodos GEO íntegros. La cuarta es la verificación instrumental del arranque coordinado mediante osciloscopio, que llegó a observarse durante el desarrollo pero cuyos registros no fueron preservados y que por lo tanto no constituye evidencia reproducible. La tolerancia de 130 µs derivada en la sección 8 permanece, en consecuencia, como requerimiento de diseño cuya capa funcional está demostrada y cuya verificación metrológica está pendiente.

Un ensayo exploratorio adicional, realizado frente al Laboratorio LED a una distancia estimada entre 20 y 27 m, registró de forma conjunta los nodos HAMMER y GEO durante 60 s bajo una secuencia de impactos manuales de cadencia aproximadamente constante. El ensayo confirma la operación conjunta de ambos nodos y motivó la línea de trabajo sobre fuentes repetitivas descrita en la sección 12, pero al no haberse conservado los datos crudos no admite cuantificación y se mantiene como observación cualitativa.

### 10.3 Campaña de campo

La campaña se realizó en un predio universitario identificado aproximadamente por el plus code M9F6+Q95, Asunción. El punto de impacto permaneció fijo a varios metros del extremo del campo de fútbol y solamente se desplazó el nodo receptor, siguiendo una línea aproximadamente paralela a los laterales de la cancha. No se conservaron coordenadas ni azimut de los extremos del tendido, limitación que se retoma en la sección 12.

Se relevaron 21 posiciones entre 10 y 50 m de offset, con paso nominal de 2 m y una apertura total de 40 m, valores que corresponden a los límites de aliasing y de apertura establecidos en la sección 8. Del conjunto de 607 registros candidatos, 598 fueron incorporados al conjunto procesado tras la auditoría de calidad, con una mediana cercana a 30 golpes por posición. Debe señalarse que la campaña se adquirió con una configuración de firmware anterior a la descrita en la sección 9.4: la tasa nativa de entonces era de 2929 muestras por segundo, y el conjunto procesado combina registros a 2929 y a 1020 Hz. La decisión de construir el arreglo desplazando un único receptor respondió a que la Facultad dispone solamente de dos geófonos; no fue la geometría prevista por el diseño ni supone que la simultaneidad resulte innecesaria.

Esa restricción define con precisión qué valida la campaña. El conjunto permite construir un **registro multicanal sintetizado por posiciones con fuente activa repetible**, y sobre él evaluar la adquisición real, formar una imagen de dispersión e invertir un perfil preliminar. No demuestra, en cambio, la operación de 21 canales físicos simultáneos, ni la sincronización entre nodos, ni la igualdad de magnitud y fase entre placas distintas. La expresión «adquisición simultánea de 21 canales» sería incorrecta y no se emplea en ningún punto de este trabajo. Conviene señalar que el uso de un solo receptor no carece de antecedentes formales: Lin y Ashlock demostraron que la simulación multicanal con un receptor puede producir imágenes de dispersión comparables a las de MASW bajo condiciones controladas, si bien su protocolo fija el receptor y desplaza la fuente, es decir, exactamente lo inverso a lo realizado aquí [LinAshlock2016].

[FIGURA 4. Croquis de la geometría de campaña: fuente fija, receptor desplazado, offsets de 10 a 50 m y paso de 2 m, con los límites de aliasing y apertura anotados. Declarar en la leyenda que el trazado es aproximado por no disponerse de relevamiento de coordenadas.]

La ventana de offsets utilizada para el resultado final no se decidió durante la adquisición sino después, sobre el conjunto completo, y ese orden debe declararse para evitar la apariencia de una selección oportunista. El análisis posterior evaluó 26 subarreglos contiguos aplicando el mismo criterio a todos ellos, con el resultado de que las ventanas medio-lejanas superan tanto al arreglo completo como a las cercanas. La interpretación es compatible con una menor contaminación por campo cercano y por modos superiores al retirar los offsets pequeños, y con la pérdida de relación señal a ruido por atenuación en los más lejanos, aunque esta explicación no fue aislada mediante un ensayo independiente.

[TABLA 3. Barrido de subarreglos contiguos.]

| Ventana de offsets | Desajuste | Soporte de profundidad | Situación |
|---|---:|---:|---|
| 10–50 m (completo) | 2,28 % | 8,81 m | Referencia |
| 18–46 m | 1,85 % | 10,06 m | Finalista (alcanza 11,83 m con otra convención) |
| 22–42 m | 1,36 % | 10,75 m | Base del modelo presentado |
| 30–50 m | 16,5 % | — | Descartada por desajuste |
| 22–38 m | — | — | Descartada: fracción excesiva de la curva sobre el límite de aliasing |

## 11. Resultados preliminares

Los resultados se presentan en los mismos tres niveles de la sección anterior, distinguiendo en cada uno lo demostrado de lo interpretado.

### 11.1 Resultados de la caracterización del instrumento

`[C20]` `[R11]` La identificación de la tabla 2 verifica el requerimiento de fase de la sección 8 para una unidad y sobre casi cuatro décadas, con tres reservas: no hay medición extremo a extremo que incluya al geófono, la dinámica subsónica del compensador no resulta observable pese a existir puntos allí, y no se midió la dispersión entre placas.

Ese resultado reordena el diagnóstico del sistema. Como el acondicionamiento preserva magnitud y fase por debajo de 10 Hz, la ausencia de señal útil en esa banda que documenta la sección 11.2 no puede atribuirse a la electrónica y debe buscarse en la energía radiada por la fuente, en la respuesta del geófono o en la propagación.

### 11.2 Resultados de la adquisición de campo

La distribución de energía y de relación señal a ruido por bandas caracteriza el desempeño conjunto de la fuente, el terreno y el instrumento. Se calculó sobre 265 golpes repartidos en quince de las distancias relevadas, que es el subconjunto que superó el control de calidad exigido por esta métrica.

La banda de 10 a 50 Hz concentra prácticamente toda la energía registrada y presenta además una coherencia entre posiciones adyacentes de 0,732 en mediana, lo que confirma que se trata de propagación organizada y no de ruido correlacionado en una sola traza. Por debajo de 10 Hz la situación se invierte: la energía cae a menos del uno por ciento del total y la relación señal a ruido llega a ser negativa en algunas posiciones. Este es el resultado central de la campaña desde el punto de vista instrumental, porque identifica la limitación efectiva del sistema y la sitúa donde la sección 8 anticipaba que estaría, esto es, en la banda que gobierna la profundidad alcanzable.

`[R19]` El espectro registrado es el producto de la firma del impacto, el acoplamiento, la propagación, el geófono y la electrónica, y separar sus contribuciones exige los ensayos que propone la sección 12. Descartado el acondicionamiento por lo expuesto en la sección 11.1, la atención debe dirigirse a la fuente y al transductor.

`[R05]` [FIGURA 5. Dos paneles. Izquierda: registro sintetizado por posiciones, en escala de grises y con los offsets rotulados. Derecha: mediana de SNR y fracción de energía por banda, con las cuatro bandas del texto (1–10, 10–50, 50–80 y 80–200 Hz) y el rango entre mínimo y máximo indicado por barras. El panel derecho sustituye a la tabla de SNR, cuyos valores deben quedar legibles en la figura.]

### 11.3 Resultados geofísicos preliminares

Sobre la imagen de dispersión se dibujan los dos límites geométricos derivados en la sección 8. La cresta coherente aparece principalmente en la zona intermedia del plano $f$–$c$, se debilita hacia baja frecuencia a medida que la energía disponible disminuye y se fragmenta en alta frecuencia al aproximarse al límite de aliasing impuesto por el paso de 2 m.

Un procesamiento anterior, restringido a la banda de 8,00 a 21,71 Hz y a una longitud de onda máxima de 10,84 m, había estimado una profundidad de 5,42 m mediante $z\approx\lambda/2$. El análisis posterior sobre el conjunto completo identificó soporte de longitudes de onda del orden de 20 a 22 m en las configuraciones finalistas, lo que conduce a una profundidad de investigación defendible de aproximadamente **10 a 11 m**. Las dos cifras no se contradicen: describen selecciones de banda y criterios de soporte distintos, y la diferencia entre ambas ilustra hasta qué punto el resultado depende de decisiones de procesamiento que deben declararse.

El modelo presentado emplea la ventana de 22 a 42 m y una parametrización de tres capas. La elección del número de capas no se justifica porque produzca menor dispersión, criterio que favorece mecánicamente a los modelos con menos parámetros, sino mediante la partición de la varianza entre sus dos fuentes posibles. Sobre 24 remuestreos por bootstrap del dato real y 5 semillas del optimizador, es decir 120 inversiones por configuración, con tres capas prácticamente la totalidad de la variabilidad del perfil resulta atribuible al remuestreo de los datos, mientras que a partir de la cuarta capa cerca de la mitad de la dispersión proviene del optimizador. Se adopta por tanto el modelo más complejo cuya incertidumbre sigue estando dominada por la medición: las capas adicionales no quedan determinadas por el dato.

El perfil resultante se comporta esencialmente como un escalón, con una velocidad somera del orden de 78 m/s, una interfaz efectiva próxima a 2,4 m y velocidades del orden de 178 m/s por debajo, dentro de buena parte del soporte disponible. Cuatro reservas acompañan necesariamente a estas cifras. La interfaz es efectiva, es decir, la profundidad a la que el modelo sitúa el cambio de rigidez que reproduce la curva observada, y no un contacto geológico identificado. La inversión impone monotonía creciente de $V_S$, restricción que en pruebas sobre modelos sintéticos ocultó por completo una inversión de velocidad conocida, y liberarla con el dato real no produjo un perfil restringido. El coeficiente de Poisson no fue medido, y su variación afecta poco a la velocidad somera pero ensancha de manera apreciable la incertidumbre en profundidad. Y un desajuste bajo demuestra consistencia con el modelo impuesto, no unicidad de la solución. Por la misma razón, $V_{S,30}$ no puede calcularse: la profundidad sustentada no alcanza los 30 m.

La sensibilidad del resultado a las decisiones de procesamiento fue evaluada de forma sistemática, y el orden de magnitud de los efectos resulta más informativo que cualquiera de las cifras por separado. Cambiar la transformada modifica la curva de dispersión en 2,28 m/s de mediana y cambiar el algoritmo de extracción en 1,89 m/s, mientras que eliminar solamente dos posiciones del tendido, las de 32 y 40 m, la desplaza 29,76 m/s en valor cuadrático medio. La geometría pesa así aproximadamente trece veces más que la elección del algoritmo. Este resultado orienta el trabajo futuro con más claridad que ningún otro: la prioridad no es refinar el procesamiento sino controlar la geometría y ampliar la banda baja.

[FIGURA 6. Imagen de dispersión con los límites de apertura y aliasing trazados, curva seleccionada superpuesta y, en panel adjunto, el perfil $V_S(z)$ de tres capas con su banda de incertidumbre. La cifra de 11,83 m no debe aparecer en el título ni en la leyenda, por corresponder a otra ventana de offsets.]

El informe hidrogeológico de julio de 2023 aporta un contraste de plausibilidad. Sus sondeos eléctricos verticales se ubican en el mismo predio, a distancias del orden de 120, 258 y 340 m de la línea de adquisición, que no pueden precisarse por no haberse registrado las coordenadas de los extremos. El sondeo más próximo presenta interfaces eléctricas a 1,00, 2,06 y 4,15 m, de modo que la interfaz efectiva de 2,4 m obtenida por inversión cae dentro de un intervalo en el que el sondeo eléctrico también detecta contactos. La coincidencia debe leerse como compatibilidad en el intervalo de 2 a 4 m y de ninguna manera como un acuerdo de centímetros, tanto por la distancia entre emplazamientos como porque ambas técnicas miden propiedades distintas: la resistividad no mide rigidez y la velocidad de corte no mide contenido de humedad. El contraste sirve para verificar que el resultado no es físicamente inverosímil, no para validarlo.

### 11.4 Síntesis: qué está demostrado y qué no

[TABLA 4. Síntesis del estado de cada afirmación.]

| Afirmación | Estado | Base |
|---|---|---|
| La plataforma adquiere de forma conjunta una referencia de impacto y la respuesta del receptor | Demostrado | 598 registros aceptados con referencia temporal |
| Los datos se almacenan, organizan y procesan mediante un flujo reproducible | Demostrado | Manifiesto, servidor de ingesta y análisis repetible |
| La ruta analógica preserva magnitud y fase con 0,200 dB y 1,16° entre 0,21 Hz y 1,11 kHz | Demostrado para una unidad | Identificación sobre 61 puntos |
| La banda útil de campo se concentra entre 10 y 50 Hz | Demostrado | Métricas de energía y SNR sobre 265 golpes en 15 distancias |
| Un arreglo sintetizado de 21 posiciones permite obtener imagen y curva de dispersión | Demostrado | Procesamiento de la campaña |
| El soporte de investigación es de aproximadamente 10 a 11 m | Preliminar | Longitud de onda soportada y convención $z\approx\lambda/2$ |
| El perfil de tres capas describe el sitio | Preliminar | 120 inversiones por configuración; sujeto a monotonía y a $\nu$ supuesto |
| La interfaz de 2,4 m corresponde a un contacto geológico | No afirmado | Es una interfaz efectiva del modelo |
| Adquisición simultánea con varios nodos GEO completos | No demostrado | Un solo nodo GEO íntegro operativo por registro |
| `[C21]` Coordinación de arranque con tres nodos simultáneos | Demostrado funcionalmente | Ensayo de laboratorio sobre los módulos de radio |
| Sincronización entre nodos dentro de 130 µs | No demostrado | Sin registros comparables entre placas completas |
| Ruido referido a entrada, ENOB y calibración extremo a extremo | No medidos | Ensayos pendientes |
| Caracterización hasta 50 m o cálculo de $V_{S,30}$ | Fuera de alcance actual | Banda y apertura insuficientes |

## 12. Limitaciones y trabajos futuros

`[C22]` **Caracterización metrológica del instrumento.** La ruta analógica está identificada desde 0,21 Hz, de modo que el trabajo pendiente no consiste en ampliar la banda medida sino en cerrar la cadena. Debe medirse magnitud y fase extremo a extremo, desde una entrada mecánica trazable hasta los códigos almacenados, para cada combinación de rango y ganancia, incorporando al geófono como elemento medido y no como modelo nominal. Del lado del compensador queda resolver el desajuste remanente en torno a 10 Hz mediante la calibración fina con tono fijo que recomienda el registro de la propia sesión de medida, y esclarecer la dinámica subsónica, que permanece no observable pese a existir puntos por debajo de 1 Hz. A ello se suman las mediciones de ruido referido a entrada, número efectivo de bits, linealidad, saturación, deriva térmica y repetibilidad de la autocalibración, ninguna de las cuales fue realizada.

`[R02]` **Operación multicanal.** Completar la revisión de placa en curso, fabricar varios nodos equivalentes y medir entre ellos la dispersión de ganancia y de fase es la condición para que el sistema pueda llamarse multicanal en sentido experimental y no sólo arquitectónico. El ensayo de sincronización debe repetirse conservando los registros, para contrastar el desempeño real contra la tolerancia de 130 µs de la sección 8, y cada captura futura deberá incorporar como metadato la revisión de circuito y de firmware que la produjo.

`[R03]` **Geometría y protocolo de campaña.** El tendido debe relevarse con coordenadas y azimut, dado que la sensibilidad medida en la sección 11.3 sitúa a la geometría como el factor dominante del resultado. Conviene repetir la línea con receptores simultáneos, incorporar una posición de referencia fija que separe la variación temporal de la espacial y contrastar el perfil con una referencia independiente en el mismo punto. Para campañas condicionadas por la disponibilidad de sensores, el esquema de simulación multicanal con un receptor ofrece una alternativa con antecedentes formales [LinAshlock2016], que no sustituye la validación final del sistema multicanal diseñado.

`[R01]` **Fuente y extensión de la banda baja.** La sección 11.2 identifica a la energía coherente por debajo de 8 Hz como la limitación efectiva de la profundidad, y de allí se sigue la línea de trabajo sobre fuentes de impacto repetitivo. Repetir impactos y acumularlos de forma coherente mejora idealmente la relación señal a ruido como $\sqrt{N}$ frente a ruido no correlacionado, pero conviene distinguir la repetición de la periodicidad: una cadencia estrictamente fija concentra esa ganancia en un peine espectral formado por la frecuencia de repetición y sus armónicos, y en una cadena lineal refuerza componentes que ya existen sin crear señal donde el producto fuente–suelo–sensor–electrónica es nulo. El diseño de leva desarrollado hasta ahora, con cadencia de 45 impactos por minuto, corresponde a una fundamental de 0,75 Hz y coloca dentro de la banda de 1 a 10 Hz solamente doce líneas, la primera a 1,50 Hz; describirla como una fuente de 1 Hz sería incorrecto. Cabe además una precisión bibliográfica, porque la literatura suele citarse en sentido inverso al que sostiene: el Mini-Sosie original variaba la velocidad del motor para obtener una secuencia aproximadamente aleatoria y registraba el instante real de cada golpe [Barbier1976], y la técnica de impacto barrido fue desarrollada para reflexión de alta frecuencia, con una secuencia que deliberadamente atenúa las frecuencias inferiores a la tasa inicial de impacto [Park1996SIST]. Ninguna de las dos avala por sí sola una ganancia en baja frecuencia, y la evaluación deberá ser comparativa, con igual número de golpes entre excitación aislada, cadencia fija y secuencia no periódica, juzgando el resultado por la longitud de onda coherente entre offsets y no por la aparición de picos espectrales.

`[R01]` De ese programa se derivan dos requerimientos que sí corresponden a la electrónica de este trabajo. El primero es que el disparo debe sensar el impacto real sobre la placa, mediante un piezoeléctrico o un acelerómetro de banda suficiente, y no la posición angular de la leva, porque el juego mecánico y el rebote introducen entre ambos una diferencia variable. El segundo es que la marca temporal de cada golpe debe generarse con el mismo reloj que muestrea el canal del receptor: la red inalámbrica transporta los datos, no define el instante del impacto. La tolerancia se obtiene del razonamiento de fase de la sección 8: para una dispersión $\sigma_t$ en los instantes de impacto el factor de coherencia del apilamiento decae como $\exp[-\tfrac{1}{2}(2\pi f\sigma_t)^2]$, de modo que una pérdida inferior al 5 % exige $\sigma_t\lesssim 0{,}051/f$, esto es 5,1 ms a 10 Hz y 1,02 ms a 50 Hz. El valor de 1,46 ms medido en la sección 10.2 resulta holgado en el extremo inferior de la banda, con 0,4 % de pérdida, y apenas marginal en el superior, con cerca del 10 %. El requerimiento de temporización lo fija por lo tanto la frecuencia más alta que se pretenda apilar, no la cadencia del martillete.

**Alcance del objetivo formal.** El objetivo de 50 m permanece como meta de diseño del proyecto y requiere, según la relación derivada en la sección 8, contenido coherente en torno a 1,5 Hz. Alcanzarlo exige actuar sobre los tres factores simultáneamente: un transductor con frecuencia natural menor o una compensación validada en esa banda, una fuente capaz de radiar energía útil allí, y una apertura de arreglo compatible con longitudes de onda de un centenar de metros. Ninguno de los tres está resuelto hoy, y presentarlo de otro modo sería incompatible con la evidencia reunida.

## Referencias

> Lista preliminar. En la versión LaTeX se conservarán únicamente las referencias efectivamente citadas y se completarán en `referencias.bib` las entradas que hoy faltan.

- Foti, S., Lai, C. G., Rix, G. J. y Strobbia, C. (2014). *Surface Wave Methods for Near-Surface Site Characterization*. [Foti2014]
- Foti, S. et al. (2018). Guidelines for the good practice of surface wave analysis. *Bulletin of Earthquake Engineering*, 16, 2367–2420. [Foti2018]
- Kramer, S. L. (1996). *Geotechnical Earthquake Engineering*. Prentice Hall. [Kramer1996]
- Park, C. B., Miller, R. D. y Xia, J. (1999). Multichannel analysis of surface waves. *Geophysics*, 64(3), 800–808. DOI: 10.1190/1.1444590 [Park1999]
- Park, C. B., Miller, R. D. y Xia, J. (1998). Imaging dispersion curves of surface waves on multi-channel record. *SEG Technical Program Expanded Abstracts*. [Park1998]
- Xia, J., Miller, R. D. y Park, C. B. (1999). Estimation of near-surface shear-wave velocity by inversion of Rayleigh waves. *Geophysics*, 64(3), 691–700. [Xia1999]
- Park, C. B., Miller, R. D. y Steeples, D. W. (1996). Swept impact seismic technique (SIST). *Geophysics*, 61(6). DOI: 10.1190/1.1444095 [Park1996SIST]
- Lin, S. y Ashlock, J. C. (2016). Surface-wave testing of soil sites using multichannel simulation with one-receiver. *Soil Dynamics and Earthquake Engineering*, 87, 82–92. DOI: 10.1016/j.soildyn.2016.04.013 [LinAshlock2016 — **entrada por agregar al .bib**]
- Barbier, M. G., Bondon, P., Mellinger, R. y Viallix, J. R. (1976). Mini-Sosie for land seismology. *Geophysical Prospecting*, 24(3), 518–527. DOI: 10.1111/j.1365-2478.1976.tb00952.x [Barbier1976 — **entrada por agregar al .bib; verificar contra la fuente primaria**]
- Guan, J. et al. (2022). Linear array analysis of passive surface waves combined with mini-Sosie technique. *Geophysical Journal International*. DOI: 10.1093/gji/ggac169 [Guan2022]
- Ma, J. et al. (2023). Compensación electrónica de geófonos mediante arquitectura $1-\mathrm{BP}$. [Ma2023 — **verificar cita completa**]
- Input/Output Inc. *SM-24 Geophone Element Data Sheet*. [SM24]
- PCB Piezotronics. *Model 086D20 Impulse Force Hammer* y notas de acondicionamiento ICP. [PCB086D20; PCBSignalConditioning]

---

# Anexos editoriales (no forman parte del texto final)

## Anexo A. Presupuesto de 15 páginas y correspondencia con la estructura del tutor

Formato supuesto: A4 a dos columnas, como el PDF actual de `latex-15p-review`. La portada no es independiente: el título y los datos del autor encabezan la página 1.

| Página | Sección del tutor | Contenido dominante |
|---:|---|---|
| 1 | §1 | Título, importancia de la caracterización, $V_S$ y $G_{\max}$, objetivo, contribución, tres alcances, hoja de ruta |
| 2 | §2 – §3 | Métodos tradicionales + Tabla 1; métodos basados en ondas mecánicas |
| 3 | §4 – §5 | Fundamentos de propagación; ondas de cuerpo y superficiales; $\lambda=c/f$ |
| 4 | §6 | Dispersión, cadena de inferencia, no unicidad + Figura 1 |
| 5 | §7 – §8 | Selección de MASW; inicio de la derivación de requerimientos |
| 6 | §8 | Derivaciones cuantitativas + **Tabla 2 (puente)** |
| 7 | §9.1 – §9.2 | Arquitectura + Figura 2; SM-24 y conflicto de banda |
| 8 | §9.3 – §9.4 | AFE, compensación y calibración + Figura 3; ADC y temporización |
| 9 | §9.5 – §9.6 | Comunicaciones y trazabilidad; fuente instrumentada |
| 10 | §10.1 – §10.2 | Caracterización electrónica + Tabla 3 + Figura 4; prueba controlada |
| 11 | §10.3 | Campaña, geometría + Figura 5, selección de subarreglos |
| 12 | §11.1 – §11.2 | Resultados de instrumentación y de adquisición + Figura 6 |
| 13 | §11.3 | Dispersión, inversión, perfil, sensibilidad + Figura 7 |
| 14 | §11.3 – §11.4 | Contraste hidrogeológico; tabla de síntesis |
| 15 | §12 + Referencias | Limitaciones y trabajos futuros; referencias |

**Riesgo de espacio.** El borrador contiene 7 figuras y 6 tablas. En 15 páginas a dos columnas eso es apretado. Orden de recorte sugerido, de menor a mayor pérdida: (1) convertir la Tabla 1 en prosa; (2) fundir la Tabla 5 dentro de la Figura 6; (3) fundir las Figuras 2 y 3 en una sola lámina de arquitectura y cadena analógica. La Tabla 2 y las Figuras 6 y 7 no deben recortarse.

## Anexo B. Diagramas Draw.io disponibles y su destino

`Diagramas_operativos_y_calibracion.drawio`

| Página del archivo | Destino |
|---|---|
| 0. Sistema completo - impacto a Vs(z) | Figuras 1 y 2 del PDF (recortes distintos) |
| 2a. Arquitectura master-slaves | Figura 2 del PDF; diapositiva principal |
| 4a. Fuente geófono y AFE | Figura 3 del PDF; diapositiva principal |
| 4b. Calibración de offset | Figura 3 del PDF (mitad inferior) |
| 1. Flujo operativo UML | Diapositiva principal |
| 2b. Sincronización y comienzo de captura | Diapositiva auxiliar (respalda §8 y §10.2 en preguntas) |
| 3a / 3b. Almacenamiento local y vaciado ordenado | Diapositivas auxiliares |
| 4c / 4d. superMáquina PSoC (Verilog) e integración | Diapositivas auxiliares |
| 5. Ingesta y procesamiento del servidor | Diapositiva principal o auxiliar |
| R. Modelo UML de nodos | Diapositiva auxiliar |

`SuperMaquina_hardware_digital_y_fsm.drawio`

| Página del archivo | Destino |
|---|---|
| 1. Hardware digital y lógica interna | Diapositiva auxiliar (respalda §9.4) |
| 2. FSM y flujo secuencial detallado | Diapositiva auxiliar |

Ninguna de estas dos páginas entra al PDF: son demasiado densas para el cuerpo principal, pero son exactamente el material que el tribunal pedirá si pregunta por determinismo de la ventana de captura.

**Mejoras a los diagramas antes de exportarlos.** Unificar tipografía y grosor de línea entre páginas; eliminar rótulos internos de desarrollo; garantizar legibilidad en escala de grises y a ancho de columna; y rotular con precisión si cada bloque corresponde al prototipo usado en la campaña, a la revisión en desarrollo o a la arquitectura objetivo.

## Anexo C. Mapa de afirmaciones y evidencia

| Afirmación del texto | Clase | Evidencia | Condición de uso |
|---|---|---|---|
| La plataforma adquirió señales de campo y las procesó hasta una inversión | Dato propio | Conjunto de datos, manifiesto, interfaces y análisis | No equivale a operación multinodo |
| 21 posiciones sintetizadas entre 10 y 50 m | Dato propio | Metadatos de la campaña | Geometría sin coordenadas precisas |
| Banda útil de campo 10–50 Hz | Dato propio | Métricas de SNR y energía | Propiedad de la campaña completa, no sólo del AFE |
| Error de fase < 2° entre 11,6 Hz y 863 Hz | Dato propio | Barridos de identificación | Una sola unidad; excluye < 11,6 Hz |
| Soporte defendible de 10–11 m | Dato propio + convención | Longitud de onda soportada y $z\approx\lambda/2$ | No es resolución uniforme |
| Tres capas es el modelo sostenible | Dato propio + criterio | 120 inversiones por configuración; partición de varianza | Depende de la parametrización adoptada |
| Interfaz efectiva de 2,4 m | Inferencia calificada | Perfil invertido | No identifica litología |
| Tolerancia de sincronización ≈ 130 µs | Consecuencia matemática | $\Delta c/c \simeq c\,\Delta t/\Delta x$ | Es un requerimiento derivado, no una medición |
| La baja frecuencia limita la profundidad | Inferencia apoyada | Energía y SNR de campo, geometría, bibliografía | No permite asignar una única causa |
| Apilar $N$ impactos mejora la SNR como $\sqrt{N}$ | Modelo ideal | SIST y buenas prácticas | Exige repetibilidad, alineación y ruido no correlacionado |
| 45 impactos por minuto dan una fundamental de 0,75 Hz | Consecuencia matemática | $f = \mathrm{rpm}/60$ | No demuestra propagación Rayleigh a 0,75 Hz |
| El sondeo eléctrico cercano es compatible | Inferencia calificada | Informe hidrogeológico 2023 | Contexto de plausibilidad, no validación puntual |

## Anexo D. Decisiones que quedan abiertas

1. **Sin sección de Conclusiones.** La estructura del tutor termina en «12. Limitaciones y trabajos futuros» y no contempla un apartado de conclusiones, por lo que el cierre argumental se resolvió dentro de §11.4. Confirmar si se mantiene así o si la cátedra espera un cierre explícito.
2. **Sin resumen.** Decidido: la estructura del tutor no incluye abstract y el documento abre directamente en §1.
3. **Cita de Ma et al. (2023).** Verificar la referencia completa de la arquitectura $1-\mathrm{BP}$ antes de pasar a LaTeX.
4. **Gao y Pan (2018).** No se cita en el cuerpo. Su aporte sobre estimación de la firma de fuente encaja mejor como diapositiva auxiliar si el tribunal pregunta por la wavelet del martillo.
5. **Fotografías del hardware.** No se localizaron fotos físicas de las placas; las imágenes disponibles son esquemáticos. Si aparecen, una lámina compacta de la evolución placa universal → placa por transferencia → PCB fabricada reforzaría el carácter de implementación electrónica en §9, y el registro completo iría a diapositivas auxiliares.
6. **Barridos de baja frecuencia ya adquiridos.** La campaña de osciloscopio incluye bandas desde 10 mHz y la tanda calibrada identifica la ruta PGA → ADC desde 0,21 Hz. El borrador anterior afirmaba que la cadena no estaba caracterizada por debajo de 11,6 Hz, lo que era incorrecto: esa cifra provenía de una corrida de identificación parcial. Confirmar que la tanda calibrada es la que debe citarse en el documento final.
7. **Informe externo sobre fuentes repetitivas (27 de agosto).** Sus correcciones sobre SIST, Mini-Sosie clásico y presupuesto de jitter ya están incorporadas a §12. Las referencias que aporta (Barbier 1976; Chen et al. 2017; Yang et al. 2020 y 2021; Lin et al. 2024) deben verificarse contra la fuente primaria antes de entrar al `.bib`; sólo Barbier se cita en el cuerpo, el resto es material de diapositiva auxiliar.
8. **Velocidad de referencia en las derivaciones de §8.** Se usó $c_R\approx150$ m/s, coherente con el perfil obtenido. Si se prefiere un valor conservador distinto, cambian las cifras de 7,5 Hz, 1,5 Hz y 130 µs de forma proporcional.


## Anexo E. Registro de cambios de esta ronda

Los marcadores `[C##]` dentro del texto señalan el inicio de cada bloque modificado, para poder revisar sólo lo que cambió. Este anexo no forma parte del texto final y debe eliminarse al pasar a LaTeX.

| Marca | Sección | Qué cambió | Origen |
|---|---|---|---|
| C01 | Encabezado | Bloque Alumno / Matrícula / Tutor / Carrera al estilo de Federico Morán. Faltan matrícula y tutor. | comentario |
| C02 | §1 | Objetivo reescrito en registro impersonal: «se tiene como objetivo de este proyecto de fin de grado». | comentario |
| C03 | §1 | Misma corrección de registro en el párrafo de foco electrónico. | comentario |
| C04 | §2 | Nuevo: control de calidad de obra y seguimiento de mantenimiento como campo de aplicación de MASW. | comentario |
| C05 | §4 | Ampliado y con fuente: rango de densidad frente al de $V_S$; $V_P$ dominada por el agua intersticial bajo el freático. | comentario |
| C06 | §4 | Reescritura del párrafo de idealizaciones; mismo mensaje, redacción más natural. | comentario |
| C07 | §5 | Nuevo: cómo P y SV se acoplan en la superficie libre y forman Rayleigh, y por qué SH forma Love y no se ve con geófono vertical. | comentario |
| C08 | §5 | Declarada la variable $z$. | comentario |
| C09 | §7 | Aclarado: dos geófonos disponibles, un nodo receptor operativo por registro. | comentario |
| C10 | §8 | Añadido el criterio $L\gtrsim1{,}5\lambda_{\max}$ y su verificación cruzada: 40 m admiten ~27 m, consistente con el soporte de 20–22 m. | comentario |
| C11 | §8 | Frase de entrada a la Tabla 2 explicando que anticipa §9 y §10, más referencias cruzadas por celda. | comentario |
| C12 | §8 | Filas de la Tabla 2 actualizadas: banda baja, sincronización y multinodo, con cita a [Ma2023]. | comentario + hallazgo |
| C13 | §9.3 | **Reescritura mayor.** Respuesta referida a velocidad frente a aceleración, por qué no se invierte la respuesta del sensor, elevación de $\zeta$ y quiebres $f_1,f_2$, derivación algebraica de la forma $1-\mathrm{BP}$, topología elegida y el precio de 1876 veces que se paga en ganancia. | comentario |
| C14 | §9.4 | Nuevo: por qué delta-sigma y no aproximaciones sucesivas. | comentario |
| C15 | §9.4 | Nuevo: la selección de la fuente de reloj queda como decisión abierta que afecta la métrica de sincronización. | comentario |
| C16 | §9.5 | Reemplazado el argumento de la interpolación por el requisito real: la pérdida invalida el registro para el cálculo de fase. | comentario |
| C17 | §10.1 | **Sección reescrita.** Se cita la tanda calibrada: ruta PGA → ADC identificada sobre 61 puntos entre 0,21 Hz y 1,11 kHz, con 0,200 dB y 1,16°. Nueva tabla y cuatro límites declarados. Corrige la afirmación anterior de que la cadena no estaba caracterizada bajo 11,6 Hz. | hallazgo |
| C18 | §10.2 | Nuevo: ensayo de laboratorio con tres nodos simultáneos. Las magnitudes a distinguir pasan de tres a cuatro. | comentario |
| C19 | §10.2 | El valor de 1,46 ms reescrito sin ambigüedad: residuo entre golpes de un mismo nodo, no deriva entre jornadas ni error de posición. | comentario |
| C20 | §11.1 | Coherente con C17, más la consecuencia argumental: si la electrónica preserva fase bajo 10 Hz, la falta de señal allí no es de la electrónica. | hallazgo |
| C21 | §11.4 | Filas de síntesis actualizadas: AFE con las cifras nuevas, coordinación de tres nodos como demostrada, sincronización métrica como pendiente. | hallazgo |
| C22 | §12 | Instrumentación reescrita: el pendiente ya no es ampliar la banda medida sino cerrar la cadena con el geófono incluido. | hallazgo |
| C23 | §12 | Fuente repetitiva: corrección sobre SIST, Mini-Sosie de Barbier, presupuesto de jitter contra el 1,46 ms medido y requisitos de disparo. | informe externo |

### Recortes de compresión de esta ronda

Marcadores `[R##]`. Cuerpo: 11.536 → 10.789 palabras. Figuras 8 → 6, tablas 7 → 4.

| Marca | Sección | Recorte |
|---|---|---|
| R01 | §12 | Bloque de fuente repetitiva de 848 → 460 palabras. Se conservan la distinción repetición/periodicidad, las doce líneas de 45 rpm, la corrección sobre SIST y Barbier, el presupuesto de jitter y los dos requerimientos de disparo. Sale el protocolo experimental detallado, que va a diapositiva auxiliar. |
| R02 | §12 | Operación multicanal condensada. |
| R03 | §12 | Geometría y protocolo de campaña condensados. |
| R04 | §9.1 | Figuras 2 y 3 fundidas en una lámina de dos paneles a ancho de página. |
| R05 | §11.2 | La tabla de SNR por banda se absorbe en la figura 5. |
| R06 | §3 | Formulación genérica del problema inverso, que §6 desarrolla mejor. |
| R07 | §4 | Efecto del coeficiente de Poisson diferido a §11.3. |
| R08 | §5 | Advertencia sobre baja frecuencia abreviada; se desarrolla en §12. |
| R09 | §6 | Cadena de cuatro etapas remitida a la figura 1. |
| R10 | §6 | No unicidad abreviada; se aplica en §11.3. |
| R11 | §11.1 | Deja de repetir las cifras de la tabla 2 y remite a ella. |
| R12 | §12 | Deja de repetir el contexto del valor de 1,46 ms. |
| R13 | §9.4 | Segunda mención de la frecuencia de muestreo eliminada. |
| R14 | §1 | No unicidad abreviada. |
| R15 | §1 | Argumento de accesibilidad condensado. |
| R16 | §1 | Hoja de ruta abreviada. |
| R17 | §2 | SPT, CPT, downhole y crosshole condensados en dos párrafos. |
| R18 | §5 | Polarización P/S fundida con la distinción SV/SH. |
| R19 | §11.2 | Causa múltiple condensada, remitiendo a §11.1. |

**Estado de espacio.** Estimación actual: 13,4 páginas de texto + 1,3 de figuras + 1,1 de tablas ≈ **15,9 páginas**. Faltan unas 700 palabras o el equivalente en elementos flotantes para entrar en 15. Los recortes que quedan afectan contenido pedido explícitamente, por lo que la decisión es del autor.
