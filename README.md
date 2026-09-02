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
