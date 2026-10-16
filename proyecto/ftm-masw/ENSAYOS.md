# Campaña para medir tolerancia y utilidad del control

Estado: propuesta para acordar. No se ejecutaron estos ensayos en hardware.

## Resultado que debe producir la campaña

La campaña debe determinar bajo qué condiciones FTM detecta discrepancias útiles respecto de la cinta.

Se informarán el error de rango y de separación longitudinal, la cobertura de sus intervalos, las falsas alarmas y la probabilidad de detectar movimientos conocidos.

También se medirán disponibilidad por enlace, tiempo de revisita, demora de alarma y tiempo de recuperación después de un reinicio.

## Preparación

1. Identificar cada placa mediante MAC y reinicio observado. Registrar su canal sísmico y rol.
2. Elegir un punto físico reproducible para medir cada antena. Medir su separación respecto del geófono.
3. Registrar orden real, espaciamientos, altura, caja, orientación, alimentación y ubicación del maestro.
4. Tender una referencia recta y medir los desvíos laterales. Registrar diferencias de altura.
5. Registrar el lugar del golpe por separado.
6. Guardar revisión de firmware, configuración, estimador y perfil de calibración con sus hashes.

Los puertos COM y números históricos sirven como antecedentes. No identifican una placa conectada actualmente.

## Primera etapa: viabilidad con pocas condiciones

Esta etapa evita una campaña extensa antes de saber si el error es útil. Las separaciones finales dependen del tendido del usuario.

Antes de ajustar un modelo angular, se repetirán colocaciones mediante el procedimiento habitual del operario. Se medirán los tramos y direcciones resultantes.

Se registrará si el operario apunta al tramo anterior, a una referencia distante o a una cuerda. Esas condiciones producen acumulaciones distintas.

Las referencias para aprender ese modelo se separarán de las usadas para evaluar la mejora FTM. Se compararán estimaciones de colocación sola, FTM solo y combinación.

| Ensayo | Cambio controlado | Qué resuelve |
|---|---|---|
| P0. Alimentación | Fuente estable frente a alimentación portátil real | Reinicios y tiempo de estabilización. |
| P1. Línea de referencia | Tres esclavos alineados; maestro desplazado lateralmente | Error básico y funcionamiento de todos los pares. |
| P2. Separaciones | Separación mínima, habitual y máxima del uso previsto | Dependencia del sesgo con distancia. |
| P3. Franja | Desvíos locales y graduales de 0, 0,1 y 0,2 veces el espaciamiento | Sensibilidad lateral y error de proyección. |
| P4. Movimiento | Mover un esclavo longitudinal y lateralmente; medir el cambio | Tamaño detectable y demora de alarma. |
| P5. Reinicio | Reiniciar un esclavo sin moverlo | Evitar confundir cambio de estado con desplazamiento. |

Las fracciones de P3 son valores de ensayo, no tolerancias aprobadas. Los patrones deben indicar si el desvío afecta uno o ambos lados del eje.

Como exploración, registrar varias ventanas de 3–5 minutos por condición y una ventana quieta de 30–60 minutos para deriva. Esas duraciones no certifican cobertura.

Si la incertidumbre no permite detectar el desplazamiento de interés, se revisa la meta antes de ampliar la campaña.

## Segunda etapa: validación fuera del ajuste

Separar las condiciones en tres conjuntos:

- **Calibración:** selecciona y ajusta el modelo y sus offsets.
- **Desarrollo del umbral:** fija el intervalo y la lógica de alarma.
- **Validación:** evalúa el umbral congelado, en nuevas colocaciones y sesiones.

No repartir al azar frames del mismo montaje entre esos conjuntos. Las muestras compartirían sesgo, orientación y entorno.

Las unidades de validación deben representar la variabilidad de uso: nueva colocación, nueva inicialización y condiciones documentadas. Reiniciar sin cambiar el entorno no garantiza independencia.

Las variaciones a cubrir incluyen orientación, caja, altura de uso, terreno, obstáculos, personas, separación y tiempo encendido.

Si no se cubre alguna condición, el informe la excluye del alcance de la tolerancia.

## Cómo definir una tolerancia comprobable

Un percentil 95 del error absoluto describe la muestra. Para evaluar su cobertura futura, se necesita validación independiente.

Con un límite prefijado y cero excedencias en `n` ensayos binomiales independientes, el límite inferior unilateral de cobertura al 95 % es:

```text
p_inferior = 0,05 ** (1/n)
```

Para 59 ensayos, `p_inferior = 0,9505`. Para 95 % de confianza sobre cobertura del 99 %, se requieren 299 éxitos sin excedencias.

Es una deducción binomial; véase [fuente S8](EVIDENCIA.md). No implica ejecutar 59 ráfagas y declarar validado el sistema.

El número debe referirse a una unidad de ensayo explícita y a condiciones representativas. Un límite elegido después de mirar esos resultados exige otra validación.

Si existen excedencias, se calculan intervalos binomiales apropiados y se publican. No se descartan observaciones solo porque empeoran la cobertura.

La cobertura por enlace tampoco equivale a cobertura simultánea de todos los nodos. Para controlar el tendido completo, se valida una estadística de arreglo.

## Alarmas: tres estados

Se propone separar «compatible», «discrepancia» y «no concluyente».

| Estado | Condición propuesta |
|---|---|
| Compatible | Observaciones recientes dentro del alcance validado; la discrepancia cumple el criterio prefijado. |
| Discrepancia | Se supera el umbral validado durante la persistencia definida. |
| No concluyente | Datos vencidos, reinicio, falta de pares, mala geometría o condiciones fuera de validación. |

La persistencia debe ensayarse: puede reducir falsas alarmas, pero aumenta la demora de detección.

Un percentil 95 de error no implica detección del 95 % para un desplazamiento de ese tamaño. Se debe medir una curva de detección.

Por ejemplo, con ruido normal de desviación 0,1 m y umbral 0,2 m, un cambio efectivo de 0,2 m se detectaría aproximadamente la mitad de las veces.

Ese ejemplo es analítico. El error real puede tener asimetría, deriva y colas diferentes.

Para movimientos, se propaga la incertidumbre de ambas ventanas. Para comparación con cinta, se incluye la incertidumbre de la referencia.

Si se suman límites conservadores, no se deben contar dos veces la deriva o la geometría ya incluidas en el error validado.

## Datos que se conservarán

Los crudos deben conservar tiempos `t1`–`t4`, CSI, RSSI, estado y asociación inequívoca con nodo, enlace y sesión.

La bitácora debe registrar arranque, alimentación, firmware, intervenciones, instante del movimiento, cinta, altura, orientación y fotografías del montaje.

Cada resultado derivado debe señalar la captura, ventana, referencias, estimador y calibración utilizados.

Se comprobará la correspondencia entre frames y CSI por sus claves. La auditoría histórica encontró registros sin pareja; contar filas no prueba emparejamiento.

## Prueba del aporte MASW

1. Tomar un registro sísmico de referencia con geometría manual documentada.
2. Procesarlo con geometría nominal y manual, manteniendo iguales los demás parámetros.
3. Perturbar las coordenadas dentro de los intervalos FTM y repetir el procesamiento.
4. Comparar curvas de dispersión y decisiones de interpretación dentro de la banda útil.
5. Evaluar si las alarmas detectan los casos que justifican revisar la geometría.

El resultado puede ser un control de errores grandes. Para afirmar mejora del perfil de velocidades se necesitan registros sísmicos y validación adicional.

IA principal: Codex, modelo no reportado.  
Delegados: GPT-5.6-sol, criterio binomial y sensibilidad de detección.  
Fallbacks: ninguno.
