"""Diagrama de bloques del AFE en formato clásico de control.
Ganancias como triángulos (K_dif·K_PGA, K_sum, K_LP), dinámicas como rectángulos (H_a, H_BP, H_LP),
punto de derivación y sumador con signos. El pasabanda es inversor: entra al sumador con + y realiza 1 − H_BP(s)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, FancyArrowPatch

INK, ORANGE, GRAY = "#1F1F1F", "#C55A11", "#555555"
plt.rcParams.update({"font.family": "Arial", "font.size": 15, "mathtext.fontset": "cm"})
fig, ax = plt.subplots(figsize=(14, 3.9), dpi=200)
Y, H = 2.2, 0.9

def block(x, w, tf, name, y=Y, color=INK):
    ax.add_patch(Rectangle((x, y - H / 2), w, H, facecolor="white", edgecolor=color, lw=1.8))
    ax.text(x + w / 2, y, tf, ha="center", va="center", fontsize=19, color=color)
    ax.text(x + w / 2, y - H / 2 - 0.2, name, ha="center", va="top", fontsize=12.5, color=GRAY if color == INK else color)

def gain(x, w, k, name, y=Y):
    ax.add_patch(Polygon([(x, y - H / 2 - 0.08), (x, y + H / 2 + 0.08), (x + w, y)], closed=True,
                         facecolor="white", edgecolor=INK, lw=1.8))
    ax.text(x + w * 0.38, y, k, ha="center", va="center", fontsize=17)
    ax.text(x + w / 2, y - H / 2 - 0.2, name, ha="center", va="top", fontsize=12.5, color=GRAY)

def arrow(p, q, label=None, dy=0.18, color=INK):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16, color=color, lw=1.6, shrinkA=0, shrinkB=0))
    if label: ax.text((p[0] + q[0]) / 2, p[1] + dy, label, ha="center", va="bottom", fontsize=16, color=color)

def line(xs, ys, color=INK):
    ax.plot(xs, ys, color=color, lw=1.6, solid_capstyle="butt")

arrow((0.0, Y), (0.65, Y), r"$a_g$")
block(0.65, 1.5, r"$H_a(s)$", "geófono SM-24")
arrow((2.15, Y), (2.8, Y), r"$v_o$")
gain(2.8, 1.75, r"$K_{\mathrm{dif}}K_{\mathrm{PGA}}$", "entrada dif. y PGA")
line([4.55, 6.0], [Y, Y]); ax.add_patch(Circle((5.0, Y), 0.06, color=INK, zorder=5))
ax.text(5.0, Y + 0.18, r"$v_1$", ha="center", va="bottom", fontsize=16)
arrow((6.0, Y), (7.1, Y))
R = 0.3; cx = 7.4
ax.add_patch(Circle((cx, Y), R, facecolor="white", edgecolor=INK, lw=1.8))
ax.plot([cx - R * 0.7, cx + R * 0.7], [Y + R * 0.7, Y - R * 0.7], color=INK, lw=1.2)
ax.plot([cx - R * 0.7, cx + R * 0.7], [Y - R * 0.7, Y + R * 0.7], color=INK, lw=1.2)
ax.text(cx - R - 0.08, Y + 0.12, "+", ha="right", va="bottom", fontsize=17)
ax.text(cx + 0.12, Y - R - 0.05, "+", ha="left", va="top", fontsize=17, color=ORANGE)
arrow((cx + R, Y), (8.3, Y))
gain(8.3, 1.2, r"$K_{\mathrm{sum}}$", "sumador")
arrow((9.5, Y), (10.05, Y))
block(10.05, 1.45, r"$H_{\mathrm{LP}}(s)$", "pasa-bajos Bessel")
arrow((11.5, Y), (11.95, Y))
gain(11.95, 1.1, r"$K_{\mathrm{LP}}$", "")
arrow((13.05, Y), (13.6, Y), r"$v_{\mathrm{ADC}}$")
ax.text(13.65, Y, "ADC", ha="left", va="center", fontsize=15, weight="bold")

yb = 0.65
line([5.0, 5.0], [Y, yb], ORANGE); arrow((5.0, yb), (5.55, yb), color=ORANGE)
block(5.55, 1.6, r"$-H_{\mathrm{BP}}(s)$", "pasabanda inversor", y=yb, color=ORANGE)
line([7.15, cx], [yb, yb], ORANGE); arrow((cx, yb), (cx, Y - R), color=ORANGE)

x0, x1, y0, y1 = 4.75, cx + R + 0.25, yb - H / 2 - 0.55, Y + 0.75
ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, edgecolor=GRAY, lw=1.2, ls=(0, (4, 3))))
ax.text((x0 + x1) / 2, y1 + 0.06, r"compensador:  $H_{\mathrm{comp}}(s) = 1 - H_{\mathrm{BP}}(s)$", fontsize=13.5, color=GRAY, ha="center", va="bottom")
ax.set_xlim(-0.1, 14.4); ax.set_ylim(-0.45, 3.45); ax.axis("off")
fig.tight_layout(); fig.savefig(__file__.replace(".py", ".png"))
