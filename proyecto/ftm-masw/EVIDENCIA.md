# Evidencia disponible y bibliografía comentada

Consulta y auditoría: 16 de octubre de 2026.

## Estado local comprobado

FTM-test está en la revisión `4c841a8d4305bc70c8660cc84980dd7cd358e5db`. El flujo Windows apunta a ESP-IDF 5.5.1 y ESP32-S3.

El código coordina seis pares, en doce sentidos, para un maestro y tres esclavos. La PC conserva el historial por USB del maestro.

| Evidencia del repositorio FTM-test | Resultado de la inspección |
|---|---|
| `bin/fts.ps1` | Compila maestro y `slave1`–`slave3`. Los perfiles adicionales no amplían automáticamente este flujo. |
| `main/poc_ranging.c`, `components/ftm/ftm_mesh.c` | Coordinación de turnos y mediciones entre pares. |
| `bin/mesh_adjust.py:104` y `:139` | Prior transversal `y=0`, maestro fijo en el origen y orientación vinculada al maestro. |
| `experiments/survey/masw_template.json` | Incluye al maestro dentro de `line.nodes`. Sus distancias son ejemplos, no referencias actuales. |
| `bin/mesh_csi.py` | Interpolación L1, transformada inversa y detección del primer cruce al 25 % del máximo. |
| Fuentes y configuraciones inspeccionadas | No se encontró una implementación de actualización OTA ni una tabla de particiones OTA propia. |

La inspección inicial encontró ausente `C:\Espressif`. Durante la preparación OTA del 16/10/2026 se instaló ESP-IDF 5.5.1 con Python 3.12 y herramientas ESP32-S3. Se verificó la activación y la configuración CMake del proyecto base. La flash y las particiones instaladas en las placas siguen sin inspeccionarse.

## Auditoría independiente de capturas históricas

Se abrieron las bases SQLite con `mode=ro`. Ambas pasaron `PRAGMA integrity_check`. Los hashes y el detalle están en [auditoria-historica.json](auditoria-historica.json).

| Captura del 09/10/2026, UTC | Sesiones | Estado FTM exitoso | Revisita mediana del mismo sentido | Registros de reinicio |
|---|---:|---:|---:|---|
| `21:59:51`–`22:44:18` | 948 | 946 | 32,45 s | Nodo 3: 6; nodo 4: 5 |
| `22:49:33`–`23:04:21` | 269 | 268 | 34,91 s | Nodo 2: 1; nodo 3: 2; nodo 4: 5 |

Los registros de reinicio son eventos encontrados en el log, no una prueba de su causa. La hipótesis de apagado de powerbanks requiere un ensayo de alimentación.

Se verificó el emparejamiento por `run, seq, src, dst, frame`. La primera captura tiene un CSI sin frame y un frame sin CSI. La segunda tiene un CSI sin frame. No se encontraron claves CSI duplicadas. Por eso la igualdad del número total de filas no demuestra emparejamiento completo.

La revisita es el intervalo entre observaciones exitosas sucesivas del mismo sentido. No mide exactamente la duración de un ciclo completo.

En la primera captura se reprodujo la comparación con cinco pares medidos con cinta. Se usó la mediana por sentido y el promedio de ambos sentidos.

Para cada par evaluado, se calculó un offset común con los otros cuatro pares. Así se obtuvieron los siguientes errores:

| Estimador | Error absoluto medio, offset por exclusión de un par | Máximo absoluto |
|---|---:|---:|
| RTT `corrected_ps`, sin CSI | 2,061 m | 4,008 m |
| Primer camino CSI | 0,770 m | 1,774 m |
| RTT menos exceso de camino CSI | 1,412 m | 2,930 m |

La primera fila no significa ausencia de calibración: el cálculo incluye el offset por exclusión. Sin ese offset, el error medio de las medianas fue 2,968 m.

La cinta del par 2–3 tenía confianza baja. Faltaba la cinta 1–4. La validación entre pares del mismo montaje no prueba transferencia a otro montaje.

No se publicó un error de distancia para la segunda captura. No se confirmó una referencia independiente aplicable a esa colocación.

## Fuentes primarias verificadas

### S1. Colinealidad en MASW

