# -*- coding: utf-8 -*-
"""Grafica la inversión libre hasta 50 m y la contrasta con el SEV 01.

La inversión ya fue realizada sin usar el SEV. Este script solo proyecta el
modelo resultante, calcula Vs media por tiempo de viaje en cada intervalo del
SEV y agrega la comparación litológica después de la inversión.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import numpy as np


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "src" / "interfaces" / "python" / "third-party" / "ADsurf"))

from ADsurf._surf96 import surf96  # noqa: E402


CURVE = REPO / "data" / "Moldeo Hidro" / "grupo1_curva_dispersion_hidro_guiada.csv"
METRICS = HERE / "metricas_hidroguiada_inversion_libre.json"
OUT_FIG = HERE / "inversion_libre_vs_sev_hasta_50m.png"
OUT_CSV = HERE / "comparacion_vs_sev_hasta_50m.csv"

SEV_BOUNDS = np.array([0.0, 1.00, 2.06, 4.15, 24.0, 50.0])
SEV_RHO = [1186.0, 15.0, 105.0, 24.2, 126.0]
SEV_DESCRIPTION = [
    "Cubierta residual seca,\nlevemente arcillosa y\n'muy compactada'",
    "Unidad superficial 0-24 m;\nnivel eléctrico conductor\ndelgado",
    "Finos cuarzosos /\nintercalaciones\nareno-cuarzosas",
    "Suelo residual y\nsedimentos areno-cuarzosos\nhasta 24 m",
    "Sedimentos cuarzosos\nfinos-medios con matriz\nlevemente arcillosa",
]

ORANGE = "#e87522"
GREEN = "#2f7d4a"
BLUE = "#245f9e"
RED = "#b24b32"
GREY = "#666666"
LIGHT_GREY = "#dedede"
SEV_COLORS = ["#f1dfba", "#d8d1bb", "#edca94", "#dcc28f", "#c8b27d"]


def forward(frequency_hz: np.ndarray, vs_ms: np.ndarray, h_m: np.ndarray) -> np.ndarray:
    """Respuesta Rayleigh fundamental del modelo libre ya invertido."""
    vp_ms = 2.081666 * np.asarray(vs_ms, dtype=float)
    density = np.full(vs_ms.size, 1850.0)
    return surf96(
        1.0 / np.asarray(frequency_hz, dtype=float),
        np.r_[h_m, 0.0] / 1000.0,
        vp_ms / 1000.0,
        np.asarray(vs_ms, dtype=float) / 1000.0,
        density / 1000.0,
        mode=0,
        itype=0,
        ifunc=2,
        dt=0.005,
    ) * 1000.0


def step_profile(vs: np.ndarray, interfaces: np.ndarray, zmax: float) -> tuple[np.ndarray, np.ndarray]:
    tops = np.r_[0.0, interfaces]
    bottoms = np.r_[interfaces, zmax]
    x, y = [], []
    for value, top, bottom in zip(vs, tops, bottoms):
        x.extend([value, value])
        y.extend([top, bottom])
    return np.asarray(x), np.asarray(y)


def travel_time_average(a: float, b: float, vs: np.ndarray, interfaces: np.ndarray) -> float:
    """Vs media armónica ponderada por espesor para el intervalo [a,b]."""
    tops = np.r_[0.0, interfaces]
    bottoms = np.r_[interfaces, np.inf]
    travel_time = 0.0
    for top, bottom, value in zip(tops, bottoms, vs):
        overlap = max(0.0, min(b, bottom) - max(a, top))
        travel_time += overlap / value
    return (b - a) / travel_time


def mechanical_class(value: float) -> str:
    # Referencia comparativa amplia: USGS PP 1500-K-R reporta 55-115 m/s
    # para arcillas muy blandas a blandas y 150-250 m/s para arenas sueltas
    # a densas. No es una identificación litológica unívoca.
    if value < 100.0:
        return "Muy blando-blando\n(baja rigidez)"
    if value < 115.0:
        return "Blando\n(baja rigidez)"
    if value < 150.0:
        return "Blando a firme;\npor debajo de arena típica"
    return "Compatible con arena\nsuelta o material más rígido"


def verdict(index: int, value: float, z_support: float) -> tuple[str, str]:
    a, b = SEV_BOUNDS[index], SEV_BOUNDS[index + 1]
    support_fraction = max(0.0, min(b, z_support) - a) / (b - a)
    if support_fraction < 0.5:
        return "NO VERIFICABLE", "extrapolado bajo 3,9 m"
    if index == 0:
        return "NO", "no respalda 'muy compactado'"
    if index in (1, 2):
        return "PARCIAL", "compatible con finos/arcilla"
    return "INDETERMINADO", "la litología no se deduce solo de Vs"


def style_axis(ax: plt.Axes) -> None:
    ax.grid(True, color=LIGHT_GREY, linewidth=0.7)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=8.5, colors="#555555")


def main() -> None:
    payload = json.loads(METRICS.read_text(encoding="utf-8"))
    vs = np.asarray(payload["model"]["vs_m_s"], dtype=float)
    interfaces = np.asarray(payload["model"]["interfaces_m"], dtype=float)
    h = np.diff(np.r_[0.0, interfaces])
    z_support = float(payload["indicative_depth_lambda_max_over_3_m"])
    misfit = 100.0 * float(payload["fit_relative_rms"])

    data = np.genfromtxt(CURVE, delimiter=",", names=True, encoding="utf-8")
    f = np.asarray(data["freq_Hz"], dtype=float)
    c = np.asarray(data["cR_pick_ms"], dtype=float)
    order = np.argsort(f)
    f, c = f[order], c[order]
    c_theory = forward(f, vs, h)

    averages = np.array([
        travel_time_average(a, b, vs, interfaces)
        for a, b in zip(SEV_BOUNDS[:-1], SEV_BOUNDS[1:])
    ])
    rows = []
    for i, (a, b, value) in enumerate(zip(SEV_BOUNDS[:-1], SEV_BOUNDS[1:], averages)):
        status, reason = verdict(i, value, z_support)
        rows.append({
            "interval_m": f"{a:.2f}-{b:.2f}",
            "rho_ohm_m": SEV_RHO[i],
            "vs_interval_m_s": float(value),
            "mechanical_class": mechanical_class(float(value)).replace("\n", " "),
            "sev_interpretation": SEV_DESCRIPTION[i].replace("\n", " "),
            "equivalence": status,
            "reason": reason,
            "supported_fraction": float(max(0.0, min(b, z_support) - a) / (b - a)),
        })

    fig = plt.figure(figsize=(16.5, 7.6), dpi=220)
    gs = fig.add_gridspec(
        1, 3, width_ratios=[1.20, 0.82, 2.45],
        left=0.045, right=0.985, top=0.88, bottom=0.11, wspace=0.25,
    )

    # 1) Ajuste de la curva, completamente independiente del SEV.
    ax = fig.add_subplot(gs[0, 0])
    ax.plot(f, c, "o", ms=3.0, color=ORANGE, alpha=0.78, label="pick hidro-guiado")
    ax.plot(f, c_theory, color=GREEN, lw=2.4,
            label=f"respuesta del modelo libre ({misfit:.1f}% RMS rel.)")
    ax.set(
        xlabel="Frecuencia [Hz]", ylabel="Velocidad de fase [m/s]",
        title="1. Inversión sin SEV", xlim=(8, 30),
    )
    ax.legend(frameon=False, fontsize=7.8, loc="upper right")
    ax.text(
        0.04, 0.04,
        f"132 puntos medidos\nProfundidad indicativa: {z_support:.1f} m",
        transform=ax.transAxes, va="bottom", fontsize=7.8,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "alpha": 0.92},
    )
    style_axis(ax)

    # 2) Perfil completo a 50 m. El tramo sin respaldo se conserva visible,
    # pero se distingue como continuación del modelo y no como estratos resueltos.
    ax = fig.add_subplot(gs[0, 1])
    for i, (a, b) in enumerate(zip(SEV_BOUNDS[:-1], SEV_BOUNDS[1:])):
        ax.axhspan(a, b, color=SEV_COLORS[i], alpha=0.48, linewidth=0)
        ax.text(39, (a + b) / 2, f"{a:g}-{b:g} m", va="center", ha="left",
                fontsize=6.9, color="#5d472d")
    for depth in SEV_BOUNDS[1:-1]:
        ax.axhline(depth, color=RED, lw=1.1, ls=(0, (4, 3)))

    xp, yp = step_profile(vs, interfaces, 50.0)
    # Trazo completo fino a 50 m y superposición sólida en el dominio respaldado.
    ax.plot(xp, yp, color=GREEN, lw=2.2, ls=(0, (5, 3)), alpha=0.75)
    mask = yp <= z_support
    ax.plot(xp[mask], yp[mask], color=GREEN, lw=3.0)
    for depth in interfaces:
        if depth <= 50:
            ax.axhline(depth, color=BLUE, lw=0.9, ls=":", alpha=0.8)
    ax.axhline(z_support, color=GREY, lw=1.3, ls=(0, (7, 3)))
    ax.axhspan(z_support, 50, facecolor="white", alpha=0.24, hatch="///", edgecolor="#bbbbbb")

    ax.set(
        xlabel="$V_S$ [m/s]", ylabel="Profundidad [m]", ylim=(50, 0),
        xlim=(35, 135), title="2. Perfil hasta 50 m",
    )
    ax.set_xticks([50, 75, 100, 125])
    ax.legend(
        handles=[
            Line2D([0], [0], color=GREEN, lw=3, label=f"respaldado hasta ~{z_support:.1f} m"),
            Line2D([0], [0], color=GREEN, lw=2, ls=(0, (5, 3)), label="continuación no resuelta"),
            Line2D([0], [0], color=RED, lw=1.1, ls=(0, (4, 3)), label="interfaces SEV"),
            Line2D([0], [0], color=BLUE, lw=1, ls=":", label="interfaces inversión libre"),
        ],
        frameon=False, fontsize=7.0, loc="lower left",
    )
    style_axis(ax)

    # 3) Tabla interpretativa solicitada, alineada por los mismos rangos.
    ax = fig.add_subplot(gs[0, 2])
    ax.axis("off")
    headers = ["Rango SEV", "$V_S$ media*", "Clase mecánica por $V_S$", "Interpretación del SEV", "¿Equivale?"]
    cell_text = []
    for i, row in enumerate(rows):
        status = row["equivalence"]
        reason = row["reason"]
        cell_text.append([
            f"{row['interval_m'].replace('.', ',')} m\n{row['rho_ohm_m']:g} Ωm",
            f"{row['vs_interval_m_s']:.0f} m/s",
            mechanical_class(row["vs_interval_m_s"]),
            SEV_DESCRIPTION[i],
            f"{status}\n{reason}",
        ])
    table = ax.table(
        cellText=cell_text, colLabels=headers, cellLoc="left", colLoc="left",
        colWidths=[0.13, 0.12, 0.20, 0.29, 0.26], bbox=[0.0, 0.08, 1.0, 0.88],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(7.4)
    for (r, col), cell in table.get_celld().items():
        cell.set_edgecolor("#d2d2d2")
        cell.set_linewidth(0.65)
        if r == 0:
            cell.set_facecolor("#ececec")
            cell.set_text_props(weight="bold", color="#252525")
            cell.set_height(0.085)
        else:
            cell.set_facecolor(SEV_COLORS[r - 1] + "70")
            cell.set_height(0.175)
            if col == 4:
                verdict_text = rows[r - 1]["equivalence"]
                if verdict_text == "NO":
                    cell.set_text_props(color=RED, weight="bold")
                elif verdict_text == "PARCIAL":
                    cell.set_text_props(color="#8a5a00", weight="bold")
                else:
                    cell.set_text_props(color=GREY, weight="bold")
    ax.set_title("3. Comparación mecánica y litológica", loc="left", pad=9)
    ax.text(
        0.0, 0.015,
        "* Media armónica por tiempo de viaje. USGS: 55-115 m/s es típico de arcilla muy blanda-blanda; "
        "150-250 m/s, de arena suelta-densa. Resistividad y Vs no identifican por sí solas una litología.",
        transform=ax.transAxes, fontsize=7.1, color="#555555", va="bottom", wrap=True,
    )

    fig.suptitle(
        "Inversión libre de la curva hidro-guiada y contraste posterior con el SEV 01 (0-50 m)",
        fontsize=13.0, color="#202020",
    )
    fig.text(
        0.045, 0.025,
        "Conclusión: la baja Vs coincide parcialmente con una componente fina/arcillosa en los primeros metros, "
        "pero no con la descripción 'muy compactada'. Debajo de ~3,9 m, el ensayo actual no valida el SEV.",
        fontsize=8.2, color="#444444",
    )
    fig.savefig(OUT_FIG, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Figura: {OUT_FIG}")
    print(f"Tabla:  {OUT_CSV}")
    for row in rows:
        print(
            f"{row['interval_m']} m | Vs={row['vs_interval_m_s']:.1f} m/s | "
            f"{row['equivalence']}: {row['reason']}"
        )


if __name__ == "__main__":
    main()
