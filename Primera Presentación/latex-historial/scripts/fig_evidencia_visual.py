# -*- coding: utf-8 -*-
"""Genera figuras visuales complementarias para los dos libros de tesis.

Las figuras de campo se construyen desde los binarios y metadatos de Canchita;
las figuras conceptuales son esquemas propios y no reutilizan material externo.

Uso:
    python fig_evidencia_visual.py data/raw/Canchita figuras/
"""
import glob
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle
import numpy as np


RAW = sys.argv[1]
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)

BLUE = "#1f5fa9"
RED = "#c1543a"
GREEN = "#3f7d4e"
PURPLE = "#73538f"
ORANGE = "#d2872c"
INK = "#1b1b1b"
MUTED = "#696969"
GRID = "#e7e7e7"
FS_TARGET = 1020.0


def clean(ax, grid=True):
    if grid:
        ax.grid(True, color=GRID, lw=0.7)
        ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#c8c8c8")
    ax.tick_params(colors=MUTED, labelsize=8)


def load_bin(base, rel, count=None):
    path = os.path.join(base, rel.replace("/", os.sep))
    if not os.path.isfile(path):
        return None
    values = np.fromfile(path, dtype="<f4")
    return values[:count] if count and values.size >= count else values


def scan_field():
    """Una captura completa por posicion, sin mezclar tasas de muestreo."""
    selected = {}
    for folder in sorted(glob.glob(os.path.join(RAW, "muestra*"))):
        meta_path = os.path.join(folder, "metadata.json")
        if not os.path.isfile(meta_path) or not os.path.isdir(folder):
            continue
        try:
            with open(meta_path, encoding="utf-8") as handle:
                meta = json.load(handle)
        except Exception:
            continue
        for capture in meta.get("captures", []):
            nodes = {str(n.get("role", "")).lower(): n
                     for n in capture.get("nodes", [])}
            geo = nodes.get("geo")
            hammer = nodes.get("hammer")
            if not geo or not hammer:
                continue
            if float(geo.get("fs") or 0) != FS_TARGET:
                continue
            position = geo.get("position_m")
            if position is None or float(position) in selected:
                continue
            raw_geo = load_bin(folder, geo.get("raw_file", ""), geo.get("raw_count"))
            filt_geo = load_bin(folder, geo.get("filt_file", ""), geo.get("filt_count"))
            raw_hammer = load_bin(folder, hammer.get("raw_file", ""), hammer.get("raw_count"))
            if raw_geo is None or raw_hammer is None or raw_geo.size < 900:
                continue
            selected[float(position)] = {
                "geo": raw_geo.astype(float),
                "filt": None if filt_geo is None else filt_geo.astype(float),
                "hammer": raw_hammer.astype(float),
                "folder": os.path.basename(folder),
                "capture": capture.get("label", capture.get("id", "")),
            }
    return selected


FIELD = scan_field()
if not FIELD:
    raise SystemExit("No se encontraron capturas de campo a 1020 Hz")


def aligned_window(record, pre=0.12, post=1.05):
    geo = record["geo"]
    hammer = record["hammer"]
    impact = int(np.argmax(np.abs(hammer - np.median(hammer))))
    npre, npost = int(pre * FS_TARGET), int(post * FS_TARGET)
    start, stop = impact - npre, impact + npost
    if start < 0 or stop > min(geo.size, hammer.size):
        return None
    t = np.arange(-npre, npost) / FS_TARGET
    filt = record["filt"]
    if filt is not None and stop <= filt.size:
        filt = filt[start:stop]
    else:
        filt = None
    return t, hammer[start:stop], geo[start:stop], filt


def nearest_position(target):
    return min(FIELD, key=lambda p: abs(p - target))