Diaz-Segura, E. G. (2020). [Influences of variations in the sledgehammer trajectory and collinearity of the geophone array in an MASW survey on the shear-wave velocity profile](https://link.springer.com/article/10.1186/s40703-020-00112-5).

Ensayó 24 geófonos separados 1,5 m y desvíos laterales del 7 %, 14 % y 21 % del espaciamiento. En sitios relativamente homogéneos, los perfiles variaron poco. La heterogeneidad lateral dificultó la interpretación. Es un antecedente para seleccionar ensayos, no una tolerancia universal ni una validación de FTM.

### S2. Diseño del tendido y muestreo espacial

Foti et al. (2018). [Guidelines for the good practice of surface wave analysis: a product of the InterPACIFIC project](https://link.springer.com/article/10.1007/s10518-017-0206-7).

Relaciona espaciamiento con la menor longitud de onda observable y longitud del arreglo con la investigación profunda. En un muestreo regular, longitudes de onda menores que dos espaciamientos sufren aliasing. No establece una tolerancia general para el error de coordenadas del sistema propuesto.

### S3. Evaluación experimental de FTM económico

Domínguez-Bolaño et al. (2024). [Fine Time Measurement for the Internet of Things: A Practical Approach Using ESP32](https://arxiv.org/html/2401.16517v1).

Estudia ESP32-S2 en interiores y exteriores. Documenta dependencia del entorno, calibración y ancho de banda. Los modelos entrenados pierden ventajas al cambiar de escenario. La aplicación principal es justificar validación en otro montaje. No se trasladan sus cifras a ESP32-S3 ni al tendido de geófonos.

### S4. Wi-PRO, alcance real de la mejora

Hunter, Ayyalasomayajula y Bharadia (2026). [Página del proyecto Wi-PRO](https://ucsdwcsng.github.io/wi-pro/).

Los autores publican errores medianos de rango de 1,51 m y 2,39 m en dos conjuntos interiores, sin promediado ni rechazo. El resultado orienta las expectativas hacia metros en esos escenarios. No respalda precisión centimétrica en nuestro sistema.

### S5. Algoritmo público Wi-PRO

[Código `wipro.rs`](https://raw.githubusercontent.com/ucsdwcsng/wi-pro-esp32-ftm/main/firmware/src/wipro.rs) y [repositorio](https://github.com/ucsdwcsng/wi-pro-esp32-ftm).

Se verificaron carga de CSI HT40, interpolación L1 y desplazamiento por RTT. El código local contiene esos pasos. Hay diferencias de implementación, incluido el cruce interpolado. No corresponde descartar el port local solamente porque usa una transformada inversa. Falta una comparación numérica contra una revisión fijada del código original.

### S6. Restricciones FTM del fabricante

Espressif. [FAQ de Wi-Fi, secciones FTM](https://raw.githubusercontent.com/espressif/esp-faq/master/docs/en/software-framework/wifi.rst).

El fabricante indica hasta 40 MHz para FTM en ESP32-S3. Una estación no ejecuta varias sesiones FTM simultáneas. FTM no requiere asociarse previamente al punto de acceso. Estas restricciones favorecen planificación por turnos; no obligan a reconectar la estación para cada par.

### S7. OTA en la versión del proyecto

Espressif, ESP-IDF `v5.5.1`: [ejemplo OTA nativo](https://raw.githubusercontent.com/espressif/esp-idf/v5.5.1/examples/system/ota/native_ota_example/main/native_ota_example.c), [API OTA](https://raw.githubusercontent.com/espressif/esp-idf/v5.5.1/components/app_update/include/esp_ota_ops.h) y [configuración del bootloader](https://raw.githubusercontent.com/espressif/esp-idf/v5.5.1/components/bootloader/Kconfig.projbuild).

Estas fuentes fijan la versión de referencia para escribir, validar y seleccionar una imagen. El ejemplo muestra confirmación de arranque y retorno a una imagen anterior. El transporte por el maestro todavía debe diseñarse y probarse.

### S8. Cobertura estadística

NIST. [Exact binomial confidence limits](https://itl.nist.gov/div898/software/dataplot/refman2/auxillar/exacbici.htm).

Proporciona el fundamento de intervalos binomiales exactos. Se aplica a ensayos independientes y a un criterio de éxito prefijado. No convierte frames consecutivos de un enlace en observaciones independientes.

## Correcciones de interpretación

- Las notas históricas atribuyen los problemas bajo 1 m a «campo cercano». Esa causa electromagnética no se demostró. Debe hablarse de errores a corta distancia.
- Para una apertura supuesta de 3 cm a 2,4 GHz, `2D²/λ` da aproximadamente 1,4 cm. Es una comprobación dimensional orientativa, no una caracterización de la antena real.
- `1/B = 25 ns` para 40 MHz describe una escala temporal convencional de resolución. No impone un error mínimo de 7,5 m a toda estimación de rango.
- Interpolar una respuesta o ajustar un modelo puede mejorar la estimación bajo ciertos supuestos. Esa mejora requiere validación con mediciones independientes.

IA principal: Codex, modelo no reportado.  
Delegados: GPT-5.6-sol, contraste formal; síntesis bibliográfica y auditoría por el principal.  
Fallbacks: ninguno.
