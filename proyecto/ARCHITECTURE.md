# Arquitectura de repositorios

## Principio de separación

Cada repositorio posee una tecnología, sus instrucciones de ejecución, sus artefactos ignorados y sus dependencias externas. Las interfaces entre sectores son protocolos o formatos documentados; no se comparten árboles de fuentes mediante rutas internas.

```text
                              comandos UART (GPIO26 -> P15[0])
ESP32 esclavo  ------------------------------------------------->  PSoC 5LP
      |                                                            |
      | <------ I2C 0x42, muestras/estado/diagnostico --------------+
      | ------ SYNC GPIO27 -> P0[4], inicio de captura ------------->|
      |
      +------ ESP-NOW ------> ESP32 maestro ------> UI web / USB
                                                     |
                                                     +--> interfaces Python/MATLAB

data/raw ------> src/interfaces/python ------> data/processed
     +---------> src/calculos_modelados/python
     +---------> src/calculos_modelados/matlab

firmware + interfaces + modelos ------> PCBs/KiCad y PCBs/JitX
```

El enlace de la placa actual es asimétrico: el ESP manda comandos al PSoC por
UART, mientras que el PSoC devuelve pings, diagnóstico y lotes por I2C como
maestro. El inicio temporal de una adquisición no viaja por esos buses sino por
la línea dedicada SYNC.

Desde el 2026-09-16 el PSoC también es dueño de la calibración de la cadena
analógica: aprende una vez las referencias lentas (IDAC0/IDAC1) cuando el
operador lo autoriza, mantiene IDAC2/IDAC3 con un PI permanente fuera de
adquisición y adjunta su estado a los metadatos de cada captura. El ESP solo
transporta los comandos `ctl` (tramas `0xD0..0xD7`) y la telemetría clave/valor
(`[0xAB][0xC6]`). Las ráfagas I2C de subida acoplan ruido en la cadena analógica
durante ~0,5 s, por eso el PSoC las espacia cuando el lazo está estable. Detalle:
`src/firmware/psoc/AcondicionamientoAnalogico.cydsn/CONTROL_UNIFICADO.md`.

## Reglas de dependencia

- `src/firmware/psoc` y `src/firmware/esp32` se coordinan por UART de bajada,
  I2C de subida y SYNC; ninguno incluye fuentes del otro.
- `src/interfaces/python` contiene sus propios submódulos `ADsurf` y
  `maswavespy`, además de Geopsy almacenado mediante LFS.
- `src/calculos_modelados/matlab` contiene el submódulo
  `third-party/MASW-Matlab-code`.
- `PCBs` posee los diseños electrónicos de KiCad y JitX; sus renders y caches
  locales no se comparten con los repositorios de firmware.
- `docs` puede enlazar a todos los sectores, pero ningún componente necesita `docs` para compilar.
- `docs/investigacion/sources` versiona punteros LFS a la biblioteca privada; los
  bytes bibliográficos viven en el folderstore.
- `data` versiona mediante LFS las mediciones y resultados, con deduplicación
  por SHA-256; el repositorio Git conserva punteros, catálogo y estructura.
- `src/interfaces/python/third-party/geopsy`, los datasets `.mat` y los paquetes
  documentales grandes siguen el mismo esquema de almacenamiento externo.

## Versionado integrado

Un commit de `Tesis` es una línea base reproducible: registra un SHA concreto para cada submódulo. El desarrollo ocurre dentro del repositorio dueño del cambio; el superproyecto se actualiza únicamente cuando una combinación de revisiones debe probarse o entregarse como conjunto.

La ruta física del folderstore no forma parte de los punteros. Cada repositorio
incluye un configurador que traduce `GITHUB_LFS_ROOT` a su carpeta independiente
en `repositories/<nombre>`.

## Propiedad de los artefactos directos

La separación por submódulos no está completa al cien por ciento. Los snapshots
de `esp-web-historicos/` son deliberadamente inmutables; el modelo directo de
`src/modelado_matlab/martinete_leva_multibody/` sigue gestionado por el
superproyecto en vez de vivir en el submódulo de cálculos MATLAB. Ambos
pertenecen a la revisión integrada de la raíz y no deben confundirse con los entrypoints
activos de firmware o modelado.
