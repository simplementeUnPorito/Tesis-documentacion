# -*- coding: utf-8 -*-
"""
Contenido espectral real del canal de geofono en campo, y SNR por banda.

Esta es la pregunta que el proyecto entero intenta responder y que nunca se
habia contestado con los datos propios: DE QUE FRECUENCIAS DISPONE REALMENTE la
senal registrada. Toda la cadena analogica existe para recuperar el extremo
bajo; conviene ver cuanto se recupero.

Metodo, por golpe:
  - ventana de SENAL: desde el trigger del martillo hasta trigger + T_SENAL
  - ventana de RUIDO: la porcion previa al trigger (el registro arranca antes)
  - espectro de potencia de ambas, promediado por distancia
  - SNR(f) = 10*log10(P_senal / P_ruido)

Salida: figuras/contenido_baja_frecuencia.png
"""
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DIR, OUT = sys.argv[1], sys.argv[2]

T_SENAL = 1.0      # s de ventana de senal tras el arribo
T_RUIDO = 1.0      # s de ventana de ruido previa al trigger
TINTA, TENUE, GRILLA = "#1b1b1b", "#6e6e6e", "#e6e6e6"


def espectro(x, fs, nfft=4096):
    if len(x) < 64:
        return None, None
    x = np.asarray(x, float)
    x = x - x.mean()
    n = min(len(x), nfft)
    w = np.hanning(n)
    X = np.fft.rfft(x[:n] * w, n=nfft)
    f = np.fft.rfftfreq(nfft, 1.0 / fs)
    return f, (np.abs(X) ** 2) / (np.sum(w ** 2) * fs)


acc = {}     # distancia -> listas de espectros
for sub in sorted(os.listdir(DIR)):
    d = os.path.join(DIR, sub)
    if not os.path.isdir(d):
        continue
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".npz"):
            continue
        try:
            z = np.load(os.path.join(d, fn), allow_pickle=True)
            fs = float(z["fs"])
            dist = float(z["distance_m"])
            t = np.asarray(z["time_s"], float)
            g = np.asarray(z["geo_v"], float)
            i0 = int(z["trigger_index"])
        except Exception:
            continue
        n_sig = int(T_SENAL * fs)
        n_noi = int(T_RUIDO * fs)
        if i0 < n_noi + 8 or i0 + n_sig > len(g):
            continue
        f1, P1 = espectro(g[i0:i0 + n_sig], fs)
        f0, P0 = espectro(g[i0 - n_noi:i0], fs)
        if P1 is None or P0 is None:
            continue
        acc.setdefault(dist, {"f": f1, "S": [], "N": [], "fs": fs})
        if len(acc[dist]["f"]) == len(f1):
            acc[dist]["S"].append(P1)
            acc[dist]["N"].append(P0)

dists = sorted(k for k, v in acc.items() if len(v["S"]) >= 3)
if not dists:
    raise SystemExit("sin datos suficientes")


def estilo(ax):
    ax.grid(True, which="both", color=GRILLA, linewidth=0.7)
    ax.set_axisbelow(True)
    for l in ("top", "right"):
        ax.spines[l].set_visible(False)
    for l in ("left", "bottom"):
        ax.spines[l].set_color("#c9c9c9")
    ax.tick_params(colors=TENUE, labelsize=8.5)


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5.75, 4.47), dpi=300,
                               gridspec_kw={"hspace": 0.28})

# Rampa secuencial: la distancia es una variable ordenada, no categorica.
cmap = plt.get_cmap("viridis")
BANDAS = [(1, 5), (5, 10), (10, 20), (20, 50)]
tabla = []

for k, dd in enumerate(dists):
    v = acc[dd]
    f = v["f"]
    S = np.median(np.array(v["S"]), axis=0)
    N = np.median(np.array(v["N"]), axis=0)
    col = cmap(k / max(1, len(dists) - 1))
    m = (f >= 0.5) & (f <= 60)
    ax1.semilogx(f[m], 10 * np.log10(S[m] + 1e-30), color=col, lw=1.2, alpha=0.85)
    snr = 10 * np.log10((S + 1e-30) / (N + 1e-30))
    ax2.semilogx(f[m], snr[m], color=col, lw=1.2, alpha=0.85)
    fila = {"d": dd, "n": len(v["S"])}
    for a, b in BANDAS:
        bb = (f >= a) & (f < b)
        fila[f"{a}-{b}"] = float(np.median(snr[bb])) if bb.any() else np.nan
    tabla.append(fila)

estilo(ax1)
ax1.set_ylabel("Densidad espectral de la señal [dB]", fontsize=9, color=TINTA)
ax1.set_xlim(0.5, 60)
if False: ax1.set_title("Contenido espectral real del canal de geófono en campo "
              f"({sum(len(acc[d]['S']) for d in dists)} golpes, "
              f"{len(dists)} distancias)",
              fontsize=10.5, color=TINTA, loc="left", pad=10)
ax1.axvspan(1, 2.5, color="#c1543a", alpha=0.12, zorder=0)
ax1.text(1.05, ax1.get_ylim()[1] - 3,
         "banda objetivo del proyecto\n(50 m de profundidad)",
         fontsize=7.6, color="#c1543a", va="top")
ax1.axvline(10, color="#999999", lw=1.0, ls=(0, (4, 3)))
ax1.text(10.4, ax1.get_ylim()[0] + 4, "$f_n$ del SM-24", fontsize=7.5, color=TENUE)

estilo(ax2)
ax2.axhline(0, color="#b8b8b8", lw=1.2)
ax2.axhline(10, color="#b8b8b8", lw=0.9, ls=(0, (4, 3)))
ax2.text(0.53, 10.6, "SNR = 10 dB", fontsize=7.4, color=TENUE)
ax2.set_ylabel("SNR señal/ruido previo [dB]", fontsize=9, color=TINTA)
ax2.set_xlabel("Frecuencia [Hz]", fontsize=9, color=TINTA)
ax2.set_xlim(0.5, 60)
ax2.axvspan(1, 2.5, color="#c1543a", alpha=0.12, zorder=0)
ax2.axvline(10, color="#999999", lw=1.0, ls=(0, (4, 3)))

sm = plt.cm.ScalarMappable(cmap=cmap,
                           norm=plt.Normalize(min(dists), max(dists)))
cb = fig.colorbar(sm, ax=[ax1, ax2], pad=0.015, fraction=0.03)
cb.set_label("Distancia fuente–receptor [m]", fontsize=8.5, color=TINTA)
cb.ax.tick_params(colors=TENUE, labelsize=8)

fig.savefig(OUT, bbox_inches="tight", facecolor="white")

print("escrito", OUT)
print(f"  {sum(len(acc[d]['S']) for d in dists)} golpes, {len(dists)} distancias")
print("\n  SNR mediana [dB] por banda y distancia:")
print("   dist    n  " + "  ".join(f"{a}-{b}Hz".rjust(9) for a, b in BANDAS))
for r in tabla:
    print(f"   {r['d']:5.0f} {r['n']:4d}  " +
          "  ".join(f"{r[f'{a}-{b}']:9.1f}" for a, b in BANDAS))
print("\n  Resumen por banda (mediana sobre distancias):")
for a, b in BANDAS:
    v = np.array([r[f"{a}-{b}"] for r in tabla], float)
    print(f"   {a:2d}-{b:2d} Hz: mediana {np.nanmedian(v):6.1f} dB   "
          f"distancias con SNR>10 dB: "
          f"{int(np.nansum(v > 10))}/{len(v)}")
