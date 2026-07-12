# HANDOFF — Sesión 2026-07-11/12 (auditoría pre-campo + SD PSoC + encadenado)

> **Para la próxima sesión (Claude/codex): leer esto PRIMERO.** Complementa
> `docs/plan_pruebas_precampo.md` (matriz de pruebas y hallazgos, la referencia fina) y
> `docs/plan_2929_decimation_sd.md` (historia de decimación/SD). Rama: `codex/capture-engine-verilog`.

## 1. Qué es el sistema hoy (foto completa)

- **PSoC5LP** (GEO, `src/psoc/AcondicionamientoAnalogico.cydsn`): ADC 2604 Hz nativo (4 configs
  de rango, assert de compilación), decimación con promedio en ISR (0xBB, 1..100, Fs=2604/N),
  captura RAM 512 lotes con **encadenado** (>512 crudos re-arma superMaquina sin resetear, un solo
  DUMP_DONE al final), **SD FatFs** (SPI Master del TopDesign, GEOLAST.BIN, hasta 60000 lotes ≈
  11.5 min a 2604 Hz), comandos SD UART: 0xBC status / 0xBD selftest / 0xBE captura-a-SD /
  0xBF leer lote. Build actual: Flash 64700 B, SRAM 79.3 %, filas 0..252, flasheado y validado.
- **ESP32 esclavo** (COM12, `slave/`, env slave1 NODE_ID=1): UART al PSoC, ESP-NOW al maestro,
  arena RAM paginada (512 lotes), jerarquía **ESP RAM → encadenado PSoC → SD PSoC**.
  Comandos de banco USB (SLAVE_LAB_TOOLS): probe/status/cap/decim/stream/sdcap/sdinfo/sdtest/
  **sdread N** (lee lote N de la SD por 0xBF e imprime por USB — mismo camino que REQ_BATCH).
- **ESP32 maestro** (COM8, AP GeoNetwork/192.168.4.1): relay stop-and-wait REQ_BATCH con
  `dumpBatchesForNode()` (N efectivo por HOTWAIT_ACK), pausa/reanuda dump según cliente WS,
  duración por tipo (0xAD HAMMER, clamp RAM), web LittleFS.
- **Web**: N (decimación) global, Duración GEOs/HAMMER, **Máx RAM (512)** y **Máx SD (60000)**,
  panel esclavo con SD auto-oculta y decimación como indicador.

## 2. Validado en hardware ESTA sesión (todo por radio/WS salvo E9)

E1 RAM 4 lotes ✅ · E2 SD 600 ✅ · E3 SD 3000 ✅ · E6 decim-2 radio 3000/3000 ✅ ·
E6b FIR radio 3000/3000 ✅ · E7 0xBE ✅ · E8 0xAD ✅ · E9 USB 9/9 ✅ · E10 UI Chrome ✅ ·
**E5b: captura de 10 min PERFECTA (52080 lotes a SD, F1 fix validado) + dump 93.2 % impecable**
(el corte fue del cliente Python, F5, ya corregido). **E5c (aceptación final) quedó EN CURSO
al cierre** — ver §5.

## 3. Bugs encontrados y su estado (detalle en plan_pruebas_precampo.md)

| ID | Qué | Estado |
|----|-----|--------|
| F1 | Watchdog SYNC_STALL re-disparaba START_NOW y destruía sesiones SD largas (causa raíz del "10 min = 0 muestras") | ✅ CORREGIDO (esclavo `a85565c1`) y validado en E5b |
| F5 | Tool WS sin watchdog de silencio → colgado en socket half-open | ✅ CORREGIDO (tool) |
| H3 | 3.6 % lecturas SD >250 ms → NACKs | ✅ timeout 250→450 ms (los picos son ~1.2-1.5 s, el retry salva SIEMPRE) |
| W1 | Botón Máx RAM no existía | ✅ agregado |
| W6 | Máx RAM 513 lotes (ceil) | ✅ floor — **FALTA re-uploadfs a COM8** |
| F2 | ACKs muestran value&0xFF (600→88) | 📝 cosmético, documentado |
| F6 | 2º 0xBB seguido puede timeout 1 vez (retry salva) | 📝 documentado |
| W3 | STOP durante dump: sin re-dump desde UI (datos quedan en SD) | 📝 documentado |
| W5 | Preview N usa input, no ACK | 📝 documentado |
| H4 | Prefetch de bloque en PSoC = dump ~2× más rápido | 📝 mejora post-campo |

