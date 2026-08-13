# -*- coding: utf-8 -*-
"""
Contraste del perfil Vs invertido por MASW contra el modelo geoelectrico del
SEV 01, que se midio en la misma cancha en julio de 2023 por terceros y con otro
metodo (resistividad DC).

No es una validacion en sentido estricto: un contraste de resistividad no es un
contraste de rigidez. Es una comparacion de PROFUNDIDADES DE INTERFAZ, que es lo
unico que las dos tecnicas comparten legitimamente.

Entradas:
  data/processed/Canchita_procesado/masw_perfil_vs.csv
  data/processed/Canchita_procesado/masw_curva_dispersion.csv
  (el modelo del SEV va embebido: son seis numeros de un informe en papel)

Salida: figuras/vs_vs_sev.png
"""
import csv
import sys
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PERFIL, CURVA, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

C_VS = "#1f5fa9"      # azul  -> MASW
C_SEV = "#c1543a"     # terracota -> SEV
C_AGUA = "#7fa8c9"    # banda del freatico
TINTA, TENUE, GRILLA = "#1b1b1b", "#6e6e6e", "#e6e6e6"

# --- SEV 01, cancha de futbol de la UC, 21/07/2023 (informe Gonzalez & Asoc.)
# (resistividad ohm.m, profundidad de la base en m)
SEV = [(1186, 1.00), (15, 2.06), (105, 4.15), (24.2, 24.0), (126, 71.8), (6.42, None)]
FREATICO = (10.0, 30.0)   # rango declarado, epoca seca

