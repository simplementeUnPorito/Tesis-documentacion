#!/usr/bin/env python3
"""Esquema propio del acondicionamiento ICP del martillo (slide larga 94).

Datos: documento de tesis, latex-15p-review/secciones/03_excitacion.tex (086D20: 20-30 V,
2-20 mA de corriente constante, polarizacion de 8-14 V; elevador 5 V -> 21 V, LM7805 con
1 kOhm ~ 5 mA, capacitor de 47 uF). Uso: python fig_icp_es.py salida.png
"""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

NAVY, BLUE, ALERT, LIGHT, GRAY = "#1F4E79", "#2E75B6", "#C55A11", "#EAF1F8", "#6B6B6B"
plt.rcParams["font.family"] = "Arial"

fig = plt.figure(figsize=(4.4, 3.73), dpi=300)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 4.4); ax.set_ylim(0, 3.73); ax.axis("off")

def box(x, y, w, h, text, fc, ec, color="black", bold=False, fs=10):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec=ec, lw=1.4))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=color,
            fontweight="bold" if bold else "normal", linespacing=1.15)

def arrow(x0, y0, x1, y1, color=NAVY):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6))

# fila superior: sensor y fuente de corriente
box(0.05, 2.55, 1.9, 1.05, "Martillo 086D20\ncuarzo ICP\n0,23 mV/N", "white", NAVY, NAVY, True)
box(2.45, 2.55, 1.9, 1.05, "Fuente de corriente\nLM7805 + 1 kΩ\n≈ 5 mA desde 21 V", LIGHT, BLUE, NAVY)
arrow(2.45, 3.07, 1.95, 3.07, BLUE)

# salida con polarización y desacople
arrow(1.0, 2.55, 1.0, 2.05)
ax.text(1.08, 2.30, "polarización 8–14 V + señal", ha="left", va="center", fontsize=8, color=GRAY)
box(0.05, 1.3, 1.9, 0.75, "Capacitor 47 µF\nbloquea la continua", "#FBE5D6", ALERT, ALERT, True)

# cadena de adquisición
arrow(1.95, 1.67, 2.45, 1.67)
box(2.45, 1.3, 1.9, 0.75, "Señal alterna", LIGHT, BLUE, NAVY)
arrow(3.4, 1.3, 3.4, 0.85)
box(0.05, 0.05, 4.3, 0.8, "PGA → pasa-bajos → ADC ΔΣ (PSoC)", NAVY, NAVY, "white", True, 11)

fig.savefig(sys.argv[1] if len(sys.argv) > 1 else "g8_icp_es.png", facecolor="white")
print("ok")
