# -*- coding: utf-8 -*-
"""Genera la figura MASW de campo (gather + imagen de dispersión) desde datos reales.

Usa directamente el estado guardado de la campaña Canchita, sin pasar por la
interfaz web. La imagen de dispersión se calcula con el método de desplazamiento
de fase de Park et al. (1998), la misma expresión que aparece en el documento:

    S(w, c) = (1/N) * | sum_j  U(x_j, w)/|U(x_j, w)| * exp(i*w*x_j/c) |

Salida: figuras/interfaces/masw_campo.png
"""
from pathlib import Path
import json

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

REPO = Path(__file__).resolve().parents[4]
PROC = REPO / "data" / "processed" / "Canchita"
OUT = Path(__file__).resolve().parent / "interfaces" / "masw_campo.png"
OUT_SPECTRUM = (
    Path(__file__).resolve().parent
    / "interfaces"
    / "autopotencia_normalizada_multicanal.png"
)

# Banda deliberadamente más ancha que la útil: se busca mostrar dónde deja de
# haber información aprovechable, no sólo el tramo que se va a usar.
FMIN, FMAX = 1.0, 100.0
CMIN, CMAX = 40.0, 300.0


def cargar():
    z = np.load(PROC / "field_review_masw_state.npz")
    estado = json.loads(
        (PROC / "field_review_masw_state.json").read_text(encoding="utf-8")
    )
    masw = estado["masw"]
    return {
        "t": z["masw_g1_time"],
        "x": z["masw_g1_distances"],
        "U": z["masw_g1_matrix"],
        "picks": np.asarray(masw["picks_by_mode"]["0"], dtype=float),
        "par": masw["image_params"],
        "dx": float(masw["geophone_spacing_m"]),
        "L": float(masw["array_length_m"]),
    }


def dispersion(
    t, x, U, cmin, cmax, cstep, fmin, fmax,
    tmax=1.6, f_oversample=8, c_chunk=48,
):
    """Imagen frecuencia-velocidad de fase por desplazamiento de fase."""
    dt = float(np.median(np.diff(t)))
    # Las trazas promediadas no cubren todas el mismo intervalo: la matriz viene
    # rellenada con NaN. Se toma la ventana contigua desde el disparo en la que
    # TODAS las trazas tienen dato, para no mezclar longitudes distintas.
    # Además se acota al tren de ondas superficiales (el arribo más lejano, a
    # 50 m, llega cerca de 1 s): incluir los 9 s completos metería sobre todo
    # ruido y enterraría la cresta de dispersión.
    valida = np.all(np.isfinite(U), axis=0) & (t >= 0.0) & (t <= tmax)
    idx = np.flatnonzero(valida)
    if idx.size == 0:
        raise SystemExit("No hay ventana común válida entre las trazas")
    corte = np.flatnonzero(np.diff(idx) != 1)
    fin = idx[corte[0]] if corte.size else idx[-1]
    seg = U[:, idx[0]: fin + 1]
    n = seg.shape[1]
    # Ventana de Tukey suave para no introducir bordes duros en el espectro.
    w = np.hanning(n)
    seg = seg * w

    # La ventana de 1,6 s fija una resolución física de 1/T = 0,625 Hz. El
    # zero-padding no agrega información, pero evalúa la DFT sobre una malla
    # bastante más fina y evita bloques anchos, sobre todo en el eje logarítmico.
    nfft_objetivo = n * f_oversample
    nfft = 1 << int(np.ceil(np.log2(nfft_objetivo)))
    F = np.fft.rfft(seg, n=nfft, axis=1)
    f = np.fft.rfftfreq(nfft, dt)
    banda = (f >= fmin) & (f <= fmax)
    f = f[banda]
    F = F[:, banda]

    # Normalización por energía de cada traza: los offsets lejanos, más
    # atenuados, siguen aportando a la suma sin que la amplitud absoluta del
    # canal más cercano domine la imagen.
    norma = np.linalg.norm(F, axis=1, keepdims=True)
    norma[norma == 0] = 1e-30
    P = F / norma

    c = np.arange(cmin, cmax + 0.5 * cstep, cstep)
    w_ang = 2.0 * np.pi * f
    # S[ic, if] = |sum_j P[j, if] * exp(i * w * x_j / c)|
    # Con dc=0,1 m/s la matriz de fase completa sería innecesariamente grande;
    # se calcula por bloques de velocidades sin cambiar el resultado.
    S = np.empty((c.size, f.size), dtype=float)
    for inicio in range(0, c.size, c_chunk):
        fin = min(inicio + c_chunk, c.size)
        cb = c[inicio:fin]
        fase = np.exp(
            1j * (
                w_ang[None, :, None]
                * x[None, None, :]
                / cb[:, None, None]
            )
        )
        S[inicio:fin] = np.abs(np.einsum("jf,cfj->cf", P, fase)) / len(x)
    df_fisica = 1.0 / (n * dt)
    df_malla = 1.0 / (nfft * dt)
    return f, c, S, df_fisica, df_malla