# --- perfil Vs invertido
z_top, z_bot, vs = [], [], []
with open(PERFIL, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        z_top.append(float(r["z_techo_m"]))
        z_bot.append(float(r["z_piso_m"]) if r["z_piso_m"] else np.nan)
        vs.append(float(r["vs_m_s"]))
        misfit = float(r["misfit_pct"])
Z_MAX = 95.0
z_bot[-1] = Z_MAX

# --- curva de dispersion
f_obs, c_obs, lam, c_teo = [], [], [], []
with open(CURVA, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        f_obs.append(float(r["freq_hz"]))
        c_obs.append(float(r["c_obs_m_s"]))
        lam.append(float(r["lambda_m"]))
        c_teo.append(float(r["c_teorica_m_s"]))


def escalones(zt, zb, v):
    """Convierte el modelo de capas en una poligonal escalonada."""
    x, y = [], []
    for a, b, c in zip(zt, zb, v):
        x += [c, c]
        y += [a, b]
    return np.array(x), np.array(y)


def estilo(ax):
    ax.grid(True, color=GRILLA, linewidth=0.7)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color("#c9c9c9")
    ax.tick_params(colors=TENUE, labelsize=8.5)


fig, (ax1, ax2, ax3) = plt.subplots(
    1, 3, figsize=(11.4, 6.4), dpi=200,
    gridspec_kw={"width_ratios": [1.25, 0.75, 1.15], "wspace": 0.30})

# ---------------------------------------------------------------- (1) Vs(z)
xv, yv = escalones(z_top, z_bot, vs)
ax1.plot(xv, yv, color=C_VS, lw=2.3, zorder=4, label="$V_S$ invertido (MASW)")
ax1.fill_betweenx(yv, 0, xv, color=C_VS, alpha=0.08, zorder=1)
ax1.axhspan(*FREATICO, color=C_AGUA, alpha=0.22, zorder=0)
ax1.text(60, FREATICO[1] - 0.8, "nivel freático SEV: 10–30 m (época seca)",
         fontsize=7.2, color="#3c6a8f", ha="left", va="bottom")
# Las tres interfaces someras del SEV caen dentro de 4 m y sus rotulos se
# pisarian: se los reparte en una escalerita a la derecha con guia horizontal.
ESCALERA = {1.00: 2.0, 2.06: 8.0, 4.15: 14.0}
for rho, base in SEV:
    if base is None or base > Z_MAX:
        continue
    ax1.axhline(base, color=C_SEV, lw=1.1, ls=(0, (5, 3)), zorder=3)
    y_rot = ESCALERA.get(base, base - 1.6)
    ax1.annotate(f"SEV {base:g} m", xy=(1090, base), xytext=(1090, y_rot),
                 fontsize=7.2, color=C_SEV, ha="right", va="center",
                 arrowprops=dict(arrowstyle="-", color=C_SEV, lw=0.6,
                                 shrinkA=0, shrinkB=0, alpha=0.65)
                 if base in ESCALERA else None)
estilo(ax1)
ax1.set_ylim(Z_MAX, 0)
ax1.set_xlim(0, 1100)
ax1.set_xlabel("$V_S$ [m/s]", fontsize=9, color=TINTA)
ax1.set_ylabel("Profundidad [m]", fontsize=9, color=TINTA)
ax1.set_title("Perfil invertido vs. interfaces del SEV 01",
              fontsize=9.5, color=TINTA, loc="left", pad=9)
ax1.legend(frameon=False, fontsize=8, loc="lower right", labelcolor=TINTA)

# ---------------------------------------------------------------- (2) SEV
rho_x, rho_y = [], []
prev = 0.0
for rho, base in SEV:
    b = Z_MAX if base is None else min(base, Z_MAX)
    rho_x += [rho, rho]
    rho_y += [prev, b]
    prev = b
    if prev >= Z_MAX:
        break
ax2.plot(rho_x, rho_y, color=C_SEV, lw=2.3, zorder=3)
ax2.fill_betweenx(rho_y, 1, rho_x, color=C_SEV, alpha=0.08)
ax2.axhspan(*FREATICO, color=C_AGUA, alpha=0.22, zorder=0)
ax2.set_xscale("log")
estilo(ax2)
ax2.set_ylim(Z_MAX, 0)
ax2.set_xlim(3, 2000)
ax2.set_xlabel(r"$\rho$ [$\Omega\cdot$m]", fontsize=9, color=TINTA)
ax2.set_title("SEV 01 (IPI2win, 2023)", fontsize=9.5, color=TINTA, loc="left", pad=9)
ax2.set_yticklabels([])

# ---------------------------------------------------------------- (3) curva
o = np.argsort(f_obs)
f_obs = np.array(f_obs)[o]
c_obs = np.array(c_obs)[o]
c_teo = np.array(c_teo)[o]
lam = np.array(lam)[o]
ax3.plot(f_obs, c_obs, "o", color=C_VS, ms=3.6, label="observada", zorder=3)
ax3.plot(f_obs, c_teo, "-", color="#3f7d4e", lw=2.0, label="teórica del modelo", zorder=2)
estilo(ax3)
ax3.set_xlabel("Frecuencia [Hz]", fontsize=9, color=TINTA)
ax3.set_ylabel("Velocidad de fase [m/s]", fontsize=9, color=TINTA)
ax3.set_title(f"Curva de dispersión (desajuste {misfit:.2f} %)",
              fontsize=9.5, color=TINTA, loc="left", pad=9)
ax3.legend(frameon=False, fontsize=8, labelcolor=TINTA)

# Aviso honesto sobre longitudes de onda mayores que la apertura
APERTURA = 40.0
mal = lam > APERTURA
if mal.any():
    ax3.plot(f_obs[mal], c_obs[mal], "o", mfc="none", mec="#c1543a", ms=8, mew=1.4,
             zorder=4, label="_")
    ax3.text(0.97, 0.30,
             f"{mal.sum()} de {len(lam)} puntos tienen\n$\\lambda$ > apertura (40 m):\n"
             "no resueltos por la\ngeometría (círculos)",
             transform=ax3.transAxes, fontsize=7.0, color="#c1543a",
             ha="right", va="top")

fig.suptitle("Contraste independiente: MASW de este proyecto frente al sondeo eléctrico "
             "de 2023 en la misma cancha",
             fontsize=11, color=TINTA, x=0.012, ha="left", y=0.985)
fig.text(0.012, 0.012,
         "Advertencia: un contraste de resistividad NO es un contraste de rigidez. "
         "La comparación legitima es de PROFUNDIDAD DE INTERFAZ, no de valores.",
         fontsize=7.4, color=TENUE, ha="left")

os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
fig.savefig(OUT, bbox_inches="tight", facecolor="white")

print("escrito", OUT)
print(f"  capas MASW: {len(vs)}, desajuste {misfit:.3f} %")
print("  interfaces MASW:", [f"{b:.2f}" for b in z_bot[:-1]])
print("  interfaces SEV :", [b for _, b in SEV if b])
print(f"  lambda maxima observada: {lam.max():.1f} m  (apertura {APERTURA:g} m)")
print(f"  puntos con lambda > apertura: {int(mal.sum())} de {len(lam)}")
