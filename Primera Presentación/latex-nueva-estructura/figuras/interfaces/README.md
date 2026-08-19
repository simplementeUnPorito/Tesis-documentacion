# Inventario de capturas de interfaces

Capturas generadas el 18 de agosto de 2026 para la versión extendida de la
primera presentación. Las aplicaciones se levantaron contra una copia de nueve
capturas de la campaña Canchita; no se modificaron los datos originales.

## Servidor web FastAPI

- `web_servidor_01_capturas_datos.png`: tabla y señales reales de martillo/geófono.
- `web_servidor_02_filtros_kalman.png`: filtros y configuración Kalman.
- `web_servidor_03_filtros_kalman_expandido.png`: panel Kalman completo y vertical.
- `web_servidor_04_agrupamiento.png`: definición de grupos.
- `web_servidor_05_enfase.png`: alineamiento temporal.
- `web_servidor_06_promedios_arrivals.png`: promedios y arribos.
- `web_servidor_07_waterfall.png`: gather por distancia.
- `web_servidor_08_masw_dispersion.png`: controles y picking de dispersión.
- `web_servidor_09_masw_inversion.png`: parametrización de inversión.
- `web_servidor_10_masw_perfil_vs.png`: salida de perfil Vs.
- `web_servidor_12_borrado.png`: operaciones destructivas separadas.

`web_servidor_01_capturas.png` y `web_servidor_11_masw_dispersion_regreso.png`
se conservaron como estados alternativos, pero no se insertaron porque duplican
una vista mejor.

## Revisión de campo PyQt

La serie `qt_revision_01` a `qt_revision_09` recorre Capturas, Filtros,
Agrupamiento, Enfase, Promedios, Waterfall y las tres vistas MASW.

## Adquisición multipunto PyQt

La serie `qt_scope_01` a `qt_scope_06` recorre Stream, tres esclavos, Log y el
tema claro.

## Interfaces MATLAB

- `matlab_scope_simple.png`: alcance USB individual.
- `matlab_interface_esp_05_stream.png`: estado global de tres nodos.
- `matlab_interface_esp_04_esclavo_1_s1.png`: esclavo 1.
- `matlab_interface_esp_03_esclavo_2_s2.png`: esclavo 2.
- `matlab_interface_esp_02_esclavo_3_s3.png`: esclavo 3.
- `matlab_interface_esp_01_log.png`: registro.

Los archivos `matlab_interface_esp_02_esclavo_1_s1.png` y
`matlab_interface_esp_03_stream.png` pertenecen a la primera ejecución de un
solo nodo y se conservaron como respaldo.

## Pendientes

- capturas directas de los cinco menús de la SPA embebida del ESP32;
- capturas de las siete versiones históricas extraídas en
  `C:\Github\Tesis\esp-web-historicos`;
- capturas completas de cada TopDesign histórico en PSoC Creator.

Las SPA históricas ya pueden ejecutarse sin placa con `serve_demo.py`; los dos
últimos grupos de capturas requieren un escritorio Windows desbloqueado.
