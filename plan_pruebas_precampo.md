# Matriz de pruebas pre-campo — 2026-07-11/12 (auditoría "no quiero sorpresas")

> Documento vivo de la sesión de auditoría total. Banco: maestro COM8 (AP GeoNetwork,
> 192.168.4.1, firmware+web del branch), esclavo GEO
> NODE_ID=1 en COM12 (PSoC + SD insertada). PC conectado a GeoNetwork → pruebas E2E por
> WebSocket con `ws_capture_test.py` / sondas propias. Regla: tras reflashear el ESP esclavo,
> `ToggleReset` al PSoC (ver memoria/BUILD_PROGRAM_PSOC.md).

## Estado del código bajo prueba

- Branch de cierre: `codex/capture-engine-verilog`. Maestro+web funcional base en `42fd0b71`;
  W6 en `c7414403`; tool/UI/evidencia final en `8c80a15e`.
- Esclavo COM12: F1+H3 en `a85565c1`, con `PSOC_SD_READ_TIMEOUT_MS` ya elevado de **250 a
  450 ms**; PSoC: SD FatFs + encadenado (`3d9dbdf9`/`738f9454`, filas 0..252).
- Tool: F5 base en `7e4e332b`; `8c80a15e` agrega watchdog pre-DATA desde ACK `B2=2` y su
  self-test de regresión. El mismo commit agrega W7 (`step=0.01`) y el JSON E5c persistente.
- Builds locales de maestro (`pio run -e esp32dev`) y esclavo (`pio run -e slave1`): **PASS**.
- LittleFS W6+W7 publicado en COM8 y verificado contra la UI/HTTP real tras dos `uploadfs`.

## Resultados

