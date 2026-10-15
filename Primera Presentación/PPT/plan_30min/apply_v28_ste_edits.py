import sys, json, pptx
from collections import Counter

# (viejo, nuevo): reemplazo de subcadena dentro de un único run
R = [
 ("Hay dos familias de ensayos; los de penetración", "Hay dos familias de ensayos, y los de penetración"),
 ("; falta la superficie", ". Faltan los métodos de superficie"),
 ("P y SV se convierten entre sí; SH queda aparte", "P y SV se convierten entre sí, y SH queda aparte"),
 ("Dan información inicial y localizada del terreno; extrapolarla", "Dan información inicial y localizada del terreno. Extrapolarla"),
 ("La medición fija requerimientos; el sistema", "La medición fija requerimientos, y el sistema"),
 ("excita la masa; la tensión", "excita la masa, y la tensión"),
 ("Cuatro técnicas para mejorar la baja frecuencia; elegimos", "Hay cuatro técnicas para mejorar la baja frecuencia, y elegimos"),
 ("de 10 mHz a 200 kHz; magnitud", "de 10 mHz a 200 kHz. Magnitud"),
 ("Gris: osciloscopio; color:", "Gris: osciloscopio. Color:"),
 ("hace falta velocidad; en señales lentas", "hace falta velocidad. En señales lentas"),
 ("por costo y simplicidad; el error de fase", "por costo y simplicidad, y el error de fase"),
 ("Lo usan equipos comerciales; costo y cobertura", "Lo usan equipos comerciales. Contras: costo y cobertura"),
 ("Sin ACK; barato y ya integrado", "Sin ACK. Barato y ya integrado"),
 ("El disparo va por broadcast; se midió su jitter y se declaran sus límites", "El disparo va por broadcast, con su jitter medido y sus límites declarados"),
 ("por determinismo: una captura que no dispara se repite; una desalineada", "por determinismo. Una captura que no dispara se repite. Una desalineada"),
 ("común a todas las trazas; con varios nodos simultáneos dominaría", "común a todas las trazas. Con varios nodos simultáneos, dominaría"),
 ("ppm ilustrativos; ±1", "ppm ilustrativos, y ±1"),
 ("con corriente constante; luego desacople", "con corriente constante. Luego, desacople"),
 ("AFE y ADC; captura y registro local", "AFE y ADC. Captura y registro local"),
 ("están diseñados; picking e inversión", "están diseñados. Picking e inversión"),
 ("reensambla las trazas; el navegador", "reensambla las trazas. El navegador"),
 ("4 m; a c = 150", "4 m. A c = 150"),
 ("sintetiza el registro; no equivale", "sintetiza el registro, que no equivale"),
 ("mueven la fuente; acá es al revés", "mueven la fuente. Aquí es al revés"),
 ("al ajustar 21 posiciones; uno sistemático", "al ajustar 21 posiciones. Uno sistemático"),
 ("se anotan a mano; no se conservaron", "se anotan a mano. No se conservaron"),
 ("Arriba: el HAMMER; su pico fija", "Arriba: el HAMMER, cuyo pico fija"),
 ("golpes por posición; se descartaron", "golpes por posición. Se descartaron"),
 ("Demuestra adquisición secuencial; la curva", "Demuestra adquisición secuencial. La curva"),
 ("aislar la electrónica; comparar con", "aislar la electrónica, y comparación con"),
 ("Adquisición simultánea; fuente más repetible; SNR bajo 10 Hz", "Adquisición simultánea, fuente más repetible y SNR bajo 10 Hz"),
 ("internas del transceptor; ≈31 ns", "internas del transceptor, y ≈31 ns"),
 ("de todo flujo sincronizado; ante CAPTURE_SYNC_STALL, abortar y enviar NACK; agregar prueba", "de todo flujo sincronizado. Ante CAPTURE_SYNC_STALL, abortar y enviar NACK. Agregar una prueba"),
 ("arrancan bien; oculta un fallo excepcional", "arrancan bien. Oculta una falla excepcional"),
 ("la adquisición secuencial es viable; falta validar", "la adquisición secuencial es viable, pero falta validar"),
 ("Se verificó la adquisición; la caracterización", "Se verificó la adquisición. La caracterización"),
 ("recorta la señal; no se puede filtrar", "recorta la señal. No se puede filtrar"),
 ("Nos proponemos definir un método de medición del terreno que, mediante el procesamiento de lo sensado, permita obtener información útil",
  "Nos proponemos definir un método que mida el terreno y procese lo medido para obtener información útil"),
 ("la plataforma que realiza la medición", "la plataforma que mide"),
 ("este se deforma de forma transitoria", "este se deforma transitoriamente"),
 ("Más canales significa más nodos GEO", "Más canales significan más nodos GEO"),
 ("Es más complejo que la solución de Pazos, pero de complejidad razonable: permite controlar con mucha más facilidad hasta dónde se compensa, y ser más agresivo cuando el geófono está lejos de donde queremos que esté.",
  "Es más complejo que la solución de Pazos, pero de complejidad razonable. Permite controlar con mucha más facilidad hasta dónde se compensa. También permite compensar más cuando el geófono está lejos de la respuesta buscada."),
 ("Su única desventaja es la pérdida de ganancia: requiere más ganancia, que se redistribuye entre las etapas",
  "Su única desventaja es la pérdida de ganancia. Se recupera con más ganancia, repartida entre las etapas"),
 ("Se decidió que sea Bessel, de fase casi lineal", "Se eligió un Bessel, de fase casi lineal"),
 ("y el geófono se tomó con su modelo nominal", "y el geófono se representó con su modelo nominal"),
 ("El hardware decide cuándo y el software qué valores", "El hardware decide cuándo y el software decide qué valores"),
 ("No se puede atribuir la baja SNR a un solo elemento: cómo separar las causas", "La baja SNR no se atribuye a un solo elemento: pruebas para separar las causas"),
 ("unos 13,8 dB, sin agregar etapas: no suma ruido ni offset", "unos 13,8 dB, sin agregar etapas, así que no suma ruido ni offset"),
 ("(propuesta mía)", "(propuesta propia)"),
 ("con un retardo fijo y común nunca calibrado", "con un retardo fijo y común que nunca se calibró"),
]

def paras(prs):
    for i, s in enumerate(prs.slides, 1):
        def walk(sh):
            if sh.shape_type == 6:
                for g in sh.shapes: yield from walk(g)
                return
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs: yield p
            if getattr(sh, "has_table", False) and sh.has_table:
                for r in sh.table.rows:
                    for c in r.cells:
                        for p in c.text_frame.paragraphs: yield p
        for sh in s.shapes:
            for p in walk(sh): yield i, p

src, dst = sys.argv[1], sys.argv[2]
prs = pptx.Presentation(src)
hits, split = Counter(), []
for i, p in paras(prs):
    for old, new in R:
        done = False
        for r in p.runs:
            if old in r.text:
                r.text = r.text.replace(old, new); hits[old] += 1; done = True
        full = "".join(r.text for r in p.runs)
        if not done and old in full:
            split.append((i, old))
prs.save(dst)
print("aplicados:", sum(hits.values()), "reglas usadas:", len(hits), "/", len(R))
for old, _ in R:
    if not hits[old]: print("  sin uso:", old[:60])
for i, old in split: print("  CORTADO EN RUNS slide", i, ":", old[:60])
