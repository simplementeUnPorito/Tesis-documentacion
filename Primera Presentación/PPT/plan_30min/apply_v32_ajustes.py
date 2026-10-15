"""v32 larga: acorta textos que desbordaban (64, 95, 114)."""
import sys, copy, pptx
from pptx_helpers_v30 import NS, ptext, unwrap, plain_par, body_par

deck = sys.argv[1]
prs = pptx.Presentation(deck)
S = lambda n: prs.slides[n - 1]

plain_par(body_par(S(64), "Cuerpo", "Una carga activa")[1],
          [("Una carga activa ", "n"), ("Z", "i"), ("L", "s"), (" (resistencia negativa) modifica el amortiguamiento", "n")])

tbl = next(sh for sh in S(95).shapes if sh.has_table).table
plain_par(tbl.cell(6, 2)._tc.find('.//a:p', NS), "≈ 150 ns (preliminar)")
plain_par(tbl.cell(4, 3)._tc.find('.//a:p', NS), "Equipos comerciales (Atom-3C). Contras: costo y cobertura")

sp = unwrap(S(114), "Cuerpo"); tx = sp.find('.//p:txBody', NS); ps = tx.findall('a:p', NS)
for p, line in zip(ps, ["FTM (IEEE 802.11) mide tiempos de vuelo entre ESP32-S3",
                        "Con FTS, cada esclavo ajusta su reloj al del maestro",
                        "Entre esclavos: flancos dentro de unos 150 ns (preliminar)",
                        "También estima distancias, aún sin precisión estable"]):
    plain_par(p, line)

prs.save(deck); print("ok")

# notas que todavía hablaban de UWB
prs = pptx.Presentation(deck)
S = lambda n: prs.slides[n - 1]
def nsub(n, old, new):
    tf = S(n).notes_slide.notes_text_frame
    if new in tf.text: return  # ya aplicado
    assert old in tf.text, (n, old[:40]); tf.text = tf.text.replace(old, new)
nsub(94, "Un posible camino futuro es UWB con ranging, que mediría la distancia entre nodos y atacaría a la vez el error de posición y el de sincronización.",
     "El FTM que estoy probando también estima distancias entre nodos: atacaría a la vez el error de posición y el de sincronización.")
nsub(95, "Por eso UWB aparece como trabajo futuro: Korsimaa publica más menos 4 nanosegundos con módulos DWM1000 de bajo costo.",
     "Por eso la sincronización sigue como trabajo en curso, con Wi-Fi FTM.")
nsub(95, "Nota para mí: las propiedades de Wi-Fi, LoRa y GPS son conocimiento general, no salen de una medición nuestra ni de una referencia citada en el repositorio; si me piden números, buscar una fuente. Los 4 nanosegundos y los demás datos de UWB salen de 08_trabajos_futuros.tex.",
     "Fuentes de la tabla: Wi-Fi, estándar IEEE 802.11-2020 (ACK, reintentos, CSMA/CA); LoRa, nota AN1200.13 de Semtech (tiempo en el aire); GPS en equipos comerciales, Geometrics Atom-3C.")
prs.save(deck); print("notas ok")
