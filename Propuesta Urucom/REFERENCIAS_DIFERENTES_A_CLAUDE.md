# Referencias adicionales encontradas — comparación con la búsqueda de Claude

**Paper objetivo:** *Automatic DC-Offset Calibration for a Low-Cost Geophone Front End*  
**Fecha de revisión:** 2026-07-15  
**Objetivo:** identificar referencias distintas de las cinco propuestas por Claude y decidir cuáles realmente fortalecen el estado del arte sin inflar artificialmente la bibliografía.

---

## 1. Referencias que ya había propuesto Claude

Claude propuso:

1. C. C. Enz and G. C. Temes, “Circuit techniques for reducing the effects of op-amp imperfections: autozeroing, correlated double sampling, and chopper stabilization,” *Proceedings of the IEEE*, 1996.
2. B. Murmann, “Digitally assisted analog circuits,” *IEEE Micro*, 2006.
3. Y. Liu et al., “A low-noise chopper amplifier with offset and low-frequency noise compensation DC servo loop,” *Electronics*, 2020.
4. J. L. Soler-Llorens et al., “Development and programming of Geophonino: A low cost Arduino-based seismic recorder for vertical geophones,” *Computers & Geosciences*, 2016.
5. K. Sonoda et al., “Wearable photoplethysmographic sensor system with PSoC microcontroller,” *ICETET*, 2012.

Estas referencias cubren bien:

- la taxonomía clásica de autozero, CDS y chopping;
- el paradigma de circuitos analógicos asistidos digitalmente;
- los lazos DC-servo continuos;
- sistemas geofónicos económicos;
- el uso general de PSoC en instrumentación.

---

# 2. Referencias diferentes encontradas en la búsqueda independiente

## A1 — Mohan et al., ISCAS 2020

### Referencia IEEE

C. Mohan, L. A. Camuñas-Mesa, E. Vianello, C. Reita, J. M. de la Rosa, T. Serrano-Gotarredona, and B. Linares-Barranco, “Experimental body-input three-stage DC offset calibration scheme for memristive crossbar,” in *Proc. IEEE International Symposium on Circuits and Systems (ISCAS)*, 2020, doi: **10.1109/ISCAS45731.2020.9180811**.

### Qué hace

El trabajo calibra físicamente el offset DC de los amplificadores asociados a las filas de una matriz memristiva. La corrección se realiza modificando el voltaje de cuerpo de un transistor del par diferencial. Emplea una palabra digital y tres niveles de resolución:

- grueso;
- fino;
- superfino.

La calibración actúa sobre el circuito analógico físico y no consiste únicamente en restar una media en el dominio digital.

### Por qué es relevante para tu paper

Es un antecedente más cercano que Murmann para justificar que:

- una lógica digital puede gobernar un elemento analógico de trim;
- la calibración puede modificar físicamente el punto de operación de un amplificador;
- la precisión final puede estar limitada por granularidad, mismatch y ruido;
- una corrección escalonada puede superar la resolución de un único elemento de trim.

### Diferencia con tu método

No calibra una cadena `PGA → BP → ADDER → LP`.

Sus “tres etapas” son tres **resoluciones de trim** aplicadas al mismo amplificador, no tres o cuatro nodos sucesivos de una cadena de acondicionamiento. Tampoco:

- usa un geófono;
- reutiliza el ADC de adquisición;
- reutiliza un filtro digital de adquisición;
- calibra secuencialmente nodos intermedios;
- congela cuatro VDAC independientes por configuración de ganancia.

### Prioridad

**ALTA — incluir.**

Es probablemente la referencia adicional más valiosa encontrada porque obliga a formular la novedad con precisión:

> La novedad no es simplemente ajustar físicamente un offset mediante control digital; eso ya tiene antecedentes. La novedad defendible es aplicar una calibración *foreground*, secuencial y por nodo a una cadena analógica completa, reutilizando los recursos de adquisición del PSoC.

### Lugar sugerido

Introducción, inmediatamente después de Murmann o en el párrafo que compara PSoC-Stat y AN68403.