# ------------------------------------------------------------------- teoria
fig, axes = plt.subplots(1, 3, figsize=(11.0, 3.55), dpi=220)
depth = np.linspace(0, 1, 400)
for ax, cycles, penetration, title, color in (
        (axes[0], 7, 0.18, "Frecuencia alta", RED),
        (axes[1], 2.2, 0.52, "Frecuencia baja", BLUE)):
    x = np.linspace(0, 1, 700)
    wave = 0.08 * np.sin(2 * np.pi * cycles * x)
    ax.plot(x, 0.08 + wave, color=color, lw=1.8)
    for frac, shade in ((0.0, "#f3f3f3"), (0.33, "#e4e4e4"), (0.66, "#d6d6d6")):
        ax.add_patch(Rectangle((0, frac), 1, 0.34, fc=shade, ec="none", zorder=-3))
    envelope = np.exp(-depth / penetration)
    ax.plot(0.5 + 0.33 * envelope, depth, color=color, lw=2.3)
    ax.fill_betweenx(depth, 0.5, 0.5 + 0.33 * envelope,
                     color=color, alpha=0.16)
    ax.axvline(0.5, color="#bcbcbc", lw=0.8)
    ax.invert_yaxis()
    ax.set_xlim(0, 1)
    ax.set_ylim(1, -0.02)
    ax.set_xticks([])
    ax.set_yticks([0, 0.33, 0.66, 1.0])
    ax.set_yticklabels(["superficie", "capa 1", "capa 2", "capa 3"])
    ax.set_title(title, fontsize=10, loc="left")
    ax.set_xlabel("amplitud relativa con profundidad", fontsize=8)
    clean(ax, grid=False)

ax = axes[2]
f = np.logspace(np.log10(3), np.log10(80), 220)
velocity = 72 + 47 / (1 + np.exp(-(np.log10(f) - np.log10(13)) * 6))
ax.semilogx(f, velocity, color=PURPLE, lw=2.2)
ax.fill_between(f, velocity - 6, velocity + 6, color=PURPLE, alpha=0.13)
for ff in (5, 10, 20, 40):
    cc = np.interp(ff, f, velocity)
    ax.plot(ff, cc, "o", color=PURPLE, mec="white", mew=0.8)
    ax.text(ff, cc + 7, f"{cc/ff:.1f} m", ha="center", fontsize=7, color=MUTED)
ax.set_xlabel("Frecuencia [Hz]", fontsize=8.5)
ax.set_ylabel("Velocidad de fase [m/s]", fontsize=8.5)
ax.set_title("Curva de dispersion y longitud de onda", fontsize=10, loc="left")
ax.text(0.04, 0.05, "$\\lambda=c/f$: cada frecuencia sondea una escala distinta",
        transform=ax.transAxes, fontsize=7.5, color=MUTED)
clean(ax)
fig.suptitle("Por que las ondas Rayleigh permiten reconstruir un perfil con profundidad",
             x=0.03, ha="left", fontsize=12, weight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.92))
fig.savefig(os.path.join(OUT, "fundamentos_dispersion.png"), bbox_inches="tight",
            facecolor="white")
plt.close(fig)


# -------------------------------------------------------------- SM-24 propio
fn = 10.0
wn = 2 * np.pi * fn
freq = np.logspace(-2, 3, 1600)
w = 2 * np.pi * freq
s = 1j * w

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 3.8), dpi=220)
for zeta, color, label in ((0.25, RED, "$\\zeta=0{,}25$ (abierto)"),
                           (0.60, BLUE, "$\\zeta=0{,}60$ (shunt nominal)")):
    hv = s ** 2 / (s ** 2 + 2 * zeta * wn * s + wn ** 2)
    ax1.semilogx(freq, 20 * np.log10(np.abs(hv)), color=color, lw=2, label=label)
    phase = np.unwrap(np.angle(hv)) * 180 / np.pi
    ax2.semilogx(freq, phase, color=color, lw=2, label=label)
for ax in (ax1, ax2):
    ax.axvline(fn, color=MUTED, lw=1, ls=(0, (4, 3)))
    ax.text(fn * 1.08, ax.get_ylim()[0] + 0.08 * np.diff(ax.get_ylim())[0],
            "$f_n=10$ Hz", fontsize=7.5, color=MUTED)
    ax.set_xlabel("Frecuencia [Hz]", fontsize=9)
    clean(ax)
