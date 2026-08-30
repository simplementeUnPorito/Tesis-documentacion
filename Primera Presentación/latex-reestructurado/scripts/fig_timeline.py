# -*- coding: utf-8 -*-
"""
Figura de panorama: actividad de commits por repositorio a lo largo del proyecto.

Diez repositorios son demasiadas categorias para codificar por color (el limite
practico son ~8 y la separacion perceptual se rompe antes). Se usa small
multiples: una fila por repositorio, misma escala temporal, magnitud en una sola
rampa. Asi la identidad la lleva la etiqueta de fila, no el color.

Entrada:  commits.csv  (repo,date,subject)
Salida:   figuras/timeline_commits.png
"""
import csv
import sys
import datetime as dt
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

CSV = sys.argv[1]
OUT = sys.argv[2]

# Orden fijo y con sentido: firmware, luego interfaces, luego calculo, luego soporte.
ORDEN = [
    ("psoc",              "Firmware PSoC 5LP"),
    ("esp32",             "Firmware ESP32"),
    ("py-interfaces",     "Interfaz Python (servidor/web)"),
    ("matlab-interfaces", "Interfaz MATLAB"),
    ("matlab-calculos",   "Modelado MATLAB"),
    ("py-calculos",       "Modelado Python"),
    ("docs",              "Documentacion e investigacion"),
    ("data",              "Datos de campo"),
    ("pcbs",              "PCBs"),
    ("super",             "Superproyecto"),
]

por_repo = defaultdict(lambda: defaultdict(int))
fechas = []
with open(CSV, newline="", encoding="utf-8", errors="replace") as fh:
    for row in csv.reader(fh):
        if len(row) < 3 or row[0] == "repo":
            continue
        repo, fecha = row[0].strip(), row[1].strip()
        try:
            d = dt.date.fromisoformat(fecha)
        except ValueError:
            continue
        # Anclar cada commit al lunes de su semana
        semana = d - dt.timedelta(days=d.weekday())
        por_repo[repo][semana] += 1
        fechas.append(semana)

if not fechas:
    raise SystemExit("sin datos")

ini, fin = min(fechas), max(fechas)
semanas = []
s = ini
while s <= fin:
    semanas.append(s)
    s += dt.timedelta(days=7)
idx = {w: i for i, w in enumerate(semanas)}

filas = [(k, lab) for k, lab in ORDEN if k in por_repo]
n = len(filas)

# Una sola rampa secuencial para magnitud (azul), fondo claro para el cero.
RAMPA = plt.get_cmap("Blues")
TINTA = "#1b1b1b"
TENUE = "#7a7a7a"

fig, ax = plt.subplots(figsize=(11.0, 0.42 * n + 1.9), dpi=300)

vmax = max(max(v.values()) for v in por_repo.values())

for r, (key, lab) in enumerate(filas):
    y = n - 1 - r
    for w, c in por_repo[key].items():
        if w not in idx:
            continue
        # Escala comprimida: la sesion de ~80 commits no puede aplastar al resto.
        t = np.sqrt(c / vmax)
        ax.add_patch(plt.Rectangle(
            (idx[w] + 0.12, y + 0.14), 0.76, 0.72,
            facecolor=RAMPA(0.18 + 0.78 * t), edgecolor="white", linewidth=0.6))

ax.set_xlim(-0.5, len(semanas) + 0.5)
ax.set_ylim(-0.3, n)
ax.set_yticks([n - 1 - r + 0.5 for r in range(n)])
ax.set_yticklabels([lab for _, lab in filas], fontsize=8.5, color=TINTA)

# Eje temporal: marca al primer lunes de cada mes
ticks, labels = [], []
MES = ["ene", "feb", "mar", "abr", "may", "jun",
       "jul", "ago", "sep", "oct", "nov", "dic"]
visto = set()
for i, w in enumerate(semanas):
    if (w.year, w.month) not in visto:
        visto.add((w.year, w.month))
        ticks.append(i + 0.5)
        labels.append(MES[w.month - 1])
ax.set_xticks(ticks)
ax.set_xticklabels(labels, fontsize=8.5, color=TENUE)

for lado in ("top", "right", "left", "bottom"):
    ax.spines[lado].set_visible(False)
ax.tick_params(length=0)
ax.grid(False)

total = sum(sum(v.values()) for v in por_repo.values())
ax.set_title(
    f"Actividad de desarrollo por repositorio  ·  {total} commits en "
    f"{len(semanas)} semanas  ·  feb--ago 2026",
    fontsize=10.5, color=TINTA, loc="left", pad=18)

# Leyenda de intensidad: arriba a la derecha, fuera del eje temporal
x0, yl = len(semanas) * 0.70, n + 0.18
for j, frac in enumerate([0.0, 0.33, 0.66, 1.0]):
    ax.add_patch(plt.Rectangle(
        (x0 + j * 1.3, yl), 1.0, 0.26,
        facecolor=RAMPA(0.18 + 0.78 * frac), edgecolor="white",
        linewidth=0.6, clip_on=False))
ax.text(x0 - 0.5, yl + 0.13, "menos", ha="right", va="center",
        fontsize=7.5, color=TENUE, clip_on=False)
ax.text(x0 + 4 * 1.3 + 0.1, yl + 0.13,
        f"mas commits/semana (max {vmax})", ha="left", va="center",
        fontsize=7.5, color=TENUE, clip_on=False)

fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight", facecolor="white")
print("escrito", OUT, "| repos:", n, "| commits:", total, "| semanas:", len(semanas))
