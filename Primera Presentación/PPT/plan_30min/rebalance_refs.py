"""Pasa la última referencia de la slide 2 de 4 a la 3, y la última de la 3 a la 4 (para la v29 se corrió dos veces)."""
import sys, pptx
A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
prs = pptx.Presentation(sys.argv[1])
boxes = [sh for s in prs.slides for sh in s.shapes if sh.name == "Referencias"]
n = len(boxes)
for src, dst in ((n - 3, n - 2), (n - 2, n - 1)):
    last = boxes[src].text_frame.paragraphs[-1]._p
    print("mueve:", "".join(t.text for t in last.iter(A + 't'))[:50])
    boxes[dst].text_frame.paragraphs[0]._p.addprevious(last)
prs.save(sys.argv[1])
