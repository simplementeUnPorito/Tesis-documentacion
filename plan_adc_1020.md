# Plan ADC 1020 Hz — 2 modos de rango (±2.5 V / ±0.512 V), botón "Máx paquetes", auditoría PGA

> **SUPERSEDIDO (2026-07-11):** este archivo conserva el historial de la
> migración anterior. La configuración operativa vigente usa **2604 Hz nativos
> en los cuatro modos ADC** y `Fs efectiva = floor(2604/N)`. No usar los
> valores 1020/2929 de este registro como defaults de firmware, interfaz o
> scripts.

> **Archivo de seguimiento para agentes (Claude/codex).** Al completar cada ítem: marcar el checkbox
> y anotar una fila en el "Registro de progreso" del final ANTES de seguir. Si una sesión queda a
> medias, la siguiente retoma desde aquí.

Fecha de creación: 2026-07-06. Plan diseñado y aprobado en sesión Claude (rama `codex/capture-engine-verilog`).

## Objetivo

1. Migrar la Fs del sistema de 2929 Hz a **1020 Hz** en todas las capas (PSoC → slave → master → web → scripts → docs).
2. Exponer **2 modos de ADC** seleccionables desde la web, por esclavo: `ADC_CF_2V5` (config 1, ±2.5 V, default) y `ADC_CF_0V512` (config 2, ±0.512 V). Ambos a 1020 Hz efectivos. Las configs 3/4 del componente (±0.256/±0.128 V, 976 Hz) **no se exponen** (fuera de UI/protocolo/firmware).
3. Botón web "Máx paquetes": fija N = 512 lotes (tope de RAM del ESP), independiente de Fs.
4. Auditar la configuración de ganancia del PGA (veredicto abajo).

> Actualización 2026-07-06 noche: el punto 3 quedó refutado por prueba real.
> 512 lotes no es un máximo seguro del slave ESP; ver "Problemas abiertos /
> retomar desde acá".

## Contexto y hechos confirmados

- El usuario regeneró el componente ADC_DelSig con 4 configs. `Generated_Source/PSoC5/ADC.h`:
  `ADC_CF_2V5`=1 (±2.5 V, DEC_DIV=32, ALIGNMENT=1), `ADC_CF_0V512`=2 (±0.512 V, DEC_DIV=0),
  `ADC_CFG_0V256`=3 (nombre inconsistente CFG_, no usar), `ADC_CF_0V128`=4 (no usar).
- Fs efectivas según customizer ("Actual conv. rate"): configs 1 y 2 → **1020 SPS** (nominal 1000 inalcanzable
  por división de clock); configs 3 y 4 → 976 SPS. Solo usamos 1020.
- **BUG CRÍTICO ACTIVO**: `psoc_adc.c` usa `ADC_CFG1_DEC_DIV`/`ADC_CFG1`, macros que dejaron de existir con
  el renombre → el `#if` compila a falso y se pierde la división /32 → capturas 32× más grandes. Fix en H1.
- `ADC_SelectConfiguration(cfg, restart)` valida 1..4, mantiene la variable global `ADC_Config` (fuente de
  verdad de config activa). Nunca se llamaba desde el firmware de aplicación.
- El sub-comando dirigido nuevo (0xBA) viaja **sin tocar `sync_protocol.h`**: la web manda
  `{cmd:"BD",node,sub:"BA",param}` → master relay genérico (`master/src/main.cpp:774-778`) → `MsgSetConfig`
  → slave `handleSetConfig()` → UART PSoC. Igual que 0xB6/0xB7.
- La Fs se propaga sola: PSoC `FS_REPORT 0xC3` → slave `psoc_uart.cpp` `_sampleRate` → HELLO cada 2 s →
  master cachea → notif exacta 0xFD/0x05 → web `fsExactKnown`.
- Decisiones del usuario: reset del PSoC vuelve SIEMPRE a 2V5 (sin EEPROM, la web reaplica de localStorage);
  **calibración SIEMPRE en ±2.5 V** (si está activo 0V512: conmutar, calibrar, restaurar);
  selector por esclavo; botón Máx = 512 lotes fijos.
- **PGAp/PGAn NO SE TOCAN** (aviso explícito del usuario): implementan el INA de entrada (clase GEO, ×2 fijo
  cada uno). Cualquier cambio de ganancia va únicamente por `PGAgain`.

## Problemas abiertos / retomar desde acá (2026-07-06 noche)

El usuario probó en campo después de reprogramar y reportó dos regresiones:

1. **Rango ADC `±0.512 V`**: el ACK llega y la web confirma el cambio, pero la
   captura queda en cero o con datos claramente erróneos. No confiar todavía en
   ese rango; volver a `±2.5 V` para pruebas largas hasta verificar.
   - Hechos revisados: `ADC_CF_0V512_COUNTS_PER_VOLT = 256000`, igual que la
     escala usada por la web; no parece ser un bug simple de `countsPerVolt`.
   - Hipótesis más fuerte: la config 2 cambia `DEC_COHER` a `LOW`, mientras el
     DMA lee `ADC_DEC_SAMP_PTR` en orden low-mid-high. En config 1 (`DEC_COHER`
     `HIGH`) ese orden es correcto; en config 2 puede liberar coherencia en el
     primer byte y mezclar bytes viejos/nuevos. Forzar coherencia `HIGH` después
     de `ADC_SelectConfiguration()` para que el DMA lea el byte llave al final.
   - También conviene reconstruir el signo según `ALIGNMENT/RESOLUTION`: en
     configs right-aligned el bit de signo real es `resolution-1`, no
     necesariamente el bit 23.

2. **Captura máxima / 512 lotes**: el botón Máx deja `512 lotes / real 15.06 s`,
   pero el usuario observó fallas graves. Pruebas reportadas: 2 s, 5 s y 10 s OK;
   11 s, 12 s y 13 s fallan; 10.8 s funcionó hasta ahora (~368 lotes).
   - El slave guarda por lote `30 * sizeof(SampleBytes) + sizeof(uint32_t)` =
     `30*10 + 4 = 304 bytes/lote`. 512 lotes consumen ~155.6 KiB solo de store,
     antes de WiFi/ESP-NOW y heap fragmentado. 368 lotes consumen ~111.9 KiB.
   - Retomar bajando el máximo visible y de firmware a un valor seguro temporal
     (sugerido 360 lotes = ~10.59 s a 1020 Hz) o implementar reporte dinámico de
     heap/allocación antes de volver a subirlo.

Pendiente inmediato:
- [x] PSoC: forzar `ADC_SetCoherency(ADC_DEC_SAMP_KEY_HIGH)` tras seleccionar
      config y ajustar extensión de signo para configs right-aligned.
- [x] ESP/web: reemplazar el supuesto `PSOC_CAPTURE_MAX_BATCHES = 512` por un
      máximo seguro temporal: 360 lotes (~10.59 s a 1020 Hz) en master, slave e interfaz.
- [x] Compilar PSoC, slave y master.
- [x] Subir PSoC y slave2. Maestro queda para el último paso porque reinicia el AP y
      requiere que el usuario reconecte al GeoNetwork antes de probar web.
- [ ] Probar `±0.512 V` con captura corta (0.2 s) y revisar raw min/max; luego
      volver a `±2.5 V`.
- [ ] Probar el botón Máx seguro y confirmar que el dump completo termina.

## Veredicto auditoría PGA (pedido #4 — COMPLETADO en la exploración)

La cadena de códigos de ganancia es **correcta** de punta a punta, no hay bug de mapeo:
- Web `config.js:70-71`: `GAIN_CODES=[1,2,4,8,16,24,32,48,50]`, índice del select = código 0..8.
- `slave_panel.js:257-261` despacha el índice; app.js `sendDirected(ch, 0xA6, code)`.
- Slave valida (`isGainCode`) y reenvía 0xA6 crudo; PSoC `PGAgain_Set(code)` (main.c:1468-1479) →
  `psoc_hw_set_pga()` → `PGAgain_SetGain(code)`; constantes `*_GAIN_01=0x00 … *_GAIN_50=0x08` coinciden
  índice=código; telemetría `psoc_hw_pga_code_to_gain_x1000` (psoc_hw.c:5-19) coincide.

Observaciones (documentar, NO cambiar hardware):
1. En clase GEO el INA de entrada (PGAp/PGAn, ×2 fijo) multiplica ANTES de PGAgain → ganancia analógica
   total = 2 × (ganancia del dropdown). La web muestra volts a la entrada del ADC (señal acondicionada),
   no input-referred. Si algún día se quiere input-referred: dividir por 2×gain (GEO) / gain (HAMMER)
   usando `pga_gain` que ya está en metadata.
2. Tras reset del PSoC, el dropdown web (PGA y el nuevo de ADC) queda desincronizado del default real
   del PSoC (GEO bootea PGA=×4 code 2; ADC=2V5) hasta que el operador reenvía config ("resend").

## Checklist

### H0 — Este archivo
- [x] Crear `docs/plan_adc_1020.md` con checklist y registro.

### H1 — PSoC (`src/psoc/AcondicionamientoAnalogico.cydsn`) — solo .c/.h, PROHIBIDO .cyprj/.cydwr/.cysch/.cyfit
- [x] `psoc_adc.h`: API nueva `psoc_adc_get_config()`, `psoc_adc_set_config(uint8)` (solo acepta
      `ADC_CF_2V5`|`ADC_CF_0V512`), `psoc_adc_effective_fs_hz()` (1020 para ambas; switch preparado para 3/4),
      `psoc_adc_select_calibration_config()`.