| # | Prueba | Cómo | Resultado |
|---|--------|------|-----------|
| E1 | Captura RAM chica por radio | `ws_capture_test.py -n 4 --node 1` | ✅ PASS 120/120 muestras, STOP limpio |
| E2 | Captura SD chica por radio (>presencia SD) | `-n 600` (6.9 s) | ✅ PASS 18000/18000, dump ~28 lotes/s |
| E3 | Captura SD mediana por radio | `-n 3000` (34.6 s) | ✅ PASS 90000/90000, dump 102 s |
| E4 | Log COM12 durante E3 | logger pyserial paralelo | ⚠️ ~108 `SD_READ timeout seq=N` (3.6 %, periódico ~26 lotes) absorbidos por retry maestro — funciona pero con tráfico NACK extra (ver H3) |
| E5 | **Aceptación 10 min** (1er intento, firmware previo al fix F1) | `--seconds 600 --fs 2604` = 52080 lotes | ❌ FAIL — reprodujo F1 y reveló la causa raíz real (ver F1) |
| E5b | **Aceptación 10 min** con fix F1 en esclavo | ídem tras flash F1+H3 | ◐ PARCIAL — captura 600 s PERFECTA (SD_SESSION 0x01, fill=52080/52080, **sin SYNC_STALL → F1 fix validado**); dump impecable hasta 93.2 % (48562 lotes, 4.37 MB por radio, 0 errores) y ahí el CLIENTE Python se colgó (socket half-open sin FIN, sin watchdog de silencio → F5). El maestro pausó el dump correctamente (datos preservados). No es fallo de firmware. |
| E5c | **Aceptación 10 min** con tool endurecido (F5 fix) | `--seconds 600 --fs 2604 --node 1`, 52080 lotes; logger COM12 paralelo | ✅ **PASS E2E** — SD 52080/52080; 1562400/1562400 muestras; 4687200 B; extra=0; cleanup limpio; 1 conexión/0 desconexiones; 2626.472 s; SHA coincidente. 0 SYNC_STALL/SD_ERROR. |
| E6 | Decimación por radio + captura decimada | 0xBB=2 dirigido + VER 100 lotes a fs 1302 | ✅ PASS 3000/3000 muestras; restore a decim 1 OK. Nota: `ws_capture_test` NO sirve para esto (fuerza decim=1 hardcodeado) — se hizo con driver WS propio |
| E7 | SD toggle web (0xBE) | code-review + runtime (E2/E3/E5 usan 0xBE) | ✅ PASS — web usa 0xBE; 0xC0 obsoleto rechazado siempre; flag ESP dual-alimentado (ACK 0xBE + bit6 SD_STATUS) |
| E8 | Duración HAMMER (0xAD) set/ACK | WS: AD=300 → ACK val=44 (=300&0xFF, F2 cosmético); AD=0 → val=0 | ✅ PASS (E2E completo requiere nodo HAMMER físico) |
| E9 | Regresión USB banco post-fixes | probe/sdinfo/cap RAM d1·d3/SD cap+sdread 0·99·fuera-de-rango/FIR d2 | ✅ **9/9 PASS** |
| E10 | UI real + publicación final | 192.168.4.1 (LittleFS real vía uploadfs) | ✅ PASS — W6: Máx RAM fija input 5.89 s, calcula 512 lotes y muestra preview real 5.90 s; sin errores de consola. Segundo uploadfs publicó W7; ping 4/4, `/health littlefs=ok` y GET real confirmó `step=0.01` + floor W6. |
| E11 | Regresión de cierre post-upload | self-test F5, builds maestro/esclavo, `ws_capture_test --batches 4` y probe final | ✅ PASS — pre-DATA watchdog 19.999/20.000 s; ambos builds limpios; smoke 120/120; probe final `psoc=1`, `fs=2604`, `bBad=0`, IDLE/fill=0; cleanup limpio. |
| E12 | Reconexión WS real durante dump | `ws_fault_test.py` (corte inyectado tras 3000 muestras) | ✅ PASS — status=ok, 2 conexiones/1 desconexión, 18000/18000 muestras, 54000 B, extra=0, SHA coincidente, cleanup limpio. |
| E13 | STOP en vivo (RUNNING y DUMPING) | `ws_fault_test.py` en el mismo socket | ✅ PASS ambos — RUNNING: ACK=0, 0 parciales, espera nominal+5 s (11.912 s) y smoke 120/120; DUMPING: 30 parciales, vuelta a ARMED, smoke 120/120. Ejercitó F6 real (BE 0→1 al retry). |
| E14 | Recorrido de operador UI real (2026-07-12) | Chrome sobre 192.168.4.1: panel esclavo, Máx RAM, captura, export, beforeunload | ✅ PASS — panel Geo1 con MAC/RSSI real (-16 dBm)/PGA/rango/SD detectada (cierra pendiente RSSI); Máx RAM→5.89 s→512 lotes; captura UI E2E 512 lotes/15360 muestras exactas graficadas; ZIP íntegro (raw_f32le 61440 B = 15360×4 exactos, 30720 filas CSV); guard `beforeunload` activo con datos sin exportar y limpio tras export (verificado por dispatch sintético, sin modal); rango ADC round-trip navegador→PSoC ±2.5→±0.512→±2.5 con `Current:` + ACK verde; 0 errores de consola. Nota entorno: Chrome retiene el rename del ZIP (Safe Browsing sin internet en el AP) — el `.tmp` es el ZIP completo e íntegro. |
| E15 | **Captura SD máxima 60000 lotes** (≈11.5 min, tope jerarquía) | `sd_max_regression_test.py --batches 60000` por USB, sin radio | ✅ **PASS** — sesión SD 60000/60000 completa en 695.2 s, 0 SYNC_STALL/SD_ERROR/eventos prohibidos; `sdread` extremos 0/59999 limpios; seq=60000 rechazado OOR con fill=60000; GEOLAST COMPLETE preservado con capture=off; cleanup limpio. 1.8 M muestras ≈ 5.4 MB canónicos. Evidencia: `slave/artifacts/e15_sd_max_60000_pass.json`. 1ª corrida reveló F8 (criterio del runner, no firmware). |
| E16 | Transiciones dirigidas rango ADC (0xBA) + decimación (0xBB) | `adc_decim_transitions_test.py` por USB: r1→r2→r4→r3→r1, d1→d2→d6→d3→d4→d1, combo r4+d3, rechazos | ✅ **PASS 49/49** — ACK y mini-captura 4 lotes en cada transición con fs exacta (2604/1302/868/651/434); combo r4 d3 OK; `range 0/5` y `decim 0/101` rechazados localmente sin ACK; restauración r1 d1. Dos transitorios clase F6 (un ACK 0xB7 y un `cap` ignorado tras cambio de config) absorbidos por el retry acotado de 2 intentos, siempre al 2°. Evidencia: `slave/artifacts/e16_adc_decim_transitions_pass.json`. |
| E17 | Reset físico PSoC (ToggleReset KitProg) + auto-cal + recovery SD | `psoc_reset_recovery_test.py`: reset real con ESP vivo y GEOLAST de 60000 montado | ✅ **PASS 30/30** — pre-reset 0x37 (COMPLETE, capture off); ToggleReset OK; PSoC sano (psoc=1, IDLE, fs=2604) a los 18.2 s de auto-cal; post-reset GEOLAST COMPLETE recuperado con capture re-armado (0x77, default de boot deliberado: `g_sd_cap_en=1` si SD montada, field-safe tras power-cycle); ACKs BB/B7/BE al primer intento; captura RAM 4 lotes y captura SD 5 lotes + sdread 0/4 + OOR post-reset; cleanup limpio. Evidencia: `slave/artifacts/e17_reset_recovery_pass.json`. |
| E18 | Mini-soak de cierre por radio | 5× `ws_capture_test --batches 4 --force` consecutivos | ✅ PASS 5/5 — 120/120 muestras cada uno, SHA-256 únicos (datos frescos), probe final `psoc=1` IDLE fs=2604 bBad=0 fill=0/0, `/health littlefs=ok`. |

