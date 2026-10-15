"""v30 larga, paso 4: ajustes de desborde (23, 33, 54 y referencias 4 de 5) y subíndices de la tabla de sensores."""
import sys, pptx
from pptx_helpers_v30 import NS, A, ptext, top_shapes, plain_par, body_par

deck = sys.argv[1]
prs = pptx.Presentation(deck)
S = lambda n: prs.slides[n - 1]
title = lambda n: ptext(top_shapes(S(n), "Título")[1][0].find('.//a:p', NS))

assert title(23).startswith("Los ángulos de las ondas")
plain_par(body_par(S(23), "Cuerpo", "Se aplica tanto")[1], "Se aplica tanto a ondas P como S")

assert title(33).startswith("La superficie libre")
plain_par(body_par(S(33), "Cuerpo", "El aire no transmite")[1], "El aire no transmite esfuerzos: en la superficie el esfuerzo es cero")

s = S(54); assert title(54).startswith("Transductores posibles")
tbl = next(sh for sh in s.shapes if sh.has_table).table
plain_par(tbl.cell(0, 2)._tc.find('.//a:p', NS), "Precio (USD, 31/08/2026)")
for r, val in ((1, "10 Hz"), (2, "4,5 Hz")):
    plain_par(tbl.cell(r, 1)._tc.find('.//a:p', NS), [("f", "i"), ("n", "s"), (" = " + val, "n")])
plain_par(tbl.cell(1, 3)._tc.find('.//a:p', NS), "Pasivo. Atenúa por debajo de su frecuencia natural")
cita = next(sh for sh in s.shapes if sh.name == "Cita")
cita.text_frame.paragraphs[0].runs[0].text = ("Sensor Nederland B.V. (2006); R. T. Clark (2026); Analog Devices (2026); "
                                              "Güralp Systems (s. f.); SparkFun Electronics (2026); DigiKey (2026).")

boxes = [sh for sl in prs.slides for sh in sl.shapes if sh.name == "Referencias"]
last = boxes[3].text_frame.paragraphs[-1]._p
boxes[4].text_frame.paragraphs[0]._p.addprevious(last)

prs.save(deck)
print("ok")
