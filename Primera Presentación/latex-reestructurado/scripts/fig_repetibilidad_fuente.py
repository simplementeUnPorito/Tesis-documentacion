# -*- coding: utf-8 -*-
"""
Repetibilidad de la fuente sismica, medida sobre el canal de martillo.

La apertura sintetica (mover un geofono y apilar golpes sucesivos) descansa en
una hipotesis nunca verificada: que el golpe es repetible. Este script la mide,
usando datos que ya existen desde julio y que nunca se habian analizado asi.

Para cada golpe se calcula, sobre la ventana del impacto en el canal de martillo:
  - amplitud pico (proxy de la energia entregada)
  - ancho del pulso a media altura de la envolvente
  - centroide espectral (proxy del contenido en frecuencia de la fuente)

Y luego, por posicion, el coeficiente de variacion entre golpes.

Entrada:  data/processed/Canchita_procesado/muestras/<NNNm>/*.npz
Salida:   figuras/repetibilidad_fuente.png  + repetibilidad_fuente.csv
"""
import csv
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DIR, OUT_PNG, OUT_CSV = sys.argv[1], sys.argv[2], sys.argv[3]

C_A = "#1f5fa9"    # amplitud
C_W = "#c1543a"    # ancho
C_F = "#3f7d4e"    # centroide
TINTA, TENUE, GRILLA = "#1b1b1b", "#6e6e6e", "#e6e6e6"

VENTANA_S = 0.25   # ventana alrededor del pico del martillo


def metricas(t, x, fs):
    """Amplitud pico, ancho a media altura y centroide espectral del impacto."""
    x = np.asarray(x, float)
    x = x - np.median(x)
    i = int(np.argmax(np.abs(x)))
    pico = float(np.abs(x[i]))
    if pico <= 0 or not np.isfinite(pico):
        return None
    n = max(8, int(VENTANA_S * fs))
    a, b = max(0, i - n // 2), min(len(x), i + n // 2)
    seg = x[a:b]
    if seg.size < 8:
        return None

    # Ancho a media altura sobre |x| suavizado: cuantas muestras superan pico/2
    ancho = float(np.sum(np.abs(seg) >= pico / 2.0) / fs)

    # Centroide espectral de la ventana del impacto
    win = seg * np.hanning(seg.size)
    esp = np.abs(np.fft.rfft(win))
    f = np.fft.rfftfreq(seg.size, 1.0 / fs)
    banda = (f >= 2.0) & (f <= min(400.0, fs / 2))
    if esp[banda].sum() <= 0:
        return None
    centroide = float((f[banda] * esp[banda]).sum() / esp[banda].sum())
    return pico, ancho, centroide


filas = []
for sub in sorted(os.listdir(DIR)):
    d = os.path.join(DIR, sub)
    if not os.path.isdir(d):
        continue
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".npz"):
            continue
        try:
            z = np.load(os.path.join(d, fn), allow_pickle=True)
            fs = float(z["fs"])
            m = metricas(z["time_s"], z["hammer_v"], fs)
            if m is None:
                continue
            filas.append({
                "distancia_m": float(z["distance_m"]),
                "archivo": fn, "fs_hz": fs,
                "pico_v": m[0], "ancho_s": m[1], "centroide_hz": m[2],
            })
        except Exception:
            continue

if not filas:
    raise SystemExit("sin golpes procesables")

with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(filas[0]))
    w.writeheader()
    w.writerows(filas)

# La nube de amplitudes es claramente BIMODAL, con un hueco vacio entre 3,08 y
# 3,22 V. No es recorte: son dos configuraciones de adquisicion distintas
# mezcladas en el mismo conjunto procesado (los 191 golpes a 2929 Hz caen todos
# del lado alto). Promediar las dos juntas inventa una dispersion que no existe,
# asi que se las separa y se informa el CV DENTRO de cada configuracion.
CORTE_V = 3.15
for r in filas:
    r["config"] = "A" if r["pico_v"] > CORTE_V else "B"

CONFIGS = ["A", "B"]
res = {}
for cfg in CONFIGS:
    sub = [r for r in filas if r["config"] == cfg]
    dists = sorted({r["distancia_m"] for r in sub})
    lista = []
    for d in dists:
        g = [r for r in sub if r["distancia_m"] == d]
        if len(g) < 3:
            continue
        fila = {"d": d, "n": len(g)}
        for k, etq in (("pico_v", "amp"), ("ancho_s", "anc"), ("centroide_hz", "cen")):
            v = np.array([x[k] for x in g], float)
            fila[etq + "_med"] = float(np.median(v))
            fila[etq + "_cv"] = (float(100 * np.std(v) / np.mean(v))
                                 if np.mean(v) else np.nan)
            fila[etq + "_vals"] = v
        lista.append(fila)
    res[cfg] = lista