### Redacción sugerida

```latex
Digitally controlled physical offset trimming has also been demonstrated
at the amplifier level, for example through multiresolution body-bias
calibration in memristive-array readout circuits \cite{Mohan2020}.
Unlike such single-amplifier trimming, the method proposed here observes
and corrects multiple intermediate nodes of a cascaded sensor front end.
```

---

## A2 — Wijayaraja et al., IEEE Access 2024

### Referencia IEEE

J. L. Wijayaraja, J. L. Wijekoon, M. Wijesundara, and L. J. M. Wickramasinghe, “Towards long range detection of elephants using seismic signals: A geophone-sensor interface for embedded systems,” *IEEE Access*, 2024, doi: **10.1109/ACCESS.2024.3401855**.

### Qué hace

Presenta una interfaz geofónica embebida compuesta por una cadena en cascada:

1. amplificador de instrumentación;
2. filtro Butterworth;
3. amplificador de señal;
4. ADC de un microcontrolador.

El trabajo discute señales geofónicas de microvoltios, selección de ganancia, filtrado y adaptación al rango del ADC.

### Por qué es relevante para tu paper

Fortalece de forma directa el contexto de aplicación:

- los geófonos requieren acondicionamiento analógico antes del ADC;
- las cadenas con amplificación y filtrado en cascada son habituales;
- la ganancia y el rango del ADC son cuestiones centrales en interfaces embebidas;
- existe interés reciente en front ends geofónicos económicos e integrados.

Es más cercano a tu aplicación que Sonoda 2012, que trata fotopletismografía.

### Diferencia con tu método

El sistema de Wijayaraja et al. utiliza amplificadores y filtros convencionales y no implementa:

- autocalibración de offset;
- observación individual de etapas;
- corrección por DAC;
- almacenamiento de códigos por ganancia;
- reutilización de un ADC y filtro compartidos;
- calibración *foreground*.

### Prioridad

**ALTA para el contexto geofónico; recomendable como reemplazo de Sonoda 2012.**

Si el espacio es limitado, esta referencia aporta más que Sonoda porque se relaciona directamente con una cadena analógica para geófonos.

### Lugar sugerido

Primer párrafo de la Introducción, junto con Kafadar y Geophonino, o en el párrafo donde se describe la necesidad de amplificar señales geofónicas débiles antes del ADC.

### Redacción sugerida

```latex
Recent embedded geophone interfaces likewise employ cascaded
instrumentation-amplifier, filtering, and gain stages to raise
microvolt-level seismic signals to the input range of a microcontroller
ADC \cite{Wijayaraja2024}; however, these systems do not address
automatic per-stage offset recovery.
```

---

## A3 — Kirchhoff et al., Review of Scientific Instruments 2018

### Referencia IEEE

R. Kirchhoff et al., “Huddle test measurement of a near Johnson noise limited geophone,” *Review of Scientific Instruments*, 2018, doi: **10.1063/1.5000592**.

### Qué hace

Caracteriza configuraciones de geófonos con amplificadores de muy bajo ruido. Utiliza amplificadores OPA188 y demuestra una configuración cercana al límite de ruido Johnson en la banda de interés.

### Por qué es relevante para tu paper

Sirve para establecer la alternativa de diseño de mayor precisión:

- elegir amplificadores externos dedicados, de bajo ruido y bajo offset;
- caracterizar rigurosamente el ruido del sensor y del preamplificador;
- mejorar el front end mediante componentes analógicos específicos.

Esto ayuda a formular correctamente el compromiso de tu arquitectura:

> tu sistema no pretende superar un preamplificador externo de precisión en ruido; pretende recuperar headroom usando recursos integrados y económicos.

También puede respaldar la limitación ya declarada de que la calibración de offset no corrige ruido ni distorsión.

### Diferencia con tu método

Kirchhoff et al. optimizan el front end por selección de componentes y caracterización de ruido. No realizan calibración automática ni corrección por etapas.

### Prioridad

**MEDIA — útil para Discussion, pero no imprescindible para la versión de cinco páginas.**

