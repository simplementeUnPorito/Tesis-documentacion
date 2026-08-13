# -*- coding: utf-8 -*-
"""
Genera el apendice con el registro completo de commits de todos los repositorios
del proyecto, agrupado por dia.

La idea es que sea una ayuda-memoria literal: leyendo un dia se recuerda que se
estaba haciendo ese dia y en que subsistema. Por eso se agrupa por FECHA y no
por repositorio: el trabajo real cruzaba repositorios el mismo dia (se tocaba el
PSoC y el ESP y la interfaz en la misma sesion).

Uso:  python gen_bitacora_commits.py <raiz_repo> <salida.tex>
"""
import subprocess
import sys
import os
import re
from collections import defaultdict

RAIZ, OUT = sys.argv[1], sys.argv[2]

REPOS = [
    (".",                          "super"),
    ("src/firmware/psoc",          "PSoC"),
    ("src/firmware/esp32",         "ESP32"),
    ("src/interfaces/python",      "Py-int"),
    ("src/interfaces/matlab",      "ML-int"),
    ("src/calculos_modelados/matlab", "ML-calc"),
    ("src/calculos_modelados/python", "Py-calc"),
    ("data",                       "Datos"),
    ("docs",                       "Docs"),
    ("PCBs",                       "PCBs"),
]

# Commits automaticos que no aportan memoria: se cuentan pero no se listan.
RUIDO = re.compile(
    r"^(Auto-guardado|Actualizar subm[oó]dulos|Merge branch|Merge pull request|"
    r"Update submodule|chore\(sync\))", re.I)


# Los mensajes traen matematica y flechas escritas en Unicode directo, que
# inputenc con T1 no sabe componer. Se traducen a macros equivalentes.
UNICODE = {
    "τ": r"$\tau$", "λ": r"$\lambda$", "ζ": r"$\zeta$", "ω": r"$\omega$",
    "μ": r"$\mu$", "Δ": r"$\Delta$", "Σ": r"$\Sigma$", "σ": r"$\sigma$",
    "π": r"$\pi$", "α": r"$\alpha$", "β": r"$\beta$", "θ": r"$\theta$",
    "φ": r"$\varphi$", "ε": r"$\varepsilon$", "ρ": r"$\rho$",
    "↔": r"$\leftrightarrow$", "→": r"$\rightarrow$", "←": r"$\leftarrow$",
    "⇒": r"$\Rightarrow$", "≥": r"$\geq$", "≤": r"$\leq$", "≈": r"$\approx$",
    "≠": r"$\neq$", "±": r"$\pm$", "×": r"$\times$", "·": r"$\cdot$",
    "∞": r"$\infty$", "√": r"$\sqrt{\ }$", "°": r"$^{\circ}$",
    "…": "...", "—": "---", "–": "--", "•": r"\textbullet{}",
    "“": "``", "”": "''", "‘": "`", "’": "'", " ": " ",
    "⚠": r"[!]", "✓": r"[ok]", "✅": r"[ok]", "❌": r"[x]", "★": r"*",
    "²": r"$^2$", "³": r"$^3$", "½": r"$1/2$", "€": r"EUR", "≡": r"$\equiv$",
}


def esc(s):
    """Escapa para LaTeX. Los mensajes traen de todo."""
    s = s.replace("\\", "\\textbackslash{}")
    for a, b in (("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"),
                 ("_", r"\_"), ("{", r"\{"), ("}", r"\}"),
                 ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}")):
        s = s.replace(a, b)
    for a, b in UNICODE.items():
        s = s.replace(a, b)
    # Cualquier resto no-latin1 se sustituye antes de que rompa la compilacion.
    fuera = []
    for ch in s:
        try:
            ch.encode("latin-1")
            fuera.append(ch)
        except UnicodeEncodeError:
            fuera.append("?")
    return "".join(fuera)


por_dia = defaultdict(list)
totales = defaultdict(int)
ruido_n = 0

for ruta, etiqueta in REPOS:
    d = os.path.join(RAIZ, ruta)
    if not os.path.isdir(os.path.join(d, ".git")) and not os.path.exists(os.path.join(d, ".git")):
        continue
    try:
        out = subprocess.run(
            ["git", "-C", d, "log", "--all", "--date=short",
             "--format=%ad\x01%s", "--no-merges"],
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=120).stdout
    except Exception as e:
        print("  ! fallo", ruta, e)
        continue
    vistos = set()
    for linea in out.splitlines():
        if "\x01" not in linea:
            continue
        fecha, asunto = linea.split("\x01", 1)
        asunto = asunto.strip()
        totales[etiqueta] += 1
        if RUIDO.match(asunto):
            ruido_n += 1
            continue
        clave = (fecha, asunto)
        if clave in vistos:      # el mismo commit puede aparecer en varias ramas
            continue
        vistos.add(clave)
        por_dia[fecha].append((etiqueta, asunto))

