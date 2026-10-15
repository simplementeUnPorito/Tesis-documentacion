"""Quita referencias duplicadas y las reparte entre las slides «Referencias» sin pasar el alto de la caja.
Altos por entrada medidos en PowerPoint: 1 línea ≈ 17,6 pt, 2 líneas ≈ 30,2 pt (con espacio posterior); caja 241 pt."""
import sys, unicodedata, re, pptx
from pptx_helpers_v30 import NS, A, top_shapes

deck = sys.argv[1]
H1, H2, CAP, CHARS_1LINE = 17.6, 30.2, 236.0, 120
prs = pptx.Presentation(deck)
boxes = [(sl, sh) for sl in prs.slides for sh in sl.shapes if sh.name == "Referencias"]
txt = lambda e: "".join(t.text or "" for t in e.iter(A + 't'))
key = lambda e: unicodedata.normalize('NFKD', txt(e)).encode('ascii', 'ignore').decode().lower()
seen, pars = set(), []
for _, b in boxes:
    for p in b.text_frame.paragraphs:
        if txt(p._p) not in seen: seen.add(txt(p._p)); pars.append(p._p)
pars.sort(key=key)
for _, b in boxes:
    tx = b.text_frame._txBody
    for p in tx.findall(A + 'p'): tx.remove(p)
hs = [H1 if len(txt(e)) <= CHARS_1LINE else H2 for e in pars]
CAP = min(CAP, sum(hs) / len(boxes) + 20)  # parejo entre slides, sin pasar la caja
k, used = 0, 0.0
for e in pars:
    h = H1 if len(txt(e)) <= CHARS_1LINE else H2
    if used + h > CAP and k < len(boxes) - 1: k, used = k + 1, 0.0
    boxes[k][1].text_frame._txBody.append(e); used += h
n = len(boxes)
for i, (sl, _) in enumerate(boxes, 1):
    for t in top_shapes(sl, "Título")[1][0].iter(A + 't'):
        if t.text and "Referencias" in t.text: t.text = re.sub(r"\(\d de \d\)", f"({i} de {n})", t.text)
prs.save(deck)
print(len(pars), "referencias únicas;", [len(b.text_frame.paragraphs) for _, b in boxes])
