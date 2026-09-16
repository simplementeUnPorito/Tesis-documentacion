# Documentación de Tesis

Entregables, diagramas, propuestas y documentos técnicos transversales del sistema MASW. El código ejecutable vive en repositorios separados y se integra desde [`Tesis`](https://github.com/simplementeUnPorito/Tesis).

## Alcance

- `Propuesta Urucom/`: fuentes y versiones renderizadas de la propuesta.
- `Urucom_2026/` y `Urucom_2026_compact/`: versiones completas y compactas de
  la comunicación.
- `Primera Presentación/`: presentación de avance, fuentes LaTeX, figuras,
  evidencia y auditorías.
- `Propuesta Tesis UCA/`: documentos institucionales.
- `calibration_fsm/`: diagramas de la máquina de calibración.
- `investigacion/`: submódulo del vault de Obsidian, incluida la bitácora.
- planes y handoffs que cruzan PSoC, ESP32, Python y MATLAB.

Las rutas vigentes dentro del superproyecto son `src/firmware/psoc`,
`src/firmware/esp32`, `src/interfaces/python`, `src/interfaces/matlab`,
`src/calculos_modelados/python`, `src/calculos_modelados/matlab`,
`docs/investigacion` y `data`.

Los paquetes ZIP y diagramas Draw.io se indexan con Git LFS. Sus contenidos viven en `Github-LFS/repositories/Tesis-documentacion`; GitHub conserva los punteros. Para restaurarlos tras un clon sin smudge:

```powershell
$env:GITHUB_LFS_ROOT = 'C:\Users\elias\OneDrive\Github-LFS'
.\scripts\configure-lfs-folderstore.ps1
.\scripts\hydrate-lfs.ps1
```

## Notas técnicas sueltas (julio–septiembre 2026)

Registros de banco escritos en caliente. Para el trabajo posterior al
2026-09-05 la bitácora está en `lab/` del superproyecto (`lab/README.md`), y el
estado vigente de la calibración en
`src/firmware/psoc/AcondicionamientoAnalogico.cydsn/CONTROL_UNIFICADO.md`.

**Planes y handoffs**

| archivo | contenido |
|---|---|
| `psoc_supermaquina_handoff.md` | CaptureEngine / superMaquina del PSoC (2026-07-02) |
| `plan_adc_1020.md` | ADC a 1020 Hz y dos rangos — **superado** el 2026-07-11 |
| `plan_2929_decimation_sd.md` | muestreo nativo, decimación con promedio y SD en el PSoC (seguimiento por checkboxes) |
| `plan_pruebas_precampo.md` | matriz de pruebas de la auditoría pre-campo (11–12/07) |
| `HANDOFF_SESION_2026-07-12.md` | cierre de la auditoría pre-campo, SD en PSoC, encadenado |
| `HANDOFF_NOCHE_2026-09-03.md` → `HANDOFF_2026-09-04.md` | puesta en marcha de la placa nueva e inicio de la autocalibración |
| `MEDICIONES_2026-09-04.md`, `MEDICIONES_2026-09-05.md` | documento único de lo medido esos días, con método y crudos |

**Registros de hardware `hardware_*.txt`** (placa nueva, firmware de campo, COM8)

| fecha | archivo | hallazgo |
|---|---|---|
| 09-03 | `hardware_psoc_field_boot`, `hardware_adc_ack`, `hardware_idac_signed` | logs crudos de arranque, ACK del ADC e IDAC con signo |
| 09-03 | `hardware_idac_end_to_end` | IDAC manual firmado `0xAA` de punta a punta |
| 09-03 | `hardware_pipeline_captura` | captura e ingesta PSoC → slave2 → maestro → ZIP → servidor sin intervención |
| 09-03 | `hardware_transferencia_vref_lp` | transferencia Vref_LP → salida medida por la ruta de captura |
| 09-03 | `hardware_recuperacion_saturacion` | la cadena se recupera de saturar con τ ≈ 31 s |
| 09-04 | `hardware_capturas_vacias` | capturas vacías esporádicas; hipótesis descartada |
| 09-04 | `hardware_adc_configs` | las cuatro configuraciones del ADC no coinciden entre sí |
| 09-04 | `hardware_calibracion_primera_corrida`, `_limite`, `_no_se_sostiene` | primera autocalibración: converge pero no se sostiene, y dónde se rompe |
| 09-04 | `hardware_matriz_acople` | matriz de acople entre etapas |
| 09-04 | `hardware_pullups_caidos` | falsa alarma: no hubo falla de hardware |

Otros: `informe_semana_2026-09-06/` (informe LaTeX de la semana, con
`compilar.ps1`), `proyecto/` (arquitectura, migración, supuestos de hardware,
conectividad del maestro), `masw/informe`, `legacy/pyqt_field_review`.
