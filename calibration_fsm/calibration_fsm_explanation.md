# Maquina de estados de calibracion PSoC GEO

Archivos generados:

- `calibration_fsm_detailed.png`: maquina de estados completa del firmware.
- `calibration_fsm_simplified.png`: vista funcional simplificada.
- `calibration_fsm_diagrams.pdf`: los dos diagramas en un solo PDF.

## Lectura rapida

La calibracion tiene tres fases grandes:

1. **Busqueda por biseccion**: para cada etapa GEO (`GEO_PGA`, `GEO_BP`, `GEO_ADDER`, `GEO_LP`) mide un DAC inicial, hace un probe para saber el sentido de la pendiente, y luego usa biseccion para encontrar el mejor codigo DAC.
2. **Verify**: vuelve a medir el `final_dac` elegido por cada etapa. Aca se decide si el resultado formalmente cumple `TOL`.
3. **Realcheck**: mide con la entrada real del geofono y puede hacer nudges finos de `+/-1 LSB` si esta habilitado para esa etapa.

Al final restaura el camino normal de captura y manda `CAL_DONE`.

## Estados internos

`CAL_ASYNC_STAGE_BEGIN` prepara la etapa actual: selecciona `AMux_ADC`, arranca ADC y mide `dac_center`.

`CAL_ASYNC_MEASURE` es un estado comun. No decide nada por si solo: escribe DAC, descarta muestras de asentamiento, promedia y vuelve al estado evaluador que lo llamo.

`CAL_ASYNC_EVAL_INIT` mira la medicion del centro. Si ya esta dentro de `TOL`, termina la etapa. Si no, manda a medir el probe.

`CAL_ASYNC_EVAL_PROBE` compara centro contra probe para deducir si subir DAC sube o baja la medicion. Con eso inicializa el rango `[lo, hi]`.

`CAL_ASYNC_PLAN_ITER` decide el siguiente DAC de biseccion. Corta si llega a `DEADBAND`, si se queda sin rango, o si llega a `MAX_ITER`.

`CAL_ASYNC_EVAL_ITER` registra el punto medido, actualiza el mejor candidato, y vuelve a `PLAN_ITER` si todavia no llego a `TOL`.

`CAL_ASYNC_VERIFY_BEGIN` y `CAL_ASYNC_EVAL_VERIFY` releen cada etapa usando su `final_dac`. El resultado formal de verify es `!saturado && error <= TOL`.

`CAL_ASYNC_REALCHECK_SWITCH` cambia hacia la fase de entrada real.

`CAL_ASYNC_REALCHECK_BEGIN` inicia realcheck de cada etapa. Si `CAL_REALCHECK_ENABLE_*` es 0, salta esa etapa.

`CAL_ASYNC_EVAL_REALCHECK` decide si el punto real ya esta OK, si conviene hacer un nudge, o si el nudge empeoro/saturo y hay que terminar.

`CAL_ASYNC_DONE` queda cuando se restaura el camino de captura y `busy=0`.

## TOL vs DEADBAND

`TOL` es el criterio formal de exito: si `abs(medido - target) <= TOL`, ese punto puede considerarse OK.

`DEADBAND` es un criterio de control: si el error actual ya entro en esa zona, deja de mover el DAC para no perseguir ruido o alternar entre codigos vecinos.

Si `DEADBAND == TOL`, el corte de movimiento coincide con el criterio formal.

Si `DEADBAND > TOL`, la biseccion puede terminar antes, pero luego `verify` podria marcar esa etapa como no OK.

Si `DEADBAND < TOL`, va a perseguir mas fino que el criterio formal, normalmente mas lento y mas sensible al ruido.

## Donde mirar en codigo

- `calibration.c`: enum `PsocCalAsyncState` y `psoc_calibration_service_async()`.
- `calibration_tables_geo_*.h`: parametros por etapa.
- `calibration.h`: structs y factor global `CAL_SETTLE_FACTOR`.
