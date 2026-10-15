"""Figuras de la v31: reflexión en la superficie libre, media móvil, diagrama del nodo HAMMER
y respuesta de geófonos de 10 Hz y 4,5 Hz. Estilo de la presentación (Arial, navy/naranja)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

NAVY, BLUE, ORANGE, GRAY, LIGHT = "#1F4E79", "#2E75B6", "#C55A11", "#7F7F7F", "#EAF1F8"
plt.rcParams.update({"font.family": "Arial", "font.size": 15, "mathtext.fontset": "cm"})
OUT = __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0] if ("\\" in __file__ or "/" in __file__) else "."
comma = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))


def ray(ax, x0, y0, ang_deg, length, color, ls="-", up=True, label=None, lpos=0.62):
    a = np.radians(ang_deg)
    dx, dy = length * np.sin(a), length * np.cos(a)
    x1, y1 = (x0 + dx, y0 - dy) if not up else (x0 + dx, y0 - dy)
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=18, color=color, lw=2.5, ls=ls))
    if label:
        ax.text(x0 + lpos * dx + 0.06, y0 - lpos * dy, label, color=color, fontsize=15, va="center")


# 1) reflexión en la superficie libre
fig, axs = plt.subplots(1, 3, figsize=(12, 4.2), dpi=200)
# Snell con Vp/Vs = sqrt(3) (nu = 0,25): reflexión especular de la misma onda; la convertida cambia de ángulo
# P a 30°: SV a asin(sin30/sqrt3) = 16,8°. SV a 25°: P a asin(sqrt3·sin25) = 47,0°.
cases = [("P incidente", ORANGE, [("P", ORANGE, 30), ("SV", NAVY, 16.8)]),
         ("SV incidente", NAVY, [("SV", NAVY, 25), ("P", ORANGE, 47.0)]),
         ("SH incidente", "#6B8E23", [("SH", "#6B8E23", 30)])]
for ax, (name, col, refl) in zip(axs, cases):
    ax.axhspan(0, 0.35, color="#F2F2F2"); ax.axhspan(-1.6, 0, color="#F3E3C9")
    ax.plot([-1.2, 1.2], [0, 0], color="#2D2D2D", lw=3)
    ax.text(-1.1, 0.17, "aire", color=GRAY, fontsize=14, va="center")
    ax.text(-1.1, -1.45, "terreno", color="#7A5C2E", fontsize=14, va="center")
    inc_a = np.radians(30 if name.startswith("P") else 25 if name.startswith("SV") else 30)
    L = 1.3
    ax.add_patch(FancyArrowPatch((-L * np.sin(inc_a), -L * np.cos(inc_a)), (0, 0), arrowstyle="-|>",
                                 mutation_scale=18, color=col, lw=2.5))
    ax.text(-L * np.sin(inc_a) * 0.75 - 0.42, -L * np.cos(inc_a) * 0.75, name.split()[0], color=col, fontsize=15)
    for lab, c, ang in refl:
        a = np.radians(ang)
        ax.add_patch(FancyArrowPatch((0, 0), (L * np.sin(a), -L * np.cos(a)), arrowstyle="-|>",
                                     mutation_scale=18, color=c, lw=2.5, ls="--"))
        ax.text(L * np.sin(a) * 0.8 + 0.06, -L * np.cos(a) * 0.8, lab, color=c, fontsize=15)
    ax.set_title(name, color="#2D2D2D", fontsize=16)
    ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.6, 0.35); ax.set_aspect("equal"); ax.axis("off")
fig.tight_layout(); fig.savefig(f"{OUT}/fig_reflexion_superficie_es.png")

# 2) media móvil normal, eje en f/fs hasta Nyquist
D = 4
f = np.linspace(1e-4, 0.5, 2000)
H = np.abs(np.sin(np.pi * f * D) / (D * np.sin(np.pi * f)))
fig, ax = plt.subplots(figsize=(8, 5), dpi=200)
ax.plot(f, 20 * np.log10(np.maximum(H, 1e-4)), color=NAVY, lw=3)
ax.axvline(1 / (2 * D), color=ORANGE, ls=":", lw=2)
ax.text(1 / (2 * D) + 0.008, -36, r"Nyquist de $f_s'$", color=ORANGE, fontsize=14)
ax.set_xlim(0, 0.5); ax.set_ylim(-40, 3)
ax.set_xlabel(r"Frecuencia normalizada  $f\,/\,f_s$"); ax.set_ylabel("Respuesta (dB)")
ax.set_title(f"Media móvil de D = {D} muestras", color="#2D2D2D", fontsize=15)
ax.xaxis.set_major_formatter(comma)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.grid(True, color="#DDDDDD", lw=0.8)
fig.tight_layout(); fig.savefig(f"{OUT}/fig_media_movil_es.png")

# 3) diagrama de bloques del nodo HAMMER
blocks = [("Martillo PCB 086D20", "sensor ICP · 0,23 mV/N", NAVY, "white"),
          ("Fuente de corriente", "LM7805 + 1 kΩ · ≈ 5 mA", BLUE, "white"),
          ("Desacople y protección", "47 µF · diodos", LIGHT, NAVY),
          ("PGA → pasa-bajos", "en el PSoC", LIGHT, NAVY),
          ("ADC ΔΣ", "PSoC · mismo firmware que GEO", ORANGE, "white")]
fig, ax = plt.subplots(figsize=(5.2, 6.6), dpi=200)
h, gap, y = 0.95, 0.38, 6.0
for i, (t1, t2, fc, tc) in enumerate(blocks):
    ax.add_patch(FancyBboxPatch((0.2, y - h), 4.6, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor=fc, edgecolor=NAVY if fc == LIGHT else fc, lw=1.5))
    ax.text(2.5, y - 0.36, t1, ha="center", va="center", color=tc, fontsize=15, weight="bold")
    ax.text(2.5, y - 0.70, t2, ha="center", va="center", color=tc, fontsize=12.5)
    if i < len(blocks) - 1:
        ax.add_patch(FancyArrowPatch((2.5, y - h - 0.02), (2.5, y - h - gap + 0.02), arrowstyle="-|>",
                                     mutation_scale=16, color=GRAY, lw=1.8))
    y -= h + gap
ax.set_xlim(0, 5); ax.set_ylim(y + gap - 0.1, 6.1); ax.axis("off")
fig.tight_layout(); fig.savefig(f"{OUT}/fig_hammer_bloques_es.png")

# 4) respuesta en velocidad de geófonos de 10 Hz y 4,5 Hz (mismo zeta, ilustrativo)
fq = np.logspace(0, 2, 500); zeta = 0.6
def resp(fn):
    r = fq / fn
    return 20 * np.log10(r ** 2 / np.sqrt((1 - r ** 2) ** 2 + (2 * zeta * r) ** 2))
fig, ax = plt.subplots(figsize=(8, 5.4), dpi=200)
ax.axvspan(1, 10, color=LIGHT)
ax.text(1.15, -44, "bajas frecuencias", color=NAVY, fontsize=14)
ax.semilogx(fq, resp(10), color=NAVY, lw=3, label=r"SM-24, $f_n$ = 10 Hz")
ax.semilogx(fq, resp(4.5), color=ORANGE, lw=3, ls="--", label=r"Geófono de $f_n$ = 4,5 Hz")
ax.set_xlim(1, 100); ax.set_ylim(-48, 5)
ax.set_xlabel("Frecuencia (Hz)"); ax.set_ylabel("Respuesta relativa a velocidad (dB)")
ax.xaxis.set_major_formatter(comma)
ax.legend(frameon=False, loc="lower right")
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.grid(True, which="both", color="#E5E5E5", lw=0.7)
fig.tight_layout(); fig.savefig(f"{OUT}/fig_geofonos_10_vs_45_es.png")
print("1 Hz: SM-24 {:.1f} dB, 4,5 Hz {:.1f} dB".format(np.interp(1, fq, resp(10)), np.interp(1, fq, resp(4.5))))
