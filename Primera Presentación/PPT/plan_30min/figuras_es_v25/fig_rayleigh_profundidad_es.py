"""Amplitud de la onda Rayleigh con la profundidad en un semiespacio homogéneo (nu = 0,25).
Solución clásica de Lamb: q = sqrt(1 - c²/Vp²), s = sqrt(1 - c²/Vs²), k = 2*pi/lambda.
u(z) ∝ -exp(-q k z) + 2 q s/(1+s²) exp(-s k z)   (horizontal)
w(z) ∝ -q exp(-q k z) + 2 q/(1+s²) exp(-s k z)   (vertical)
Como en Foti et al. (2014), cap. 2, fig. 2.16 (cualitativa); aquí calculada."""
import numpy as np
from scipy.optimize import brentq
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker

NAVY, ORANGE, GRAY = "#1F4E79", "#C55A11", "#7F7F7F"
plt.rcParams.update({"font.family": "Arial", "font.size": 15, "mathtext.fontset": "cm"})

nu = 0.25
kappa2 = 2 * (1 - nu) / (1 - 2 * nu)          # (Vp/Vs)²
f = lambda x: (2 - x) ** 2 - 4 * np.sqrt(1 - x / kappa2) * np.sqrt(1 - x)   # x = (c/Vs)²
x = brentq(f, 0.5, 0.99)
q, s = np.sqrt(1 - x / kappa2), np.sqrt(1 - x)
z = np.linspace(0, 1.5, 600)                  # z / lambda
k = 2 * np.pi
u = -np.exp(-q * k * z) + 2 * q * s / (1 + s * s) * np.exp(-s * k * z)
w = -q * np.exp(-q * k * z) + 2 * q / (1 + s * s) * np.exp(-s * k * z)
u, w = u / abs(w[0]), w / abs(w[0])
print(f"c/Vs = {np.sqrt(x):.4f}; |w/u| en superficie = {abs(w[0] / u[0]):.2f}; u cambia de signo en z/λ = {z[np.argmax(np.sign(u) != np.sign(u[0]))]:.3f}")

fig, ax = plt.subplots(figsize=(6.4, 6), dpi=200)
ax.axvline(0, color=GRAY, lw=1)
ax.plot(abs(w[0]) * w / w[0], z, color=NAVY, lw=3, label="vertical")
ax.plot(u * np.sign(w[0]) * np.sign(w[0]), z, color=ORANGE, lw=3, ls="--", label="horizontal")
ax.invert_yaxis(); ax.set_ylim(1.5, 0); ax.set_xlim(-0.8, 1.3)
ax.set_xlabel("Amplitud relativa"); ax.set_ylabel(r"Profundidad  $z\,/\,\lambda$")
fmt = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))
ax.xaxis.set_major_formatter(fmt); ax.yaxis.set_major_formatter(fmt)
ax.legend(frameon=False, loc="lower right")
for sp in ("top", "right"): ax.spines[sp].set_visible(False)
ax.grid(True, color="#DDDDDD", lw=0.8)
fig.tight_layout(); fig.savefig(__file__.replace(".py", ".png"))