## 4. Trampas operativas (¡leer antes de tocar el banco!)

1. **Reflashear el ESP esclavo cuelga el PSoC** → SIEMPRE `ToggleReset` por KitProg después
   (`GetPorts` → runfile con `ToggleReset 0 100`, ver `src/psoc/BUILD_PROGRAM_PSOC.md`).
2. **Tras ToggleReset esperar la auto-cal (~10-60 s)** antes de mandar configs (0xBB/…): si no,
   el PSoC no ackea en 750 ms y el esclavo NACKea (parece bug y no lo es).
3. **Prefijos de log del esclavo = `micros()`, dan la vuelta a los 4294.97 s** — un salto de
   timestamp NO es un reboot.
4. **Reflashear/uploadfs el maestro tira el AP** y en esta máquina `netsh wlan connect` está
   bloqueado; reconectar con **WlanConnect por ctypes** (perfil "GeoNetwork", sin escaneo —
   receta en memoria y en §"Operativo WiFi" de plan_pruebas_precampo.md). Si el AP no vuelve:
   pulso RTS por COM8 (reset estilo esptool) y reintentar.
5. **`ws_capture_test.py` fuerza decim=1** (hardcodeado): no sirve para probar captura decimada
   por radio — usar driver WS propio (patrón en scratchpad `ws_directed.py`, secuencia
   BB→A2→AE→B2 y contar DATA).
6. **No abrir la web UI mientras corre un test WS por consola**: pelean el takeover del socket.
7. pyserial a COM8/COM12 SIEMPRE con `dtr=False; rts=False` (si no, resetea el ESP).

## 5. Estado del banco AL CIERRE + próximos pasos

- **E5c (aceptación 10 min final, tool endurecido) quedó corriendo** (~00:56→01:45 aprox):
  outputs en el scratchpad de la sesión (`e5c_geo10min.i24le/.json`, log `e5c_com12.txt`).
  El criterio: PASS = 1.562.400 muestras exactas + SHA. Si la sesión ya murió, verificar el
  `.json`; si `error=null` y `sample_count=1562400` → **cerrar E5c como PASS en la matriz**.
  Si falló, el log COM12 tiene los síntomas (buscar `SYNC_STALL|SD_ERROR|SD_READ timeout`).
- **Falta `uploadfs` a COM8** para publicar W6 (floor del Máx RAM) — 30 s + reconexión WiFi (§4.4).
- Pendientes de hardware: probar duración HAMMER E2E con nodo HAMMER físico; multi-esclavo
  (2 GEO + HAMMER) end-to-end; H4 (prefetch SD) si el dump de 40 min molesta en campo.
- El PSoC quedó flasheado con el build SD validado; el esclavo con F1+H3+sdread; el maestro
  con los fixes de dump (firmware del working tree ya commiteado) y la web con Máx RAM (sin W6).

## 6. Commits de la sesión (más viejo→nuevo)

- `a6600941` esclavo: fix carrera cap (ARMED antes de sync) + encadenado validado (11.8/17.7 s)
- `3d9dbdf9` SD en PSoC validada + comando sdread N
- `738f9454` PSoC: snapshot TopDesign GEO arreglado (fitea) + build SD
- `a85565c1` esclavo: **F1** watchdog SYNC_STALL vs SD + H3
- `42fd0b71` maestro+web: fixes dump/ACK + botón Máx RAM + matriz
- `(commit artifacts)` evidencia del fallo F1 (geo_10min_2604.json)
- `(commit tool)` ws_capture_test: watchdog de silencio (F5)
- `(commit web)` W6 floor + matriz actualizada

## 7. Herramientas de la sesión (scratchpad, recrear si hace falta)

`com12_logger.py` (logger pyserial), `ws_directed.py` (comandos WS + ACKs), `test_e9_regression.py`
(regresión USB 9 checks), `test_caprace.py`/`test_maxdur.py` (encadenado), `test_sdread.py` (SD).
Patrón común: pyserial dtr/rts=False timeout=0.2; WS handshake manual + takeover=1 + frames 6-byte
0x56 (ptype 0=DATA, 1=HB, 3=READY, 7=ACK).
