"""Genera Presentacion_1ra_Borrador_v06.pptx: v05 + imágenes placeholder en cada slide.

Texto a la izquierda, imágenes a la derecha; pie de 7 pt con la fuente de cada imagen.
Las imágenes usadas se copian a placeholder_images/ (reproducible).
"""
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Emu, Inches, Pt

PPT = Path(__file__).resolve().parent
PRES = PPT.parent
DOCS = PRES.parent
A = DOCS / "investigacion" / "Assets"
FIG = PRES / "latex-15p-profesor" / "figuras"
HIST = PRES / "latex-historial" / "figuras"
REV = PRES / "latex-15p-review" / "figuras"
VIS = PRES / "recopilacion_figuras" / "vistas"
MASW = DOCS / "masw" / "informe" / "figuras"
WEB = Path.home() / "AppData/Local/Temp/w"  # descargas Wikimedia (ver CREDITS)
V04 = WEB / "v04"
OUTDIR = PPT / "placeholder_images"
OUTDIR.mkdir(exist_ok=True)
SRC = PPT / "Presentacion_1ra_Borrador_v05.pptx"
OUT = PPT / "Presentacion_1ra_Borrador_v06.pptx"


# ---------- figuras generadas en código ----------
def gen(name, fn, size=(6, 4)):
    p = OUTDIR / name
    fig, ax = plt.subplots(figsize=size, dpi=200)
    fn(ax)
    fig.tight_layout()
    fig.savefig(p)
    plt.close(fig)
    return p


def g_gmax(ax):
    g = np.logspace(-4, 0, 200)
    ax.semilogx(g, 1 / (1 + (g / 0.03) ** 0.9), color="#1f77b4", lw=2)
    ax.axvspan(1e-4, 1e-3, color="#2ca02c", alpha=0.2)
    ax.text(1.3e-4, 0.35, "pequeñas\ndeformaciones\nG ≈ Gmax = ρ·Vs²", fontsize=9)
    ax.set(xlabel="Deformación cortante γ (%)", ylabel="G / Gmax", title="Degradación de rigidez (esquema)")
    ax.grid(alpha=0.3)


def g_pie(ax):
    ax.pie([67, 26, 7], labels=["Rayleigh 67 %", "S 26 %", "P 7 %"], colors=["#1f77b4", "#ff7f0e", "#7f7f7f"],
           startangle=90, autopct=None, textprops={"fontsize": 11})
    ax.set_title("Reparto de energía, fuente vertical\n(Miller & Pursey 1955)")


def g_flat(ax):
    f = np.linspace(1, 60, 200)
    ax.plot(f, np.full_like(f, 180), lw=2.5, label="semiespacio homogéneo")
    ax.set(xlabel="f (Hz)", ylabel="cR (m/s)", ylim=(0, 400), title="cR sin dispersión")
    ax.legend()
    ax.grid(alpha=0.3)


def g_nu(ax):
    nu = np.linspace(0, 0.5, 100)
    ax.plot(nu, (0.862 + 1.14 * nu) / (1 + nu), lw=2.5)
    ax.set(xlabel="Poisson ν", ylabel="cR / Vs", ylim=(0.85, 0.96), title="cR ≈ 0.87–0.955·Vs (Viktorov)")
    ax.axhline(0.92, ls="--", color="gray")
    ax.grid(alpha=0.3)


def g_comp(ax):
    f = np.logspace(-1, 2, 400)
    fn, z = 10, 0.56
    s = f / fn
    sm = s**2 / np.sqrt((1 - s**2) ** 2 + (2 * z * s) ** 2)
    db = lambda x: 20 * np.log10(x)
    comp = 1 / np.maximum(sm, 1e-4)
    comp = np.minimum(comp, 10 ** (30 / 20))
    ax.semilogx(f, db(sm), label="SM-24 (2º orden HP)")
    ax.semilogx(f, db(sm * comp), label="SM-24 + compensación LF")
    ax.set(xlabel="f (Hz)", ylabel="|H| (dB)", ylim=(-50, 10), title="Compensación de baja frecuencia (concepto)")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, which="both")