ax1.set_ylabel("Magnitud relativa [dB]", fontsize=9)
ax2.set_ylabel("Fase [grados]", fontsize=9)
ax1.set_title("Respuesta a velocidad del suelo", fontsize=10, loc="left")
ax2.set_title("Rotacion de fase alrededor de la resonancia", fontsize=10, loc="left")
ax1.legend(frameon=False, fontsize=8, loc="lower right")
fig.suptitle("Modelo nominal del geofono SM-24", x=0.04, ha="left",
             fontsize=12, weight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.91))
fig.savefig(os.path.join(OUT, "respuesta_sm24_modelo.png"), bbox_inches="tight",
            facecolor="white")
plt.close(fig)


# --------------------------------------------------------- captura individual
pos_one = nearest_position(24)
window = aligned_window(FIELD[pos_one])
if window is None:
    raise SystemExit("La captura elegida no contiene una ventana valida")
t, hammer, geo, filt = window
hammer0 = hammer - np.median(hammer[t < 0])
geo0 = geo - np.median(geo[t < 0])
filt0 = None if filt is None else filt - np.median(filt[t < 0])

fig, axes = plt.subplots(3, 1, figsize=(10.6, 6.15), dpi=220, sharex=True)
axes[0].plot(t, hammer, color=ORANGE, lw=1.0)
axes[0].axvline(0, color=RED, lw=1, ls=(0, (4, 3)))
axes[0].set_ylabel("Martillo [V]", fontsize=8.5)
axes[0].set_title("Canal crudo de referencia del impacto", fontsize=10, loc="left")

axes[1].plot(t, geo, color=BLUE, lw=0.85)
axes[1].axhline(np.median(geo[t < 0]), color=MUTED, lw=0.8, ls=(0, (4, 3)))
axes[1].set_ylabel("Geofono crudo [V]", fontsize=8.5)
axes[1].set_title("Registro preservado, incluido su nivel de continua", fontsize=10, loc="left")

axes[2].plot(t, geo0, color="#a8a8a8", lw=0.75, label="crudo centrado")
if filt0 is not None:
    axes[2].plot(t, filt0, color=BLUE, lw=1.2, label="salida FIR centrada")
axes[2].axvline(0, color=RED, lw=1, ls=(0, (4, 3)))
axes[2].set_ylabel("Amplitud [V]", fontsize=8.5)
axes[2].set_xlabel("Tiempo relativo al impacto [s]", fontsize=9)
axes[2].set_title("Vista de trabajo para alineacion y procesamiento", fontsize=10, loc="left")
axes[2].legend(frameon=False, fontsize=8, ncol=2)
for ax in axes:
    clean(ax)
