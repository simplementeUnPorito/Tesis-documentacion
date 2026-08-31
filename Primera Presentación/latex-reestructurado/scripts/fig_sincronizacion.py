# -*- coding: utf-8 -*-
"""Presupuesto de sincronizacion, rehecho para el criterio vigente.

La figura historica dibujaba error de FASE contra un umbral de 5 grados y una
observacion preliminar de 400 us. El requerimiento del documento es otro: un
error admisible del 5 % sobre la VELOCIDAD DE FASE, que con c = 150 m/s y
dx = 2 m da unos 670 us. Esta figura dibuja esa relacion.

    dc/c = c * dt / dx

Salida: figuras/f_presupuesto_sincronizacion.png
"""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = sys.argv[1] if len(sys.argv) > 1 else "figuras/f_presupuesto_sincronizacion.png"

DX = 2.0                      # m, separacion entre posiciones
TOL = 5.0                     # %, error admisible adoptado
C_REF = 150.0                 # m/s, velocidad de fase observada en el sitio
TINTA, TENUE, GRILLA = "#1b1b1b", "#6e6e6e", "#e6e6e6"
COLORES = {120: "#3f7d4e", 150: "#1f5fa9", 200: "#c1543a"}

dt = np.linspace(0, 1100, 600)          # us

fig, ax = plt.subplots(figsize=(6.10, 3.55), dpi=300)

for c, color in COLORES.items():
    err = 100.0 * c * (dt * 1e-6) / DX  # %
    ancho = 2.2 if c == C_REF else 1.4
    ax.plot(dt, err, color=color, lw=ancho,
            label=f"$c_R$ = {c:.0f} m/s")
    presupuesto = (TOL / 100.0) * DX / c * 1e6   # us
    if presupuesto <= dt[-1]:
        ax.plot([presupuesto], [TOL], "o", color=color, mec="white", mew=0.8,
                ms=6, zorder=4)
        ax.annotate(f"{presupuesto:.0f} µs", (presupuesto, TOL),
                    textcoords="offset points", xytext=(6, -12),
                    fontsize=8, color=color)

ax.axhline(TOL, color=TENUE, lw=1.1, ls=(0, (4, 3)))
ax.text(20, TOL + 0.25, f"error admisible {TOL:.0f} %", fontsize=8, color=TENUE)

ax.set_xlim(0, 1100)
ax.set_ylim(0, 9)
ax.set_xlabel("Desalineamiento temporal entre nodos  $\\Delta t$  [µs]", fontsize=9)
ax.set_ylabel("Error de velocidad de fase  $\\Delta c/c$  [%]", fontsize=9)
ax.grid(True, color=GRILLA, lw=0.7)
ax.set_axisbelow(True)
for lado in ("top", "right"):
    ax.spines[lado].set_visible(False)
for lado in ("left", "bottom"):
    ax.spines[lado].set_color("#c9c9c9")
ax.tick_params(colors=TENUE, labelsize=8)
ax.legend(frameon=False, fontsize=8, loc="upper left", labelcolor=TINTA)
ax.text(0.99, 0.03,
        f"$\\Delta x$ = {DX:.0f} m   ·   $\\Delta c/c = c\\,\\Delta t/\\Delta x$",
        transform=ax.transAxes, ha="right", va="bottom",
        fontsize=8, color=TENUE)

fig.tight_layout()
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
fig.savefig(OUT, bbox_inches="tight", facecolor="white")
print(f"escrito {OUT}")
for c in COLORES:
    print(f"  c={c:5.0f} m/s -> presupuesto {(TOL/100.0)*DX/c*1e6:6.0f} us")
