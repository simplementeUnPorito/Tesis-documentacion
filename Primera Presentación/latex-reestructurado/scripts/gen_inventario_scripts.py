# -*- coding: utf-8 -*-
"""
Genera el apendice de inventario de codigo: cada script de MATLAB y de Python
del proyecto, con su tamano y la primera linea util de su cabecera.

La descripcion NO se inventa: se extrae del propio archivo (docstring de Python,
bloque de comentario inicial de MATLAB). Si un archivo no tiene cabecera, se
declara "sin cabecera" en lugar de rellenar con una descripcion supuesta.

Uso:  python gen_inventario_scripts.py <raiz_repo> <salida.tex>
"""
import os
import re
import sys

RAIZ, OUT = sys.argv[1], sys.argv[2]

# Se excluyen dependencias de terceros, entornos virtuales y artefactos de build:
# no son trabajo del proyecto y ahogarian el inventario.
EXCLUIR = re.compile(
    r"(^|[\\/])(\.git|\.venv|venv|node_modules|third-party|__pycache__|"
    r"\.pio|site-packages|libdeps|Generated_Source|build|dist|\.vs)([\\/]|$)")

GRUPOS = [
    ("src/calculos_modelados/matlab",  "C\\'alculo y modelado --- MATLAB"),
    ("src/calculos_modelados/python",  "C\\'alculo y modelado --- Python"),
    ("src/interfaces/matlab",          "Interfaces de banco --- MATLAB"),
    ("src/interfaces/python",          "Interfaces y servidor --- Python"),
    ("src/firmware",                   "Utilidades del firmware"),
    ("data/scripts",                   "Gesti\\'on de datos"),
    ("scripts",                        "Automatizaci\\'on del repositorio"),
    ("docs",                           "Generaci\\'on de figuras y documentos"),
]


def esc(s):
    s = s.replace("\\", "/")
    for a, b in (("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"),
                 ("_", r"\_"), ("{", r"\{"), ("}", r"\}"),
                 ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}")):
        s = s.replace(a, b)
    salida = []
    for ch in s:
        try:
            ch.encode("latin-1")
            salida.append(ch)
        except UnicodeEncodeError:
            salida.append("?")
    return "".join(salida)


def cabecera(ruta):
    """Primera frase util del archivo, tomada de su propia cabecera."""
    try:
        with open(ruta, encoding="utf-8", errors="replace") as f:
            lineas = [next(f, "") for _ in range(40)]
    except Exception:
        return ""
    ext = os.path.splitext(ruta)[1].lower()
    texto = []
    if ext == ".py":
        cuerpo = "".join(lineas)
        m = re.search(r'"""(.*?)(?:"""|$)', cuerpo, re.S)
        if m:
            texto = [x.strip() for x in m.group(1).strip().splitlines()]
        else:
            texto = [l.lstrip("# ").strip() for l in lineas
                     if l.startswith("#") and not l.startswith("#!")
                     and "coding" not in l]
    else:  # MATLAB
        for l in lineas:
            l = l.strip()
            if l.startswith("%"):
                l = l.lstrip("%").strip()
                if l and not set(l) <= set("=-_ *"):
                    texto.append(l)
            elif l and not l.startswith("function"):
                break
            elif l.startswith("function"):
                continue
    # Se juntan las primeras lineas hasta tener una frase razonable.
    acum = ""
    for t in texto:
        if not t:
            if acum:
                break
            continue
        acum = (acum + " " + t).strip()
        if len(acum) > 130 or acum.endswith("."):
            break
    return acum[:230]


L = []
L.append(r"\section{Inventario de c\'odigo: todos los \emph{scripts} del proyecto}")
L.append(r"\label{sec:inventario-scripts}")
L.append("")
L.append(r"""Listado exhaustivo de los archivos \texttt{.m} y \texttt{.py}
escritos para el proyecto, con su tama\~no y la descripci\'on tomada
\textbf{de la propia cabecera del archivo}. Cuando un archivo no tiene cabecera
se declara as\'i, en lugar de rellenar con una descripci\'on supuesta. Se excluyen
dependencias de terceros, entornos virtuales y c\'odigo generado por las
herramientas.""")
L.append("")

total_arch = total_lin = 0
resumen = []

for base, titulo in GRUPOS:
    d = os.path.join(RAIZ, base)
    if not os.path.isdir(d):
        continue
    filas = []
    for dirpath, dirnames, filenames in os.walk(d):
        dirnames[:] = [x for x in dirnames if not EXCLUIR.search(x)]
        if EXCLUIR.search(dirpath):
            continue
        for fn in sorted(filenames):
            if not fn.lower().endswith((".m", ".py")):
                continue
            full = os.path.join(dirpath, fn)
            if EXCLUIR.search(full):
                continue
            try:
                with open(full, encoding="utf-8", errors="replace") as f:
                    n = sum(1 for _ in f)
            except Exception:
                continue
            rel = os.path.relpath(full, os.path.join(RAIZ, base)).replace("\\", "/")
            filas.append((rel, n, cabecera(full)))
    if not filas:
        continue
    filas.sort(key=lambda r: -r[1])
    lin = sum(r[1] for r in filas)
    total_arch += len(filas)
    total_lin += lin
    resumen.append((titulo, base, len(filas), lin))

    L.append(r"\subsection{%s}" % titulo)
    L.append(r"\textit{\small %s/ --- %d archivos, %s l\'ineas}" %
             (esc(base), len(filas), f"{lin:,}".replace(",", ".")))
    L.append(r"\footnotesize")
    L.append(r"\begin{longtable}{@{}p{5.4cm} r p{8.6cm}@{}}")
    L.append(r"\toprule \textbf{Archivo} & \textbf{L\'in.} & \textbf{Qu\'e hace (seg\'un su cabecera)} \\ \midrule")
    L.append(r"\endfirsthead")
    L.append(r"\toprule \textbf{Archivo} & \textbf{L\'in.} & \textbf{Qu\'e hace (seg\'un su cabecera)} \\ \midrule")
    L.append(r"\endhead")
    L.append(r"\bottomrule \endfoot")
    for rel, n, desc in filas:
        desc = esc(desc) if desc else r"\textit{sin cabecera}"
        L.append(r"\texttt{\scriptsize %s} & %d & %s \\" % (esc(rel), n, desc))
    L.append(r"\end{longtable}")
    L.append(r"\normalsize")
    L.append("")

# Resumen al principio: se inserta despues de haber contado.
cab = [r"\begin{center}\footnotesize",
       r"\begin{tabular}{@{}l r r@{}}", r"\toprule",
       r"Grupo & Archivos & L\'ineas \\", r"\midrule"]
for titulo, base, na, nl in resumen:
    cab.append(r"%s & %d & %s \\" % (titulo, na, f"{nl:,}".replace(",", ".")))
cab.append(r"\midrule")
cab.append(r"\textbf{Total} & \textbf{%d} & \textbf{%s} \\" %
           (total_arch, f"{total_lin:,}".replace(",", ".")))
cab += [r"\bottomrule", r"\end{tabular}", r"\end{center}", ""]

L = L[:5] + cab + L[5:]

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print(f"escrito {OUT}: {total_arch} archivos, {total_lin} lineas")
