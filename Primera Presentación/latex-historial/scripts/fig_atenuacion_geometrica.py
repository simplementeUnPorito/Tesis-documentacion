# -*- coding: utf-8 -*-
"""
Decaimiento de la amplitud del geofono con la distancia, y que tipo de onda implica.

Es una verificacion fisica barata y fuerte de que lo registrado son ondas
superficiales y no otra cosa. La teoria (Foti, seccion 2.4.3) dice:

  ondas de cuerpo en superficie ~ 1/r^2 ; en el interior ~ 1/r
  ondas Rayleigh               ~ 1/sqrt(r)   -> exponente -0,5

Ajustando log(A) = log(A0) - n*log(r) sobre los datos propios se obtiene n. Si da
cerca de 0,5, lo registrado esta dominado por ondas superficiales, que es
exactamente la hipotesis sobre la que descansa todo el metodo MASW.

Se separa por banda porque el contenido util no es el mismo en todas
(vease el analisis de banda util): las bandas sin senal deberian dar un
exponente cercano a CERO, porque un piso de ruido no se atenua con la distancia.
Eso convierte la figura en un segundo diagnostico independiente.

Salida: figuras/atenuacion_geometrica.png
"""
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DIR, OUT = sys.argv[1], sys.argv[2]

BANDAS = [(1, 5, "#c1543a"), (5, 10, "#d69f3a"),
          (10, 20, "#1f5fa9"), (20, 50, "#3f7d4e")]
TINTA, TENUE, GRILLA = "#1b1b1b", "#6e6e6e", "#e6e6e6"
T_SENAL = 1.0


def banda_rms(x, fs, a, b):
    """Amplitud RMS de x limitada a la banda [a,b), por FFT."""
    n = len(x)
    X = np.fft.rfft(np.asarray(x, float) - np.mean(x))
    f = np.fft.rfftfreq(n, 1.0 / fs)
    X[(f < a) | (f >= b)] = 0
    return float(np.sqrt(np.mean(np.abs(np.fft.irfft(X, n)) ** 2)))


datos = {}   # (a,b) -> {dist: [amplitudes]}
for sub in sorted(os.listdir(DIR)):
    d = os.path.join(DIR, sub)
    if not os.path.isdir(d):
        continue
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".npz"):
            continue
        try:
            z = np.load(os.path.join(d, fn), allow_pickle=True)
            fs = float(z["fs"]); g = np.asarray(z["geo_v"], float)
            i0 = int(z["trigger_index"]); dist = float(z["distance_m"])
        except Exception:
            continue
        if dist <= 0:
            continue                      # log(0): la posicion 0 m no entra
        n = int(T_SENAL * fs)
        if i0 + n > len(g):
            continue
        seg = g[i0:i0 + n]
        for a, b, _ in BANDAS:
            if b > fs / 2:
                continue
            datos.setdefault((a, b), {}).setdefault(dist, []).append(
                banda_rms(seg, fs, a, b))

fig, ax = plt.subplots(figsize=(9.2, 6.2), dpi=200)
resumen = []

for a, b, col in BANDAS:
    g = datos.get((a, b))
    if not g:
        continue
    ds = sorted(k for k, v in g.items() if len(v) >= 3)
    if len(ds) < 4:
        continue
    amp = np.array([np.median(g[d]) for d in ds])
    r = np.array(ds, float)
    # Normalizar a la primera distancia para poder superponer las bandas
    amp_n = amp / amp[0]
    ax.loglog(r, amp_n, "o", color=col, ms=5, mec="white", mew=0.7, zorder=4)
    # Ajuste log-log
    n_exp, log_a0 = np.polyfit(np.log10(r), np.log10(amp_n), 1)
    rr = np.array([r.min(), r.max()])
    ax.loglog(rr, 10 ** (log_a0 + n_exp * np.log10(rr)), "-", color=col, lw=1.8,
              label=f"{a}–{b} Hz:  $n$ = {-n_exp:.2f}", zorder=3)
    # Coeficiente de determinacion
    pred = log_a0 + n_exp * np.log10(r)
    ss_res = np.sum((np.log10(amp_n) - pred) ** 2)
    ss_tot = np.sum((np.log10(amp_n) - np.mean(np.log10(amp_n))) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
    resumen.append((a, b, -n_exp, r2, len(ds), int(sum(len(g[d]) for d in ds))))

# Referencias teoricas, ancladas al primer punto
ref_r = np.array([10.0, 50.0])
for n_t, est, lab in ((0.5, (0, (5, 3)), r"Rayleigh: $1/\sqrt{r}$  ($n$ = 0,5)"),
                      (1.0, (0, (2, 2)), r"cuerpo interior: $1/r$  ($n$ = 1)"),
                      (2.0, (0, (1, 2)), r"cuerpo en superficie: $1/r^2$  ($n$ = 2)")):
    ax.loglog(ref_r, (ref_r / ref_r[0]) ** (-n_t), color="#8a8a8a", lw=1.3,
              ls=est, zorder=1, label=lab)

ax.grid(True, which="both", color=GRILLA, linewidth=0.7)
ax.set_axisbelow(True)
for l in ("top", "right"):
    ax.spines[l].set_visible(False)
for l in ("left", "bottom"):
    ax.spines[l].set_color("#c9c9c9")
ax.tick_params(colors=TENUE, labelsize=9)
ax.set_xlabel("Distancia fuente–receptor [m]", fontsize=9.5, color=TINTA)
ax.set_ylabel("Amplitud RMS en banda, normalizada al primer punto",
              fontsize=9.5, color=TINTA)
ax.set_title("Decaimiento geométrico medido: ¿qué tipo de onda se está registrando?",
             fontsize=11, color=TINTA, loc="left", pad=11)
ax.legend(frameon=False, fontsize=8.5, labelcolor=TINTA, loc="lower left")

fig.text(0.012, 0.005,
         "Ajuste log-log de A ∝ r^(−n) sobre la mediana por posición. "
         "Un piso de ruido daría n ≈ 0 porque no se atenúa con la distancia.",
         fontsize=7.4, color=TENUE, ha="left")

fig.savefig(OUT, bbox_inches="tight", facecolor="white")

print("escrito", OUT)
print(f"\n  {'banda':>10s} {'n':>6s} {'R2':>6s} {'posic':>6s} {'golpes':>7s}")
for a, b, n_exp, r2, nd, ng in resumen:
    print(f"  {f'{a}-{b} Hz':>10s} {n_exp:6.2f} {r2:6.2f} {nd:6d} {ng:7d}")
print("\n  Referencia: Rayleigh n=0,5 | cuerpo interior n=1 | cuerpo superficie n=2 | ruido n=0")
