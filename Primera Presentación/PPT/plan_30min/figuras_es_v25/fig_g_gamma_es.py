"""Curva ilustrativa G/Gmax contra deformación de corte (modelo hiperbólico, Hardin y Drnevich, 1972).
gamma_r = 1e-3 es ilustrativo: con ese valor, en gamma = 1e-5 la rigidez conserva el 99 %."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker

NAVY, ORANGE, GRAY = "#1F4E79", "#C55A11", "#7F7F7F"
plt.rcParams.update({"font.family": "Arial", "font.size": 15, "mathtext.fontset": "cm"})

g_r = 1e-3
g = np.logspace(-6, -1, 400)
G = 1 / (1 + g / g_r)

fig, ax = plt.subplots(figsize=(8, 6), dpi=200)
ax.axvspan(1e-6, 1e-5, color="#EAF1F8", zorder=0)
ax.text(3.2e-6, 0.12, "ondas de\nprospección", ha="center", va="bottom", color=NAVY, fontsize=14)
ax.axhline(1, color=GRAY, ls="--", lw=1.2)
ax.text(1.4e-6, 1.03, r"$G = G_{\mathrm{max}}$", color=GRAY, fontsize=15, va="bottom")
ax.plot(g, G, color=NAVY, lw=3)
ax.axvline(g_r, color=ORANGE, ls=":", lw=1.5)
ax.annotate(r"$\gamma = \gamma_r$:  $G = G_{\mathrm{max}}/2$", xy=(g_r, 0.5), xytext=(4e-3, 0.62),
            color=ORANGE, fontsize=15, arrowprops=dict(arrowstyle="->", color=ORANGE))
ax.plot([g_r], [0.5], "o", color=ORANGE, ms=7)
ax.set_xscale("log"); ax.set_xlim(1e-6, 1e-1); ax.set_ylim(0, 1.15)
ax.set_xlabel(r"Deformación de corte $\gamma$")
ax.set_ylabel(r"$G\,/\,G_{\mathrm{max}}$")
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.1f}".replace(".", ",")))
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.grid(True, which="major", color="#DDDDDD", lw=0.8)
fig.tight_layout()
fig.savefig(__file__.replace(".py", ".png"))
