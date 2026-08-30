# -*- coding: utf-8 -*-
"""
Las dos inversiones del mismo sitio, una al lado de la otra, contra el SEV 01.

El proyecto conserva DOS estados de inversion de Canchita:
  (a) el exportado de julio (masw_perfil_vs.csv): 51 puntos, 9 capas hasta 82,6 m,
      desajuste 2,554 %, con longitudes de onda de hasta 130,6 m
  (b) el estado persistido posterior (field_review_masw_state.npz): 112 puntos,
      8 capas hasta 9,7 m, desajuste 7,11 %, con lambda maxima de 20,7 m

Compararlos no es un ejercicio academico: muestra que el analisis se volvio mas
disciplinado con el tiempo (el segundo respeta la apertura y acepta peor ajuste),
y deja ver de un vistazo cuanta profundidad esta realmente sostenida por los datos.

Salida: figuras/dos_inversiones.png
"""
import csv
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV_JUL, NPZ_ACT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

C_JUL = "#8a8a8a"    # julio: gris, es el historico
C_ACT = "#1f5fa9"    # actual: azul
C_SEV = "#c1543a"
C_AGUA = "#7fa8c9"
TINTA, TENUE, GRILLA = "#1b1b1b", "#6e6e6e", "#e6e6e6"

SEV = [(1186, 1.00), (15, 2.06), (105, 4.15), (24.2, 24.0), (126, 71.8)]
FREATICO = (10.0, 30.0)
APERTURA = 40.0
Z_MAX = 30.0

# ---- julio
zt_j, zb_j, vs_j = [], [], []
with open(CSV_JUL, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        zt_j.append(float(r["z_techo_m"]))
        zb_j.append(float(r["z_piso_m"]) if r["z_piso_m"] else np.nan)
        vs_j.append(float(r["vs_m_s"]))
        mis_j = float(r["misfit_pct"])
zb_j[-1] = Z_MAX

# ---- actual
z = np.load(NPZ_ACT, allow_pickle=True)
h, beta = z["inv_h"], z["inv_beta"]
frq, c_obs, c_t, lam = z["inv_freqs"], z["inv_c_obs"], z["inv_c_t"], z["inv_wavelengths"]
top = np.concatenate([[0.0], np.cumsum(h)])
zt_a = list(top)
zb_a = list(top[1:]) + [Z_MAX]
vs_a = list(beta)
mis_a = 100 * np.mean(np.abs(c_obs - c_t) / c_obs)

# Vs30
def vs30(zt, zb, vs):
    acc, rem = 0.0, 30.0
    for a, b, v in zip(zt, zb, vs):
        hh = min((b - a) if np.isfinite(b) else rem, rem)
        if hh <= 0:
            break
        acc += hh / v
        rem -= hh
        if rem <= 0:
            break
    if rem > 0:
        acc += rem / vs[-1]
    return 30.0 / acc


def escalones(zt, zb, vs):
    x, y = [], []
    for a, b, v in zip(zt, zb, vs):
        x += [v, v]
        y += [a, b]
    return np.array(x), np.array(y)


def estilo(ax):
    ax.grid(True, color=GRILLA, linewidth=0.7)
    ax.set_axisbelow(True)
    for l in ("top", "right"):
        ax.spines[l].set_visible(False)
    for l in ("left", "bottom"):
        ax.spines[l].set_color("#c9c9c9")
    ax.tick_params(colors=TENUE, labelsize=8.5)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 6.4), dpi=300,
                               gridspec_kw={"width_ratios": [1.0, 1.2],
                                            "wspace": 0.26})

# ------------------------------------------------------------------ perfiles
xj, yj = escalones(zt_j, zb_j, vs_j)
xa, ya = escalones(zt_a, zb_a, vs_a)
ax1.axhspan(*FREATICO, color=C_AGUA, alpha=0.18, zorder=0)
ax1.plot(xj, yj, color=C_JUL, lw=2.0, ls=(0, (5, 3)), zorder=3,
         label=f"julio: 9 capas, desajuste {mis_j:.2f} %")