MESES = {"01": "enero", "02": "febrero", "03": "marzo", "04": "abril",
         "05": "mayo", "06": "junio", "07": "julio", "08": "agosto",
         "09": "septiembre", "10": "octubre", "11": "noviembre",
         "12": "diciembre"}

L = []
L.append(r"\section{Registro completo de \emph{commits}}")
L.append(r"\label{sec:commits}")
L.append("")
L.append(r"""Este ap\'endice lista \textbf{todos} los \emph{commits} de los diez
repositorios del proyecto, agrupados por d\'ia y no por repositorio. El
agrupamiento por fecha es deliberado: el trabajo real cruzaba subsistemas dentro
de la misma sesi\'on ---se tocaba el PSoC, el ESP y la interfaz el mismo d\'ia---
y leer un d\'ia completo reconstruye mejor el recuerdo que leer un repositorio
completo.""")
L.append("")
L.append(r"""Los mensajes se transcriben \textbf{literalmente}, incluidos los que
no son descriptivos. Se conservan a prop\'osito: ``\texttt{AYUDAAAAAAAAAAA}'' del
28 de mayo o ``\texttt{ayuda dios santo que dificil todo}'' del 11 de julio son,
en la pr\'actica, marcadores de las semanas duras, y ubicarlos en el calendario
tiene valor de memoria. Se omiten \'unicamente los \emph{commits} autom\'aticos de
guardado y de actualizaci\'on de subm\'odulos, que no aportan informaci\'on
(%d en total).""" % ruido_n)
L.append("")

# Tabla de totales
L.append(r"\begin{center}\footnotesize")
L.append(r"\begin{tabular}{@{}lr@{}}")
L.append(r"\toprule")
L.append(r"Repositorio & \emph{Commits} \\")
L.append(r"\midrule")
NOMBRES = {"super": "Superproyecto", "PSoC": "Firmware PSoC 5LP",
           "ESP32": "Firmware ESP32", "Py-int": "Interfaces Python",
           "ML-int": "Interfaces MATLAB", "ML-calc": "C\\'alculos MATLAB",
           "Py-calc": "C\\'alculos Python", "Datos": "Datos",
           "Docs": "Documentaci\\'on", "PCBs": "PCBs"}
for _, et in REPOS:
    if totales[et]:
        L.append(r"%s & %d \\" % (NOMBRES.get(et, et), totales[et]))
L.append(r"\midrule")
L.append(r"\textbf{Total} & \textbf{%d} \\" % sum(totales.values()))
L.append(r"\bottomrule")
L.append(r"\end{tabular}")
L.append(r"\end{center}")
L.append("")

mes_actual = None
L.append(r"\footnotesize")
L.append(r"\begin{longtable}{@{}p{1.7cm} p{1.5cm} p{12.2cm}@{}}")
L.append(r"\toprule \textbf{Fecha} & \textbf{Repo} & \textbf{Mensaje del \emph{commit}} \\ \midrule")
L.append(r"\endfirsthead")
L.append(r"\toprule \textbf{Fecha} & \textbf{Repo} & \textbf{Mensaje del \emph{commit}} \\ \midrule")
L.append(r"\endhead")
L.append(r"\bottomrule \endfoot")

for fecha in sorted(por_dia):
    a, m, d = fecha.split("-")
    mes = MESES[m] + " " + a
    if mes != mes_actual:
        mes_actual = mes
        L.append(r"\multicolumn{3}{@{}l}{\rule{0pt}{1.5em}\textbf{\large %s}} \\[0.2em]"
                 % mes.capitalize())
    entradas = por_dia[fecha]
    for i, (et, asunto) in enumerate(entradas):
        celda_fecha = r"\textbf{%s/%s}" % (d, m) if i == 0 else ""
        L.append(r"%s & \texttt{\scriptsize %s} & %s \\" % (celda_fecha, et, esc(asunto)))

L.append(r"\end{longtable}")
L.append(r"\normalsize")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")

print(f"escrito {OUT}: {sum(len(v) for v in por_dia.values())} commits listados "
      f"en {len(por_dia)} dias ({ruido_n} automaticos omitidos, "
      f"{sum(totales.values())} totales)")
