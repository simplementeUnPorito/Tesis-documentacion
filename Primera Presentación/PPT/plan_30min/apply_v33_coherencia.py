"""v33 larga: correcciones de coherencia tras la lectura completa."""
import sys, pptx
from pptx_helpers_v30 import NS, A, ptext, top_shapes, unwrap, plain_par, body_par

deck = sys.argv[1]
prs = pptx.Presentation(deck)
S = lambda n: prs.slides[n - 1]
title = lambda n: ptext(top_shapes(S(n), "Título")[1][0].find('.//a:p', NS))
shape = lambda n, nm: next(sh for sh in S(n).shapes if sh.name == nm)
def check(n, start): assert title(n).startswith(start), (n, title(n)[:50])

# 97: la viñeta de los 35 Hz se había borrado por error al limpiar «(cálculo propio)» en la v29
check(97, "Un desfase de tiempo")
sp = unwrap(S(97), "Cuerpo"); ps = sp.findall('.//a:p', NS)
import copy
vacios = [p for p in ps if not ptext(p).strip()]
q = copy.deepcopy(ps[0]); plain_par(q, "Con 400 µs, los 5° se cumplen hasta unos 35 Hz")   # formato de la primera viñeta
if vacios: vacios[0].addprevious(q); vacios[0].getparent().remove(vacios[0])
else: ps[-1].addnext(q)

# 63: un solo término, «continua»
check(63, "Limitaciones de la compensación inversa")
plain_par(body_par(S(63), "Cuerpo", "Altísima ganancia")[1], "Altísima ganancia cerca de continua")

# 62: la tarjeta describe las dos técnicas activas, que ahora tienen una slide cada una (64 y 65)
check(62, "Existen cuatro familias")
p = shape(62, "Text 12").text_frame.paragraphs[0]
p.runs[0].text = "Un lazo activo modifica el amortiguamiento: con una carga negativa o con corriente en la bobina."
for r in p.runs[1:]: r._r.getparent().remove(r._r)

# 95: «No se conservaron coordenadas ni azimut» ya está en la 93
check(95, "Un error en la posición")
plain_par(body_par(S(95), "Cuerpo", "Hoy las posiciones")[1], "Hoy las posiciones se miden con cinta y se anotan a mano")

# 96: la frase final apunta al trabajo en curso, no a un «trabajo futuro» genérico
check(96, "Se eligió ESP-NOW")
p = shape(96, "Text 1").text_frame.paragraphs[0]
p.runs[0].text = "Con 400 µs el presupuesto de 5° a 50 Hz (278 µs) no se cumple: por eso se prueba Wi-Fi FTM."
for r in p.runs[1:]: r._r.getparent().remove(r._r)

prs.save(deck); print("ok")