Inclúyela solamente si querés comparar explícitamente la filosofía de “componentes externos de precisión” frente a “observabilidad y asistencia digital”.

### Lugar sugerido

Discusión, después de:

> “The method trades component precision for system-level observability and digital assistance.”

### Redacción sugerida

```latex
This tradeoff differs from precision geophone front ends built around
dedicated low-noise amplifiers and characterized near the sensor's
Johnson-noise limit \cite{Kirchhoff2018}; the present work instead
targets integrated, low-cost recovery of analog headroom.
```

---

## A4 — Othman et al., Wireless Networks 2020

### Referencia IEEE

A. Othman, W. Mesbah, N. Iqbal, S. Al-Dharrab, A. Muqaibel, and G. L. Stüber, “Sum-rate maximization and data delivery for wireless seismic acquisition,” *Wireless Networks*, 2020, doi: **10.1007/s11276-020-02427-8**.

### Qué hace

Estudia la transmisión de grandes volúmenes de datos desde geófonos hacia gateways en sistemas sísmicos inalámbricos.

### Por qué podría ser relevante

Puede respaldar la motivación general de nodos sísmicos inalámbricos y la complejidad de sustituir sistemas cableados.

### Diferencia con tu método

No trata:

- front ends analógicos;
- offset;
- calibración;
- PSoC;
- instrumentación de bajo costo.

### Prioridad

**BAJA — no incluir en este paper.**

Es válida para el proyecto IoT completo, pero consume espacio bibliográfico sin fortalecer la contribución específica de autocalibración.

---

# 3. Candidatas encontradas, pero no recomendadas todavía

Las siguientes aparecen como antecedentes dentro de la literatura de calibración física de offset, pero no se recomienda insertarlas hasta verificar de forma independiente todos los metadatos y leer el texto completo:

## B1 — Nagy, Arbet y Stopjakova, DDECS 2013

G. Nagy, D. Arbet, and V. Stopjakova, “Digital methods of offset compensation in 90 nm CMOS operational amplifiers,” in *Proc. 16th IEEE International Symposium on Design and Diagnostics of Electronic Circuits & Systems (DDECS)*, pp. 124–127, 2013.

### Valor potencial

- corrección digital del offset de amplificadores operacionales;
- antecedente directo de trim digital de amplificador;
- puede ser más específico que Murmann.

### Estado

**PENDIENTE DE VERIFICACIÓN COMPLETA DEL DOI Y DEL MÉTODO.**

No citar todavía basándose únicamente en la referencia secundaria.

---

## B2 — Gins, Peralías y Rueda, IEEE TVLSI 2015

A. J. Gins, E. Peralías, and A. Rueda, “Background digital calibration of comparator offsets in pipeline ADCs,” *IEEE Transactions on Very Large Scale Integration (VLSI) Systems*, vol. 23, no. 7, pp. 1345–1349, Jul. 2015.

### Valor potencial

Demuestra calibración digital de offset dentro de una cadena de conversión.

### Limitación

El problema es el offset de comparadores de un pipeline ADC, no el punto de operación de etapas analógicas de un front end de sensor.

### Estado

**NO RECOMENDADA para la versión actual**, salvo que se agregue una discusión más amplia sobre calibración de convertidores. AN68403 y PSoC-Stat ya cubren mejor la comparación end-to-end para tu implementación.

---

## B3 — Mohan et al., Microelectronic Engineering 2018

C. Mohan et al., “Calibration of offset via bulk for low-power HfO2-based 1T1R memristive crossbar read-out system,” *Microelectronic Engineering*, vol. 198, pp. 35–47, 2018.

### Valor potencial

Es el antecedente de revista de la calibración física mediante body bias que posteriormente fue validada experimentalmente en ISCAS.

### Estado

**INTERESANTE, pero no añadir junto con Mohan 2020 sin necesidad.**

Ambas referencias cubren la misma familia de técnica. Para un paper de cinco páginas, Mohan 2020 basta como comparación compacta, salvo que el artículo de 2018 contenga una formulación teórica necesaria.