## Fallos / hallazgos

- **F1 (crítico) — CAUSA RAÍZ ENCONTRADA EN VIVO Y CORREGIDA (E5 del 23:31 la reprodujo)**:
  el watchdog `VIEW/START_SYNC_STALL` del ESCLAVO estaba diseñado para capturas RAM (donde
  `fill`/`bOK` crecen durante el muestreo). En capturas a SD NO llegan lotes UART durante el
  muestreo (fill=0 y bOK congelado POR DISEÑO) y el cierre de GEOLAST.BIN crece con el tamaño
  (~3.3 s con 52080 lotes ≈ 4.7 MB). Con el margen fijo (~2.3 s), a los `elapsed=602500 ms` el
  watchdog declaró stall y **mandó `START_NOW` de nuevo al PSoC 955 ms ANTES de que llegara el
  `SD_SESSION 0x01`** de la captura que había terminado BIEN (fill=52080/52080). El START_NOW
  fantasma re-armó el PSoC (nueva sesión SD) → invalidó GEOLAST.BIN → `SD_ERROR 0x08` → NACK
  eterno a los `REQ_BATCH` del maestro → 0 muestras. E2 (600) y E3 (3000) pasaban porque el
  cierre SD llegaba antes del margen; **toda captura SD larga perdía la carrera siempre**.
  Nota: los prefijos de log del esclavo son `micros()` y dan la vuelta a los 4294.97 s — el
  "reboot" aparente en el log era el wrap, no un reset real.
  **Fix (esclavo, commiteado)**: en modo SD el fallback (a) suma margen proporcional
  (`+15 s + n/2 ms`; 52080 → +41 s) y (b) si aún así vence, hace ABORT limpio (NACK CMD_VIEW/
  CMD_START, sync LOW, STOPPED) y **jamás re-dispara START_NOW** (destruiría la sesión).
  El fix del maestro en `42fd0b71` (`dumpBatchesForNode()` etc.) es complementario y correcto.
  Validación: E5b y ambos intentos E5c llegaron a SD 52080/52080 sin `SYNC_STALL` ni
  `SD_ERROR`; la repetición final E5c también cerró el transporte E2E 1562400/1562400 PASS.
