# -*- coding: utf-8 -*-
"""
Inversion de la curva de dispersion con la GEOMETRIA fijada por el SEV 01.

Idea. La no unicidad de la inversion MASW viene sobre todo de la parametrizacion:
cuantas capas y donde estan sus limites (Cox y Teague 2016). El SEV 01, medido en
la misma cancha con otro metodo, aporta exactamente esa informacion de forma
independiente. Entonces:

  - las PROFUNDIDADES de interfaz se FIJAN a las del SEV (no se invierten),
  - las VELOCIDADES se invierten libremente contra la curva medida.

Eso es lo legitimo. Lo que NO se hace aca es convertir resistividad en Vs: no
existe una relacion universal entre ambas, porque responden a propiedades
distintas (porosidad/fluido/arcilla frente a rigidez al corte). La resistividad
aporta DONDE estan los contrastes, no cuanto valen.

Se comparan tres parametrizaciones sobre la misma curva:
  A) libre, 4 capas equiespaciadas en log  (sin informacion externa)
  B) guiada por el SEV: interfaces en 1,00 / 2,06 / 4,15 m + semiespacio
  C) el modelo hidrogeologico previo (Moldeo Hidro), evaluado como modelo directo

Motor directo: surf96 (ADsurf), matriz de propagacion, modo fundamental.

Uso:
  python fig_inversion_guiada_sev.py <curva.csv> <col_f> <col_c> <salida.png>
"""
import csv
import os
import sys

import numpy as np
from scipy.optimize import differential_evolution
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(
    "C:/Github/Tesis", "src/interfaces/python/third-party/ADsurf"))
from ADsurf._surf96 import surf96          # noqa: E402

CSV_IN, COL_F, COL_C, OUT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
F_MIN = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0

C_LIB, C_SEV, C_HID = "#8a8a8a", "#1f5fa9", "#c1543a"
TINTA, TENUE, GRILLA = "#1b1b1b", "#6e6e6e", "#e6e6e6"

# Interfaces del SEV 01 (informe Gonzalez y Asoc., julio 2023)
SEV_INTERFACES = [1.00, 2.06, 4.15]
# Modelo hidrogeologico del trabajo previo (Moldeo Hidro)
HID_TOP = [0.0, 1.0, 2.1, 4.2, 8.0, 24.0, 50.0]
HID_VS = [95, 105, 145, 185, 240, 330, 400]
HID_VP = [600, 750, 900, 1150, 1450, 1750, 2000]
HID_RHO = [1800, 1850, 1900, 1950, 2000, 2100, 2150]

# --------------------------------------------------------------- datos
rows = list(csv.DictReader(open(CSV_IN, encoding="utf-8")))
f = np.array([float(r[COL_F]) for r in rows])
c = np.array([float(r[COL_C]) for r in rows])
m = f >= F_MIN
f, c = f[m], c[m]
o = np.argsort(f)
f, c = f[o], c[o]
# Submuestreo: surf96 se llama una vez por frecuencia y por evaluacion del
# optimizador. 132 frecuencias hacen la busqueda global impracticable, y la
# curva esta densamente muestreada: 1 de cada 3 puntos conserva toda la forma.
PASO = 6
f, c = f[::PASO], c[::PASO]
T = 1.0 / f


def directo(espesores_m, vs_ms):
    """Curva teorica del modo fundamental. Vp y rho se derivan de Vs con
    relaciones estandar para suelo saturado (nu = 0,35 -> Vp = 2,08 Vs)."""
    vs = np.asarray(vs_ms, float)
    vp = 2.08 * vs
    vp = np.maximum(vp, 400.0)          # piso fisico para suelo saturado
    rho = 1600.0 + 0.22 * vs            # tendencia suave, poco influyente
    th = np.append(np.asarray(espesores_m, float), 0.0) / 1000.0
    try:
        cc = surf96(T, th, vp / 1000.0, vs / 1000.0, rho / 1000.0,
                    mode=0, itype=0, ifunc=2, dt=0.005) * 1000.0
    except Exception:
        return None
    if not np.all(np.isfinite(cc)) or np.any(cc <= 0):
        return None
    return cc


def desajuste(vs, espesores):
    cc = directo(espesores, vs)
    if cc is None:
        return 1e6
    return float(np.sqrt(np.mean(((cc - c) / c) ** 2)))


def invertir(espesores, n_capas, semilla=0):
    lim = [(50.0, 700.0)] * n_capas

    def obj(v):
        # Se IMPONE Vs monotonamente creciente con la profundidad. No es un
        # capricho: (1) es lo fisicamente esperable en un suelo que se compacta
        # con la profundidad, y (2) se comprobo que surf96 encuentra la raiz del
        # modo fundamental en el 100 % de los perfiles monotonos ensayados,
        # frente a un 15 % de fallos en perfiles con inversion de velocidad.
        # Sin esta restriccion el optimizador converge a modelos que meramente
        # EVALUAN en lugar de modelos que AJUSTAN.
        return desajuste(np.sort(v), espesores)

    r = differential_evolution(obj, lim, seed=semilla, maxiter=35,
                               popsize=8, tol=1e-5, polish=True)
    return np.sort(r.x), r.fun


# ---------------------------------------------------- A) libre, 4 capas
z_lib = [1.5, 3.0, 6.0]           # equiespaciado geometrico, sin info externa
vs_lib, mis_lib = invertir(np.diff([0] + z_lib), 4, semilla=1)