def autopotencia_normalizada(
    t, U, fmin=1.0, fmax=100.0, tmin=0.0, tmax=2.0,
):
    """Autopotencia unilateral de cada traza, normalizada por su propio máximo."""
    dt = float(np.median(np.diff(t)))
    fs = 1.0 / dt
    valida = np.all(np.isfinite(U), axis=0) & (t >= tmin) & (t <= tmax)
    idx = np.flatnonzero(valida)
    if idx.size == 0:
        raise SystemExit("No hay ventana común para el análisis espectral")
    corte = np.flatnonzero(np.diff(idx) != 1)
    fin = idx[corte[0]] if corte.size else idx[-1]
    seg = U[:, idx[0]: fin + 1].astype(float, copy=True)
    seg -= np.mean(seg, axis=1, keepdims=True)

    ventana = np.hanning(seg.shape[1])
    nfft_objetivo = 4 * seg.shape[1]
    nfft = 1 << int(np.ceil(np.log2(nfft_objetivo)))
    X = np.fft.rfft(seg * ventana, n=nfft, axis=1)
    f = np.fft.rfftfreq(nfft, dt)

    # Estimador de autopotencia unilateral. La normalización posterior se hace
    # por traza: compara forma espectral, no amplitud absoluta entre receptores.
    Pxx = np.abs(X) ** 2 / (fs * np.sum(ventana ** 2))
    if nfft % 2 == 0:
        Pxx[:, 1:-1] *= 2.0
    else:
        Pxx[:, 1:] *= 2.0
    banda = (f >= fmin) & (f <= fmax)
    f = f[banda]
    Pxx = Pxx[:, banda]
    maximo = np.max(Pxx, axis=1, keepdims=True)
    maximo[maximo == 0] = 1.0
    Pnorm = Pxx / maximo
    Pdb = 10.0 * np.log10(np.maximum(Pnorm, 1e-5))
    return f, Pxx, Pdb


