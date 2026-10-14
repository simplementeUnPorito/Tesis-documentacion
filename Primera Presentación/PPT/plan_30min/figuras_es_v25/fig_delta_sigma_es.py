#!/usr/bin/env python3
"""Figura propia ilustrativa (slide larga 76): sobremuestreo y conformación del ruido delta-sigma.

Modelo genérico: ruido de cuantización blanco, función de transferencia del ruido de un
modulador de 2.º orden |NTF| = (2 sen(pi f/fs))^2 y filtro de diezmado sinc^3 con M = 64.
NO son los parámetros del ADC del PSoC: es un ejemplo para explicar el principio.
Uso: python fig_delta_sigma_es.py salida.png
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NAVY, BLUE, ALERT, LIGHT, GRAY = "#1F4E79", "#2E75B6", "#C55A11", "#EAF1F8", "#6B6B6B"
plt.rcParams["font.family"] = "Arial"
M = 64
f = np.logspace(-4, np.log10(0.5), 2000)          # frecuencia normalizada a fs
ntf = (2 * np.sin(np.pi * f)) ** 2
sinc3 = np.abs(np.sin(np.pi * f * M) / (M * np.sin(np.pi * f))) ** 3
db = lambda x: 20 * np.log10(np.maximum(x, 1e-12))

fig = plt.figure(figsize=(7.1, 2.99), dpi=250)
ax = fig.add_axes([0.09, 0.2, 0.89, 0.66])
fb = 1 / (2 * M)
ax.axvspan(1e-4, fb, color=LIGHT, zorder=0)
ax.text(np.sqrt(1e-4 * fb), -8, "banda de interés", ha="center", va="top", fontsize=10, color=NAVY)
ax.plot(f, np.zeros_like(f), "--", color=GRAY, lw=1.6, label="ruido de cuantización sin conformar")
ax.plot(f, db(ntf), color=ALERT, lw=2.2, label="ruido conformado por el ΔΣ")
ax.plot(f, db(sinc3), color=NAVY, lw=2.2, label="filtro digital (sinc³)")
ax.set_xscale("log"); ax.set_xlim(1e-4, 0.5); ax.set_ylim(-120, 25)
ax.set_xlabel("Frecuencia / frecuencia de muestreo", fontsize=11)
ax.set_ylabel("Nivel relativo (dB)", fontsize=11)
ax.tick_params(labelsize=9.5)
ax.grid(True, which="major", color="#E0E0E0", lw=0.6)
ax.annotate("el ruido sube fuera de la banda\ny el filtro lo descarta", xy=(0.12, -12), xytext=(1.3e-4, -62),
            fontsize=10, color=ALERT, arrowprops=dict(arrowstyle="->", color=ALERT, lw=1.2))
fig.legend(*ax.get_legend_handles_labels(), loc="upper center", ncol=3, fontsize=9, frameon=False, bbox_to_anchor=(0.53, 1.0))
fig.savefig(sys.argv[1] if len(sys.argv) > 1 else "g7_delta_sigma_propia.png", facecolor="white")
print("ok")
