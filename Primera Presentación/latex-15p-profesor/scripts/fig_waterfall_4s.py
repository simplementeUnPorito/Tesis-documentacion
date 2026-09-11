import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

src, dst = sys.argv[1], sys.argv[2]
d = np.genfromtxt(src, delimiter=",", names=True, dtype=float)
t = d["time_s"]
names = list(d.dtype.names[1:])
dist = np.array([float(n.rstrip("m")) for n in names])
mask = (t >= -0.2) & (t <= 4.0)
t = t[mask]

fig, ax = plt.subplots(figsize=(8.6, 4.8), dpi=240)
spacing = 2.0
for name, dd in zip(names, dist):
    x = np.asarray(d[name][mask], float)
    finite = np.isfinite(x)
    if not finite.any():
        continue
    peak = np.nanmax(np.abs(x)) or 1.0
    ax.plot(t, x / peak * spacing * 0.38 + dd, color="#1c1c1c", lw=0.8)
    ax.text(-0.18, dd, f"{int(dd):02d} m", ha="right", va="center", fontsize=7)

ax.axvline(0, color="#2878b5", lw=1.0, ls=(0, (3, 2)))
ax.text(0.03, 51.4, "referencia del impacto", color="#2878b5", fontsize=7.5, va="top")
ax.set_xlim(-0.2, 4.0)
ax.set_ylim(8, 52)
ax.set_xlabel("Tiempo relativo al impacto [s]")
ax.set_ylabel("Distancia [m] + amplitud normalizada")
ax.grid(True, color="#e6e6e6", lw=0.6)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(dst, bbox_inches="tight", facecolor="white")
print("escrito", dst)
