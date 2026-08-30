# -*- coding: utf-8 -*-
"""
Resultado MASW de la campana Canchita: curva de dispersion observada contra la
teorica del modelo invertido, y perfil Vs(z) resultante.

Entradas (data/processed/Canchita_procesado/):
    masw_curva_dispersion.csv  freq_hz,c_obs_m_s,lambda_m,c_teorica_m_s
    masw_perfil_vs.csv         capa,z_techo_m,z_piso_m,espesor_m,vs_m_s,...
Salida: figuras/masw_resultado.png
"""
import csv
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DISP, PERF, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

C_OBS = "#1f5fa9"
C_TEO = "#c1543a"
C_VS = "#1f5fa9"
TINTA, TENUE, GRILLA = "#1b1b1b", "#6e6e6e", "#e6e6e6"


def leer(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return np.nan


d = leer(DISP)
f = np.array([num(r["freq_hz"]) for r in d])
cobs = np.array([num(r["c_obs_m_s"]) for r in d])
cteo = np.array([num(r["c_teorica_m_s"]) for r in d])
lam = np.array([num(r["lambda_m"]) for r in d])
orden = np.argsort(f)
f, cobs, cteo, lam = f[orden], cobs[orden], cteo[orden], lam[orden]

p = [r for r in leer(PERF) if num(r["vs_m_s"]) == num(r["vs_m_s"])]
z_top = np.array([num(r["z_techo_m"]) for r in p])
z_bot = np.array([num(r["z_piso_m"]) for r in p])
vs = np.array([num(r["vs_m_s"]) for r in p])
misfit = num(p[0]["misfit_pct"])
# El semiespacio no tiene piso: se dibuja una prolongacion visual
z_bot[-1] = z_top[-1] * 1.25 if np.isnan(z_bot[-1]) else z_bot[-1]

fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.30, 2.80), dpi=300,
                             gridspec_kw={"width_ratios": [1.25, 1.0]})

# ---- Curva de dispersion
a1.plot(f, cteo, color=C_TEO, lw=2.2, zorder=2,
        label="Teorica del modelo invertido")
a1.plot(f, cobs, "o", color=C_OBS, ms=5.0, mew=0.9, mec="white", zorder=3,
        label="Observada (picks sobre la imagen)")
a1.set_xlabel("Frecuencia [Hz]", fontsize=9, color=TINTA)
a1.set_ylabel("Velocidad de fase [m/s]", fontsize=9, color=TINTA)
a1.set_title(f"Curva de dispersion  ·  {len(f)} picks  ·  desajuste {misfit:.2f} %",
             fontsize=10, color=TINTA, loc="left", pad=9)
a1.legend(frameon=False, fontsize=8.5, labelcolor=TINTA)

# ---- Perfil Vs(z): escalonado, profundidad hacia abajo
zz, vv = [], []
for zt, zb, v in zip(z_top, z_bot, vs):
    zz += [zt, zb]
    vv += [v, v]
a2.step(vv, zz, where="post", color=C_VS, lw=2.2)
a2.fill_betweenx(zz, 0, vv, step="post", color=C_VS, alpha=0.10)
a2.invert_yaxis()
a2.set_xlabel("$V_S$ [m/s]", fontsize=9, color=TINTA)
a2.set_ylabel("Profundidad [m]", fontsize=9, color=TINTA)
a2.set_title(f"Perfil $V_S(z)$  ·  {len(vs)} capas + semiespacio",
             fontsize=10, color=TINTA, loc="left", pad=9)
a2.set_xlim(0, max(vs) * 1.12)

# Marca de la apertura del arreglo: hasta donde la geometria da soporte real
APERTURA = 40.0
a2.axhline(APERTURA / 2, color="#b04a2a", lw=1.2, ls=(0, (4, 3)), zorder=4)
a2.text(max(vs) * 0.02, APERTURA / 2 - 2.0,
        "$L/2$ = 20 m  ·  mitad de la apertura del arreglo",
        fontsize=7.5, color="#b04a2a", ha="left", va="bottom")

for ax in (a1, a2):
    ax.grid(True, color=GRILLA, linewidth=0.7)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color("#c9c9c9")
    ax.tick_params(colors=TENUE, labelsize=8.5)

fig.tight_layout()
fig.savefig(OUT, bbox_inches="tight", facecolor="white")

print("escrito", OUT)
print(f"  f: {f.min():.2f}-{f.max():.2f} Hz | c_obs: {cobs.min():.0f}-{cobs.max():.0f} m/s")
print(f"  lambda: {np.nanmin(lam):.1f}-{np.nanmax(lam):.1f} m  (apertura del arreglo = 40 m)")
print(f"  Vs: {vs.min():.1f}-{vs.max():.1f} m/s | base del modelo: {z_top[-1]:.1f} m")
rms = np.sqrt(np.nanmean((cobs - cteo) ** 2))
print(f"  RMS obs-teo: {rms:.1f} m/s")
