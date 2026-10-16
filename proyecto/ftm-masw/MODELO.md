# Modelo de línea imperfecta y vínculo con MASW

Estado: propuesta. Las ecuaciones son deducciones geométricas; sus ejemplos no representan precisión medida.

## Colocación encadenada descrita por el operario

El operario mide 1 m o 2 m desde el esclavo anterior y coloca el siguiente. La dirección puede cambiar en cada tramo.

Este procedimiento aporta información sobre la longitud de cada enlace vecino. La dirección del enlace sigue siendo incierta si no se mide un ángulo.

Conocer la longitud ubica al siguiente nodo sobre una circunferencia. Admitir error de longitud produce una corona circular.

La intención de avanzar aproximadamente recto favorece un sector de esa corona. Su apertura debe estimarse mediante colocaciones reales, no elegirse para mejorar el gráfico.

Se propone el siguiente modelo plano:

```text
p[i+1] = p[i] + L[i] * (cos(theta[i]), sin(theta[i]))
L[i] = d[i] + b_longitud + epsilon[i]
```

Aquí `p[i]` es una posición en metros y `d[i]` es el tramo nominal en metros. `b_longitud` representa un sesgo compartido en metros.

`epsilon[i]` representa el error particular del tramo, en metros. `theta[i]` representa su dirección en radianes; todavía no se dispone de una medición angular.

Se compararán dos formas de representar esa dirección:

- Referencia visual global: cada dirección se distribuye alrededor de un rumbo común.
- Referencia al tramo anterior: la dirección cambia mediante un giro local, con posible tendencia persistente hacia un lado.

La segunda hipótesis admite `theta[i+1] = theta[i] + b_giro + eta[i]`. El giro medio `b_giro` y su variación `eta[i]` se expresan en radianes.

La aclaración posterior del operario favorece un modelo mixto: mira hacia el esclavo inicial y el conjunto, pero da más peso a los esclavos cercanos.

Se propone representar la dirección mediante la línea visual estimada a partir de varios nodos previos. La influencia de los nodos cercanos será mayor.

Los pesos, la dispersión angular y su correlación quedan por identificar. Esta referencia visual no equivale a medir un azimut absoluto.

Mirar solamente hacia el esclavo inicial define una dirección desde la posición actual. No demuestra que esa posición siga sobre el eje de los primeros tramos.

La secuencia de instalación y la intención de usar un espaciamiento común quedan confirmadas. La longitud concreta y el orden de identificadores se registrarán por montaje.

Con espaciamiento nominal `d`, la progresiva nominal del nodo `i` es `i*d`. Esa progresiva describe la cadena prevista; no es su coordenada longitudinal medida.

La secuencia fija qué nodos son vecinos y evita buscar permutaciones arbitrarias. La longitud aporta escala, con incertidumbre y posibles sesgos compartidos.

La cadena todavía puede doblarse. El modelo visual favorece continuidad, pero debe admitir una colocación excepcional que contradiga esa intención.

Ninguna distribución angular está validada. El procedimiento de colocar placas no equivale a disponer de una odometría que mida posición y orientación.

En un tramo de 2 m, una desviación de 10° respecto de la dirección prevista produce 0,347 m laterales y 1,970 m de avance.

La longitud puede ser correcta y la posición lateral cambiar 35 cm. Una rotación idéntica de todo el tendido es una orientación global; la deformación aparece con cambios relativos.

La longitud acumulada de la cadena, la distancia entre extremos y la proyección sobre un eje son magnitudes distintas.

### Acumulación y conocimiento previo

Los errores independientes de longitud acumulan varianza. Un sesgo de longitud repetido acumula error aproximadamente proporcional al número de tramos.

Con ángulos pequeños y direcciones independientes respecto de un rumbo común, la desviación lateral típica puede crecer como la raíz del número de tramos.

Si los giros incrementales son independientes y la dirección acumula esos giros, esa desviación puede crecer como el número de tramos elevado a 3/2.

Son aproximaciones para modelos distintos, no predicciones del tendido real. Las correlaciones y tendencias del operario deben medirse.

El ejemplo del usuario sobre el esclavo 15 no fija el número final de placas. Los índices geométricos tampoco sustituyen los identificadores de firmware.

### Estimación propuesta

Se propone ajustar conjuntamente todas las posiciones quietas. Cada tramo aporta su longitud aproximada y cada rango FTM aporta una restricción entre dos nodos.

El conocimiento de colocación entra como distribución previa. Los rangos FTM entran como observaciones con error, sesgo y condiciones documentadas.

