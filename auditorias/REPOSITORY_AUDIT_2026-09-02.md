# Auditoría e índice del repositorio — 2 de septiembre de 2026

Este documento es una fotografía operativa del superproyecto después de la
puesta en marcha digital de la primera placa. Su objetivo es responder cuatro
preguntas: qué vive en cada repositorio, cuál es el entrypoint vigente, qué se
verificó y qué deuda sigue abierta.

## Método y alcance

La auditoría recorrió los archivos versionados, `.gitmodules`, los README de
entrada, manifests de build, scripts de prueba, historia reciente, estado Git,
catálogo de datos y enlaces Markdown locales. No interpreta los 230 documentos
académicos de Obsidian ni el contenido de bibliotecas de terceros como
documentación operativa. Los snapshots históricos se conservan como evidencia y
no se reescriben para que parezcan actuales.

Comandos reproducibles:

```powershell
Set-Location C:\Github\Tesis
.\scripts\check-layout.ps1
.\scripts\audit-documentation.ps1
```

`audit-documentation.ps1 -Strict` devuelve error si encuentra enlaces locales
rotos o rutas legacy dentro de los documentos de entrada.

## Inventario de repositorios

Los conteos provienen de `git ls-files`; incluyen fuentes y artefactos
versionados, pero no archivos ignorados.

| Sector | Archivos | Markdown | Revisión auditada | Entry point |
|---|---:|---:|---|---|
| superproyecto | 182 | 19 | `6deba5ce` durante esta auditoría | `README.md`, `scripts/bootstrap.ps1` |
| PCBs | 199 | 5 | `2dfed11` | `PCBs/README.md` |
| datos | 25.900 | 6 | `867cb38` | `data/CATALOGO.md` |
| documentación | 1.152 | 15 | `4405e5c` | `docs/README.md` |
| investigación | 354 | 230 | `af42527` | `docs/investigacion/README.md` |
| cálculos MATLAB | 636 | 5 | `9253b86` | `init_project.m` |
| cálculos Python | 402 | 24 | `548740a` | README de cada frente |
| firmware ESP32 | 96 | 1 | `8a0db0a` | `Nodo comunicación/*/platformio.ini` |
| firmware PSoC | 2.611 | 6 | `443a4ca` | dos workspaces PSoC Creator |
| interfaces MATLAB | 30 | 2 | `b39a307` | `init_project.m` |
| interfaces Python | 764 | 22 | `8dc1a69` | `geophone_scope/main.py`, `python -m server` |

Los SHA identifican la base inspeccionada. A las 01:04 el auto-guardado local
registró las primeras correcciones de README en cinco submódulos y actualizó
sus punteros en `6deba5ce`; las correcciones posteriores se integran en commits
de cierre separados.

## Arquitectura vigente

El PSoC y el ESP esclavo ya no usan una UART bidireccional:

```text
ESP GPIO26  -- UART comandos -->  PSoC Rx P15[0]
PSoC        -- I2C 0x42 ------->  ESP SDA21/SCL22 (muestras y diagnóstico)
ESP GPIO27  -- SYNC ----------->  PSoC P0[4]
ESP esclavo -- ESP-NOW -------->  maestro -- web/USB --> interfaces
```

El pinout se verificó contra los dos `cyfitter.h` generados y en hardware. La
explicación completa está en `docs/proyecto/ARCHITECTURE.md` y el procedimiento de placa en
`src/firmware/psoc/AUTOTEST_NODO_ESCLAVO.md`.

## Entry points y gates conocidos

| Frente | Comando principal | Gate o evidencia |
|---|---|---|
| layout modular | `.\scripts\check-layout.ps1` | nueve submódulos registrados e inicializados |
| documentación | `.\scripts\audit-documentation.ps1 -Strict` | enlaces locales y rutas operativas |
| ESP maestro | `pio run -e esp32dev` desde `master/` | build PlatformIO |
| ESP esclavo de campo | `pio run -e slave2` desde `slave/` | build PlatformIO |
| ESP autotest | `pio run -e slaveTest` | runner 28/28 y formato 17/17 |
| PSoC de campo | `.\program_psoc.ps1` | build, identidad GEO+SPI, 4 Fs ADC y programado 4×256 ECC |
| PSoC autotest | `.\program_psoc.ps1 -SelfTest` | mismo gate sobre el workspace de banco |
| GUI PyQt | `python main.py` desde `geophone_scope/` | tests unitarios locales por archivo |
| servidor web | `python -m server` desde `src/interfaces/python` | `python server/smoke_test.py` |
| MATLAB cálculos | `init_project` | agrega repo y MASW-Matlab al path |
| MATLAB interfaces | `init_project` | agrega ambas interfaces al path |
| JitX | entorno definido en cada `pyproject.toml` | `validate.py` de cada variante |

