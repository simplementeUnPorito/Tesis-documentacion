# -*- coding: utf-8 -*-
"""Figuras del estado vigente, trazables al JSON persistido y al firmware.

Entradas:
  1. data/processed/Canchita/field_review_masw_state.json
  2. directorio de salida

Salidas:
  geometria_campanas.png     Grupos persistidos y apertura sintetica
  masw_estado_actual.png     Picks modo 0 y perfil editado vigente
  sincronizacion_fase.png    Conversion exacta entre jitter y error de fase
  arquitectura_vigente.png  Particion actual del sistema
"""
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

STATE, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
with open(STATE, encoding="utf-8") as fh:
    root = json.load(fh)
m = root["masw"]

C_BLUE = "#1f5fa9"
C_RED = "#c1543a"
C_GREEN = "#3f7d4e"
C_PURPLE = "#73538f"
INK = "#1b1b1b"
MUTED = "#6e6e6e"
GRID = "#e6e6e6"


def clean(ax):
    ax.grid(True, color=GRID, lw=0.7)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#c9c9c9")
    ax.tick_params(colors=MUTED, labelsize=8.5)


# ---------------------------------------------------------------- geometria
# El offset de 10 m proviene de los metadatos de Canchita; spacing y length
# provienen del estado persistido. La figura no infiere posiciones de nombres.
offset = 10.0
groups = []
for key, g in sorted(m["raw_groups"].items(), key=lambda kv: int(kv[0])):
    dx, length = float(g["spacing"]), float(g["length"])
    positions = np.arange(offset, offset + length + 0.5 * dx, dx)
    groups.append((key, g["name"], dx, length, positions,
                   float(m["group_weights"].get(key, 0))))

fig, ax = plt.subplots(figsize=(5.95, 3.31), dpi=300)
for i, (key, name, dx, length, positions, weight) in enumerate(groups):
    y = len(groups) - 1 - i
    color = C_BLUE if weight > 0 else MUTED
    ax.plot([0, positions[-1]], [y, y], color="#d7d7d7", lw=1.4)
    ax.plot([0], [y], marker="*", ms=15, color=C_RED, mec="white", mew=0.8)
    ax.scatter(positions, np.full_like(positions, y), s=46, color=color,
               edgecolor="white", lw=0.8, zorder=3)
    active = "activo" if weight > 0 else "peso 0"
    ax.text(positions[-1] + 1.8, y,
            f"{len(positions)} posiciones · Δx={dx:.0f} m · L={length:.0f} m · {active}",
            va="center", fontsize=6.4, color=color)
    ax.text(-2.2, y, name, ha="right", va="center", fontsize=7.6, color=INK)
ax.set_xlim(-3, max(g[4][-1] for g in groups) + 28)
ax.set_ylim(-0.65, len(groups) - 0.35)
ax.set_yticks([])
ax.set_xticks(np.arange(0, 55, 10))
ax.set_xlabel("Distancia a la fuente [m]", fontsize=7.2)
if False: ax.set_title("Geometría persistida — apertura sintética con un geófono móvil",
             loc="left", fontsize=8.4, pad=10)
ax.grid(axis="x", color=GRID, lw=0.7)
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color("#c9c9c9")
ax.tick_params(colors=MUTED, labelsize=8.5, length=0)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "geometria_campanas.png"), bbox_inches="tight",
            facecolor="white")


# ------------------------------------------------------------ MASW vigente
if "edited_profile" in m:
    picks = np.asarray(m["picks_by_mode"][str(m["active_mode"])], dtype=float)
    profile = m["edited_profile"]
    beta = np.asarray(profile["beta"], dtype=float)
    h = np.asarray(profile["h"], dtype=float)
    tops = np.r_[0.0, np.cumsum(h)]
    bottoms = np.r_[np.cumsum(h), np.sum(h) + max(3.0, 0.35 * np.sum(h))]
    zz, vv = [], []
    for zt, zb, v in zip(tops, bottoms, beta):
        zz += [zt, zb]
        vv += [v, v]

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.30, 2.70), dpi=300,
                                 gridspec_kw={"width_ratios": [1.25, 1.0]})
    a1.plot(picks[:, 0], picks[:, 1], "o", ms=3.1, color=C_BLUE,
            mec="white", mew=0.35, label="Picks persistidos, modo 0")
    a1.set_xlabel("Frecuencia [Hz]", fontsize=9)
    a1.set_ylabel("Velocidad de fase [m/s]", fontsize=9)
    a1.set_title(f"Estado actual · {len(picks)} picks · modo 0",
                 loc="left", fontsize=10, pad=9)
    a1.legend(frameon=False, fontsize=8)
    clean(a1)

    a2.step(vv, zz, where="post", lw=2.1, color=C_BLUE)
    a2.fill_betweenx(zz, 0, vv, step="post", color=C_BLUE, alpha=0.10)
    a2.invert_yaxis()
    a2.set_xlabel("$V_S$ [m/s]", fontsize=9)
    a2.set_ylabel("Profundidad [m]", fontsize=9)
    a2.set_title("Perfil editado · 7 capas + semiespacio", loc="left", fontsize=10, pad=9)
    a2.text(0.03, 0.97,
            f"motor: {m['inv_scalars']['engine']}\ndesajuste: {m['inv_scalars']['misfit']:.4f} %",
            transform=a2.transAxes, ha="left", va="top", fontsize=7.8, color=MUTED)
    clean(a2)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "masw_estado_actual.png"), bbox_inches="tight",
                facecolor="white")