- [x] `psoc_adc.c`: `static uint8 g_psoc_adc_config = ADC_CF_2V5;` + implementación de la API.
- [x] `psoc_adc.c` **fix bug DEC_DIV**: `psoc_adc_counts_right_aligned()` →
      `#if (ADC_CF_2V5_DEC_DIV != 0)` / `if (ADC_Config == ADC_CF_2V5) { adc_counts /= ADC_CF_2V5_DEC_DIV; }`.
- [x] `psoc_adc.c`: `psoc_adc_select_capture_config()` → `ADC_SelectConfiguration(g_psoc_adc_config, 0u);
      ADC_Start(); ADC_StopConvert();`.
- [x] `psoc_hw.h`: `#define PSOC_CMD_ADC_CONFIG 0xBAu` (param 1|2).
- [x] `main.c`: eliminar `PSOC_REPORTED_SRATE_HZ 2929u` (~línea 394); `uart_send_fs_report()` usa
      `psoc_adc_effective_fs_hz()`; `capture_expected_ms()` (~829-834) divide por Fs efectiva.
- [x] `main.c`: case `PSOC_CMD_ADC_CONFIG` en el switch de comandos (junto a SELECT_STREAM ~1856):
      gate `g_state == PSOC_IDLE`, `psoc_adc_set_config(rx_p1)`, `psoc_prepare_capture_path()`,
      `uart_send_cfg_ack(0xBA, config)`, `uart_send_fs_report()`; rechazo → ack con 0.
- [x] `main.c`: calibración SIEMPRE en 2V5 — llamar `psoc_adc_select_calibration_config()` al entrar a
      calibración (`psoc_start_calibration_if_idle()`); verificar que ningún Stop/Start del camino de cal
      pise `ADC_Config`; al terminar `psoc_prepare_capture_path()` restaura el modo elegido.
- [ ] Build `cyprjmgr` OK.
- [ ] Flash `ppcli` OK (GetPorts antes; `$lastRow = ceil(flash/256)-1`).

**Prueba de aceptación H1**: consola del slave (COM12, 115200): `probe` → FS_REPORT=1020;
`cap 1` → amplitudes plausibles (÷32 respecto al firmware con bug).

### H2 — ESP slave (`src/esp/Nodo comunicación/slave/src`)
- [x] `psoc_uart.h`: `#define PSOC_CMD_ADC_CONFIG 0xBA` + `void setAdcConfig(uint8_t cfg);`.
- [x] `psoc_uart.cpp`: `setAdcConfig` → `_sendCmd1(PSOC_CMD_ADC_CONFIG, c);`.
- [x] `main.cpp` `handleSetConfig()`: validar param ∈ {1,2}, despachar `psoc.setAdcConfig(param)`, waitAck.
- [x] `main.cpp`: eliminar `PSOC_NOMINAL_SAMPLE_RATE_HZ`/`PSOC_EFFECTIVE_SAMPLE_RATE_HZ` (97-101);
      `effectivePsocSampleRateHz()` → `return psoc.sampleRate();` (1903-1910); fallback 1020 en
      `expectedCaptureMs()` (~1923).
- [ ] `pio run -t upload --upload-port COM12` OK.

**Prueba de aceptación H2**: log del master muestra HELLO fs=1020; web ya no necesita Fs manual.

### H3 — ESP master + web mínima
- [ ] `master/src/main.cpp:96`: `ADC_SAMPLE_RATE_HZ 1020`.
- [ ] `matlab_transport.h:203` y `web_server.h:104`: fs/100 → `(fs + 50)/100` (redondeo, legacy cosmético);
      `web_server.h:89`: `fsArg = 1020`.
- [ ] `master/data/js/config.js:57`: `DEFAULT_SAMPLE_RATE_HZ = 1020`.
- [ ] `master/data/index.html:62`: Fs manual `value="1020"`.
- [ ] Botón `btn-max-batches` "Máx (512 lotes)" en `index.html` junto a `capture-secs` + listener en `app.js`:
      `secs = 512*30/currentFsHz()` redondeado hacia ARRIBA a 2 decimales (clamp de `batchesForSeconds()`
      lo deja exacto en 512); sin Fs conocida → log y no-op.
- [ ] `pio run -t upload` (COM8) + `pio run -t uploadfs` OK.

**Prueba de aceptación H3**: web muestra fs=1020 sin intervención; botón Máx → preview "512 lotes /
real ~15.06 s"; captura completa 15360 muestras/nodo; cronometrar ≈15.06 s (valida 1020 Hz real — R1).

### H4 — Web: dropdown Rango ADC por esclavo + escala por nodo + metadata
- [ ] `config.js`: `SUBCMD_ADC_CONFIG = 0xBA` + `ADC_CONFIGS = [{code:1,label:'±2.5 V',rangeV:2.5,
      countsPerVolt:131072/2.5},{code:2,label:'±0.512 V',rangeV:0.512,countsPerVolt:131072/0.512}]`.