def estilo(ax):
    ax.grid(True, color=GRILLA, linewidth=0.7)
    ax.set_axisbelow(True)
    for l in ("top", "right"):
        ax.spines[l].set_visible(False)
    for l in ("left", "bottom"):
        ax.spines[l].set_color("#c9c9c9")
    ax.tick_params(colors=TENUE, labelsize=8.5)
    ax.set_xlabel("Distancia fuente--receptor [m]", fontsize=9, color=TINTA)


fig, axes = plt.subplots(3, 1, figsize=(4.10, 3.71), dpi=300, sharex=True,
                         gridspec_kw={"hspace": 0.22})

ESTILO_CFG = {"A": dict(marker="o", ls="-", lab="Configuración A (incluye todo 2929 Hz)"),
              "B": dict(marker="s", ls=(0, (5, 3)), lab="Configuración B (sólo 1020 Hz)")}
ALPHA = {"A": 1.0, "B": 0.55}

for ax, (etq, col, lab, uni) in zip(axes, [
        ("amp", C_A, "Amplitud pico del golpe", "V"),
        ("anc", C_W, "Ancho del pulso a media altura", "ms"),
        ("cen", C_F, "Centroide espectral de la fuente", "Hz")]):
    txt = []
    for cfg in CONFIGS:
        lst = res[cfg]
        if not lst:
            continue
        e = ESTILO_CFG[cfg]
        for r in lst:
            v = r[etq + "_vals"] * (1000 if etq == "anc" else 1)
            ax.plot([r["d"]] * len(v), v, "o", color=col, ms=2.6,
                    alpha=0.20 * ALPHA[cfg], mew=0)
        xs = [r["d"] for r in lst]
        med = [r[etq + "_med"] * (1000 if etq == "anc" else 1) for r in lst]
        ax.plot(xs, med, ls=e["ls"], color=col, lw=1.9, zorder=4,
                alpha=ALPHA[cfg], label=e["lab"] if etq == "amp" else "_")
        ax.plot(xs, med, e["marker"], color=col, ms=4.6, zorder=5,
                mec="white", mew=0.8, alpha=ALPHA[cfg])
        cvs = np.array([r[etq + "_cv"] for r in lst], float)
        txt.append(f"{cfg}: {np.nanmedian(cvs):.0f} %")
    estilo(ax)
    ax.set_ylabel(f"{lab}\n[{uni}]", fontsize=8.5, color=TINTA)
    ax.text(0.995, 0.94, "CV mediano dentro de cada configuración — " + ",  ".join(txt),
            transform=ax.transAxes, fontsize=8, color=col, ha="right", va="top")

axes[0].axhspan(3.08, 3.22, color="#999999", alpha=0.30, zorder=0)
axes[0].text(0.5, 3.15, "hueco vacío: no hay ningún golpe aquí",
             fontsize=7.2, color="#555555", va="center")
axes[0].legend(frameon=False, fontsize=7.8, loc="lower right", labelcolor=TINTA)

for ax in axes[:-1]:
    ax.set_xlabel("")
axes[0].set_title(
    f"Repetibilidad del golpe: {len(filas)} golpes en "
    f"{len({r['distancia_m'] for r in filas})} posiciones (Canchita, julio 2026)",
    fontsize=10.5, color=TINTA, loc="left", pad=10)
fig.text(0.012, 0.004,
         "Puntos claros: cada golpe. Líneas: mediana por posición. El conjunto procesado "
         "MEZCLA DOS CONFIGURACIONES de adquisición; promediarlas juntas inventa una "
         "dispersión que no existe.\nEl canal de martillo mide FUERZA (sensor PCB 086D20).",
         fontsize=7.2, color=TENUE, ha="left")

fig.savefig(OUT_PNG, bbox_inches="tight", facecolor="white")

print("escrito", OUT_PNG, "y", OUT_CSV)
print(f"  {len(filas)} golpes en {len({r['distancia_m'] for r in filas})} posiciones")
for cfg in CONFIGS:
    sub = [r for r in filas if r["config"] == cfg]
    lst = res[cfg]
    fss = sorted({r["fs_hz"] for r in sub})
    print(f"\n  --- configuracion {cfg}: {len(sub)} golpes, {len(lst)} posiciones "
          f"con n>=3, fs={fss}")
    for etq, nom in (("amp", "amplitud"), ("anc", "ancho"), ("cen", "centroide")):
        cvs = np.array([r[etq + "_cv"] for r in lst], float)
        if not len(cvs):
            continue
        print(f"    CV {nom:10s}: mediana {np.nanmedian(cvs):6.1f} %  "
              f"min {np.nanmin(cvs):5.1f} %  max {np.nanmax(cvs):6.1f} %")