ax1.plot(xa, ya, color=C_ACT, lw=2.4, zorder=4,
         label=f"actual: 8 capas, desajuste {mis_a:.2f} %")
for _, base in SEV:
    if base <= Z_MAX:
        ax1.axhline(base, color=C_SEV, lw=1.0, ls=(0, (4, 3)), zorder=2)
ax1.text(700, 24.4, "SEV 24 m", fontsize=7.2, color=C_SEV, ha="right", va="bottom")

# Profundidad sostenida por los datos de cada inversion
for lm, col, dy in ((lam.max(), C_ACT, 0.0),):
    ax1.axhspan(lm / 3, lm / 2, color=col, alpha=0.10, zorder=1)
    ax1.text(700, lm / 2 + 0.4,
             f"prof. sostenida por $\\lambda_{{max}}$ = {lm:.1f} m",
             fontsize=7.2, color=col, ha="right", va="top")

estilo(ax1)
ax1.set_ylim(Z_MAX, 0)
ax1.set_xlim(0, 720)
ax1.set_xlabel("$V_S$ [m/s]", fontsize=9, color=TINTA)
ax1.set_ylabel("Profundidad [m]", fontsize=9, color=TINTA)
ax1.set_title("Las dos inversiones del mismo sitio", fontsize=10, color=TINTA,
              loc="left", pad=9)
ax1.legend(frameon=False, fontsize=8, loc="lower right", labelcolor=TINTA)

# ------------------------------------------------------------------ curva
o = np.argsort(frq)
ax2.plot(frq[o], c_obs[o], "o", color=C_ACT, ms=3.4, label="observada", zorder=3)
ax2.plot(frq[o], c_t[o], "-", color="#3f7d4e", lw=1.8, label="teórica del modelo",
         zorder=2)
ax2.axvspan(ax2.get_xlim()[0], 10, color="#c1543a", alpha=0.10, zorder=0)
estilo(ax2)
ax2.set_xlabel("Frecuencia [Hz]", fontsize=9, color=TINTA)
ax2.set_ylabel("Velocidad de fase [m/s]", fontsize=9, color=TINTA)
ax2.set_title(f"Curva del estado actual: {len(frq)} puntos, "
              f"$\\lambda$ = {lam.min():.1f}–{lam.max():.1f} m",
              fontsize=10, color=TINTA, loc="left", pad=9)
ax2.legend(frameon=False, fontsize=8, labelcolor=TINTA)
n_bajo = int((frq < 10).sum())
ax2.text(0.02, 0.05,
         f"{n_bajo} de {len(frq)} puntos ({100*n_bajo/len(frq):.0f} %) están por debajo\n"
         "de 10 Hz, donde la SNR medida es de 0–2 dB",
         transform=ax2.transAxes, fontsize=7.4, color="#c1543a", va="bottom")

fig.text(0.012, 0.005,
         f"Ninguno de los {len(frq)} puntos del estado actual supera $\\lambda$ = "
         f"{APERTURA:g} m (la apertura), frente a 3 que sí lo hacían en el export de julio.",
         fontsize=7.4, color=TENUE, ha="left")

os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
fig.savefig(OUT, bbox_inches="tight", facecolor="white")

print("escrito", OUT)
print(f"  julio : {len(vs_j)} capas, desajuste {mis_j:.3f} %, "
      f"Vs30 = {vs30(zt_j, zb_j, vs_j):.1f} m/s")
print(f"  actual: {len(vs_a)} capas hasta {top[-1]:.2f} m, desajuste {mis_a:.2f} %, "
      f"Vs30 = {vs30(zt_a, zb_a, vs_a):.1f} m/s")
print(f"  actual: lambda {lam.min():.2f}–{lam.max():.2f} m, "
      f"{int((lam > APERTURA).sum())} puntos por encima de la apertura")
print(f"  actual: {n_bajo} de {len(frq)} puntos por debajo de 10 Hz")
