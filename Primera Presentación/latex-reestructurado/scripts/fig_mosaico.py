# -*- coding: utf-8 -*-
"""
Construye hojas de contacto (mosaicos) a partir de conjuntos grandes de figuras
ya generadas durante el proyecto.

Motivo: la campana de caracterizacion de la cadena analogica produjo 65 graficos
de osciloscopio + 65 de preprocesamiento espectral por tanda, y hay tres tandas.
Ponerlos uno por pagina serian 300 paginas; ponerlos en una hoja de contacto
permite que "todo lo hecho" quede efectivamente visible y verificable de un
vistazo, con el nombre de cada barrido debajo.

Uso:
    python fig_mosaico.py <dir_entrada> <salida.png> <titulo> [columnas]

Toma todos los .png del directorio, los ordena por nombre, los rotula con una
version abreviada del nombre de archivo y los pega en una grilla.
"""
import sys
import os
import re
from PIL import Image, ImageDraw, ImageFont

DIR_IN, OUT, TITULO = sys.argv[1], sys.argv[2], sys.argv[3]
COLS = int(sys.argv[4]) if len(sys.argv) > 4 else 6

CELDA_W = 460          # ancho de cada miniatura
MARGEN = 10
ALTO_ROTULO = 34
FONDO = (255, 255, 255)
TINTA = (27, 27, 27)
TENUE = (110, 110, 110)


def fuente(tam):
    for nombre in ("DejaVuSans.ttf", "arial.ttf", "Arial.ttf"):
        try:
            return ImageFont.truetype(nombre, tam)
        except OSError:
            continue
    return ImageFont.load_default()


F_ROT = fuente(15)
F_TIT = fuente(30)
F_SUB = fuente(17)


def etiqueta(nombre):
    """Reduce 'osciloscopio_100mHzto1Hz_200s_25s_div_XD_ALL0011_F0011.png'
    a algo legible: '100mHz-1Hz  XD_ALL0011'."""
    s = os.path.splitext(nombre)[0]
    s = re.sub(r'^(osciloscopio|preprocesamiento|normalizado|identificacion)_', '', s)
    m = re.search(r'([0-9]+(?:m?Hz))to([0-9]+(?:k?m?Hz))', s)
    banda = f"{m.group(1)}-{m.group(2)}" if m else ""
    m2 = re.search(r'((?:XD_)?ALL[0-9]+)', s)
    cap = m2.group(1) if m2 else s[:26]
    return (banda + "  " + cap).strip()


archivos = sorted(f for f in os.listdir(DIR_IN) if f.lower().endswith(".png"))
if not archivos:
    raise SystemExit(f"sin PNG en {DIR_IN}")

# Relacion de aspecto tomada de la primera imagen, para no deformar
with Image.open(os.path.join(DIR_IN, archivos[0])) as im0:
    aspecto = im0.height / im0.width
CELDA_H = int(CELDA_W * aspecto)

filas = (len(archivos) + COLS - 1) // COLS
ALTO_TIT = 78
W = COLS * (CELDA_W + MARGEN) + MARGEN
H = ALTO_TIT + filas * (CELDA_H + ALTO_ROTULO + MARGEN) + MARGEN

lienzo = Image.new("RGB", (W, H), FONDO)
dib = ImageDraw.Draw(lienzo)
dib.text((MARGEN + 4, 14), TITULO, font=F_TIT, fill=TINTA)
dib.text((MARGEN + 4, 52), f"{len(archivos)} figuras — {DIR_IN.replace(os.sep, '/')}",
         font=F_SUB, fill=TENUE)

for i, nombre in enumerate(archivos):
    fila, col = divmod(i, COLS)
    x = MARGEN + col * (CELDA_W + MARGEN)
    y = ALTO_TIT + fila * (CELDA_H + ALTO_ROTULO + MARGEN)
    with Image.open(os.path.join(DIR_IN, nombre)) as im:
        im = im.convert("RGB").resize((CELDA_W, CELDA_H), Image.LANCZOS)
        lienzo.paste(im, (x, y))
    dib.rectangle([x, y, x + CELDA_W - 1, y + CELDA_H - 1], outline=(200, 200, 200))
    dib.text((x + 3, y + CELDA_H + 7), etiqueta(nombre), font=F_ROT, fill=TENUE)

# Un mosaico de 65 celdas a 460 px de ancho es enorme; se reduce a un ancho
# manejable para LaTeX conservando legibilidad de las curvas.
MAX_W = 2600
if lienzo.width > MAX_W:
    escala = MAX_W / lienzo.width
    lienzo = lienzo.resize((MAX_W, int(lienzo.height * escala)), Image.LANCZOS)

os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
lienzo.save(OUT, optimize=True)
print(f"escrito {OUT}  ({len(archivos)} figuras, {filas}x{COLS}, {lienzo.width}x{lienzo.height})")
