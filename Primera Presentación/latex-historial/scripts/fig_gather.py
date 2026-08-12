# -*- coding: utf-8 -*-
"""
Construye, DESDE LOS BINARIOS CRUDOS de campo, el gather sintetizado de la
campana Canchita: una traza por posicion de receptor, alineadas por el pico
del canal de martillo de cada disparo.

Es exactamente la operacion que hace posible el MASW con dos nodos: el arreglo
multicanal no existe fisicamente, se ensambla a partir de disparos repetidos.

Entrada: data/raw/Canchita/muestra*/metadata.json + raw_f32le.bin
Salida:  figuras/gather_sintetizado.png
"""
import json
import os
import glob
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SITIO = sys.argv[1]
OUT = sys.argv[2]
FS_OBJ = 1020.0          # solo la tanda de 1020 Hz, para no mezclar tasas
VENTANA_S = 0.55         # ventana util despues del impacto
PRE_S = 0.05

TINTA, TENUE, GRILLA = "#1b1b1b", "#6e6e6e", "#ececec"
C_TRAZA = "#1f5fa9"
C_REL = "#c1543a"


def leer(base, rel, n):
    p = os.path.join(base, rel.replace("/", os.sep))
    if not os.path.isfile(p):
        return None
    a = np.fromfile(p, dtype="<f4")
    return a[:n] if n and a.size >= n else a


mejor = {}   # position_m -> (geo, hammer, fs)
for d in sorted(glob.glob(os.path.join(SITIO, "muestra*"))):
    mp = os.path.join(d, "metadata.json")
    if not os.path.isfile(mp) or not os.path.isdir(d):
        continue
    try:
        m = json.load(open(mp, encoding="utf-8"))
    except Exception:
        continue
    for c in m.get("captures", []):
        nodos = {str(n.get("role", "")).lower(): n for n in c.get("nodes", [])}
        g, h = nodos.get("geo"), nodos.get("hammer")
        if not g or not h or not g.get("raw_file") or not h.get("raw_file"):
            continue
        if float(g.get("fs") or 0) != FS_OBJ:
            continue
        pos = g.get("position_m")
        if pos is None or pos in mejor:
            continue
        vg = leer(d, g["raw_file"], g.get("raw_count"))
        vh = leer(d, h["raw_file"], h.get("raw_count"))
        if vg is None or vh is None or vg.size < 1000:
            continue
        mejor[float(pos)] = (vg, vh)
        break

if not mejor:
    raise SystemExit("no se armo ningun gather")

pos = sorted(mejor)
npre, nven = int(PRE_S * FS_OBJ), int(VENTANA_S * FS_OBJ)
t = (np.arange(-npre, nven) / FS_OBJ) * 1000.0   # ms

fig, (ax, axs) = plt.subplots(
    1, 2, figsize=(10.6, 6.0), dpi=200,
    gridspec_kw={"width_ratios": [2.35, 1.0], "wspace": 0.24})
esc = 1.55   # separacion en metros entre trazas vecinas (dx = 2 m)

snr = []
for p in pos:
    vg, vh = mejor[p]
    t0 = int(np.argmax(np.abs(vh - np.median(vh))))   # instante del impacto
    a, b = t0 - npre, t0 + nven
    if a < 0 or b > vg.size:
        continue
    tr = vg[a:b].astype(float)
    tr -= np.median(tr)
    m = np.max(np.abs(tr))
    if m <= 0:
        continue
    # SNR: RMS en la ventana de senal contra RMS del ruido pre-impacto
    #      (los npre puntos anteriores a t=0 del mismo registro)
    ruido = tr[:npre]
    senal = tr[npre:]
    if ruido.size > 8 and np.std(ruido) > 0:
        snr.append((p, 20 * np.log10(np.std(senal) / np.std(ruido))))
    tr = tr / m * esc
    ax.plot(t, p + tr, color=C_TRAZA, lw=0.75, zorder=3)
    ax.fill_between(t, p, p + tr, where=(tr > 0), color=C_TRAZA,
                    alpha=0.30, lw=0, zorder=2)

ax.axvline(0, color=TENUE, lw=1.0, ls=(0, (4, 3)), zorder=1)
ax.text(2, max(pos) + 3.0, "impacto ($t=0$, pico del canal de martillo)",
        fontsize=7.5, color=TENUE)

ax.set_xlabel("Tiempo desde el impacto [ms]", fontsize=9, color=TINTA)
ax.set_ylabel("Distancia a la fuente [m]", fontsize=9, color=TINTA)
ax.set_xlim(t.min(), t.max())
ax.set_ylim(min(pos) - 4, max(pos) + 6)
ax.set_title(
    f"Gather sintetizado desde los binarios crudos  ·  {len(pos)} posiciones  ·  "
    f"$F_s$ = {FS_OBJ:.0f} Hz",
    fontsize=10, color=TINTA, loc="left", pad=10)

# ---- Panel derecho: relacion senal/ruido por distancia
if snr:
    dd = np.array([p for p, _ in snr])
    ss = np.array([s for _, s in snr])
    axs.plot(ss, dd, "o-", color=C_TRAZA, lw=1.6, ms=4.5, mec="white", mew=0.8)
    axs.axvline(0, color=C_REL, lw=1.2, ls=(0, (4, 3)))
    axs.text(0.6, min(dd) - 2.4, "0 dB", fontsize=7.5, color=C_REL)
    axs.set_ylim(min(pos) - 4, max(pos) + 6)
    axs.set_xlabel("SNR aparente [dB]", fontsize=9, color=TINTA)
    axs.set_title("Senal contra ruido pre-impacto",
                  fontsize=10, color=TINTA, loc="left", pad=10)

for a_ in (ax, axs):
    a_.grid(True, color=GRILLA, linewidth=0.7)
    a_.set_axisbelow(True)
    for lado in ("top", "right"):
        a_.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        a_.spines[lado].set_color("#c9c9c9")
    a_.tick_params(colors=TENUE, labelsize=8.5)

fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight", facecolor="white")
print("escrito", OUT, "| posiciones:", [int(p) for p in pos])
if snr:
    dd = np.array([p for p, _ in snr]); ss = np.array([s for _, s in snr])
    cerca, lejos = ss[dd <= 26], ss[dd >= 30]
    print(f"  SNR 10-26 m: mediana {np.median(cerca):.1f} dB "
          f"({cerca.min():.1f} a {cerca.max():.1f})")
    print(f"  SNR 30-50 m: mediana {np.median(lejos):.1f} dB "
          f"({lejos.min():.1f} a {lejos.max():.1f})")