def graficar_autopotencia(
    t, x, U, salida, titulo, nombre_senales, etiqueta_posicion,
    tmin=0.0, tmax=2.0,
):
    f, Pxx, Pdb = autopotencia_normalizada(t, U, tmin=tmin, tmax=tmax)
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.3), width_ratios=[1.0, 1.08])

    cmap = plt.get_cmap("turbo")
    normaliza_distancia = matplotlib.colors.Normalize(vmin=float(x.min()), vmax=float(x.max()))
    for i, xi in enumerate(x):
        ax[0].semilogx(
            f, Pdb[i], color=cmap(normaliza_distancia(xi)),
            lw=0.75, alpha=0.82,
        )
    espectro_mediano = np.median(Pxx, axis=0)
    espectro_mediano /= max(float(np.max(espectro_mediano)), 1e-30)
    mediana_db = 10.0 * np.log10(np.maximum(espectro_mediano, 1e-5))
    ax[0].semilogx(f, mediana_db, color="black", lw=2.0, label="mediana")
    ax[0].set_xlim(1.0, 100.0)
    ax[0].set_ylim(-50.0, 1.0)
    ax[0].set_xticks([1, 2, 5, 10, 20, 50, 100])
    ax[0].get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax[0].set_xlabel("frecuencia [Hz]")
    ax[0].set_ylabel(r"$10\log_{10}(P_{xx}/P_{xx,\max})$ [dB]")
    ax[0].set_title(f"(a) Espectros normalizados de {nombre_senales}", fontsize=10)
    ax[0].grid(alpha=0.25, lw=0.45)
    ax[0].legend(loc="lower left", fontsize=8, framealpha=0.85)
    sm = matplotlib.cm.ScalarMappable(norm=normaliza_distancia, cmap=cmap)
    cb0 = fig.colorbar(sm, ax=ax[0], pad=0.025)
    cb0.set_label(etiqueta_posicion)

    im = ax[1].pcolormesh(
        f, x, Pdb, shading="auto", cmap="turbo",
        vmin=-50.0, vmax=0.0, rasterized=True,
    )
    ax[1].set_xscale("log")
    ax[1].set_xlim(1.0, 100.0)
    ax[1].set_xticks([1, 2, 5, 10, 20, 50, 100])
    ax[1].get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax[1].set_xlabel("frecuencia [Hz]")
    ax[1].set_ylabel(etiqueta_posicion)
    ax[1].set_title("(b) Autopotencia normalizada por posición", fontsize=10)
    cb1 = fig.colorbar(im, ax=ax[1], pad=0.025)
    cb1.set_label("autopotencia normalizada [dB]")

    fig.suptitle(titulo, fontsize=12, weight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    salida.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(salida, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    pico = f[np.argmax(Pxx, axis=1)]
    bordes = [(1.0, 5.0), (5.0, 20.0), (20.0, 50.0), (50.0, 100.0)]
    total = np.trapezoid(Pxx, f, axis=1)
    fracciones = []
    for inferior, superior in bordes:
        sel = (f >= inferior) & (f < superior)
        energia = np.trapezoid(Pxx[:, sel], f[sel], axis=1)
        fracciones.append(np.median(energia / np.maximum(total, 1e-30)))
    return pico, bordes, np.asarray(fracciones)


def main():
    d = cargar()
    par = d["par"]
    f, c, S, df_fisica, df_malla = dispersion(
        d["t"], d["x"], d["U"],
        CMIN, CMAX, 0.1, FMIN, FMAX,
    )
    # Normalizar por frecuencia: resalta la cresta en toda la banda.
    S = S / S.max(axis=0, keepdims=True)
    # Suavizado leve a lo largo de la frecuencia, sólo para lectura visual.
    nucleo = np.array([0.25, 0.5, 0.25])
    S = np.apply_along_axis(lambda v: np.convolve(v, nucleo, mode="same"), 1, S)

    fig, ax = plt.subplots(
        1, 3, figsize=(14.0, 4.2),
        width_ratios=[1.0, 1.18, 1.18],
    )

    # ── (a) gather real ────────────────────────────────────────────────────
    t, x, U = d["t"], d["x"], d["U"]
    vis = (t >= -0.05) & (t <= 2.0) & np.all(np.isfinite(U), axis=0)
    esc = 0.9 * float(np.median(np.diff(x)))
    for i, xi in enumerate(x):
        tr = U[i, vis]
        pico = np.max(np.abs(tr)) or 1.0
        wiggle = xi + esc * tr / pico
        ax[0].plot(t[vis], wiggle, color="#1a2b4c", lw=0.55)
        ax[0].fill_between(
            t[vis], xi, wiggle, where=(wiggle >= xi),
            color="#1a2b4c", alpha=0.82, linewidth=0,
        )
    ax[0].set_xlabel("tiempo relativo al martillo [s]")
    ax[0].set_ylabel("distancia fuente–receptor [m]")
    ax[0].set_title("(a) Registro multicanal sintetizado", fontsize=10)
    ax[0].set_xlim(-0.05, 2.0)
    ax[0].grid(alpha=0.25, lw=0.4)

    # ── (b) imagen completa: permite reconocer los límites geométricos ─────
    im = ax[1].pcolormesh(
        f, c, S, shading="auto", cmap="turbo",
        vmin=0.0, vmax=1.0, rasterized=True,
    )
    # Cotas geométricas del arreglo: por debajo de c = 2*dx*f hay aliasing
    # espacial; por encima de c = L*f la longitud de onda excede la apertura.
    halo = [pe.Stroke(linewidth=2.7, foreground="white"), pe.Normal()]
    ax[1].plot(
        f, 2.0 * d["dx"] * f, "--", color="#6a1b9a", lw=1.25,
        path_effects=halo,
        label=r"$c=2\,\Delta x\,f$  (aliasing espacial)",
    )
    ax[1].plot(
        f, d["L"] * f, ":", color="#005bbb", lw=1.35,
        path_effects=halo,
        label=r"$\lambda=L$  (apertura del arreglo)",
    )
    ax[1].set_ylim(CMIN, CMAX)
    ax[1].set_xscale("log")
    ax[1].set_xlim(1.0, FMAX)
    ax[1].set_xticks([1, 2, 5, 10, 20, 50, 100])
    ax[1].get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax[1].set_xlabel("frecuencia [Hz]")
    ax[1].set_ylabel("velocidad de fase [m/s]")
    ax[1].set_title("(b) Dispersión completa", fontsize=10)
    ax[1].legend(loc="upper left", fontsize=8, framealpha=0.85)

    # ── (c) ampliación 5–50 Hz: recupera la vista usada durante el análisis ─
    ax[2].pcolormesh(
        f, c, S, shading="auto", cmap="turbo",
        vmin=0.0, vmax=1.0, rasterized=True,
    )
    ax[2].plot(
        f, 2.0 * d["dx"] * f, "--", color="#6a1b9a", lw=1.25,
        path_effects=halo,
    )
    ax[2].plot(
        f, d["L"] * f, ":", color="#005bbb", lw=1.35,
        path_effects=halo,
    )
    ax[2].set_xlim(5.0, 50.0)
    ax[2].set_ylim(CMIN, CMAX)
    ax[2].set_xticks([5, 10, 20, 30, 40, 50])
    ax[2].set_xlabel("frecuencia [Hz]")
    ax[2].set_ylabel("velocidad de fase [m/s]")
    ax[2].set_title("(c) Detalle de 5 a 50 Hz", fontsize=10)

    fig.subplots_adjust(left=0.055, right=0.91, bottom=0.15, top=0.89, wspace=0.34)
    cax = fig.add_axes([0.93, 0.15, 0.012, 0.74])
    fig.colorbar(im, cax=cax, label="energía normalizada")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=200, bbox_inches="tight")
    plt.close(fig)
    pico, bordes, fracciones = graficar_autopotencia(
        t, x, U, OUT_SPECTRUM,
        "Análisis espectral del registro multicanal",
        "las 21 trazas", "distancia fuente–receptor [m]",
    )
    print(f"escrito: {OUT}")
    print(f"escrito: {OUT_SPECTRUM}")
    print(f"trazas={len(x)}  dx={d['dx']} m  L={d['L']} m  "
          f"banda={f.min():.1f}-{f.max():.1f} Hz")
    print(f"malla: df={df_malla:.4f} Hz, dc={c[1]-c[0]:.1f} m/s; "
          f"resolución física aproximada={df_fisica:.3f} Hz")
    print(
        "picos por traza: "
        f"mediana={np.median(pico):.2f} Hz, "
        f"rango={np.min(pico):.2f}-{np.max(pico):.2f} Hz"
    )
    print(
        "fracción mediana de autopotencia: "
        + ", ".join(
            f"{a:g}-{b:g} Hz={100*q:.1f}%"
            for (a, b), q in zip(bordes, fracciones)
        )
    )


if __name__ == "__main__":
    main()
