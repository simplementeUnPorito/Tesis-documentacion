# Copia de referencia de la app PyQt (field_review)

Snapshot tomado el **2026-07-26**, antes de portar la ventana Capturas entera a
la web. El commit exacto del que salió está en `COMMIT.txt`.

**Para qué está**: la web tiene que hacer *lo mismo* que esta app. Cuando algo de
la web se comporte distinto, esta copia es la referencia contra la que comparar,
sin depender de que los archivos vivos sigan igual.

Archivos:

| Archivo | Qué es |
|---|---|
| `field_review_app.py` | la app entera (todas las pestañas, PyQt6 + pyqtgraph) |
| `review_field_data.py` | lanzador de la app |
| `main.py` | entrada del paquete |

**No se copió** `field_review_data.py` a propósito: no tiene Qt, sigue vivo y es
**la misma capa de datos que usa el servidor web**. Copiarlo habría creado una
segunda versión que se desincroniza (PORT_PLAN §0.4).

Mapa rápido de la ventana Capturas, por si hace falta buscar algo:

| Qué | Línea |
|---|---|
| Armado de la ventana (splitter 480/900, tabla, controles, plots) | `_build_ui` :480 |
| Columnas y colores de la tabla | `_update_table_row` :907 |
| Estado a partir de (reviewed, accepted) | `_estado_display` :931 |
| Orden Pico a pico / original | `_compute_row_order` :872 |
| Filtros Todas / Sin revisión / N metros | `_row_matches_filter` :960 |
| Dibujo de los dos gráficos | `_refresh_plot` :1091 |
| Colores de traza por tema | `_plot_colors` :1510 |
| Teclas (W/S, A/D, ←/→, ↑/↓, Espacio, X) | `_handle_review_key` :1534 |
| Overlays: mismo label, promedio OK, promedio carpeta | :1206, :1264, :1322 |