- **F2 (cosmético)**: los ACK reflejan `value & 0xFF` (SET_RECLEN=600 → ACK val=88; 3000 → 184).
  Confunde al leer logs. MsgCfgAck.ok es uint8 por diseño; opción: ACK "ok=1" fijo o
  informar módulo 256 documentado.
- **H3 (robustez, corregido)**: lecturas SD del PSoC >250 ms en ~3.6 % de lotes (periódico
  ~cada 26) hacían vencer al esclavo, NACK y retry del maestro. `a85565c1` elevó
  `PSOC_SD_READ_TIMEOUT_MS` de **250 a 450 ms** y el build/ejecución actuales ya incluyen ese
  valor. Los picos de ~1.2-1.5 s todavía requieren retry, pero no pierden lotes.
- **H4 (rendimiento, NO bloquea campo)**: durante el dump SD de E5b (52080 lotes) se midió
  que ~1 de cada 26 lecturas 0xBF tarda **~1.2-1.5 s** (2 timeouts de 450 ms + retry hasta
  éxito; máx 2 timeouts por seq, después siempre entrega). Esas ~2000 lecturas lentas suman
  ~22 min del dump de ~40 min. El retry maestro↔esclavo lo absorbe SIEMPRE (0 lotes perdidos),
  pero el dump sería ~2× más rápido con prefetch del bloque siguiente en el PSoC
  (leer block+1 apenas se envía el frame) o fast-seek CLMT de FatFs. Candidato post-campo.
  En E5c final se observaron 2449 timeouts en 1230 secuencias de 52080 (2.36 %): 1219
  secuencias requirieron dos timeouts, 11 uno y ninguna más de dos; todas se recuperaron.
