# Matriz de pruebas pre-campo — 2026-07-11/12 (auditoría "no quiero sorpresas")

> Documento vivo de la sesión de auditoría total. Banco: maestro COM8 (AP GeoNetwork,
> 192.168.4.1, firmware+web del working tree flasheados por el usuario ~20:57), esclavo GEO
> NODE_ID=1 en COM12 (PSoC + SD insertada). PC conectado a GeoNetwork → pruebas E2E por
> WebSocket con `ws_capture_test.py` / sondas propias. Regla: tras reflashear el ESP esclavo,
> `ToggleReset` al PSoC (ver memoria/BUILD_PROGRAM_PSOC.md).

## Estado del código bajo prueba

- Maestro: working tree (103 líneas sin commitear sobre `738f9454`) — incluye `g_effNBatches`/
  `dumpBatchesForNode()` (techo real de dump por HOTWAIT_ACK), dedup de ACKs de completado,
  `abortCaptureToArmed()` (START rechazado / watchdog HOT_WAIT), NACK inmediato a comandos
  directed durante captura, `0xAD` SET_RECLEN_HAMMER + `nBatchesForNode()` por hw_class (Fase A).
- Web: working tree (app.js 78 líneas sin commitear) — Duración GEOs/HAMMER separadas,
  botón "Máx SD (60000)", decimación global en barra superior, fila SD oculta sin sd_present.
- Esclavo COM12: HEAD (`3d9dbdf9`) + sdread. PSoC: HEAD (SD FatFs + encadenado, filas 0..252).

## Resultados

| # | Prueba | Cómo | Resultado |
|---|--------|------|-----------|
| E1 | Captura RAM chica por radio | `ws_capture_test.py -n 4 --node 1` | ✅ PASS 120/120 muestras, STOP limpio |
| E2 | Captura SD chica por radio (>presencia SD) | `-n 600` (6.9 s) | ✅ PASS 18000/18000, dump ~28 lotes/s |
| E3 | Captura SD mediana por radio | `-n 3000` (34.6 s) | ✅ PASS 90000/90000, dump 102 s |
| E4 | Log COM12 durante E3 | logger pyserial paralelo | ⚠️ ~108 `SD_READ timeout seq=N` (3.6 %, periódico ~26 lotes) absorbidos por retry maestro — funciona pero con tráfico NACK extra (ver H3) |
| E5 | **Aceptación 10 min** (1er intento, firmware previo al fix F1) | `--seconds 600 --fs 2604` = 52080 lotes | ❌ FAIL — reprodujo F1 y reveló la causa raíz real (ver F1) |
| E5b | **Aceptación 10 min** con fix F1 en esclavo | ídem tras flash F1+H3 | 🔄 EN CURSO |
| E6 | Decimación por radio (0xBB global) + captura decimada | WS: SET_CONFIG 0xBB=3, VER chico, fs=868 | ⏳ tras E5 |
| E7 | SD toggle web (0xC0) vs 0xBE del tool | WS + revisar slave handleSetConfig | ⏳ tras E5 |
| E8 | Duración HAMMER (0xAD) — set/ACK/preview | WS: AD=300 → ACK; sin nodo HAMMER real solo se valida el set | ⏳ tras E5 |
| E9 | Regresión USB banco (cap/decim/sdcap/sdread) post-todo | COM12 | ⏳ al final |
| E10 | UI real en Chrome (botones nuevos, captura, export) | claude-in-chrome → 192.168.4.1 | ⏳ si la extensión está disponible |

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
  El fix del maestro del working tree (`dumpBatchesForNode()` etc.) es complementario y correcto.
  Reintento completo: E5b en curso.
- **F2 (cosmético)**: los ACK reflejan `value & 0xFF` (SET_RECLEN=600 → ACK val=88; 3000 → 184).
  Confunde al leer logs. MsgCfgAck.ok es uint8 por diseño; opción: ACK "ok=1" fijo o
  informar módulo 256 documentado.
- **H3 (robustez)**: lecturas SD del PSoC >250 ms en ~3.6 % de lotes (periódico ~cada 26) →
  `PSOC_SD_READ_TIMEOUT_MS 250` del esclavo vence, NACK, retry del maestro. Funciona, pero
  el margen es fino: subir a ~400-500 ms y/o `DUMP_BATCH_TIMEOUT_MS 300→400` absorbería casi
  todos. Candidato a fix tras E5.
- **W1 (UI)**: el usuario cree haber agregado botón "Máx RAM" — NO existe (solo "Máx SD
  (60000)"). Agregar "Máx RAM (512)" que fije Duración GEOs a 512×30/fs.
- **W2 (menor)**: "Máx SD" no avisa si el esclavo no tiene SD (el clamp del esclavo salva,
  y `dumpBatchesForNode` evita la tormenta, pero la UI debería avisar).
- **OK-1**: `sync_protocol.h` maestro/esclavo: idénticos semánticamente (solo comentarios).
- **OK-2**: constantes web/ESP coherentes: 60000 SD / 512 RAM / 30 muestras-lote / 2604 Hz.
- **OK-3**: buffers web se redimensionan a la captura (`resizePresentCaptureBuffers`); 60000
  lotes = 1.8 M muestras ≈ 29 MB por nodo activo en el navegador — OK en PC, vigilar en celular.

## Operativa

- La auditoría multiagente (6 subagentes) murió por límite de sesión — auditoría hecha inline.
- Reflash del esclavo ⇒ el PSoC se cuelga ⇒ `ToggleReset` KitProg SIEMPRE después.
