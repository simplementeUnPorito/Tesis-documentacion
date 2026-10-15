"""Balance de fuerza en formato clásico de control.
La fuerza inercial −m·a_g y la fuerza de la bobina entran a un sumador; la mecánica del geófono da el desplazamiento
relativo u; la misma bobina, como sensor, entrega v = G0·s·u; el controlador C(s) calcula la corriente i y la bobina,
como actuador, aplica F = G0·i, que se resta (realimentación negativa). G0: constante electromecánica de la bobina."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, FancyArrowPatch

INK, ORANGE, GRAY = "#1F1F1F", "#C55A11", "#555555"
plt.rcParams.update({"font.family": "Arial", "font.size": 15, "mathtext.fontset": "cm"})
fig, ax = plt.subplots(figsize=(11, 4.4), dpi=200)
Y, H = 2.6, 0.95

def block(x, w, tf, name, y=Y, color=INK, below=True):
    ax.add_patch(Rectangle((x, y - H / 2), w, H, facecolor="white", edgecolor=color, lw=1.8))
    ax.text(x + w / 2, y, tf, ha="center", va="center", fontsize=19, color=color)
    ax.text(x + w / 2, (y - H / 2 - 0.18) if below else (y + H / 2 + 0.15), name, ha="center",
            va="top" if below else "bottom", fontsize=12.5, color=GRAY if color == INK else color)

def arrow(p, q, label=None, dy=0.18, color=INK, ha="center"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16, color=color, lw=1.6, shrinkA=0, shrinkB=0))
    if label: ax.text((p[0] + q[0]) / 2, p[1] + dy, label, ha=ha, va="bottom", fontsize=16, color=color)

def line(xs, ys, color=INK):
    ax.plot(xs, ys, color=color, lw=1.6, solid_capstyle="butt")

# cadena directa
arrow((0.0, Y), (1.1, Y), r"$-m\,a_g$")
R, cx = 0.3, 1.4
ax.add_patch(Circle((cx, Y), R, facecolor="white", edgecolor=INK, lw=1.8))
ax.plot([cx - R * 0.7, cx + R * 0.7], [Y + R * 0.7, Y - R * 0.7], color=INK, lw=1.2)
ax.plot([cx - R * 0.7, cx + R * 0.7], [Y - R * 0.7, Y + R * 0.7], color=INK, lw=1.2)
ax.text(cx - R - 0.08, Y + 0.12, "+", ha="right", va="bottom", fontsize=17)
ax.text(cx + 0.14, Y - R - 0.04, "−", ha="left", va="top", fontsize=19, color=ORANGE)
arrow((cx + R, Y), (2.4, Y))
block(2.4, 2.4, r"$\dfrac{1}{m s^2 + c s + k}$", "mecánica del geófono")
arrow((4.8, Y), (5.6, Y), r"$u$")
block(5.6, 1.5, r"$G_0\, s$", "bobina como sensor")
line([7.1, 8.4], [Y, Y]); ax.add_patch(Circle((8.0, Y), 0.06, color=INK, zorder=5))
arrow((8.4, Y), (9.4, Y), r"$v_o$")
ax.text(9.45, Y, "salida", ha="left", va="center", fontsize=14, color=GRAY)

# realimentación
yb = 0.75
line([8.0, 8.0], [Y, yb], ORANGE); arrow((8.0, yb), (7.15, yb), color=ORANGE)
block(5.65, 1.5, r"$C(s)$", "controlador", y=yb, color=ORANGE)
arrow((5.65, yb), (4.35, yb), r"$i$", color=ORANGE)
# ganancia pura: triángulo hacia la izquierda, como en el diagrama del AFE
ax.add_patch(Polygon([(4.35, yb - H / 2 - 0.08), (4.35, yb + H / 2 + 0.08), (2.85, yb)], closed=True, facecolor="white", edgecolor=ORANGE, lw=1.8))
ax.text(3.75, yb, r"$G_0$", ha="center", va="center", fontsize=19, color=ORANGE)
ax.text(3.6, yb - H / 2 - 0.18, "bobina como actuador", ha="center", va="top", fontsize=12.5, color=ORANGE)
line([2.85, cx], [yb, yb], ORANGE); arrow((cx, yb), (cx, Y - R), color=ORANGE)
ax.text(cx - 0.12, (yb + Y) / 2 - 0.1, r"$F_c$", ha="right", va="center", fontsize=16, color=ORANGE)

ax.set_xlim(-0.1, 10.4); ax.set_ylim(-0.25, 3.55); ax.axis("off")
fig.tight_layout(); fig.savefig(__file__.replace(".py", ".png"))