fig.suptitle(f"Ejemplo de adquisicion real a {pos_one:.0f} m - {FIELD[pos_one]['capture']}",
             x=0.04, ha="left", fontsize=12, weight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig(os.path.join(OUT, "captura_cruda_campo.png"), bbox_inches="tight",
            facecolor="white")
plt.close(fig)


# -------------------------------------------- registros y espectros por rango
targets = [10, 24, 38, 50]
chosen = []
for target in targets:
    p = nearest_position(target)
    if p not in chosen:
        chosen.append(p)

fig, axes = plt.subplots(len(chosen), 2, figsize=(10.8, 7.3), dpi=220,
                         gridspec_kw={"width_ratios": [1.55, 1.0]})
if len(chosen) == 1:
    axes = np.asarray([axes])
for row, p in enumerate(chosen):
    win = aligned_window(FIELD[p], pre=0.06, post=0.80)
    if win is None:
        continue
    tt, _, gg, ffilt = win
    gg = gg - np.median(gg[tt < 0])
    use = gg if ffilt is None else ffilt - np.median(ffilt[tt < 0])
    scale = np.max(np.abs(use)) or 1.0
    axes[row, 0].plot(tt, use / scale, color=BLUE, lw=0.9)
    axes[row, 0].axvline(0, color=RED, lw=0.8, ls=(0, (4, 3)))
    axes[row, 0].text(0.99, 0.86, f"{p:.0f} m", transform=axes[row, 0].transAxes,
                      ha="right", fontsize=9, weight="bold", color=INK)
    axes[row, 0].set_ylim(-1.1, 1.1)
    axes[row, 0].set_ylabel("norm.", fontsize=8)
    clean(axes[row, 0])

    segment = use[tt >= 0]
    segment = segment - np.mean(segment)
    taper = np.hanning(segment.size)
    spec = np.abs(np.fft.rfft(segment * taper)) ** 2
    ff = np.fft.rfftfreq(segment.size, 1 / FS_TARGET)
    band = (ff >= 2) & (ff <= 150)
    db = 10 * np.log10(np.maximum(spec[band], np.finfo(float).tiny))
    db -= np.max(db)
    axes[row, 1].semilogx(ff[band], db, color=PURPLE, lw=1.2)
    axes[row, 1].set_ylim(-60, 3)
    axes[row, 1].set_ylabel("PSD rel. [dB]", fontsize=8)
    clean(axes[row, 1])
axes[-1, 0].set_xlabel("Tiempo desde el impacto [s]", fontsize=9)
axes[-1, 1].set_xlabel("Frecuencia [Hz]", fontsize=9)
axes[0, 0].set_title("Forma de onda filtrada, normalizada por registro",
                     fontsize=10, loc="left")
axes[0, 1].set_title("Contenido espectral posterior al impacto",
                     fontsize=10, loc="left")
fig.suptitle("Adquisiciones representativas a lo largo del arreglo virtual",
             x=0.04, ha="left", fontsize=12, weight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig(os.path.join(OUT, "adquisiciones_por_distancia.png"),
            bbox_inches="tight", facecolor="white")
plt.close(fig)


# ---------------------------------------------------------- mapa de amplitud
positions = []
traces = []
t_heat = None
for p in sorted(FIELD):
    win = aligned_window(FIELD[p], pre=0.05, post=0.70)
    if win is None:
        continue
    tt, _, gg, ffilt = win
    use = gg if ffilt is None else ffilt
    use = use - np.median(use[tt < 0])
    peak = np.max(np.abs(use)) or 1.0
    positions.append(p)
    traces.append(use / peak)
    t_heat = tt
matrix = np.asarray(traces)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.7, 5.3), dpi=220,
                               gridspec_kw={"width_ratios": [2.25, 1.0]})
extent = [t_heat[0], t_heat[-1], min(positions), max(positions)]
im = ax1.imshow(matrix, aspect="auto", origin="lower", extent=extent,
                cmap="RdBu_r", vmin=-0.75, vmax=0.75, interpolation="bilinear")
ax1.axvline(0, color="black", lw=0.8, ls=(0, (4, 3)))
ax1.set_xlabel("Tiempo desde el impacto [s]", fontsize=9)
ax1.set_ylabel("Distancia a la fuente [m]", fontsize=9)
ax1.set_title("Mapa tiempo-distancia (cada traza normalizada)", fontsize=10, loc="left")
clean(ax1, grid=False)
cb = fig.colorbar(im, ax=ax1, fraction=0.025, pad=0.02)
cb.set_label("amplitud relativa", fontsize=8)
cb.ax.tick_params(labelsize=7)

peak_times = []
for trace in matrix:
    post = t_heat >= 0
    peak_times.append(t_heat[post][np.argmax(np.abs(trace[post]))])
ax2.plot(peak_times, positions, "o-", color=GREEN, lw=1.4, ms=4,
         mec="white", mew=0.7)