---

# 4. Comparación directa: Claude frente a la búsqueda independiente

| Necesidad del paper | Referencia de Claude | Referencia adicional encontrada | Qué conviene |
|---|---|---|---|
| Fundar “digitally assisted analog” | Murmann 2006 | Mohan 2020 | Usar ambas: Murmann funda el paradigma; Mohan aporta un ejemplo físico concreto |
| Clasificar autozero/chopper | Enz & Temes 1996 | — | Mantener Enz & Temes |
| Comparar con DC-servo continuo | Liu 2020 | — | Mantener Liu, pero redactar cuidadosamente el tradeoff |
| Contexto de geófono económico | Soler-Llorens 2016 | Wijayaraja 2024 | Wijayaraja es más reciente y más cercano a una cadena AFE en cascada |
| Uso de PSoC en instrumentación | Sonoda 2012 | — | Sonoda es opcional y prescindible |
| Alternativa con amplificadores de precisión | — | Kirchhoff 2018 | Útil en Discussion si hay espacio |
| Calibración física de offset controlada digitalmente | — | Mohan 2020 | Hueco importante en la lista de Claude |
| Contexto de adquisición sísmica inalámbrica | — | Othman 2020 | No incluir: demasiado periférico |

---

# 5. Recomendación final

## Incluir con prioridad

### 1. Murmann 2006 — ya encontrado por Claude

Fundamento del paradigma general.

### 2. Enz & Temes 1996 — ya encontrado por Claude

Clasificación canónica de técnicas clásicas de reducción de offset y ruido de baja frecuencia.

### 3. Mohan et al. 2020 — nuevo respecto de Claude

Antecedente concreto de calibración física de offset bajo control digital. Es la referencia adicional más importante.

### 4. Wijayaraja et al. 2024 — nuevo respecto de Claude

Contexto moderno y directamente geofónico de una cadena analógica embebida en cascada.

## Incluir solamente si hay espacio

### 5. Liu et al. 2020 — encontrado por Claude

Útil para el contraste con servo continuo, pero hay que evitar afirmar que reproduce exactamente el servo probado por los autores.

### 6. Kirchhoff et al. 2018 — nuevo respecto de Claude

Útil para contrastar una solución basada en componentes externos de precisión y para contextualizar la limitación de ruido.

## Omitir en esta versión

- Sonoda et al. 2012: demasiado indirecta.
- Othman et al. 2020: trata comunicaciones, no el AFE.
- Gins et al. 2015: calibración interna de pipeline ADC, demasiado distante.
- Mohan et al. 2018: probablemente redundante si ya se usa Mohan 2020.
- Nagy et al. 2013: no incluir hasta verificar completamente el documento.

---

# 6. Conclusión sobre la novedad después de estas referencias

La búsqueda independiente modifica ligeramente la formulación más fuerte del reporte de Claude.

No conviene afirmar:

> “Nadie ha realizado calibración física de offset controlada digitalmente.”

Eso sería demasiado amplio porque Mohan et al. demuestran calibración física digitalmente gobernada de amplificadores.

La afirmación defendible es más específica:

> No se encontró un trabajo anterior que aplique una calibración *foreground*, secuencial y por nodo a las etapas intermedias de un front end geofónico en cascada, reutilizando el ADC y los recursos digitales de adquisición y congelando correcciones analógicas independientes antes de medir.

Esa formulación preserva la novedad real sin ignorar antecedentes cercanos de trim físico de offset.

---

# 7. Subconjunto mínimo recomendado para el límite de cinco páginas

Si solo entran tres nuevas referencias:

1. **Murmann 2006**
2. **Enz & Temes 1996**
3. **Mohan et al. 2020**

Si entran cuatro:

4. **Wijayaraja et al. 2024**

Si entra una quinta y la Discussion necesita el contraste:

5. **Kirchhoff et al. 2018**

Este conjunto ofrece mejor cobertura conceptual y técnica que aumentar el número de citas con antecedentes periféricos.