else:
    print("AVISO: sin edited_profile en el JSON; se omite masw_estado_actual")


# --------------------------------------------------------------- fase/jitter
dt = np.linspace(0, 600, 500)  # us
fig, ax = plt.subplots(figsize=(6.10, 4.52), dpi=300)
for f, color in ((20, C_GREEN), (50, C_BLUE), (100, C_RED)):
    phase = 360.0 * f * dt * 1e-6
    ax.plot(dt, phase, color=color, lw=2, label=f"{f} Hz")
    budget = 5.0 / (360.0 * f) * 1e6
    ax.plot([budget], [5], "o", color=color, mec="white", mew=0.7)
    ax.text(budget + 8, 5.35, f"{budget:.0f} µs", fontsize=6.0, color=color)
ax.axhline(5, color=MUTED, lw=1, ls=(0, (4, 3)))
ax.axvline(400, color=C_PURPLE, lw=1.2, ls=(0, (4, 3)))
ax.text(405, 1.0, "observación preliminar\n<400 µs", fontsize=6.0,
        color=C_PURPLE, va="bottom")
ax.set_xlim(0, 750)
ax.set_ylim(0, 23)
ax.set_xlabel("Desfasaje temporal Δt [µs]", fontsize=7.2)
ax.set_ylabel("Error de fase Δφ [°]", fontsize=7.2)
ax.set_title("El criterio temporal depende de la frecuencia analizada",
             loc="left", fontsize=8.0, pad=9)
ax.legend(frameon=False, fontsize=6.4, ncol=3, loc="upper left")
clean(ax)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sincronizacion_fase.png"), bbox_inches="tight",
            facecolor="white")


# ------------------------------------------------------------- arquitectura
fig, ax = plt.subplots(figsize=(10.6, 4.6), dpi=300)
ax.set_xlim(0, 12)
ax.set_ylim(0, 6)
ax.axis("off")


def box(x, y, w, h, title, detail, color):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.09",
                       ec=color, fc=color + "14", lw=1.5)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h * 0.64, title, ha="center", va="center",
            fontsize=9, weight="bold", color=INK)
    ax.text(x + w / 2, y + h * 0.29, detail, ha="center", va="center",
            fontsize=7.1, color=MUTED, linespacing=1.25)


def arrow(x1, y1, x2, y2, label=""):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=12, lw=1.2, color=MUTED))
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.16, label,
                ha="center", va="bottom", fontsize=6.8, color=MUTED)


box(0.2, 3.6, 1.35, 1.2, "SM-24", "10 Hz · ζ₀=0,25", C_RED)
box(1.9, 3.35, 2.0, 1.7, "DA-AFE", "PGA → BP → SUM → LP\n4 referencias ajustables", C_RED)
box(4.25, 3.35, 1.65, 1.7, "ADC + DFB", "18 bits · 2604 SPS\nFIR / estimador DC", C_GREEN)
box(6.25, 3.35, 1.75, 1.7, "UDB + DMA", "superMaquina\nruta determinista", C_GREEN)
box(8.35, 3.35, 1.45, 1.7, "ESP32", "UART ↓ · I²C ↑\nflanco local", C_PURPLE)
box(10.15, 3.35, 1.6, 1.7, "Maestro", "ESP-NOW · AP\nSPA + WebSocket", C_PURPLE)
for a, b in ((1.55, 1.9), (3.9, 4.25), (5.9, 6.25), (8.0, 8.35), (9.8, 10.15)):
    arrow(a, 4.2, b, 4.2)

box(2.15, 0.55, 2.2, 1.35, "Calibración foreground",
    "AMUX + ADC + PI → códigos DAC\nse desactiva al adquirir", C_BLUE)
box(5.05, 0.55, 2.0, 1.35, "Memoria", "RAM ESP · RAM PSoC · SD\ncrudo preservado", C_BLUE)
box(7.75, 0.55, 1.8, 1.35, "Revisión", "FastAPI · alineación\ncontrol de calidad", C_BLUE)
box(10.1, 0.55, 1.65, 1.35, "MASW", "dispersión · backends\nresultado: modo 0", C_BLUE)
arrow(3.25, 1.9, 2.9, 3.35, "antes de medir")
arrow(7.1, 3.35, 6.15, 1.9, "lotes")
arrow(7.05, 1.22, 7.75, 1.22)
arrow(9.55, 1.22, 10.1, 1.22)
ax.text(0.2, 5.55, "Arquitectura vigente y partición de responsabilidades",
        fontsize=12, weight="bold", color=INK)
ax.text(0.2, 5.18,
        "La ruta de muestra se mantiene en hardware; radio, almacenamiento y análisis quedan fuera del instante crítico.",
        fontsize=8.2, color=MUTED)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "arquitectura_vigente.png"), bbox_inches="tight",
            facecolor="white")

print("figuras escritas en", OUT)
print("grupos:", [(g[1], len(g[4]), g[3], g[5]) for g in groups])
print("MASW:", m.get("inv_scalars"))
