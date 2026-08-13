# -*- coding: utf-8 -*-
"""
Dos figuras sobre la compensacion del geofono.

(A) Reproduce ComparacionFiltros.m (30/04/2026), el script que dictamino el
    pivote de topologia: MFB vs Sallen-Key/VCVS vs la respuesta objetivo.
    Mismos valores de componente que el .m original.

(B) Muestra que hace la compensacion: respuesta del SM-24 solo contra
    SM-24 x (pasa-todo - pasa-banda), que es la estrategia de Ma et al. 2023
    (subir el amortiguamiento manteniendo la frecuencia natural).

Salida: figuras/comparacion_topologias.png, figuras/extension_banda.png
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUTA, OUTB = sys.argv[1], sys.argv[2]

# Paleta categorica en orden fijo (nunca ciclada). Verificada para CVD.
C_MFB = "#1f5fa9"   # azul
C_SK = "#c1543a"    # terracota
C_OBJ = "#3f7d4e"   # verde
C_GEO = "#8a8a8a"   # gris
TINTA, TENUE, GRILLA = "#1b1b1b", "#6e6e6e", "#e3e3e3"


def bode(num, den, w):
    """Magnitud en dB de una TF dada por coeficientes en potencias
    decrecientes de s."""
    jw = 1j * w
    return 20 * np.log10(np.abs(np.polyval(num, jw) / np.polyval(den, jw)))


def estilo(ax):
    ax.set_xscale("log")
    ax.grid(True, which="both", color=GRILLA, linewidth=0.7)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color("#c9c9c9")
    ax.tick_params(colors=TENUE, labelsize=8.5)
    ax.set_xlabel("Frecuencia [Hz]", fontsize=9, color=TINTA)
    ax.set_ylabel("Magnitud [dB]", fontsize=9, color=TINTA)


f = np.logspace(-4, 4, 5000)
w = 2 * np.pi * f

# ---------------------------------------------------------------- FIGURA A
# Valores exactos de ComparacionFiltros.m
R1_1, R2_1, R5_1, C3_1, C4_1 = 82e3, 750e3, 80e3, 44e-6, 1e-9
num1 = [-(1 / (R1_1 * C4_1)), 0.0]
den1 = [1.0,
        (C3_1 + C4_1) / (C3_1 * C4_1 * R5_1),
        (1 / (R5_1 * C3_1 * C4_1)) * (1 / R1_1 + 1 / R2_1)]

R1_2, R2_2, Rf_2, Ra_2, Rb_2, C1_2, C2_2 = 330e3, 91e3, 2e6, 40e3, 120e3, 1e-9, 10e-6
num2 = [(1 + Rb_2 / Ra_2) * (1 / (R1_2 * C1_2)), 0.0]
den2 = [1.0,
        (1 / (R1_2 * C1_2) + 1 / (R2_2 * C1_2) + 1 / (R2_2 * C2_2)
         - Rb_2 / (Ra_2 * Rf_2 * C1_2)),
        (R1_2 + Rf_2) / (R1_2 * Rf_2 * R2_2 * C1_2 * C2_2)]

g1, g0, w0 = 100.0, 0.25, 2 * np.pi * 10
num3 = [2 * (g1 * w0 - g0 * w0), 0.0]
den3 = [1.0, 2 * g1 * w0, w0 ** 2]

m1, m2, m3 = bode(num1, den1, w), bode(num2, den2, w), bode(num3, den3, w)

fig, (ax, axr) = plt.subplots(
    2, 1, figsize=(7.4, 5.2), dpi=200, sharex=True,
    gridspec_kw={"height_ratios": [2.3, 1.0], "hspace": 0.18})

ax.plot(f, m3, color=C_OBJ, lw=3.0, zorder=2,
        label="Objetivo: pasa-banda de compensacion")
ax.plot(f, m1, color=C_MFB, lw=1.8, zorder=4, label="MFB")
ax.plot(f, m2, color=C_SK, lw=1.8, ls=(0, (5, 3)), zorder=3,
        label="Sallen-Key / VCVS")
estilo(ax)
ax.set_xlabel("")
ax.set_ylim(-60, 20)
ax.axvline(10, color="#b8b8b8", lw=1.0, ls=(0, (4, 3)), zorder=1)
ax.text(10.6, 14, "$f_n$ = 10 Hz", fontsize=7.5, color=TENUE)
ax.legend(frameon=False, fontsize=8.5, loc="lower center", labelcolor=TINTA)
ax.set_title("Comparacion de topologias — el grafico que decidio el pivote (30/04/2026)",
             fontsize=10, color=TINTA, loc="left", pad=10)

# Panel de residuo: la diferencia contra el objetivo es lo unico legible
axr.axhline(0, color="#c9c9c9", lw=1.0)
axr.plot(f, m1 - m3, color=C_MFB, lw=1.8)
axr.plot(f, m2 - m3, color=C_SK, lw=1.8, ls=(0, (5, 3)))
estilo(axr)
axr.set_ylabel("Desviacion [dB]", fontsize=9, color=TINTA)
axr.set_ylim(-2.0, 2.0)
axr.axvline(10, color="#b8b8b8", lw=1.0, ls=(0, (4, 3)), zorder=1)
axr.text(1.2e-2, 1.35,
         "Ambas topologias reproducen el objetivo dentro de +/-1 dB en toda la "
         "banda sismica:\nla eleccion NO se decidio por respuesta, sino por "
         "sensibilidad a tolerancias.",
         fontsize=7.5, color=TENUE, va="top")

fig.savefig(OUTA, bbox_inches="tight", facecolor="white")
banda = (f >= 0.1) & (f <= 200)
print("escrito", OUTA,
      f"| desv. max en 0,1-200 Hz: MFB {np.abs(m1 - m3)[banda].max():.2f} dB, "
      f"SK {np.abs(m2 - m3)[banda].max():.2f} dB")

# ---------------------------------------------------------------- FIGURA B
# Geofono en aceleracion:  Ha(s) = -G0*s / (s^2 + 2*z0*wn*s + wn^2)
z0, wn = 0.25, 2 * np.pi * 10.2046
numg, deng = [1.0, 0.0], [1.0, 2 * z0 * wn, wn ** 2]


def comp_db(z1):
    """Ha(s) * [1 - BP(s)], la compensacion allpass-menos-pasabanda."""
    jw = 1j * w
    ha = np.polyval(numg, jw) / np.polyval(deng, jw)
    bp = (np.polyval([2 * (z1 - z0) * wn, 0.0], jw)
          / np.polyval([1.0, 2 * z1 * wn, wn ** 2], jw))
    return 20 * np.log10(np.abs(ha * (1 - bp)))


fig, ax = plt.subplots(figsize=(7.4, 3.9), dpi=200)
ref = bode(numg, deng, w)
ax.plot(f, ref - ref.max(), color=C_GEO, lw=2.0,
        label=r"SM-24 sin compensar ($\zeta_0$ = 0,25)")
for z1, col, lab in ((10.0, C_SK, r"$\zeta_1$ = 10  (Ma et al. 2023)"),
                     (937.4, C_MFB,
                      r"$\zeta_1$ = 937,4  (denominador BP medido, 21/07)")):
    y = comp_db(z1)
    ax.plot(f, y - y.max(), color=col, lw=2.2, label=lab)
estilo(ax)
ax.set_ylabel("Magnitud normalizada [dB]", fontsize=9, color=TINTA)
ax.set_xlim(1e-4, 1e3)
ax.set_ylim(-60, 6)
ax.axhline(-3, color="#b8b8b8", lw=1.0, ls=(0, (4, 3)), zorder=1)
ax.text(1.1e-4, -2.4, "-3 dB", fontsize=7.5, color=TENUE)
ax.axvline(5.44e-3, color=C_MFB, lw=0.9, ls=(0, (3, 3)), alpha=0.75)
ax.text(6.0e-3, -15, "5,44 mHz\n(polo ideal)", fontsize=7.2,
        color=C_MFB, ha="left", va="center")
ax.axvline(10, color="#b8b8b8", lw=1.0, ls=(0, (4, 3)), zorder=1)
ax.text(10.6, 3.2, "$f_n$ = 10 Hz", fontsize=7.5, color=TENUE)
ax.legend(frameon=False, fontsize=8.5, loc="lower right", labelcolor=TINTA)
ax.set_title("Efecto de la compensacion: extension de la banda hacia abajo",
             fontsize=10, color=TINTA, loc="left", pad=10)
fig.tight_layout()
fig.savefig(OUTB, bbox_inches="tight", facecolor="white")

# Dato duro para el texto: donde cae el -3 dB en cada caso
for z1 in (0.0, 10.0, 937.4):
    y = ref - ref.max() if z1 == 0.0 else comp_db(z1) - comp_db(z1).max()
    baja = f[(f < 10) & (y > -3)]
    print(f"  zeta1={z1:>8}: -3 dB inferior en {baja.min():.3f} Hz"
          if baja.size else f"  zeta1={z1}: sin cruce")