ax2.set_xlabel("Tiempo del maximo [s]", fontsize=9)
ax2.set_ylabel("Distancia [m]", fontsize=9)
ax2.set_title("Maximo observado por posicion", fontsize=10, loc="left")
clean(ax2)
fig.suptitle("Vista densa de las adquisiciones de Canchita",
             x=0.04, ha="left", fontsize=12, weight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig(os.path.join(OUT, "mapa_tiempo_distancia.png"), bbox_inches="tight",
            facecolor="white")
plt.close(fig)


# ---------------------------------------------------------- flujo del sistema
fig, ax = plt.subplots(figsize=(11.3, 3.2), dpi=220)
ax.set_xlim(0, 15)
ax.set_ylim(0, 4)
ax.axis("off")
steps = [
    ("1", "Impacto", "martillo + canal de referencia", ORANGE),
    ("2", "Captura", "crudo y FIR por nodo", BLUE),
    ("3", "Alineacion", "pico del martillo + metadatos", GREEN),
    ("4", "Gather", "trazas por posicion virtual", PURPLE),
    ("5", "Dispersion", "imagen f-c y picks editables", RED),
    ("6", "Inversion", "perfil Vs exploratorio", BLUE),
]
for i, (num, title, detail, color) in enumerate(steps):
    x = 0.25 + i * 2.45
    patch = FancyBboxPatch((x, 1.0), 2.0, 1.65,
                           boxstyle="round,pad=0.04,rounding_size=0.10",
                           fc=color + "15", ec=color, lw=1.5)
    ax.add_patch(patch)
    ax.text(x + 0.18, 2.38, num, fontsize=12, weight="bold", color=color)
    ax.text(x + 1.0, 1.91, title, ha="center", fontsize=10, weight="bold", color=INK)
    ax.text(x + 1.0, 1.42, detail, ha="center", fontsize=7.3, color=MUTED,
            linespacing=1.2)
    if i < len(steps) - 1:
        ax.add_patch(FancyArrowPatch((x + 2.02, 1.82), (x + 2.41, 1.82),
                                     arrowstyle="-|>", mutation_scale=11,
                                     color=MUTED, lw=1.2))
ax.text(0.25, 3.45, "Del impacto al perfil: que evidencia produce cada etapa",
        fontsize=12, weight="bold", color=INK)
ax.text(0.25, 0.45,
        "El crudo se conserva; alineacion, filtrado, picking e inversion son operaciones reproducibles y revisables.",
        fontsize=8.2, color=MUTED)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "flujo_adquisicion_masw.png"), bbox_inches="tight",
            facecolor="white")
plt.close(fig)


# -------------------------------------------------------------- comparativas
fig, ax = plt.subplots(figsize=(10.8, 4.5), dpi=220)
ax.set_xlim(0, 10.8)
ax.set_ylim(0, 5)
ax.axis("off")
methods = [
    ("SPT / sondeo", "puntual", "invasivo", "alto", "referencia local", RED),
    ("SASW", "2 receptores", "activo", "medio", "barrido secuencial", ORANGE),
    ("MASW activo", "arreglo lineal", "activo", "alto", "adoptado", BLUE),
    ("ReMi / SPAC", "arreglo", "pasivo", "bajo", "extension futura", GREEN),
]
headers = ["Metodo", "Cobertura", "Fuente", "Resolucion", "Rol en el proyecto"]
widths = [2.05, 1.7, 1.45, 1.55, 3.25]
x0 = 0.15
x_positions = [x0]
for width in widths[:-1]:
    x_positions.append(x_positions[-1] + width)
for x, width, header in zip(x_positions, widths, headers):
    ax.add_patch(Rectangle((x, 4.15), width, 0.62, fc="#efefef", ec="white"))
    ax.text(x + 0.10, 4.46, header, va="center", fontsize=8.5, weight="bold")
for row, values in enumerate(methods):
    y = 3.35 - row * 0.86
    color = values[-1]
    for col, (x, width, value) in enumerate(zip(x_positions, widths, values[:-1])):
        bg = color + "12" if col == 0 else "#fafafa"
        ax.add_patch(Rectangle((x, y), width, 0.72, fc=bg, ec="white"))
        ax.text(x + 0.10, y + 0.36, value, va="center", fontsize=8.3,
                weight="bold" if col == 0 else "normal", color=INK)
ax.text(0.15, 4.92, "Comparacion visual de familias de caracterizacion somera",
        fontsize=12, weight="bold", color=INK)