No se ejecutaron todos esos gates durante el scrapeo: la tabla distingue
entrypoints descubiertos de resultados verificados. La sesión digital anterior
sí compiló ambos PSoC, `slave2` y `slaveTest`, y ejecutó las 45 comprobaciones
offline del autotest.

## Correcciones documentales realizadas

1. El README raíz ya no afirma que el superproyecto contiene sólo gitlinks:
documenta `scripts/`, `src/mecanica/`, snapshots web y el modelo directo del
   martinete.
2. `docs/proyecto/ARCHITECTURE.md` refleja UART de bajada, I2C de subida y SYNC dedicado.
3. `docs/proyecto/MIGRATION.md` distingue la modularización del 20 de julio de la
   reorganización por propósito del 24 de julio.
4. Los README de documentación, investigación, firmware, interfaces, cálculos,
   datos y PCB usan las rutas actuales bajo `src/` y `docs/investigacion`.
5. El catálogo de datos incorpora las campañas de osciloscopio calibradas,
   procesados omitidos, el snapshot del servidor y el modelo hidrogeológico.
6. `data/server/README.md` separa claramente evidencia de campo de código
   ejecutable.
7. Se agregó un auditor local para impedir que enlaces y rutas operativas
   vuelvan a degradarse silenciosamente.

## Deuda y riesgos descubiertos

### Prioridad alta

- **Analógico pendiente:** la placa es digitalmente apta, pero faltan
  calibración EEPROM, matriz IDAC→etapas, PGAout, rangos ADC, ruido y geófono.
- **Cambios locales sin publicar:** al inicio del scrapeo, `main` estaba 50
  commits por delante de `origin/main`; ESP32 8, PSoC 13, documentación 10,
  investigación 3 e interfaces Python 1. No se hizo `push` porque publicar
  remotos no formaba parte de la autorización.
- **Estado personal PSoC:**
  `AcondicionamientoAnalogico.cywrk.elias` permanece modificado y sin commit.
  Es estado de GUI previo a la auditoría y no debe mezclarse con fuentes.

### Prioridad media

- `src/calculos_modelados/python` no tiene entorno de dependencias unificado;
  sus ocho scripts de prueba no forman todavía una suite con un comando único.
- `src/modelado_matlab/martinete_leva_multibody/` queda versionado directamente
  por la raíz, separado del repositorio `src/calculos_modelados/matlab`.
- `scripts/autonomia/` versiona un `__pycache__`, `loop.lock`, `status.json` y
  `port_state.json`. Son estado de ejecución, no fuentes; deben retirarse del
  índice en una limpieza específica que preserve cualquier evidencia útil.
- El catálogo de datos ahora cubre las carpetas principales, pero los ZIP
  sueltos de intercambio y `.ingest_staging` necesitan una política explícita
  antes de otra ingesta masiva.
- Las advertencias históricas del fitter PSoC (P15[1] usado para ruteo y setup
  CyBUS_CLK) siguen abiertas aunque ambos builds terminan correctamente.

### Prioridad baja o histórica

- Handoffs, planes cerrados y bitácoras conservan rutas antiguas porque
  describen el estado de su fecha. No deben usarse como instrucciones actuales.
- `esp-web-historicos/` contiene siete versiones completas y deliberadamente
  duplicadas de la UI. La autoridad activa está en el firmware maestro.
- Los READMEs académicos de Obsidian usan wikilinks; el auditor Markdown no
  valida esa semántica.

## Regla para mantenerlo vigente

Todo cambio de rutas, protocolo o entrypoint debe actualizar en el mismo
commit: README del repositorio dueño, `docs/proyecto/ARCHITECTURE.md` si cruza sectores y esta
auditoría si altera un riesgo o gate. Antes de fijar nuevos punteros de
submódulos, ejecutar `check-layout.ps1` y `audit-documentation.ps1 -Strict`.
