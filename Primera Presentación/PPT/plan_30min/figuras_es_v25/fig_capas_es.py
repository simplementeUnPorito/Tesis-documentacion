"""Esquema de un terreno modelado en capas homogéneas separadas por interfaces (ilustrativo)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

NAVY, ORANGE = "#1F4E79", "#C55A11"
plt.rcParams.update({"font.family": "Arial", "font.size": 16, "mathtext.fontset": "cm"})
fig, ax = plt.subplots(figsize=(8, 6), dpi=200)
capas = [  # (alto, color, rótulo)
    (1.2, "#F3E3C9", r"Capa 1:  $\rho_1,\ V_{p1},\ V_{s1}$"),
    (1.6, "#E2C99F", r"Capa 2:  $\rho_2,\ V_{p2},\ V_{s2}$"),
    (1.4, "#C9A974", r"Capa 3:  $\rho_3,\ V_{p3},\ V_{s3}$"),
    (1.8, "#A9875A", r"Semiespacio:  $\rho_4,\ V_{p4},\ V_{s4}$"),
]
y = 6.0
for i, (h, c, lab) in enumerate(capas):
    ax.add_patch(Rectangle((0, y - h), 7, h, facecolor=c, edgecolor="none"))
    ax.text(0.3, y - h / 2, lab, va="center", color="#2D2D2D")
    if i < len(capas) - 1:
        ax.plot([0, 7], [y - h, y - h], color=NAVY, lw=2.5)
        ax.annotate("interfaz", xy=(7, y - h), xytext=(7.25, y - h), va="center", color=NAVY, fontsize=15)
    y -= h
ax.plot([0, 7], [6, 6], color="#2D2D2D", lw=3)
ax.text(7.25, 6, "superficie", va="center", color="#2D2D2D", fontsize=15)
ax.annotate("", xy=(-0.35, 0.2), xytext=(-0.35, 5.8), arrowprops=dict(arrowstyle="->", color="#555555", lw=1.5))
ax.text(-0.55, 3, "profundidad $z$", rotation=90, va="center", ha="right", color="#555555")
ax.set_xlim(-1.1, 9.0); ax.set_ylim(0, 6.3); ax.axis("off")
fig.tight_layout()
fig.savefig(__file__.replace(".py", ".png"))