- [ ] `slave_panel.js`: dropdown "Rango ADC" + dot (patrón del select PGA, líneas 111-119), evento
      `adc-config-changed {code}`, API `setAdcConfig(code)`/`setAdcConfigLock(state)`.
- [ ] `app.js`: handler calcado de `onPgaChanged` (pending + sendDirected + saveSlaveSetting); rama de ACK
      dirigido (~1723) → `nd.adcConfigCode`/`nd.countsPerVolt`/lock; reenvío en resend/send-all (~1403);
      restaurar de localStorage (~1549).
- [ ] `app.js`: `adcCountsToVolts` por nodo (`nd.countsPerVolt || cfg.ADC_COUNTS_PER_VOLT`).
- [ ] `data_store.js` `NodeData`: `adcConfigCode = 1`, `countsPerVolt = 0`.
- [ ] `export.js`: `adc_config`, `adc_range_v`, `adc_counts_per_volt` en metadata por nodo + columnas CSV;
      nota en metadata global del ZIP.
- [ ] Bump caché `?v=field-study-16` → `-17` (index.html + imports).
- [ ] `pio run -t uploadfs` + hard-refresh.

**Prueba de aceptación H4**: cambiar a ±0.512 V → dot verde (CFG_ACK); captura con señal conocida
(VDAC 0xAA / snapshot 0xB8) → volts correctos con countsPerVolt=256000; /32 solo en config 1;
calibrar con config 2 activa → corre en 2V5 y restaura; export ZIP con campos nuevos.

### H5 — Scripts, docs, cierre
- [ ] `master/ws_capture_test.py:134-135` → fs 1020; `simulate_hammer_dummy.py:21` → 1020.
- [ ] `README.md:91`, `master/WEB_FIELD_TESTS.md:70,134` → 1020.
- [ ] `docs/psoc_supermaquina_handoff.md`: sección nueva (cmd 0xBA, 2 modos, Fs 1020, cal en 2V5,
      bug DEC_DIV corregido, observaciones PGA/INA).
- [ ] `src/psoc/BUILD_PROGRAM_PSOC.md`: flash/lastRow nuevos; corregir COM del slave (es COM12; master COM8).
- [ ] Cerrar registro de progreso.

## Riesgos
- **R1** 1020 Hz solo confirmado por customizer → cronometrar captura en H3; si difiere, ajustar
  `psoc_adc_effective_fs_hz()` (el resto es data-driven).
- **R2** counts/V de 0V512 (=256000) confirmado por `ADC.h`, pero la ruta DMA debe usar coherencia compatible
  y extensión de signo por resolución → verificar con señal conocida.
- **R3** FIR hardware (0xB7) y presets FIR web diseñados para ~2929 Hz → a 1020 Hz los cortes quedan ~3× más
  abajo. Desaconsejar FIR hardware hasta regenerar coeficientes; verificar que el FIR software web use la fs
  vigente.
- **R4** Calibración en 2V5: offset residual puede ser fracción visible de ±0.512 V → verificar con 0xB8.
- **R5** Dropdown desincronizado tras reset del PSoC → mitigado con resend + localStorage.

## Registro de progreso

| Fecha | Hito | Resultado | Notas |
|-------|------|-----------|-------|
| 2026-07-06 | H0 | ✅ | Plan aprobado por el usuario; archivo creado. Exploración: bug DEC_DIV confirmado; PGA auditado OK; PGAp/PGAn = INA, no tocar. |
| 2026-07-06 | H1 código PSoC | ✅ parcial | API ADC 1/2, Fs 1020, fix DEC_DIV, comando 0xBA y calibración forzada/restaurada en 2V5 implementados. Build/flash pendientes. |
| 2026-07-06 | H2 código slave | ✅ parcial | Subcomando ADC 0xBA agregado al driver UART/handleSetConfig; Fs efectiva ahora viene del PSoC, fallback 1020. Upload pendiente. |
| 2026-07-06 | Revisión post-prueba | ⚠️ | Usuario reporta `±0.512 V` en cero/datos malos y fallo desde ~11 s. Investigación apunta a coherencia DMA del ADC en config 2 y a heap insuficiente para 512 lotes en slave. |
| 2026-07-06 | Fix ADC/rango y max seguro | ✅ parcial | PSoC: coherencia ADC forzada a HIGH para DMA low-mid-high y signo raw por resolución; build OK, flash filas 0..161 OK (`psoc_program_adc_coherency_20260706_195239.log`). ESP: `PSOC_CAPTURE_MAX_BATCHES=360`; master/slave builds OK; slave2 upload COM12 OK. Falta subir maestro/web y probar en página. |
