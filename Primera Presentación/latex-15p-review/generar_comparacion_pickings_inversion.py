# -*- coding: utf-8 -*-
"""Compara los dos pickings de Canchita e invierte el pick hidro-guiado.

La respuesta directa se calcula con surf96 (modo fundamental de Rayleigh). El
SEV 01 solo fija las interfaces 1.00, 2.06 y 4.15 m; las velocidades Vs se
ajustan a la curva naranja medida. No se convierte resistividad en Vs.
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
sys.path.insert(0, str(REPO / "src" / "interfaces" / "python" / "third-party" / "ADsurf"))
sys.path.insert(0, str(REPO / "src" / "interfaces" / "python"))

from ADsurf._surf96 import surf96  # noqa: E402
from geophone_scope.masw_dispersion import (  # noqa: E402
    common_finite_window,
    phase_shift_dispersion_image,
)


HIST_CSV = REPO / "data" / "processed" / "Canchita_procesado" / "masw_curva_dispersion.csv"
HYDRO_CSV = REPO / "data" / "Moldeo Hidro" / "grupo1_curva_dispersion_hidro_guiada.csv"
STATE_NPZ = REPO / "data" / "processed" / "Canchita" / "field_review_masw_state.npz"

OUT_COMPARE = HERE / "comparacion_dos_pickings.png"
OUT_INVERSION = HERE / "inversion_pick_naranja_sev.png"
OUT_MODEL = HERE / "modelo_vs_pick_naranja.csv"
OUT_METRICS = HERE / "metricas_pick_naranja.json"

SEV_INTERFACES = np.array([1.00, 2.06, 4.15], dtype=float)
SEV_RHO = np.array([1186.0, 15.0, 105.0, 24.2, 126.0, 6.42])
SEV_TOP = np.array([0.0, 1.0, 2.06, 4.15, 24.0, 71.8])
SEV_BOTTOM = np.array([1.0, 2.06, 4.15, 24.0, 71.8, np.inf])

# Perfil de velocidades que se empleo para construir la guia visual original.
HID_TOP = np.array([0.0, 1.0, 2.1, 4.2, 8.0, 24.0, 50.0])
HID_VS = np.array([95.0, 105.0, 145.0, 185.0, 240.0, 330.0, 400.0])

COL_HYDRO = "#e87522"
COL_HIST = "#255f9e"
COL_INV = "#2f7d4a"
COL_OLD = "#b04a32"
COL_PRIOR = "#527da6"
INK = "#202020"
GRID = "#dedede"


def load_csv(path: Path) -> np.ndarray:
    return np.genfromtxt(path, delimiter=",", names=True, encoding="utf-8-sig")


def forward_curve(frequency_hz: np.ndarray, thickness_m: np.ndarray, vs_ms: np.ndarray) -> np.ndarray:
    """Modo fundamental de Rayleigh con supuestos de Vp y densidad declarados."""
    frequency_hz = np.asarray(frequency_hz, dtype=float)
    vs_ms = np.asarray(vs_ms, dtype=float)
    vp_ms = np.maximum(2.08 * vs_ms, 400.0)
    density_kgm3 = 1600.0 + 0.22 * vs_ms
    thickness_km = np.append(np.asarray(thickness_m, dtype=float), 0.0) / 1000.0
    return surf96(
        1.0 / frequency_hz,
        thickness_km,
        vp_ms / 1000.0,
        vs_ms / 1000.0,
        density_kgm3 / 1000.0,
        mode=0,
        itype=0,
        ifunc=2,
        dt=0.005,
    ) * 1000.0


def relative_rms(observed: np.ndarray, predicted: np.ndarray) -> float:
    return float(np.sqrt(np.mean(((predicted - observed) / observed) ** 2)))


def invert_hydro_pick(frequency_hz: np.ndarray, c_obs_ms: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    thickness = np.diff(np.r_[0.0, SEV_INTERFACES])
    # La curva esta densamente muestreada (paso ~0.167 Hz). Para el ajuste se
    # conserva uno de cada seis puntos; la metrica publicada se evalua despues
    # sobre los 132 puntos, de modo que el submuestreo no oculta el error.
    fit_frequency = frequency_hz[::6]
    fit_observed = c_obs_ms[::6]

    def objective(vs: np.ndarray) -> float:
        try:
            predicted = forward_curve(fit_frequency, thickness, vs)
        except Exception:
            return 1e6
        return relative_rms(fit_observed, predicted)

    constraints = [
        {"type": "ineq", "fun": lambda v, i=i: v[i + 1] - v[i]}
        for i in range(3)
    ]
    result = minimize(
        objective,
        x0=np.array([72.0, 86.0, 86.0, 111.0]),
        method="SLSQP",
        bounds=[(50.0, 350.0)] * 4,
        constraints=constraints,
        options={"maxiter": 45, "ftol": 1e-8, "disp": False},
    )
    vs = np.asarray(result.x, dtype=float)
    predicted = forward_curve(frequency_hz, thickness, vs)
    return vs, predicted, relative_rms(c_obs_ms, predicted)


def vs30_extrapolated(vs: np.ndarray) -> float:
    tops = np.r_[0.0, SEV_INTERFACES]
    bottoms = np.r_[SEV_INTERFACES, 30.0]
    thickness = bottoms - tops
    return float(30.0 / np.sum(thickness / vs))


def style_axis(ax: plt.Axes) -> None:
    ax.grid(True, color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(colors="#606060", labelsize=8.5)


def dispersion_image() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    state = np.load(STATE_NPZ)
    time = np.asarray(state["masw_g1_time"], dtype=float)
    distances = np.asarray(state["masw_g1_distances"], dtype=float)
    matrix = np.asarray(state["masw_g1_matrix"], dtype=float)
    time, matrix = common_finite_window(time, matrix, t_min=0.0)
    fs = float(1.0 / np.median(np.diff(time)))
    f, c, energy = phase_shift_dispersion_image(
        np.nan_to_num(matrix.T), distances, fs,
        c_min=50.0, c_max=350.0, c_step=1.0, f_min=5.0, f_max=36.0,
    )
    return f, c, energy


def step_profile(vs: np.ndarray, zmax: float) -> tuple[np.ndarray, np.ndarray]:
    tops = np.r_[0.0, SEV_INTERFACES]
    bottoms = np.r_[SEV_INTERFACES, zmax]
    xx, yy = [], []
    for top, bottom, value in zip(tops, bottoms, vs):
        xx.extend([value, value])
        yy.extend([top, bottom])
    return np.asarray(xx), np.asarray(yy)


def save_model(vs: np.ndarray) -> None:
    lithology = [
        "capa geoeléctrica superficial muy resistiva",
        "nivel conductor delgado dentro del suelo residual",
        "nivel areno-cuarzoso de resistividad intermedia",
        "continuación de la unidad superficial hasta 24 m",
    ]
    with OUT_MODEL.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["top_m", "bottom_m", "vs_invertida_ms", "rho_sev_ohm_m", "interpretacion"])
        for i, value in enumerate(vs):
            top = float(np.r_[0.0, SEV_INTERFACES][i])
            bottom = float(np.r_[SEV_INTERFACES, np.inf][i])
            writer.writerow([top, bottom, float(value), float(SEV_RHO[i]), lithology[i]])


def main() -> None:
    hist = load_csv(HIST_CSV)
    hydro = load_csv(HYDRO_CSV)
    f_hist = np.asarray(hist["freq_hz"], dtype=float)
    c_hist = np.asarray(hist["c_obs_m_s"], dtype=float)
    f_hydro = np.asarray(hydro["freq_Hz"], dtype=float)
    c_hydro = np.asarray(hydro["cR_pick_ms"], dtype=float)
    c_prior = np.asarray(hydro["cR_hydro_prior_ms"], dtype=float)

    order = np.argsort(f_hydro)
    f_hydro, c_hydro, c_prior = f_hydro[order], c_hydro[order], c_prior[order]
    vs_inv, c_inv, misfit = invert_hydro_pick(f_hydro, c_hydro)
    c_old = forward_curve(f_hydro, np.diff(HID_TOP), HID_VS)

    mask_overlap = (f_hist >= f_hydro.min()) & (f_hist <= f_hydro.max())
    c_hydro_at_hist = np.interp(f_hist[mask_overlap], f_hydro, c_hydro)
    rmse_between_picks = float(np.sqrt(np.mean((c_hist[mask_overlap] - c_hydro_at_hist) ** 2)))
    heuristic_rel = relative_rms(c_old, c_prior)
    max_wavelength = float(np.max(c_hydro / f_hydro))
    support_lambda3 = max_wavelength / 3.0
    vs30 = vs30_extrapolated(vs_inv)

    f_img, c_img, energy = dispersion_image()

    # Figure 1: the reason the two orange curves seen in the document differ.
    fig, (ax0, ax1) = plt.subplots(
        1, 2, figsize=(11.4, 4.9), dpi=210,
        gridspec_kw={"width_ratios": [1.35, 1.0], "wspace": 0.24},
    )
    mesh = ax0.pcolormesh(f_img, c_img, energy.T, shading="auto", cmap="viridis", rasterized=True)
    ax0.plot(f_hydro, c_hydro, color=COL_HYDRO, lw=2.0, label="pick hidro-guiado (curva naranja)")
    ax0.plot(f_hydro, c_prior, color=COL_PRIOR, lw=1.6, ls="--", label="guía heurística original")
    keep_hist = (f_hist >= 5.0) & (f_hist <= 36.0) & (c_hist <= 350.0)
    ax0.scatter(
        f_hist[keep_hist], c_hist[keep_hist], s=22, facecolors="white", edgecolors=COL_HIST,
        linewidths=1.1, label="picking histórico (rama distinta)", zorder=5,
    )
    ax0.set(xlim=(5, 36), ylim=(50, 350), xlabel="Frecuencia [Hz]", ylabel="Velocidad de fase [m/s]",
            title="Misma campaña, dos selecciones de cresta")
    ax0.legend(frameon=True, fontsize=7.2, loc="upper right")
    fig.colorbar(mesh, ax=ax0, pad=0.015, label="Energía normalizada")

    ax1.plot(f_hist, c_hist, "o", ms=4.0, color=COL_HIST, label="picking histórico: 51 puntos")
    ax1.plot(f_hydro, c_hydro, color=COL_HYDRO, lw=2.0, label="picking hidro-guiado: 132 puntos")
    ax1.plot(f_hydro, c_inv, color=COL_INV, lw=1.8, label="respuesta del perfil invertido")
    ax1.set(xlim=(5, 30), ylim=(50, 700), xlabel="Frecuencia [Hz]", ylabel="Velocidad de fase [m/s]",
            title="Las curvas no son equivalentes")
    ax1.text(
        0.04, 0.04,
        f"RMSE entre pickings en el solape: {rmse_between_picks:.1f} m/s\n"
        "La discrepancia se concentra en 5-14 Hz",
        transform=ax1.transAxes, va="bottom", fontsize=7.8, color=INK,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "alpha": 0.92},
    )
    ax1.legend(frameon=False, fontsize=7.4, loc="upper right")
    for ax in (ax0, ax1):
        style_axis(ax)
    fig.suptitle("Auditoría del picking: origen de la discrepancia entre las dos curvas", fontsize=12, color=INK)
    fig.savefig(OUT_COMPARE, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    # Figure 2: actual inversion of the orange hydro-guided pick.
    fig, (ax0, ax1) = plt.subplots(
        1, 2, figsize=(11.2, 5.15), dpi=210,
        gridspec_kw={"width_ratios": [1.35, 0.9], "wspace": 0.28},
    )
    ax0.plot(f_hydro, c_hydro, "o", ms=3.1, color=COL_HYDRO, alpha=0.78,
             label="observada: pick naranja")
    ax0.plot(f_hydro, c_inv, color=COL_INV, lw=2.2,
             label=f"invertida con interfaces SEV (RMS rel. {100*misfit:.1f} %)")
    ax0.plot(f_hydro, c_old, color=COL_OLD, lw=1.7, ls="--",
             label="respuesta directa del modelo hidro previo")
    ax0.plot(f_hydro, c_prior, color=COL_PRIOR, lw=1.4, ls=":",
             label="guía original (heurística, no curva teórica)")
    ax0.set(xlim=(8, 30), xlabel="Frecuencia [Hz]", ylabel="Velocidad de fase [m/s]",
            title="Ajuste directo al picking hidro-guiado")
    ax0.legend(frameon=False, fontsize=7.5)
    style_axis(ax0)

    x_step, y_step = step_profile(vs_inv, 24.0)
    for top, bottom, color in (
        (0.0, 1.0, "#f6dfb5"), (1.0, 2.06, "#d9d2be"),
        (2.06, 4.15, "#edc792"), (4.15, 24.0, "#d8b378"),
    ):
        ax1.axhspan(top, bottom, color=color, alpha=0.42, linewidth=0)
    ax1.plot(x_step, y_step, color=COL_INV, lw=2.5)
    ax1.plot([vs_inv[-1], vs_inv[-1]], [4.15, 24.0], color=COL_INV, lw=2.5, ls="--")
    for depth in SEV_INTERFACES:
        ax1.axhline(depth, color=COL_HIST, lw=0.9, ls=(0, (2, 2)))
    ax1.axhline(support_lambda3, color="#6d6d6d", lw=1.0, ls=(0, (5, 3)))
    ax1.text(0.98, support_lambda3 + 0.18, f"z~lambda_max/3 = {support_lambda3:.1f} m",
             transform=ax1.get_yaxis_transform(), ha="right", va="top", fontsize=7.2, color="#555555")
    for i, value in enumerate(vs_inv):
        top = np.r_[0.0, SEV_INTERFACES][i]
        bottom = np.r_[SEV_INTERFACES, 7.0][i]
        y = (top + min(bottom, 7.0)) / 2.0
        ax1.text(value + 4.0, y, f"{value:.0f} m/s", fontsize=7.5, color=COL_INV, va="center")
    ax1.set(xlim=(50, max(155.0, float(vs_inv.max()) + 35.0)), ylim=(24, 0),
            xlabel="$V_S$ [m/s]", ylabel="Profundidad [m]",
            title="Perfil Vs con geometría del SEV 01")
    ax1.text(
        0.03, 0.04,
        "SEV 01: interfaces 1,00 / 2,06 / 4,15 / 24,0 m\n"
        "Línea sólida: tramo condicionado por la curva\n"
        "Línea discontinua: semiespacio extrapolado",
        transform=ax1.transAxes, va="bottom", fontsize=7.4,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "alpha": 0.92},
    )
    style_axis(ax1)

    fig.suptitle("Inversión de la curva naranja: el SEV fija interfaces, la curva fija Vs", fontsize=12, color=INK)
    fig.text(
        0.01, 0.005,
        "El informe eléctrico no se transforma a Vs. El resultado Vs30 = "
        f"{vs30:.0f} m/s sería una extrapolación desde ~{support_lambda3:.1f} m y no se reporta como medición.",
        fontsize=7.4, color="#606060",
    )
    fig.savefig(OUT_INVERSION, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    save_model(vs_inv)
    payload = {
        "hydro_pick_points": int(f_hydro.size),
        "frequency_range_hz": [float(f_hydro.min()), float(f_hydro.max())],
        "phase_velocity_range_m_s": [float(c_hydro.min()), float(c_hydro.max())],
        "max_wavelength_m": max_wavelength,
        "depth_proxy_lambda_max_over_3_m": support_lambda3,
        "sev_fixed_interfaces_m": SEV_INTERFACES.tolist(),
        "vs_inverted_m_s": vs_inv.tolist(),
        "relative_rms_misfit": misfit,
        "vs30_extrapolated_not_measured_m_s": vs30,
        "old_hydro_model_relative_rms": relative_rms(c_hydro, c_old),
        "old_heuristic_vs_true_forward_relative_rms": heuristic_rel,
        "historical_vs_hydro_pick_overlap_rmse_m_s": rmse_between_picks,
        "forward_model_assumptions": {
            "rayleigh_mode": 0,
            "vp_relation": "max(2.08*Vs, 400 m/s)",
            "density_relation": "1600 + 0.22*Vs kg/m3",
            "engine": "surf96 / ADsurf",
        },
    }
    OUT_METRICS.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
