# FTM para controlar la geometría de un tendido MASW

Fecha: 16 de octubre de 2026. Estado: propuesta para discutir, sin implementación OTA ni nuevas pruebas de hardware.

**Se propone usar FTM como control de la medición manual del tendido.** La prioridad es la separación relativa entre esclavos. El maestro queda fuera del eje.

## Qué leer

| Documento | Pregunta que responde |
|---|---|
| [Evidencia y fuentes](EVIDENCIA.md) | ¿Qué está comprobado y qué procede de otros montajes? |
| [Modelo geométrico](MODELO.md) | ¿Cómo representar una línea imperfecta sin inventar precisión? |
| [Campaña de validación](ENSAYOS.md) | ¿Cómo obtener una tolerancia y evaluar alarmas? |
| [Preparación OTA](OTA.md) | ¿Cómo llegar a actualizar los esclavos desde el maestro por USB? |
| [Datos pendientes de campaña](plan-campana.json) | ¿Qué falta acordar antes de medir? |

## Recomendación de partida

1. Registrar el orden físico de los esclavos, la cinta y la posición de la fuente sísmica.
2. Representar la colocación como una cadena de tramos medidos desde el esclavo anterior, con incertidumbre de longitud y dirección.
3. Mantener al maestro libre respecto de ese eje.
4. Conservar rangos entre esclavos y entre maestro y esclavos, en ambos sentidos.
5. Separar la comparación independiente FTM/cinta de la solución combinada.
6. Informar incertidumbre validada, antigüedad y estado de cada enlace.

La franja alrededor de un eje queda como restricción adicional cuando exista una referencia de alineación. La longitud medida por tramo no garantiza esa franja.

La aclaración del operario del 16/10/2026 está incorporada en el [modelo de colocación encadenada](MODELO.md#colocación-encadenada-descrita-por-el-operario). Los tramos candidatos son 1 m y 2 m; la longitud total sigue sin confirmarse.

También se confirmó la intención de usar un espaciamiento común, conocer la secuencia y alinear visualmente con mayor peso en los nodos cercanos. El cálculo inicial se hará en PC, primero sobre capturas guardadas. La plataforma final queda aplazada.

## Hallazgos que cambian el planteo

- La plantilla vigente incluye al maestro en la línea. El ajuste también vincula la línea al origen del maestro. Debe cambiarse antes de usarlo en este montaje.
- La auditoría de dos capturas históricas confirmó reinicios y revisitas por enlace de aproximadamente 32–35 s. Los rangos no son simultáneos.
- Se reprodujeron los errores publicados de la primera captura. Esos resultados incluyen un offset ajustado dejando un par de cinta afuera.
- Un rango estable puede mantener un sesgo. La covarianza del ajuste y el número de frames no demuestran una tolerancia de campo.
- Las desviaciones laterales producen cambios pequeños en el rango entre vecinos. Deben acotarse durante la instalación si FTM no puede observarlas.

## Decisiones abiertas para conversar

| Decisión | Por qué hace falta |
|---|---|
| Espaciamiento, número de esclavos y longitud del tendido | Determinan alcance, redundancia y tiempo entre revisitas. |
| Desplazamiento mínimo que interesa detectar | Permite evaluar si la incertidumbre de FTM es útil. |
| Semiancho lateral y diferencias de altura admisibles | Acotan la conversión de rango a separación longitudinal. |
| Altura, caja y orientación de antena | Definen las condiciones que debe cubrir la validación. |
| Orden físico de los nodos y punto de golpe | Evitan ambigüedades al asociar la geometría con los canales sísmicos. |
| Comparación antes/después o control contra cinta | Requieren umbrales y referencias distintos. |

Como hipótesis inicial, conviene evaluar alarmas de errores grandes y movimientos longitudinales. Los desplazamientos laterales necesitan una prueba específica.

## Reproducción y ubicación de archivos

Desde `C:\Github\Tesis`:

```powershell
python scripts/test_ftm_masw_geometry.py
python scripts/ftm_masw_geometry.py
```

Los ejemplos analíticos y la figura se generan en `outputs/ftm_masw/`. No son resultados de precisión medida.

La evidencia histórica resumida está en [auditoria-historica.json](auditoria-historica.json). Las bases originales permanecen en `C:\Github\FTM-test\data`.

El submódulo vive en `src/firmware/ftm-test`. `C:\Github\FTM-test` y el submódulo son dos checkouts independientes del mismo repositorio. Sus cambios sin commit no se propagan entre ellos. Antes de programar habrá que elegir un checkout de trabajo y registrar la revisión integrada.

La investigación quedó en el repositorio documental existente. No se trasladaron ni se sobrescribieron capturas, calibraciones o firmware históricos.

IA principal: Codex, modelo no reportado.  
Delegados: GPT-5.6-sol, análisis formal y generador numérico.  
Fallbacks: ninguno.