ax.text(0.15, 0.15,
        "La eleccion de MASW no elimina la necesidad de contraste: el SPT queda como referencia externa del perfil Vs.",
        fontsize=8.2, color=MUTED)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "comparacion_metodos.png"), bbox_inches="tight",
            facecolor="white")
plt.close(fig)


# ---------------------------------------------------------- tablero de cierre
fig, ax = plt.subplots(figsize=(10.8, 4.55), dpi=220)
ax.set_xlim(0, 12)
ax.set_ylim(0, 5)
ax.axis("off")
items = [
    ("Transductor", "modelo + parametros", "documentado", GREEN),
    ("DA-AFE", "8 configuraciones", "medido", GREEN),
    ("Adquisicion", "10 min + SD", "funcional", GREEN),
    ("Sincronizacion", "PRESTART / GPIO", "falta jitter E2E", ORANGE),
    ("Campo", "21 posiciones", "exploratorio", ORANGE),
    ("MASW", "113 picks modo 0", "sin contraste SPT", ORANGE),
]
for i, (title, metric, status, color) in enumerate(items):
    col, row = i % 3, 1 - i // 3
    x, y = 0.35 + col * 3.9, 0.55 + row * 2.0
    patch = FancyBboxPatch((x, y), 3.35, 1.42,
                           boxstyle="round,pad=0.05,rounding_size=0.10",
                           fc=color + "12", ec=color, lw=1.4)
    ax.add_patch(patch)
    ax.add_patch(Rectangle((x + 0.22, y + 0.24), 0.12, 0.92, fc=color, ec="none"))
    ax.text(x + 0.54, y + 1.04, title, fontsize=9.5, weight="bold", color=INK)
    ax.text(x + 0.54, y + 0.67, metric, fontsize=8.0, color=MUTED)
    ax.text(x + 0.54, y + 0.32, status, fontsize=8.1, color=color, weight="bold")
ax.text(0.35, 4.65, "Tablero de evidencia al cierre de esta etapa",
        fontsize=12, weight="bold", color=INK)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "tablero_evidencia.png"), bbox_inches="tight",
            facecolor="white")
plt.close(fig)


# -------------------------------------------------------------- hoja de ruta
fig, ax = plt.subplots(figsize=(10.8, 4.45), dpi=220)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_xlabel("Esfuerzo relativo", fontsize=9)
ax.set_ylabel("Impacto sobre la validez del resultado", fontsize=9)
tasks = [
    (2.2, 9.1, "Medir jitter hasta ADC", RED),
    (4.0, 9.3, "Campana simultanea\ncon mayor apertura", RED),
    (3.3, 8.1, "Contraste SPT / perfil", RED),
    (4.8, 7.2, "Repetir sintesis\ndel compensador", ORANGE),
    (6.7, 6.4, "PCB propia", ORANGE),
    (7.7, 5.4, "Fuente de leva", ORANGE),
    (5.8, 4.1, "UWB como alternativa", BLUE),
    (2.4, 3.2, "Mejoras de interfaz", GREEN),
]
for x, y, label, color in tasks:
    ax.scatter(x, y, s=190, color=color, alpha=0.88, edgecolor="white", linewidth=1.0)
    ax.text(x + 0.18, y + 0.16, label, fontsize=8, color=INK)
ax.axhline(7.5, color="#bdbdbd", lw=0.8, ls=(0, (4, 3)))
ax.axvline(5.0, color="#bdbdbd", lw=0.8, ls=(0, (4, 3)))
ax.text(0.25, 9.75, "Prioridad metodologica", fontsize=10, weight="bold", color=RED)
ax.text(5.18, 0.45, "Desarrollo de producto", fontsize=9, color=MUTED)
ax.set_title("Hoja de ruta: primero cerrar la evidencia, despues escalar el hardware",
             loc="left", fontsize=11, pad=10)
ax.set_xticks(range(1, 11))
ax.set_yticks(range(1, 11))
clean(ax)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "roadmap_validacion.png"), bbox_inches="tight",
            facecolor="white")
plt.close(fig)


print("Figuras escritas en", OUT)
print("Posiciones de campo:", [int(p) for p in sorted(FIELD)])