Un grafo de factores permite expresar esas relaciones y realizar estimación de máximo a posteriori. La [introducción de GTSAM](https://gtsam.org/tutorials/intro.html) describe este marco general.

La elección es conceptual: todavía no se propone añadir GTSAM como dependencia. Puede evaluarse primero con las herramientas numéricas existentes.

Para el montaje estático, el ajuste conjunto permite que un rango entre nodos alejados corrija varias posiciones anteriores.

Un filtro de Kalman extendido o un suavizador son alternativas. El índice de colocación y el tiempo de nuevas observaciones deben distinguirse explícitamente.

La misma cinta o longitud nominal se incorpora una vez. Reintroducirla como una observación independiente en cada lectura reduciría artificialmente la incertidumbre.

Las partículas o varias inicializaciones ayudan cuando existen formas alternativas, reflexiones o ambigüedades. Una nube más estrecha no demuestra mayor exactitud.

La longitud vecina, la continuidad angular y la alineación visual provienen del mismo procedimiento de colocación. No deben contarse como tres mediciones independientes.

Se recomienda un modelo generativo conjunto del procedimiento o una representación explícita de sus dependencias. Esto evita reforzar artificialmente el conocimiento previo.

Solo medir vecinos deja muchos giros sin observar. Conviene medir también enlaces que salten nodos, enlaces largos y distancias al maestro fuera del eje.

Los enlaces largos tampoco garantizan sensibilidad lateral suficiente. Se evaluará su información aportada frente al costo de radio y la incertidumbre real.

No se ajustarán sesgos arbitrarios por enlace junto con posiciones sin referencias suficientes. Esos parámetros podrían absorber cualquier geometría.

### Cómo demostrar que FTM mejora el conocimiento previo

Se compararán tres estimaciones contra referencias reservadas: solo colocación, solo FTM y colocación combinada con FTM.

El modelo angular, la calibración y los umbrales se fijarán antes de evaluar esas referencias. La comparación medirá error y cobertura de incertidumbre.

Las paredes se registrarán como condición de propagación, aunque las placas estén aproximadamente alineadas. Su efecto no se modelará automáticamente como ruido de media cero.

Una prueba doméstica con paredes sirve para ensayar el funcionamiento y estudiar fallos. No sustituye la validación exterior con altura y alimentación de uso.

### Ejecución inicial en PC

El usuario confirmó que la primera implementación debe calcular en PC. La selección del dispositivo final queda aplazada.

Se propone empezar con cálculo por lotes sobre capturas guardadas. Esto permite repetir estimaciones con diferentes modelos sobre exactamente los mismos datos.

La función estimadora recibirá observaciones, secuencia, espaciamiento previsto, referencias y parámetros del modelo. Devolverá geometría, incertidumbre, residuos y observabilidad.

La lectura de puertos, la base de datos y la presentación quedan fuera de esa función. Esta separación facilita su futura integración.

Una actualización en vivo también puede ejecutarse en PC. «En línea» describe cuándo se calcula; no exige que el algoritmo viva en un ESP32.

Para el tendido quieto, el cálculo por lotes aprovecha el conjunto de enlaces de cada ventana. Las ventanas deben separar movimientos, reinicios y cambios de configuración.

La versión en vivo se añadirá después para informar antigüedad, discrepancias y movimientos. No debe mezclar como simultáneos rangos tomados antes y después de mover una placa.

No se seleccionan ahora microcontrolador, navegador o servidor. Esa decisión dependerá del tiempo y la memoria medidos sobre el algoritmo validado.

La descripción del operario sustituye la franja fija como único modelo de colocación. Los intervalos siguientes siguen siendo válidos si se verifica su supuesto de franja.

## Magnitudes y referencia

Se define un eje propio del tendido de esclavos. El maestro se representa fuera de ese eje.

| Símbolo | Significado | Unidad |
|---|---|---|
| `s_i` | Coordenada longitudinal del esclavo i | m |
| `t_i` | Desviación lateral del esclavo i | m |
| `z_i` | Altura de la antena i en una referencia común | m |
| `w` | Semiancho permitido de la franja, `abs(t_i) <= w` | m |
| `r_ij` | Distancia entre antenas i y j | m |
| `e` | Semiancho del intervalo de error del rango | m |
| `h_max` | Límite de la diferencia absoluta de altura entre antenas | m |

El primer esclavo fija el origen longitudinal. La orientación y el signo lateral son convenciones. El orden físico debe registrarse; no se infiere del número del firmware.

La referencia lateral puede provenir de una cuerda o del replanteo. Si se define mediante extremos, sus errores también deben considerarse.

El rango satisface:

```text
r_ij² = (s_j - s_i)² + (t_j - t_i)² + (z_j - z_i)²
```

El ancho no determina por sí solo cuánto se dobla el tendido entre nodos. Debe anotarse si el desvío es alternado, gradual o local.

## Intervalos antes de elegir un estimador

Si el rango observado es `r_hat`, se supone `r ∈ [max(0,r_hat-e), r_hat+e]`.

Con `abs(t_i) <= w` y `abs(z_j-z_i) <= h_max`, la separación longitudinal absoluta queda contenida en:

```text
s_min = sqrt(max(0, max(0,r_hat-e)² - (2w)² - h_max²))
s_max = r_hat + e
```

El máximo usa diferencia lateral y vertical cero. Si se conocen diferencias de altura mínimas positivas, se puede estrechar ese límite.

El intervalo es geométricamente conservador bajo los supuestos anteriores. Su cobertura estadística depende de cómo se obtuvo `e`. No es automáticamente una garantía.

### Ejemplo: vecinos a 2 m

Con separación longitudinal de 2 m, igual altura y diferencia lateral de 0,4 m, el rango es 2,0396 m. El exceso es 3,96 cm.

Una franja de ±0,2 m permite esa diferencia entre dos nodos situados en lados opuestos. No debe confundirse el semiancho de la franja con la diferencia lateral de un par.

Si el rango observado fuera 2 m con error ±0,5 m, esa franja daría un intervalo longitudinal aproximado de 1,446–2,500 m.

El error del rango domina ese ejemplo. Un dibujo con nodos alineados y varios decimales ocultaría esa limitación.

## Qué se puede observar

Las distancias entre esclavos casi alineados cambian poco frente a desplazamientos laterales pequeños. La sensibilidad lateral se anula en la alineación perfecta.

El maestro fuera del eje aporta otra dirección de observación. Su utilidad depende de la posición, los errores de sus rangos y las referencias disponibles.

En una línea perfecta, un maestro y su reflejo al otro lado producen los mismos rangos. Se necesita una convención o una referencia para elegir el lado.

La solución debe distinguir tres resultados:

1. **Geometría FTM independiente:** usa rangos, orden y restricciones de colocación declaradas. Se compara con cintas reservadas.
2. **Geometría manual:** conserva la referencia que anotó el operario, con su incertidumbre.
3. **Geometría combinada:** reúne ambas modalidades y muestra qué observaciones influyeron en cada posición.

La tercera solución no valida la primera. Una cinta usada en el ajuste no puede servir también como prueba independiente de esa misma posición.

Para un futuro ajuste puntual, se propone una pérdida que limite la influencia de observaciones incompatibles. El informe debe conservar los residuos y exclusiones.

Las elipses de covarianza son condicionales al modelo. Deben acompañarse de sensibilidad al sesgo, al ancho de franja y a la falta de enlaces.

## Cómo aporta a MASW

Para una onda plana ideal, un error longitudinal proyectado `δx` produce:

```text
δφ = 2π δx / λ
δt_equivalente = δx / c_fase
```

Aquí `δφ` es el error de fase en radianes, `λ` la longitud de onda en metros y `c_fase` la velocidad de fase en m/s.

Con `δx = 0,5 m` y `λ = 5 m`, el error es 36°. Con `λ = 20 m`, es 9°.

Estas cifras describen sensibilidad de fase. No son límites de aceptación para la inversión ni errores porcentuales de velocidad de onda de corte.

Si todas las coordenadas se multiplican por `1+ε`, una onda ideal se interpreta con `c_estimado = (1+ε)c_real`. Una traslación común no cambia sus separaciones.

Los errores no uniformes requieren evaluar el procesamiento completo. No se puede trasladar directamente un error de rango al error final del perfil de velocidades.

La fuente sísmica debe registrarse por separado. El maestro de comunicaciones no representa el lugar del golpe.

Las alturas de antena y geófono también son diferentes. La referencia de cinta debe indicar si corresponde a antenas, geófonos, distancia inclinada o proyección horizontal.

## Criterio para la contribución de tesis

Se propone evaluar si la redundancia detecta errores de colocación que alterarían el procesamiento o justificarían revisar el tendido.

La comparación incluiría geometría nominal, manual y FTM. Se mantendrían iguales los registros sísmicos y los parámetros de procesamiento.

Si FTM solo detecta cambios grandes, ese resultado sigue siendo útil si se cuantifican falsas alarmas, cambios no detectados y condiciones de uso.

Las [fuentes S1 y S2](EVIDENCIA.md) justifican estudiar la geometría. La validación del sistema debe aportar el alcance cuantitativo específico.

IA principal: Codex, modelo no reportado.  
Delegados: GPT-5.6-sol, derivaciones y revisión de supuestos.  
Fallbacks: ninguno.