- **W1 (UI)**: el usuario cree haber agregado botón "Máx RAM" — NO existía (solo "Máx SD
  (60000)"). CORREGIDO: agregado "Máx RAM (512)" (index.html + app.js, commit `42fd0b71`),
  publicado por `uploadfs` y validado en la UI real.
- **W2 (menor)**: "Máx SD" no avisa si el esclavo no tiene SD (el clamp del esclavo salva,
  y `dumpBatchesForNode` evita la tormenta, pero la UI debería avisar).
- **OK-1**: `sync_protocol.h` maestro/esclavo: idénticos semánticamente (solo comentarios).
- **OK-2**: constantes web/ESP coherentes: 60000 SD / 512 RAM / 30 muestras-lote / 2604 Hz.
- **OK-3**: buffers web se redimensionan a la captura (`resizePresentCaptureBuffers`); 60000
  lotes = 1.8 M muestras ≈ 29 MB por nodo activo en el navegador — OK en PC, vigilar en celular.

- **F5 (tooling, corregido y endurecido)**: `ws_capture_test.py` no detectaba un socket WS medio-muerto
  (drop de WiFi sin FIN): `poll_once` devolvía timeout limpio para siempre y el tool esperaba
  todo el `dump_timeout` (46 min) sin reconectar → E5b congelado al 93.2 %. Fix: watchdog de
  silencio (sin DATA >20 s en fase dump → drop + re-takeover; el maestro reanuda donde quedó).
  La auditoría de cierre del código expuso un segundo hueco: si el socket quedaba half-open después de
  entrar a dump pero **antes del primer DATA**, el reloj todavía no existía. `8c80a15e`
  ahora lo inicia al recibir ACK `VER/B2=2`, conserva `last_data_at` como timestamp exclusivo
  de DATA real y contiene un self-test que construye ese estado pre-DATA, verifica que no
  desconecte a 19.999 s y que sí cierre/rearme takeover a 20.000 s. Self-test: **PASS**.
- **F6 (menor, transitorio)**: un segundo 0xBB (decim) inmediatamente después de otro puede
  dar `PSoC cfg ack timeout 750 ms` una vez; el reintento inmediato funciona. La web ya
  serializa configs y reintenta. También pasa si se manda 0xBB con la auto-cal del PSoC
  corriendo (tras ToggleReset esperar ~60 s o reintentar). E16 amplió la caracterización:
  la misma clase transitoria afecta a 0xB7 (stream) y al `cap` USB inmediatamente después de
  un cambio de config (el `cap` queda ignorado en silencio: fill=0/0, state=0, sin mensaje de
  error). El retry acotado de 2 intentos con evidencia por intento lo resuelve SIEMPRE al 2°;
  todos los runners del banco lo implementan.
- **F8 (tooling, corregido)**: el criterio de cleanup de `sd_max_regression_test.py` (E15)
  bloqueaba el veredicto si el contador `drop` del esclavo crecía durante la corrida. Ese
  contador es `_syncDrops` (`psoc_uart.cpp`): cuenta bytes de TEXTO UART del PSoC descartados
  por el framer mientras busca el marcador 0xAB — crece de forma benigna con cada línea de log
  del PSoC, incluso en idle (observado: +58 en reposo, +18/+14 en corridas de 12 min). Solo
  `bBad`/`badLen` indican frames corruptos. Fix: `uart_integrity_errors()` bloquea únicamente
  por bBad/badLen y el delta de drops queda informativo en el JSON (`sync_drops_delta`);
  self-test cubre ambos casos. La 1ª corrida E15 (capture 60000/60000 PERFECTA) solo falló
  por este criterio; la 2ª cerró PASS integral.
- **OK-4 (E17)**: el PSoC re-arma deliberadamente `g_sd_cap_en=1` al boot si la SD está
  presente y el FAT montado (`main.c`, tras `sd_session_recover()`): default field-safe para
  que tras un power-cycle en campo las capturas sigan yendo a SD sin necesitar 0xBE. No es un
  bug; los criterios post-reset deben esperar bit 0x40 ENCENDIDO (status 0x71/0x77).
- **W5 (menor, UI)**: el preview "N (decimación) → Hz" usa el valor del INPUT (localStorage),
  no el confirmado por ACK — puede diferir de la Fs real de la barra superior hasta apretar
  "Aplicar N". Confuso pero coherente con el patrón input+Apply.
- **W6 (corregido, publicado y verificado)**: "Máx RAM" fijaba 5.90 s → recomputaba 513 lotes
  (ceil) y el esclavo clampaba a 512. `c7414403` usa floor: input **5.89 s**, **512 lotes**
  exactos y preview real **5.90 s**. El `uploadfs` a COM8 y la prueba en UI real pasaron sin
  errores.
- **W7 (corregido, publicado y verificado)**: el input Duración GEO todavía
  declaraba `step="0.1"`; aunque W6 escribía correctamente 5.89, el navegador lo consideraba
  un valor inválido por step mismatch. Cambiado a `step="0.01"`. El segundo `uploadfs` a
  COM8 y su verificación pasaron; el HTML servido ya contiene `step="0.01"`.
- **Operativo WiFi**: `netsh wlan connect` está bloqueado sin permiso de ubicación/elevación
  en esta máquina. Desde `src/esp/Nodo comunicación/master`, ejecutar
  `python reconnect_geonetwork.py --timeout 120`: usa **WlanConnect por ctypes** con el perfil
  guardado `GeoNetwork`, sin escanear SSIDs, y sólo retorna éxito cuando
  `http://192.168.4.1/health` responde con `littlefs=ok`. Esta ruta ya fue validada después
  del `uploadfs` W6.

## Gate de aceptación E5c

El intento heredado prueba un **FAIL E2E**, no un PASS: no dejó
`e5c_geo10min.json`; sólo `e5c_geo10min.i24le`, truncado en **442353 B = 147451/1562400
muestras**. En paralelo, `e5c_com12.txt` prueba que la adquisición física fue correcta: SD
**52080/52080**, **0 `SYNC_STALL`** y **0 `SD_ERROR`**. La repetición final volvió a alcanzar
SD **52080/52080** y completó el dump; binario/JSON/log crudos quedaron en el scratchpad como
`e5c_final_geo10min.i24le`, `e5c_final_geo10min.json` y `e5c_rerun_com12.txt`.

<!-- E5C_FINAL_BEGIN: CERRADO 2026-07-12 -->
> **E5c FINAL: ✅ PASS — SISTEMA DEL BANCO LISTO PARA CAMPO.**
>
> JSON versionado: `master/artifacts/e5c_geo10min_2604_pass.json` · `status="ok"` ·
> `error=null` · `expected_samples=samples_written=1562400` ·
> `bytes_written=actual_file_bytes=4687200` · `extra_samples=0` ·
> `final_cleanup_ok=true` · `cleanup_errors=[]` · 1 conexión/0 desconexiones ·
> 2626.472 s · SHA-256 recalculado:
> `6332b571f9f688ef828b23906d51cdc0d82c1e5b294a3f522a34cacfeedd64db`.
<!-- E5C_FINAL_END -->

Para emitir PASS deben cumplirse **todos** los invariantes del JSON:

- `status == "ok"` y `error == null`;
- `expected_samples == samples_written == 1562400`;
- `bytes_written == actual_file_bytes == 4687200`;
- `extra_samples == 0`;
- `final_cleanup_ok == true` y `cleanup_errors == []`;
- `sha256` tiene 64 dígitos hexadecimales y coincide con el SHA-256 recalculado del `.i24le`.

**Gate cerrado:** E5c, W7, reconexión, ping, `/health` y smoke post-upload pasaron. El sistema
disponible en este banco queda **LISTO PARA CAMPO**.

**Ampliación de cobertura cerrada (2026-07-12, segunda tanda):** E12/E13 (fallas WS y STOP),
E14 (operador UI completo con export y beforeunload), E15 (tope SD 60000), E16 (transiciones
rango/decimación), E17 (power-cycle PSoC + recovery SD) y E18 (mini-soak 5/5) — **todo PASS**.
Con esto el veredicto LISTO PARA CAMPO queda ratificado con el tope de la jerarquía de memoria,
el recorrido de operador real y el ciclo de reset físico validados. Los únicos pendientes
siguen siendo los de hardware ausente (HAMMER E2E y multi-esclavo) y H4 opcional.

## Pendientes fuera del banco y mejora post-campo

- **Requieren hardware no presente:** duración HAMMER E2E con nodo HAMMER físico y prueba
  multi-esclavo (2 GEO + HAMMER). No deben confundirse con fallos del banco disponible.
- **H4, opcional post-campo y no bloqueante:** prefetch del bloque SD siguiente en el PSoC
  (o fast-seek CLMT FatFs) para llevar el dump a aproximadamente 2× de velocidad.

## Operativa

- La auditoría multiagente (6 subagentes) murió por límite de sesión — auditoría hecha inline.
- Reflash del esclavo ⇒ el PSoC se cuelga ⇒ `ToggleReset` KitProg SIEMPRE después.
- Commits relevantes, sin placeholders: `a6600941`, `3d9dbdf9`, `738f9454`, `a85565c1`,
  `42fd0b71`, `dea23474`, `7e4e332b`, `c7414403`, `89816ca5`, `8c80a15e`, `ae2d0315`,
  `f4461dd9` (runners E15/E16/E17 + gate USB + ws_fault + evidencia E15). Esta actualización
  documental de la segunda tanda se commitea inmediatamente después de `f4461dd9`.
- Runners persistentes del banco (todos con `--self-test` offline): `slave/usb_regression_test.py`
  (gate 33/33), `slave/sd_max_regression_test.py` (E15), `slave/adc_decim_transitions_test.py`
  (E16), `slave/psoc_reset_recovery_test.py` (E17, ejecuta ToggleReset por ppcli él solo),
  `master/ws_fault_test.py` (E12/E13), `master/ws_capture_test.py` (aceptación/smoke).
