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
  corriendo (tras ToggleReset esperar ~60 s o reintentar).
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

## Pendientes fuera del banco y mejora post-campo

- **Requieren hardware no presente:** duración HAMMER E2E con nodo HAMMER físico y prueba
  multi-esclavo (2 GEO + HAMMER). No deben confundirse con fallos del banco disponible.
- **H4, opcional post-campo y no bloqueante:** prefetch del bloque SD siguiente en el PSoC
  (o fast-seek CLMT FatFs) para llevar el dump a aproximadamente 2× de velocidad.

## Operativa

- La auditoría multiagente (6 subagentes) murió por límite de sesión — auditoría hecha inline.
- Reflash del esclavo ⇒ el PSoC se cuelga ⇒ `ToggleReset` KitProg SIEMPRE después.
- Commits relevantes, sin placeholders: `a6600941`, `3d9dbdf9`, `738f9454`, `a85565c1`,
  `42fd0b71`, `dea23474`, `7e4e332b`, `c7414403`, `89816ca5`, `8c80a15e`. Esta
  actualización documental final se commitea inmediatamente después de `8c80a15e`.
