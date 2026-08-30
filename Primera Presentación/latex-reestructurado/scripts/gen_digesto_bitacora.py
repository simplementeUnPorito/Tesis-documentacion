# -*- coding: utf-8 -*-
"""
Digesto cronologico de la bitacora.

Cada entrada diaria de la bitacora arranca con una cabecera estructurada:
  **Etapa:**  ...
  **Hito:**   ...
  **Commits:** ...
  **Estado emocional:** ...

Este script extrae esos campos de las 68 entradas y arma un indice de una linea
por dia. No resume ni reescribe: transcribe lo que ya esta escrito, recortando
donde hace falta. La bitacora completa (1,3 MB) sigue siendo la fuente; esto es
el mapa para saber a que dia ir.

Uso:  python gen_digesto_bitacora.py <dir_bitacora> <salida.tex>
"""
import os
import re
import sys

DIR, OUT = sys.argv[1], sys.argv[2]

MESES = {"01": "enero", "02": "febrero", "03": "marzo", "04": "abril",
         "05": "mayo", "06": "junio", "07": "julio", "08": "agosto",
         "09": "septiembre", "10": "octubre", "11": "noviembre",
         "12": "diciembre"}

UNI = {"…": "...", "—": "---", "–": "--", "“": "``", "”": "''",
       "‘": "`", "’": "'", "→": r"$\rightarrow$", "←": r"$\leftarrow$",
       "↔": r"$\leftrightarrow$", "⇒": r"$\Rightarrow$", "≈": r"$\approx$",
       "≥": r"$\geq$", "≤": r"$\leq$", "±": r"$\pm$", "×": r"$\times$",
       "·": r"$\cdot$", "°": r"$^{\circ}$", "µ": r"$\mu$", "μ": r"$\mu$",
       "Δ": r"$\Delta$", "ζ": r"$\zeta$", "ω": r"$\omega$", "λ": r"$\lambda$",
       "τ": r"$\tau$", "σ": r"$\sigma$", "α": r"$\alpha$", "β": r"$\beta$",
       "π": r"$\pi$", "Σ": r"$\Sigma$", "∞": r"$\infty$", "²": r"$^2$",
       "³": r"$^3$", "•": r"\textbullet{}", " ": " ", "≠": r"$\neq$"}


def esc(s):
    s = s.replace("\\", "/")
    # El markdown de la bitacora usa **negrita** y `codigo`.
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r"`([^`]+?)`", lambda m: "\x02" + m.group(1) + "\x03", s)
    for a, b in (("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"),
                 ("_", r"\_"), ("^", r"\textasciicircum{}"),
                 ("~", r"\textasciitilde{}")):
        s = s.replace(a, b)
    for a, b in UNI.items():
        s = s.replace(a, b)
    s = s.replace("\x02", r"\texttt{").replace("\x03", "}")
    salida = []
    for ch in s:
        try:
            ch.encode("latin-1")
            salida.append(ch)
        except UnicodeEncodeError:
            salida.append("")
    return "".join(salida)


def campo(texto, nombre, tope=None):
    m = re.search(r"\*\*%s:?\*\*\s*(.+)" % nombre, texto)
    if not m:
        return ""
    v = m.group(1).strip()
    if tope and len(v) > tope:
        corte = v.rfind(" ", 0, tope)
        v = v[:corte if corte > tope * 0.6 else tope].rstrip(" ,;.") + "..."
    return v


entradas = []
for fn in sorted(os.listdir(DIR)):
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})\.md$", fn)
    if not m:
        continue
    with open(os.path.join(DIR, fn), encoding="utf-8", errors="replace") as f:
        txt = f.read(9000)
    entradas.append({
        "fecha": (m.group(1), m.group(2), m.group(3)),
        "etapa": campo(txt, "Etapa", 190),
        "hito": campo(txt, "Hito", 620),
        "commits": campo(txt, "Commits", 60),
        "animo": campo(txt, "Estado emocional", 300),
        "bytes": os.path.getsize(os.path.join(DIR, fn)),
    })

L = []
L.append(r"\section{Digesto cronol\'ogico de la bit\'acora}")
L.append(r"\label{sec:digesto}")
L.append("")
L.append(r"""La bit\'acora diaria son \textbf{%d entradas} y
\textbf{\SI{%.1f}{\mebi\byte}} de texto en
\texttt{docs/investigacion/Notes/bitacora/}. Cada entrada abre con una cabecera
estructurada ---etapa, hito, \emph{commits} y una nota sobre el \'animo del
d\'ia--- y sigue con el an\'alisis t\'ecnico completo de lo que se hizo, con
\emph{diffs} y mediciones.

Este digesto transcribe esas cabeceras, una l\'inea por d\'ia. No resume ni
reescribe: sirve para saber \emph{a qu\'e d\'ia ir} cuando uno recuerda un
problema pero no la fecha. La entrada completa siempre tiene m\'as.""" % (
    len(entradas), sum(e["bytes"] for e in entradas) / 1048576.0))
L.append("")

mes_actual = None
for e in entradas:
    a, m, d = e["fecha"]
    mes = f"{MESES[m].capitalize()} de {a}"
    if mes != mes_actual:
        mes_actual = mes
        L.append(r"\subsection{%s}" % mes)
    L.append(r"\paragraph{%s de %s.}" % (d.lstrip("0"), MESES[m]))
    if e["etapa"]:
        L.append(r"\emph{%s}" % esc(e["etapa"]))
    if e["hito"]:
        L.append("")
        L.append(esc(e["hito"]))
    if e["animo"]:
        L.append("")
        L.append(r"{\footnotesize\itshape \'Animo: %s}" % esc(e["animo"]))
    L.append("")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print(f"escrito {OUT}: {len(entradas)} entradas, "
      f"{sum(e['bytes'] for e in entradas)/1048576:.2f} MiB de bitacora")