G = {
    "gmax": gen("gen_gmax_degradacion.png", g_gmax),
    "pie": gen("gen_energia_miller_pursey.png", g_pie, (4.5, 4)),
    "flat": gen("gen_cR_homogeneo.png", g_flat),
    "nu": gen("gen_cR_vs_poisson.png", g_nu),
    "comp": gen("gen_compensacion_LF.png", g_comp),
}
# recorte Fig. 1 de Lin & Ashlock (2016)
lin = Image.open(PPT / "lin2016-p2.png").crop((170, 1305, 1100, 1560))
lin.save(OUTDIR / "lin2016_fig1_recorte.png")
LIN = OUTDIR / "lin2016_fig1_recorte.png"

# ---------- mapa slide -> [(imagen, fuente)] ----------
W = "Wikimedia Commons"
M = {
    1: [(V04 / "s06_46c357.png", "Esquema Love/Rayleigh (generado)")],
    2: [(WEB / "foundation.jpg", f"{W}, CC BY-SA 4.0"), (WEB / "landslide.jpg", f"{W}, CC BY 4.0")],
    3: [(V04 / "s03_4093d7.png", "SPT / CPT (generado)"), (V04 / "s05_2f069b.png", "Ondas de cuerpo (generado)"),
        (V04 / "s06_46c357.png", "Ondas superficiales (generado)")],
    4: [(WEB / "spt.jpg", f"SPT, {W}, CC BY 4.0"), (WEB / "cpt_truck.jpg", f"CPT, {W} (geograph)"),
        (V04 / "s03_4093d7.png", "Esquema (generado)")],
    5: [(V04 / "s04_7b0b76.png", "Downhole / crosshole (generado)"), (A / "ch1_crosshole_testing.png", "Foti et al. 2014, cap. 1")],
    6: [(V04 / "s05_2f069b.png", "Refracción/reflexión (generado)"), (WEB / "refraction.png", f"{W}, dominio público")],
    7: [(V04 / "s06_46c357.png", "Love/Rayleigh en superficie (generado)"), (A / "ch1_2D_radiation_pattern_Rayleigh_surface.png", "Foti et al. 2014, Fig. 1.1")],
    8: [(V04 / "s11_607714.png", "Love (generado)"), (V04 / "s12_15a820.png", "Rayleigh (generado)")],
    9: [(FIG / "fig01_ondas_p_s_es.png", "Ondas P y S (propio)"), (A / "Pasted image 20260316135658.png", "Foti et al. 2014, Fig. 2.7")],
    10: [(G["gmax"], "Generado (esquema)")],
    11: [(FIG / "fig02_conversion_interfaz_es.png", "Conversión en interfaz (propio)"), (A / "Pasted image 20260316141217.png", "Foti et al. 2014, Fig. 2.10")],
    12: [(G["pie"], "Generado, datos Miller & Pursey"), (A / "Pasted image 20260316143212.png", "Foti et al. 2014, Fig. 2.12")],
    13: [(V04 / "s11_607714.png", "Love (generado)"), (A / "Pasted image 20260316140712.png", "Foti et al. 2014, Fig. 2.9")],
    14: [(V04 / "s12_15a820.png", "Rayleigh (generado)"), (A / "Pasted image 20260316144208.png", "Foti et al. 2014, Fig. 2.13")],
    15: [(A / "ch1_2D_radiation_pattern_Rayleigh_surface.png", "Foti et al. 2014, Fig. 1.1"), (A / "Pasted image 20260408094144.png", "Foti et al. 2014, Fig. 3.3")],
    16: [(V04 / "s14_b93a34.png", "Semiespacio homogéneo (generado)"), (G["flat"], "Generado")],
    17: [(G["nu"], "Generado (aprox. de Viktorov)")],
    18: [(V04 / "s18_6ae378.png", "Medio estratificado (generado)"), (A / "ch1 Geometric Dispersion of rayleigh waves.png", "Foti et al. 2014, Fig. 1.2")],
    19: [(V04 / "s17_e60734.png", "Profundidad vs λ (generado)"), (PRES / "dispersion_profundidad.png", "Propio")],
    20: [(A / "ch1_Example of processing of experimental data using wavenumber analysis.png", "Foti et al. 2014, Fig. 1.6"), (MASW / "figuras_informe__fig_curvas.png", "Propio (MASW)")],
    21: [(A / "ch1 Example of inversion procecss.png", "Foti et al. 2014, Fig. 1.7"), (MASW / "figuras_informe__fig_vs.png", "Propio (inversión)")],
    22: [(A / "Pasted image 20260414154041.png", "Foti et al. 2014, Fig. 3.43"), (A / "Pasted image 20260415161954.png", "Foti et al. 2014, Fig. 4.5")],
    23: [(A / "Pasted image 20260414154541.png", "Foti et al. 2014, Fig. 3.45"), (A / "Pasted image 20260408105916.png", "Foti et al. 2014, Fig. 3.5")],
    24: [(LIN, "Lin & Ashlock 2016, Fig. 1"), (MASW / "figuras__fig1_qc_alineacion_stack.png", "Propio (alineación y stack)")],
    25: [(MASW / "figuras_informe__fig_gather.png", "Propio (gather)"), (MASW / "figuras_informe__fig_imagenes.png", "Propio (imaging)")],
    26: [(HIST / "geometria_campanas.png", "Propio (histórico, revisar)"), (A / "Pasted image 20260408110343.png", "Foti et al. 2014, Fig. 3.7")],
    27: [(PRES / "d_arquitectura_nodos.png", "Propio"), (VIS / "D04.png", "Propio (drawio D04)")],
    28: [(V04 / "s26_0c5aa1.png", "SM-24 (propio/brochure)"), (WEB / "geophone.jpg", f"Geófono, {W}")],
    29: [(FIG / "fig07_respuesta_sm24_modelo.png", "Propio (modelo SM-24)")],
    30: [(G["comp"], "Generado (concepto)"), (REV / "transductores" / "sm24_funcion_transferencia_previa.png", "Propio")],
    31: [(VIS / "D08.png", "Propio (drawio D08)"), (G["comp"], "Generado (concepto)")],
    32: [(V04 / "s33_dae964.png", "Propio (AFE PSoC)"), (FIG / "fig08_f_frente_analogico_crop.png", "Propio (frente analógico)")],
    33: [(V04 / "s34_dc6945.png", "Propio (Bode medido)"), (FIG / "fig12_f_cadena_geo_adc_magcoh.png", "Propio (cadena GEO-ADC)")],
    34: [(FIG / "fig09_d_calibracion_offset.png", "Propio (calibración offset)"), (VIS / "D09.png", "Propio (drawio D09)")],
    35: [(VIS / "D10.png", "Propio (FSM captura)"), (FIG / "fig10_f_senales_por_etapa.png", "Propio (señales por etapa)")],
    36: [(V04 / "s39_865328.png", "Propio (señales por etapa)"), (FIG / "fig11_f_ruta_pga_adc.png", "Propio (ruta PGA-ADC)")],
    37: [(V04 / "s40_a0c4b0.png", "Propio (hardware digital PSoC)"), (VIS / "D13.png", "Propio (drawio D13)")],
    38: [(V04 / "s41_f569d7.png", "Propio (secuencia START)"), (VIS / "D05.png", "Propio (drawio D05)")],
    39: [(HIST / "sincronizacion_fase.png", "Propio (histórico, rehacer)"), (FIG / "secuencia_start_multinodo.png", "Propio")],
    40: [(V04 / "s43_68a402.png", "Martillo PCB 086D20 (propio)"), (FIG / "fig14_acondicionamiento_martillo_psoc.png", "Propio")],
    41: [(FIG / "fig15_i_web_maestro_claro.png", "Propio (web maestro)"), (V04 / "s44_be8902.jpg", "Propio (Geophone Scope)")],
    42: [(V04 / "s43_8a29b0.png", "Propio (secuencia)"), (WEB / "esp32.jpg", f"ESP32, {W}, CC BY-SA 4.0")],
    43: [(V04 / "s46_047827.png", "Propio (SNR por banda)")],
    44: [(V04 / "s47_25cc1c.png", "Propio (registro U(x,t))"), (FIG / "fig19_waterfall_4s_v2.png", "Propio (waterfall)")],
    45: [(V04 / "s50_154727.png", "Propio (MASW)"), (V04 / "s45_29830d.png", "Propio (adquisición real)")],
    46: [(FIG / "fuente_excitacion_actual.jpg", "Propio (excitación actual)"), (PRES / "evidencia" / "ensayo_impactos_periodicos_manual" / "01_senal_geo1_60s_impactos_aprox_1Hz.png", "Propio (impactos 1 Hz)")],
    47: [(VIS / "D01.png", "Propio (sistema completo, drawio D01)")],
}