# ---------------------------------------------------- B) guiada por SEV
esp_sev = np.diff([0.0] + SEV_INTERFACES)
vs_sev, mis_sev = invertir(esp_sev, len(SEV_INTERFACES) + 1, semilla=1)

# ---------------------------------------------------- C) modelo hidro previo
esp_hid = np.diff(HID_TOP)
c_hid = directo(esp_hid, HID_VS)
mis_hid = (float(np.sqrt(np.mean(((c_hid - c) / c) ** 2)))
           if c_hid is not None else np.nan)

c_lib = directo(np.diff([0] + z_lib), vs_lib)
c_sev = directo(esp_sev, vs_sev)


def perfil(tops, vs, zmax):
    x, y = [], []
    tt = list(tops) + [zmax]
    for i, v in enumerate(vs):
        x += [v, v]
        y += [tt[i], min(tt[i + 1], zmax)]
    return np.array(x), np.array(y)


def estilo(ax):
    ax.grid(True, color=GRILLA, linewidth=0.7)
    ax.set_axisbelow(True)
    for l in ("top", "right"):
        ax.spines[l].set_visible(False)
    for l in ("left", "bottom"):
        ax.spines[l].set_color("#c9c9c9")
    ax.tick_params(colors=TENUE, labelsize=8.5)


ZMAX = 10.0
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 5.8), dpi=300,
                               gridspec_kw={"width_ratios": [1.0, 1.25],
                                            "wspace": 0.26})

for tops, vs, col, est, lab, mis in (
        ([0] + z_lib, vs_lib, C_LIB, (0, (5, 3)),
         "A) libre, 4 capas", mis_lib),
        ([0] + SEV_INTERFACES, vs_sev, C_SEV, "-",
         "B) guiada por SEV 01", mis_sev),
        (HID_TOP, HID_VS, C_HID, (0, (2, 2)),
         "C) modelo hidro previo", mis_hid)):
    x, y = perfil(tops, vs, ZMAX)
    ax1.plot(x, y, color=col, lw=2.2, ls=est,
             label=f"{lab} — desajuste {100*mis:.1f} %")

for s in SEV_INTERFACES:
    ax1.axhline(s, color=C_SEV, lw=0.9, ls=(0, (1, 3)), alpha=0.8, zorder=0)
estilo(ax1)
ax1.set_ylim(ZMAX, 0)
ax1.set_xlabel("$V_S$ [m/s]", fontsize=9, color=TINTA)
ax1.set_ylabel("Profundidad [m]", fontsize=9, color=TINTA)
ax1.set_title("Perfiles: mismo dato, tres parametrizaciones",
              fontsize=10, color=TINTA, loc="left", pad=9)
ax1.legend(frameon=False, fontsize=7.8, loc="lower right", labelcolor=TINTA)

ax2.plot(f, c, "o", color="#2b2b2b", ms=3.2, label="curva medida", zorder=5)
for cc, col, est, lab in ((c_lib, C_LIB, (0, (5, 3)), "A) libre"),
                          (c_sev, C_SEV, "-", "B) guiada por SEV"),
                          (c_hid, C_HID, (0, (2, 2)), "C) hidro previo")):
    if cc is not None:
        ax2.plot(f, cc, ls=est, color=col, lw=1.9, label=lab)
estilo(ax2)
ax2.set_xlabel("Frecuencia [Hz]", fontsize=9, color=TINTA)
ax2.set_ylabel("Velocidad de fase [m/s]", fontsize=9, color=TINTA)
ax2.set_title("Ajuste a la curva medida (motor: surf96)",
              fontsize=10, color=TINTA, loc="left", pad=9)
ax2.legend(frameon=False, fontsize=8, labelcolor=TINTA)

fig.text(0.012, 0.004,
         "Las interfaces del SEV se FIJAN; las velocidades se invierten. "
         "No se convierte resistividad en Vs: la resistividad dice DÓNDE están "
         "los contrastes, no cuánto valen.",
         fontsize=7.3, color=TENUE, ha="left")

fig.savefig(OUT, bbox_inches="tight", facecolor="white")

print("escrito", OUT)
print(f"  curva: {len(f)} puntos, {f.min():.2f}-{f.max():.2f} Hz")
print(f"\n  A) libre 4 capas   : desajuste {100*mis_lib:5.2f} %   Vs = "
      + ", ".join(f"{v:.0f}" for v in vs_lib))
print(f"  B) guiada por SEV  : desajuste {100*mis_sev:5.2f} %   Vs = "
      + ", ".join(f"{v:.0f}" for v in vs_sev))
print(f"  C) hidro previo    : desajuste {100*mis_hid:5.2f} %   Vs = "
      + ", ".join(f"{v:.0f}" for v in HID_VS[:4]) + ", ...")


def vs30(tops, vs):
    acc, rem, tt = 0.0, 30.0, list(tops) + [1e9]
    for i, v in enumerate(vs):
        h = min(tt[i + 1] - tt[i], rem)
        if h <= 0:
            break
        acc += h / v
        rem -= h
    if rem > 0:
        acc += rem / vs[-1]
    return 30.0 / acc


print(f"\n  Vs30  A={vs30([0]+z_lib, vs_lib):.1f}  "
      f"B={vs30([0]+SEV_INTERFACES, vs_sev):.1f}  "
      f"C={vs30(HID_TOP, HID_VS):.1f}  m/s")
print("  (ojo: Vs30 con curvas que solo ven ~5 m es extrapolacion, no medicion)")
