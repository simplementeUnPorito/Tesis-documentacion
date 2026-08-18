"""Genera una vista tiempo-frecuencia reproducible de una captura real a 24 m."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


ROOT = Path(r"C:\Github\Tesis")
CSV = ROOT / "data/raw/Canchiga/muestra24metros_20260703_170413/combined/signals.csv"
OUT = Path(__file__).with_name("espectrograma_campo_24m.png")
CAPTURE = "2"

hammer_t, hammer_v, geo_t, geo_v = [], [], [], []
fs = None
with CSV.open(encoding="utf-8", newline="") as stream:
    for row in csv.DictReader(stream):
        if row["capture_order"] != CAPTURE:
            continue
        fs = float(row["fs_hz"])
        if row["node_role"] == "hammer":
            hammer_t.append(float(row["aligned_time_s"]))
            hammer_v.append(float(row["value_v"]))
        elif row["node_role"] == "geo":
            geo_t.append(float(row["aligned_time_s"]))
            geo_v.append(float(row["value_v"]))

hammer_t = np.asarray(hammer_t)
hammer_v = signal.detrend(np.asarray(hammer_v))
geo_t = np.asarray(geo_t)
geo_v = signal.detrend(np.asarray(geo_v))
t0 = hammer_t[np.argmax(np.abs(hammer_v))]
t = geo_t - t0

# La vista no inventa baja frecuencia: solo remueve continua y limita el gráfico.
f, ts, sxx = signal.spectrogram(
    geo_v,
    fs=fs,
    window="hann",
    nperseg=512,
    noverlap=448,
    detrend="constant",
    scaling="density",
    mode="psd",
)
ts = ts + geo_t[0] - t0
sdb = 10 * np.log10(np.maximum(sxx, np.finfo(float).tiny))
mask_f = (f >= 1) & (f <= 100)
mask_t = (ts >= -0.2) & (ts <= 1.5)

plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
fig, (ax0, ax1) = plt.subplots(2, 1, figsize=(10.5, 5.6), dpi=180, sharex=True,
                               gridspec_kw={"height_ratios": [1, 2.1], "hspace": 0.10})
wmask = (t >= -0.2) & (t <= 1.5)
ax0.plot(t[wmask], geo_v[wmask], color="#245fa8", lw=0.8)
ax0.axvline(0, color="#c65438", ls="--", lw=1)
ax0.set_ylabel("amplitud [V]")
ax0.set_title("Captura real a 24 m: forma de onda y espectrograma")
ax0.grid(alpha=0.25)

mesh = ax1.pcolormesh(ts[mask_t], f[mask_f], sdb[np.ix_(mask_f, mask_t)],
                      shading="auto", cmap="magma")
ax1.axhspan(1, 5, color="#56a6cf", alpha=0.16, label="banda objetivo profunda")
ax1.axhline(10, color="white", ls="--", lw=1.0, alpha=0.9, label="$f_n$ SM-24")
ax1.axvline(0, color="white", ls=":", lw=1)
ax1.set(xlabel="tiempo relativo al impacto [s]", ylabel="frecuencia [Hz]", ylim=(1, 100))
ax1.legend(loc="upper right", framealpha=0.85, fontsize=8)
fig.colorbar(mesh, ax=ax1, pad=0.012, label="PSD [dB/Hz]")
fig.text(0.01, 0.005,
         "El registro concentra energía visible por encima de 10 Hz; la banda 1–5 Hz queda próxima al piso de ruido.",
         fontsize=8, color="#555555")
fig.savefig(OUT, bbox_inches="tight", facecolor="white")
print(OUT)
