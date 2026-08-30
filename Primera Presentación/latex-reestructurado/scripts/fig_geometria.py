# -*- coding: utf-8 -*-
"""
Geometria real de adquisicion, reconstruida desde los metadata.json de campo.

Hallazgo: cada captura tiene UN solo geofono mas el martillo. El arreglo
multicanal no existe fisicamente: se SINTETIZA repitiendo el disparo en el
mismo origen y moviendo el receptor. La figura muestra que posiciones se
ocuparon efectivamente en cada sitio y cuantas capturas hay en cada una.

Salida: figuras/geometria_campanas.png
"""
import json
import os
import glob
import sys
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAW = sys.argv[1]
OUT = sys.argv[2]

SITIOS = [("Canchiga", "Canchiga"),
          ("Canchita", "Canchita"),
          ("Canchita_2", "Canchita 2")]

C_GEO = "#1f5fa9"
C_FTE = "#c1543a"
TINTA, TENUE = "#1b1b1b", "#6e6e6e"

datos = {}
for carpeta, label in SITIOS:
    cnt = Counter()
    fs = set()
    for p in glob.glob(os.path.join(RAW, carpeta, "*", "metadata.json")):
        try:
            m = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if m.get("fs"):
            fs.add(m["fs"])
        for c in m.get("captures", []):
            for nd in c.get("nodes", []):
                if str(nd.get("role", "")).lower() == "geo" \
                        and nd.get("position_m") is not None:
                    cnt[float(nd["position_m"])] += 1
            break
    datos[label] = (cnt, sorted(fs))

n = len(datos)
fig, ax = plt.subplots(figsize=(9.6, 0.95 * n + 1.9), dpi=300)

vmax = max((max(c.values()) if c else 1) for c, _ in datos.values())

for i, (label, (cnt, fs)) in enumerate(datos.items()):
    y = n - 1 - i
    if not cnt:
        continue
    pos = sorted(cnt)
    ax.plot([0, max(pos)], [y, y], color="#dcdcdc", lw=1.4, zorder=1,
            solid_capstyle="round")
    # Fuente en el origen
    ax.plot([0], [y], marker="*", ms=15, color=C_FTE, zorder=4,
            mec="white", mew=0.8)
    tam = [26 + 90 * (cnt[p] / vmax) for p in pos]
    ax.scatter(pos, [y] * len(pos), s=tam, color=C_GEO, zorder=3,
               edgecolor="white", linewidth=0.9)
    dx = min(b - a for a, b in zip(pos, pos[1:])) if len(pos) > 1 else 0
    ax.text(max(pos) + 2.0, y,
            f"{len(pos)} posiciones  ·  $\\Delta x$ = {dx:.0f} m  ·  "
            f"{min(pos):.0f}–{max(pos):.0f} m  ·  {sum(cnt.values())} capturas",
            fontsize=8, color=TENUE, va="center")
    ax.text(-2.5, y, label, fontsize=9.5, color=TINTA, ha="right", va="center")

ax.set_xlim(-3, 96)
ax.set_ylim(-0.8, n - 0.2)
ax.set_yticks([])
ax.set_xticks([0, 10, 20, 30, 40, 50])
ax.set_xlabel("Distancia a la fuente [m]", fontsize=9, color=TINTA)
ax.tick_params(colors=TENUE, labelsize=8.5, length=0)
for lado in ("top", "right", "left"):
    ax.spines[lado].set_visible(False)
ax.spines["bottom"].set_color("#c9c9c9")
ax.grid(axis="x", color="#eeeeee", linewidth=0.8)
ax.set_axisbelow(True)

ax.plot([], [], marker="*", ls="", ms=11, color=C_FTE, label="Fuente (martillo, 0 m)")
ax.scatter([], [], s=60, color=C_GEO, label="Posicion de geofono ocupada\n(area $\\propto$ capturas)")
ax.legend(frameon=False, fontsize=8, loc="lower right", labelcolor=TINTA,
          handletextpad=0.8, borderaxespad=0.2)
ax.set_title("Geometria real de las campanas — arreglo sintetizado moviendo un unico receptor",
             fontsize=10.5, color=TINTA, loc="left", pad=12)

fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight", facecolor="white")

print("escrito", OUT)
for label, (cnt, fs) in datos.items():
    if cnt:
        pos = sorted(cnt)
        print(f"  {label}: {len(pos)} pos {min(pos):.0f}-{max(pos):.0f} m, "
              f"{sum(cnt.values())} capturas, fs={fs}")
