# -*- coding: utf-8 -*-
"""
Vuelca la base de datos bibliografica estructurada del proyecto.

La base tiene 65 articulos con 34 campos cada uno, entre ellos "conclusiones
clave" y "utilidad para tesis", escritos durante la revision. Es el registro de
QUE se leyo y PARA QUE servia cada cosa; sin volcarlo, esa informacion solo vive
en un CSV que nadie va a abrir dentro de seis meses.

Se emite en dos partes:
  1) una tabla-indice compacta (id, autores, ano, metodo, relevancia)
  2) una ficha por articulo con los campos sustantivos

Uso:  python gen_base_bibliografica.py <csv> <salida.tex>
"""
import csv
import io
import re
import sys

CSV, OUT = sys.argv[1], sys.argv[2]

UNI = {"…": "...", "—": "---", "–": "--", "“": "``", "”": "''", "‘": "`",
       "’": "'", "→": r"$\rightarrow$", "≈": r"$\approx$", "≥": r"$\geq$",
       "≤": r"$\leq$", "±": r"$\pm$", "×": r"$\times$", "·": r"$\cdot$",
       "°": r"$^{\circ}$", "µ": r"$\mu$", "μ": r"$\mu$", "Δ": r"$\Delta$",
       "λ": r"$\lambda$", "ζ": r"$\zeta$", "ω": r"$\omega$", "σ": r"$\sigma$",
       "α": r"$\alpha$", "β": r"$\beta$", "π": r"$\pi$", "²": r"$^2$",
       "³": r"$^3$", "•": r"\textbullet{}", " ": " ", "∼": r"$\sim$",
       "~": r"\textasciitilde{}"}


def esc(s, tope=None):
    s = (s or "").strip()
    if tope and len(s) > tope:
        c = s.rfind(" ", 0, tope)
        s = s[:c if c > tope * 0.6 else tope].rstrip(" ,;.") + "..."
    s = s.replace("\\", "/")
    for a, b in (("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"),
                 ("_", r"\_"), ("{", r"\{"), ("}", r"\}"),
                 ("^", r"\textasciicircum{}")):
        s = s.replace(a, b)
    for a, b in UNI.items():
        s = s.replace(a, b)
    out = []
    for ch in s:
        try:
            ch.encode("latin-1")
            out.append(ch)
        except UnicodeEncodeError:
            out.append("")
    return "".join(out)


def primer_autor(a):
    a = (a or "").split(";")[0].strip()
    return a if a else "---"


with io.open(CSV, encoding="utf-8", errors="replace") as f:
    filas = list(csv.DictReader(f))

L = []
L.append(r"\section{La base bibliogr\'afica, art\'iculo por art\'iculo}")
L.append(r"\label{sec:base-biblio}")
L.append("")
L.append(r"""Durante la revisi\'on se construy\'o una base de datos estructurada
de \textbf{%d art\'iculos}, con \textbf{34 campos por entrada}: m\'etodo
principal y secundario, tipo de sensor y de fuente, geometr\'ia del arreglo, tipo
de sitio, procesamiento e inversi\'on empleados, variables estimadas,
limitaciones reportadas, conclusiones clave y ---el campo que m\'as se us\'o---
\emph{utilidad para la tesis}.

Ese trabajo est\'a hoy en un CSV
(\texttt{docs/investigacion/sources/research/tables/}) que nadie va a volver a
abrir. Se vuelca aqu\'i para que quede legible: primero el \'indice, despu\'es
una ficha por art\'iculo con los campos sustantivos.""" % len(filas))
L.append("")

# ------------------------------------------------------------------ indice
L.append(r"\subsection{\'Indice}")
L.append(r"\footnotesize")
L.append(r"\begin{longtable}{@{}p{0.9cm} p{3.5cm} p{0.9cm} p{3.4cm} p{6.4cm}@{}}")
enc = (r"\toprule \textbf{Id} & \textbf{Primer autor} & \textbf{A\~no} & "
       r"\textbf{M\'etodo} & \textbf{Relevancia declarada} \\ \midrule")
L.append(enc)
L.append(r"\endfirsthead")
L.append(enc)
L.append(r"\endhead")
L.append(r"\bottomrule \endfoot")
for r in filas:
    L.append(r"%s & %s & %s & %s & %s \\" % (
        esc(r.get("id", "")), esc(primer_autor(r.get("autores")), 26),
        esc(r.get("anio", "")), esc(r.get("metodo_principal", ""), 26),
        esc(r.get("relevancia_para_tesis", "") or r.get("categoria", ""), 96)))
L.append(r"\end{longtable}")
L.append(r"\normalsize")
L.append("")

# ------------------------------------------------------------------ fichas
L.append(r"\subsection{Fichas}")
L.append("")
CAMPOS = [
    ("metodo_principal",        "M\\'etodo principal", 120),
    ("metodo_secundario",       "M\\'etodo secundario", 120),
    ("tipo_de_sensor",          "Sensor", 110),
    ("tipo_de_fuente",          "Fuente", 110),
    ("geometria_del_arreglo",   "Arreglo", 130),
    ("tipo_de_sitio",           "Sitio", 110),
    ("profundidad_investigada", "Profundidad", 110),
    ("procesamiento_usado",     "Procesamiento", 170),
    ("inversion_usada",         "Inversi\\'on", 170),
    ("variables_estimadas",     "Variables estimadas", 170),
    ("limitaciones_reportadas", "Limitaciones reportadas", 420),
    ("conclusiones_clave",      "Conclusiones clave", 520),
    ("utilidad_para_tesis",     "Utilidad para la tesis", 520),
    ("economicidad_y_factibilidad", "Economicidad y factibilidad", 300),
]
for r in filas:
    titulo = esc(r.get("titulo", ""), 150)
    autores = esc(r.get("autores", ""), 170)
    L.append(r"\paragraph{[%s] %s} \emph{%s} (%s)." % (
        esc(r.get("id", "")), titulo, autores, esc(r.get("anio", ""))))
    if r.get("doi"):
        L.append(r"{\scriptsize DOI: \texttt{%s}}" % esc(r["doi"]))
    L.append("")
    L.append(r"\begin{center}\scriptsize")
    L.append(r"\begin{tabularx}{\textwidth}{@{}>{\bfseries}p{3.3cm} X@{}}")
    L.append(r"\toprule")
    hay = False
    for clave, etiqueta, tope in CAMPOS:
        v = (r.get(clave) or "").strip()
        if not v or v.lower() in ("n/a", "na", "-", "no aplica"):
            continue
        hay = True
        L.append(r"%s & %s \\" % (etiqueta, esc(v, tope)))
    if not hay:
        L.append(r"--- & sin datos registrados \\")
    L.append(r"\bottomrule")
    L.append(r"\end{tabularx}")
    L.append(r"\end{center}")
    L.append("")

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print(f"escrito {OUT}: {len(filas)} articulos")
