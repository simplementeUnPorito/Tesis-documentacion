# Auditoría de correctness, regresiones y validez numérica — 2026-09-02

## Alcance y criterio

Auditoría dirigida sobre los cinco repositorios prioritarios. Cada cambio
numérico partió de una reproducción automatizada con seed fija; no se alteró
ninguna topología analógica ni se aceptó una mejora visual como evidencia.
Los commits indicados son locales y no fueron enviados a ningún remoto.

## Bugs confirmados y corregidos

| Sev. | Archivo / función | Reproducción y causa raíz | Fix y prueba | Evidencia antes → después | Commit |
|---|---|---|---|---|---|
| P0 | `masw_analysis.py::two_receiver_dispersion` | Dos ruidos independientes daban coherencia mediana 1,0: el cociente de magnitudes de una sola FFT se cancela algebraicamente. | Welch/CSD segmentado; test sintético reproducible. | mediana 1,0 → 0,0077038; p95 0,0256409 | `2c93e19` |
| P0 | `masw_analysis.py::two_receiver_dispersion` | Para `cos(2πf(t-x/c))`, `angle(CSD(x1,x2))=-kΔx`; el signo positivo producía velocidades negativas y luego NaN. | Se usa `c=-2πfΔx/dphi`, sin `abs`; cuatro casos de frecuencia, velocidad, SNR y separación. | casos no ambiguos fallaban → pasan | `2c93e19` |
| P0 | `masw_analysis.py::phase_shift_image` | Onda multicanal a 300 m/s: la compensación negativa sobre fase FFT no conjugada elegía 240/500/455/125 m/s. | Compensación positiva; comparación con backend activo y ecuación de MASWavesPy. | 0/4 frecuencias correctas → 4/4 a 300 m/s | `2c93e19` |
| P0 | `masw_inversion.py::dispersion_misfit` | El mínimo `N//2` aceptaba sólo 1/3 y 2/5 raíces válidas. | Mínimo `ceil(N/2)`; tests N=3,5 y pares 4,6. | casos impares inválidos aceptados → rechazados | `d1475a5` |
| P1 | `masw_inversion.py::monte_carlo_inversion` | Tras 50 rechazos, `np.sort(beta_test)` ordenaba todo el perfil y destruía inversiones permitidas. | Se ordena sólo `beta_test[reversals:]`, como MASWavesPy; mocks fuerzan fallback con 0/1/2 inversiones. | inversiones pedidas eliminadas → preservadas | `d1475a5` |
| P1 | `masw_inversion.py::monte_carlo_inversion` | El retorno `False` del callback inicial era ignorado y ejecutaba una propuesta. | Retorno inmediato antes del muestreo; cancelación antes, durante y final cubierta. | 1 iteración indebida → 0 | `d1475a5` |
| P2 | `master/ws_cmd_test.py` | El diagnóstico reconstruía `(b1<<8)|b0`, aunque el ACK define `b1=low8` y `b0=reservado`; mostraba 22528 para echo 88. | Decodificación inequívoca de low8 y test de contrato. | 22528 → 88 | `247cb0c` |
| P2 docs | `PCBs/JitX/README.md` | Conteos 46/37, Micro-USB y 175x125 divergían de `spec.py/validate.py`. | Se eliminaron conteos manuales y se remitió al validador/fuentes derivadas. | README histórico → contrato derivable (53/41 actualmente) | `9e6e4ec` |

## Tests automáticos agregados o endurecidos

- `src/calculos_modelados/python/tests/test_masw_analysis.py`: coherencia,
  signo, SNR/separación, alias de fase y cresta multicanal contra referencia.
- `src/interfaces/python/geophone_scope/test_masw_inversion_correctness.py`:
  umbral de raíces, reversals y cancelación del callback.
- `src/firmware/esp32/Nodo comunicación/master/ack_contract_test.py`:
  contrato de ACK low8.
- `masw_bench/test_sintetico.py`: banda válida 12–20 Hz y aserción cuantitativa
  para una onda de 90 m/s con `dx=2 m`.

## Clasificación

