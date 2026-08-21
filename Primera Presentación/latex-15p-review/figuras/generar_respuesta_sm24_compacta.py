"""Genera la respuesta compacta del SM-24 usada en el documento."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


out = Path(__file__).resolve().parent / "transductores" / "respuesta_sm24_vel_acel.png"
fn = 10.0
wn = 2.0 * np.pi * fn
zeta = 0.25
freq = np.logspace(-1, 2.25, 1200)
s = 1j * 2.0 * np.pi * freq
den = s**2 + 2.0 * zeta * wn * s + wn**2
hv = s**2 / den
ha = wn * s / den

fig, ax = plt.subplots(figsize=(4.25, 3.05), dpi=260)
ax.semilogx(
    freq, 20.0 * np.log10(np.abs(hv)),
    color="#c1543a", lw=1.8, label=r"Velocidad: $|H_v|/G_0$",
)
ax.semilogx(
    freq, 20.0 * np.log10(np.abs(ha)),
    color="#1f5fa9", lw=1.8,
    label=r"Aceleración: $\omega_n|H_a|/G_0$",
)
ax.axvline(fn, color="#6b4c9a", lw=1.1, ls=(0, (3, 2)))
ax.text(10.7, -55, r"$f_n=10$ Hz", color="#6b4c9a", fontsize=7.5)
ax.axhline(0, color="#777777", lw=0.7, ls=(0, (2, 2)))
ax.set(xlim=(0.1, 180), ylim=(-82, 10),
       xlabel="Frecuencia [Hz]", ylabel="Magnitud normalizada [dB]")
ax.set_title(r"SM-24 en circuito abierto ($\zeta=0{,}25$)", fontsize=9.5, loc="left")
ax.grid(True, which="major", color="#d8d8d8", lw=0.65)
ax.grid(True, which="minor", color="#eeeeee", lw=0.45)
ax.tick_params(labelsize=7.5, colors="#303030")
ax.legend(loc="lower right", frameon=True, framealpha=0.94, fontsize=7.2)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color("#b8b8b8")
fig.tight_layout(pad=0.7)
fig.savefig(out, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(out)
