# -*- coding: utf-8 -*-
"""Inversion ciega de la curva hidro-guiada y contraste posterior con el SEV.

El SEV no participa en el modelo inicial, la funcion objetivo, los limites ni
las restricciones. Sus interfaces se dibujan solamente despues de terminar la
inversion para evaluar coincidencias externas.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "src" / "interfaces" / "python"))
sys.path.insert(0, str(REPO / "src" / "interfaces" / "python" / "third-party" / "ADsurf"))

from ADsurf._surf96 import surf96  # noqa: E402
from geophone_scope.masw_inversion import monte_carlo_inversion  # noqa: E402


CURVE = REPO / "data" / "Moldeo Hidro" / "grupo1_curva_dispersion_hidro_guiada.csv"
OUT_FIG = HERE / "inversion_hidroguiada_libre_vs_sev.png"
OUT_CSV = HERE / "modelo_hidroguiado_inversion_libre.csv"
OUT_JSON = HERE / "metricas_hidroguiada_inversion_libre.json"

SEV_INTERFACES = np.array([1.00, 2.06, 4.15, 24.0, 71.8])
SEV_RANGES = ["0-1,00", "1,00-2,06", "2,06-4,15", "4,15-24", "24-71,8", ">71,8"]

ORANGE = "#e87522"
GREEN = "#2f7d4a"
BLUE = "#245f9e"
RED = "#b24b32"
GREY = "#686868"
GRID = "#dfdfdf"


def forward(frequency_hz: np.ndarray, vs_ms: np.ndarray, h_m: np.ndarray) -> np.ndarray:
    """Respuesta Rayleigh fundamental; parametros auxiliares no vienen del SEV."""
    vp_ms = 2.081666 * np.asarray(vs_ms, dtype=float)  # nu = 0.35
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


def relative_rms(observed: np.ndarray, predicted: np.ndarray) -> float:
    return float(np.sqrt(np.mean(((predicted - observed) / observed) ** 2)))


def invert_blind(f: np.ndarray, c: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict]:
    # Inicializacion y exploracion global obtenidas solo de f, c y lambda=c/f.
    mc = monte_carlo_inversion(
        f[::3], c[::3], n_layers=4, n_iterations=3000,
        bs=8.0, bh=12.0, nu=0.35, rho=1850.0,
        reversals=0, c_test_step=1.0, seed=42,
    )
    vs0 = np.asarray(mc["beta"], dtype=float)
    h0 = np.asarray(mc["h"], dtype=float)
    fit_f, fit_c = f[::6], c[::6]

    def objective(x: np.ndarray) -> float:
        vs, h = x[:5], x[5:]
        try:
            ct = forward(fit_f, vs, h)
        except Exception:
            return 1e6
        return relative_rms(fit_c, ct)

    constraints = [
        {"type": "ineq", "fun": lambda x, i=i: x[i + 1] - x[i]}
        for i in range(4)
    ]
    result = minimize(
        objective,
        np.r_[vs0, h0],
        method="SLSQP",
        bounds=[(35.0, 300.0)] * 5 + [(0.20, 5.0)] * 4,
        constraints=constraints,
        options={"maxiter": 65, "ftol": 1e-9, "disp": False},
    )
    vs = np.asarray(result.x[:5], dtype=float)
    h = np.asarray(result.x[5:], dtype=float)
    c_theory = forward(f, vs, h)
    meta = {
        "monte_carlo_misfit_percent": float(mc["misfit"]),
        "local_optimizer_success": bool(result.success),
        "local_optimizer_message": str(result.message),
        "local_objective_subsample_relative_rms": float(result.fun),
    }
    return vs, h, c_theory, meta


def profile_xy(vs: np.ndarray, interfaces: np.ndarray, zmax: float) -> tuple[np.ndarray, np.ndarray]:
    tops = np.r_[0.0, interfaces]
    bottoms = np.r_[interfaces, zmax]
    xx, yy = [], []
    for value, top, bottom in zip(vs, tops, bottoms):
        xx.extend([value, value])
        yy.extend([top, bottom])
    return np.asarray(xx), np.asarray(yy)


def style(ax: plt.Axes) -> None:
    ax.grid(True, color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=8.2, colors="#606060")


def main() -> None:
    data = np.genfromtxt(CURVE, delimiter=",", names=True, encoding="utf-8")
    f = np.asarray(data["freq_Hz"], dtype=float)
    c = np.asarray(data["cR_pick_ms"], dtype=float)
    order = np.argsort(f)
    f, c = f[order], c[order]

    vs, h, c_theory, meta = invert_blind(f, c)
    interfaces = np.cumsum(h)
    misfit = relative_rms(c, c_theory)
    lam_max = float(np.max(c / f))
    z_proxy = lam_max / 3.0
    equiv_vs_range = [float(np.min(c / 0.92)), float(np.max(c / 0.92))]

    # Comparacion uno-a-uno de las tres interfaces someras. Esto se calcula
    # despues de la inversion: no retroalimenta el modelo.
    shallow_deltas = interfaces[:3] - SEV_INTERFACES[:3]

    fig, axes = plt.subplots(
        1, 3, figsize=(13.2, 5.25), dpi=220,
        gridspec_kw={"width_ratios": [1.35, 0.92, 0.92], "wspace": 0.31},
    )
    ax = axes[0]
    ax.plot(f, c, "o", ms=3.3, color=ORANGE, alpha=0.78, label="curva hidro-guiada medida")
    ax.plot(f, c_theory, color=GREEN, lw=2.3,
            label=f"respuesta de la inversión libre ({100*misfit:.1f} % RMS rel.)")
    ax.set(xlabel="Frecuencia [Hz]", ylabel="Velocidad de fase [m/s]",
           title="Ajuste sin usar el SEV", xlim=(8, 30))
    ax.legend(frameon=False, fontsize=7.8)
    ax.text(
        0.04, 0.05,
        f"cR medida: {c.min():.0f}-{c.max():.0f} m/s\n"
        f"Vs homogénea equivalente cR/0,92: {equiv_vs_range[0]:.0f}-{equiv_vs_range[1]:.0f} m/s",
        transform=ax.transAxes, fontsize=7.6, va="bottom",
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "alpha": 0.92},
    )
    style(ax)

    x8, y8 = profile_xy(vs, interfaces, 8.0)
    ax = axes[1]
    ax.plot(x8, y8, color=GREEN, lw=2.5, label="perfil invertido")
    for depth in SEV_INTERFACES[:3]:
        ax.axhline(depth, color=RED, lw=1.1, ls=(0, (4, 3)))
    for depth in interfaces:
        if depth <= 8:
            ax.axhline(depth, color=BLUE, lw=0.9, ls=":")
    ax.axhline(z_proxy, color=GREY, lw=1.0, ls=(0, (6, 3)))
    for i, value in enumerate(vs):
        top = np.r_[0.0, interfaces][i]
        bottom = np.r_[interfaces, 8.0][i]
        if top < 8:
            ax.text(value + 2.0, (top + min(bottom, 8.0)) / 2.0, f"{value:.0f}",
                    fontsize=7.2, color=GREEN, va="center")
    ax.set(xlabel="$V_S$ [m/s]", ylabel="Profundidad [m]", ylim=(8, 0),
           xlim=(35, max(145.0, float(vs.max()) + 25.0)), title="Detalle somero")
    ax.text(
        0.03, 0.03,
        "Rojo: SEV; azul: inversión libre",
        transform=ax.transAxes, va="bottom", fontsize=7.2,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "alpha": 0.92},
    )
    style(ax)

    x80, y80 = profile_xy(vs, interfaces, 80.0)
    ax = axes[2]
    colors = ["#f4dfb9", "#d8d0b9", "#edc890", "#dcc08e", "#c7b17b", "#afa06e"]
    bounds = np.r_[0.0, SEV_INTERFACES, 80.0]
    for i in range(6):
        ax.axhspan(bounds[i], bounds[i + 1], color=colors[i], alpha=0.42, linewidth=0)
    ax.plot(x80, y80, color=GREEN, lw=2.5)
    for depth in SEV_INTERFACES:
        ax.axhline(depth, color=RED, lw=1.0, ls=(0, (4, 3)))
    ax.axhspan(z_proxy, 80.0, facecolor="white", alpha=0.32, hatch="///", edgecolor="#bbbbbb")
    ax.set(xlabel="$V_S$ [m/s]", ylabel="Profundidad [m]", ylim=(80, 0),
           xlim=(35, max(145.0, float(vs.max()) + 25.0)), title="Rangos completos del SEV")
    for i, label in enumerate(SEV_RANGES):
        if i < 3:
            continue  # los tres intervalos someros se leen en el panel central
        mid = (bounds[i] + bounds[i + 1]) / 2.0
        ax.text(0.98, mid, label + " m", transform=ax.get_yaxis_transform(),
                ha="right", va="center", fontsize=6.7, color="#5a4328")
    ax.text(
        0.04, 0.98,
        f"Profundidad indicativa de la curva: ~{z_proxy:.1f} m\n"
        "El rayado no está resuelto por estos datos",
        transform=ax.transAxes, va="top", fontsize=7.1,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "alpha": 0.92},
    )
    style(ax)

    fig.suptitle(
        "Inversión ciega de la curva hidro-guiada y comparación posterior con el SEV 01",
        fontsize=12.2, color="#202020",
    )
    fig.text(
        0.01, 0.005,
        "El SEV no intervino en la inversión. La proximidad de interfaces se evalúa sólo después del ajuste.",
        fontsize=7.6, color="#606060",
    )
    fig.savefig(OUT_FIG, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    tops = np.r_[0.0, interfaces]
    bottoms = np.r_[interfaces, np.inf]
    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["layer", "top_m", "bottom_m", "vs_m_s", "source"])
        for i, (top, bottom, value) in enumerate(zip(tops, bottoms, vs), start=1):
            writer.writerow([i, float(top), float(bottom), float(value), "inversion_hidroguiada_sin_SEV"])

    payload = {
        "sev_used_in_inversion": False,
        "observed_points": int(f.size),
        "frequency_range_hz": [float(f.min()), float(f.max())],
        "observed_phase_velocity_range_m_s": [float(c.min()), float(c.max())],
        "max_wavelength_m": lam_max,
        "indicative_depth_lambda_max_over_3_m": z_proxy,
        "model": {
            "vs_m_s": vs.tolist(),
            "thickness_m": h.tolist(),
            "interfaces_m": interfaces.tolist(),
        },
        "fit_relative_rms": misfit,
        "homogeneous_equivalent_vs_c_over_0p92_range_m_s": equiv_vs_range,
        "sev_interfaces_added_after_inversion_m": SEV_INTERFACES.tolist(),
        "free_minus_sev_first_three_interfaces_m": shallow_deltas.tolist(),
        "optimizer": meta,
        "interpretation_limit": "Interfaces below approximately lambda_max/3 are not resolved by this curve.",
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