# ---------- construcción ----------
prs = Presentation(SRC)
SW, SH = prs.slide_width, prs.slide_height
TOP, BOT = Inches(0.95), Inches(4.95)
X0, X1 = Inches(4.6), Inches(9.6)


def fit(w, h, bw, bh):
    r = min(bw / w, bh / h)
    return int(w * r), int(h * r)


def add_img(slide, path, box):
    l, t, bw, bh = box
    path = Path(path)
    assert path.exists(), path
    shutil.copy(path, OUTDIR / path.name) if path.parent != OUTDIR else None
    iw, ih = Image.open(path).size
    cap_h = Inches(0.18)
    w, h = fit(iw, ih, bw, bh - cap_h)
    pic = slide.shapes.add_picture(str(path), l + (bw - w) // 2, t + (bh - cap_h - h) // 2, width=w, height=h)
    return pic, l, t + bh - cap_h, bw, cap_h


def caption(slide, text, l, t, w, h):
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame
    tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "Placeholder · " + text
    p.runs[0].font.size = Pt(7)
    p.runs[0].font.italic = True
    p.runs[0].font.color.rgb = RGBColor(0x80, 0x80, 0x80)
    p.alignment = 2


for i, slide in enumerate(prs.slides, 1):
    items = M[i]
    body = slide.shapes[2]
    if i == 1:  # portada: texto intacto, imagen decorativa abajo-derecha
        boxes = [(Inches(6.0), Inches(0.4), Inches(3.6), Inches(2.4))]
    else:
        body.left, body.top, body.width, body.height = Inches(0.5), Inches(1.0), Inches(3.9), Inches(3.8)
        for r in body.text_frame.paragraphs[0].runs:
            r.font.size = Pt(16)
        n = len(items)
        if n == 1:
            boxes = [(X0, TOP, X1 - X0, BOT - TOP)]
        elif n == 2:
            h = (BOT - TOP - Inches(0.1)) // 2
            boxes = [(X0, TOP, X1 - X0, h), (X0, TOP + h + Inches(0.1), X1 - X0, h)]
        else:
            h = (BOT - TOP - Inches(0.2)) // 3
            boxes = [(X0, TOP + k * (h + Inches(0.1)), X1 - X0, h) for k in range(3)]
    for (path, src), box in zip(items, boxes):
        pic, cl, ct, cw, ch = add_img(slide, path, box)
        caption(slide, src, cl, ct, cw, ch)

prs.save(OUT)
print("saved", OUT, len(prs.slides))
