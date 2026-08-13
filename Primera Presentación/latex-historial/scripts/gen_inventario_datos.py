# -*- coding: utf-8 -*-
"""
Recorre los datos crudos y arma el inventario de campanas: cuantas capturas,
en que fechas, con que frecuencia de muestreo, con que roles de nodo y con que
offsets geometricos.

Todo sale de los metadata.json que la propia interfaz escribio en cada captura,
asi que es el registro de lo que realmente se midio, no de lo que se planeo.

Uso:  python gen_inventario_datos.py <data/raw> <salida.tex>
"""
import json
import os
import sys
from collections import Counter, defaultdict

RAW, OUT = sys.argv[1], sys.argv[2]


def esc(s):
    s = str(s)
    for a, b in (("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"),
                 ("_", r"\_"), ("{", r"\{"), ("}", r"\}"),
                 ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}")):
        s = s.replace(a, b)
    return "".join(c if c.isascii() or c in "áéíóúñÁÉÍÓÚÑüÜ" else "?" for c in s)


campanas = {}
for camp in sorted(os.listdir(RAW)):
    d = os.path.join(RAW, camp)
    if not os.path.isdir(d):
        continue
    info = {
        "capturas": 0, "fs": Counter(), "fechas": set(), "lotes": [],
        "roles": Counter(), "offsets": set(), "nodos": Counter(),
        "tipos_hw": Counter(), "adc": Counter(),
    }
    for dirpath, dirnames, filenames in os.walk(d):
        if "metadata.json" not in filenames:
            continue
        try:
            with open(os.path.join(dirpath, "metadata.json"),
                      encoding="utf-8", errors="replace") as f:
                m = json.load(f)
        except Exception:
            continue
        if not isinstance(m, dict) or "fs" not in m:
            continue
        info["capturas"] += 1
        if m.get("fs"):
            info["fs"][m["fs"]] += 1
        st = m.get("save_time") or ""
        if len(st) >= 8:
            info["fechas"].add(f"{st[0:4]}-{st[4:6]}-{st[6:8]}")
        if m.get("n_batches"):
            info["lotes"].append(m["n_batches"])
        if m.get("n_slaves"):
            info["nodos"][m["n_slaves"]] += 1
        for nd in m.get("nodes", []) or []:
            if nd.get("role"):
                info["roles"][nd["role"]] += 1
            off = nd.get("offset_m", nd.get("offset"))
            if off is not None:
                try:
                    info["offsets"].add(round(float(off), 2))
                except (TypeError, ValueError):
                    pass
            if nd.get("type"):
                info["tipos_hw"][nd["type"]] += 1
            if nd.get("adc_range") is not None:
                info["adc"][nd["adc_range"]] += 1
    if info["capturas"]:
        campanas[camp] = info

L = []
L.append(r"\section{Inventario de datos crudos y campa\~nas}")
L.append(r"\label{sec:inventario-datos}")
L.append("")
L.append(r"""Reconstruido recorriendo los archivos \texttt{metadata.json} que la
propia interfaz escribi\'o junto a cada captura. Es, por lo tanto, el registro de
lo que \emph{realmente} se midi\'o, y no de lo que estaba planificado medir. Los
conjuntos completos viven bajo Git~LFS y hay que hidratarlos con
\texttt{data/scripts/hydrate-lfs.ps1} antes de poder abrirlos.""")
L.append("")

L.append(r"\begin{center}\footnotesize")
L.append(r"\begin{tabularx}{\textwidth}{@{}l r l r X@{}}")
L.append(r"\toprule")
L.append(r"Campa\~na & Capt. & Fechas & Lotes (mediana) & $F_s$ y roles observados \\")
L.append(r"\midrule")
for camp, i in campanas.items():
    fechas = sorted(i["fechas"])
    rango = fechas[0] if len(fechas) == 1 else (
        f"{fechas[0]} a {fechas[-1]}" if fechas else "---")
    lotes = sorted(i["lotes"])
    med = lotes[len(lotes) // 2] if lotes else 0
    fs_txt = ", ".join(f"{k}~Hz ({v})" for k, v in i["fs"].most_common())
    roles = ", ".join(f"{k} ({v})" for k, v in i["roles"].most_common())
    L.append(r"\texttt{%s} & %d & {\scriptsize %s} & %d & {\scriptsize %s%s} \\" % (
        esc(camp), i["capturas"], esc(rango), med, esc(fs_txt),
        ("; " + esc(roles)) if roles else ""))
L.append(r"\bottomrule")
L.append(r"\end{tabularx}")
L.append(r"\end{center}")
L.append("")

for camp, i in campanas.items():
    L.append(r"\subsection{\texttt{%s}}" % esc(camp))
    lotes = sorted(i["lotes"])
    if lotes:
        n = len(lotes)
        L.append(r"\textbf{Duraci\'on de captura.} %d capturas con recuento de lotes "
                 r"entre %d y %d (mediana %d). A 30 muestras por lote, eso son entre "
                 r"%s y %s muestras por canal." % (
                     n, lotes[0], lotes[-1], lotes[n // 2],
                     f"{lotes[0]*30:,}".replace(",", "."),
                     f"{lotes[-1]*30:,}".replace(",", ".")))
    if i["fechas"]:
        L.append(r"\textbf{D\'ias de adquisici\'on} (%d): %s." % (
            len(i["fechas"]), esc(", ".join(sorted(i["fechas"])))))
    if i["offsets"]:
        offs = sorted(i["offsets"])
        L.append(r"\textbf{Posiciones registradas} (%d distintas): de "
                 r"\SI{%g}{\meter} a \SI{%g}{\meter}." % (len(offs), offs[0], offs[-1]))
    if i["nodos"]:
        L.append(r"\textbf{Nodos por captura}: %s." % esc(
            ", ".join(f"{k} nodos en {v} capturas" for k, v in i["nodos"].most_common())))
    if i["tipos_hw"]:
        L.append(r"\textbf{Clases de hardware declaradas}: %s." % esc(
            ", ".join(f"{k} ({v})" for k, v in i["tipos_hw"].most_common())))
    L.append("")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print(f"escrito {OUT}: {len(campanas)} campanas, "
      f"{sum(i['capturas'] for i in campanas.values())} capturas con metadata")