| Hallazgo | Clasificación | Resultado |
|---|---|---|
| Coherencia de una FFT | CONFIRMED BUG | corregido |
| Signo de fase de dos receptores | CONFIRMED BUG | corregido analíticamente |
| Signo discrepante de phase-shift | CONFIRMED BUG | unificado con backend validado |
| Umbral impar de raíces | CONFIRMED BUG | corregido |
| Fallback global de reversals | CONFIRMED BUG | corregido |
| Callback inicial ignorado | CONFIRMED BUG | corregido |
| ACK refleja sólo low8 | NOT A BUG | contrato deliberado, documentado |
| Diagnóstico ACK como uint16 | CONFIRMED BUG | corregido |
| `masw_analysis.py` standalone | LEGACY | retenido porque sigue ejecutable/documentado; ahora validado |
| Benchmark 90 m/s en 20–35 Hz, dx=2 m | LEGACY | test inválido: excedía Nyquist espacial; corregido el benchmark, no el algoritmo |
| Ambigüedad módulo 2π con dos receptores | NEEDS SCIENTIFIC DECISION | limitación fundamental documentada |
| AMS1117/VREF_2V048/divisor/IDAC | NEEDS HARDWARE | matriz creada; arquitectura intacta |
| Error alto PWS/HRLRT en diagnóstico dispersivo | NEEDS SCIENTIFIC DECISION | no se cambió sin especificación/ground truth acordado |
| F1 SD larga | NOT A BUG | regresión permanece cerrada, 16/16 |
| F5 WebSocket half-open | NOT A BUG | watchdog pre-DATA y liveness pasan |
| F9 START/HOT_WAIT/ARMED | NOT A BUG | 4/4; retry no reenvía PRESTART |

## Evidencia de regresión y compilación

- Cálculos: 4 tests MASW nuevos, 16 tests históricos invocados, ocho
  transformadas sobre caso no dispersivo y diagnósticos extra pasan.
- Interfaces: discovery completo, 28 tests pasan.
- JitX: `python -m JitX.tesis_carrier.validate` pasa con 53 partes, 41 redes
  activas, 161 endpoints, 25 señales PSoC bloqueadas y 100 pines nombrados.
- ESP32: PlatformIO `master/esp32dev`, `slave/slave2` y `slave/slaveTest`
  compilan correctamente. F1, F5 y F9 pasan.
- PSoC Creator: proyecto de campo y autotest enlazan y generan HEX. Campo:
  flash 23,1%, SRAM 79,2%; autotest: flash 25,7%, SRAM 26,5%. Persisten
  warnings de P15[1], timing CyBUS_CLK y mensajes M0072 de ítems duplicados
  durante generación de API; no impiden `Rebuild Succeeded` y no se alteraron
  por no existir una reproducción funcional del daño.

## Hallazgos no corregidos: requieren decisión del investigador

1. Elegir límites físicos/prior de velocidad para resolver o rechazar bins
   donde `f·|Δx|/c >= 1/2`. Dos receptores no permiten desenvolver fase de
   forma única: por ejemplo 400 y 80 m/s son indistinguibles para 50 Hz y 2 m.
2. Resolver la arquitectura de referencia analógica. La matriz completa está
   en `docs/proyecto/HARDWARE_REFERENCE_ASSUMPTIONS_2026-09-02.md`. Los valores actuales
   R22=1 kΩ, R23=620 Ω e IADJ=60 µA modelan 2,0622 V, aunque nombres y
   serigrafía dicen 2,048 V. No se eligió entre AMS1117 y referencia 2,5 V +
   IDAC.
3. Definir un dataset dispersivo y tolerancias de aceptación para PWS/HRLRT.
   El diagnóstico actual muestra errores máximos aproximados de 30,2 y
   177,1 m/s; esto no basta para atribuir un bug ni autoriza cambiar algoritmos.
4. Decidir si los warnings de timing de PSoC requieren cierre formal con
   restricciones/medición. Ambos firmwares compilan; no hay evidencia de una
   falla funcional nueva asociada.

## Estado del árbol y trazabilidad

No se incluyeron en commits el archivo personal PSoC `.cywrk.elias`, los
artefactos regenerados por PSoC Creator ni un `.pyc` regenerado por Python.
La memoria operativa y los comandos reproducibles están en
`docs/auditorias/AUDIT_SESSION_MEMORY.md`; la matriz analógica está separada para impedir que
una decisión de topología se mezcle con fixes de software.
