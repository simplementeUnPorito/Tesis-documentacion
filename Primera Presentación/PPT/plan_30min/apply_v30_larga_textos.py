"""v30 larga, paso 1: textos sobre la numeración de la v29.
Registro impersonal (sin primera persona), títulos que presentan sin repetir las viñetas,
«pequeña señal» -> «pequeña deformación», y los ajustes puntuales de las slides 22 y 32–43."""
import sys, copy
import pptx
from lxml import etree

NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
      'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math'}
P = '{%s}' % NS['p']; A = '{%s}' % NS['a']; M = '{%s}' % NS['m']; MC = '{%s}' % NS['mc']
src, dst = sys.argv[1], sys.argv[2]
prs = pptx.Presentation(src)
S = lambda n: prs.slides[n - 1]

def in_fallback(el):
    return any(a.tag == MC + 'Fallback' for a in el.iterancestors())

def ptext(p):
    return "".join(t.text or "" for t in p.iter(A + 't', M + 't') if not in_fallback(t))

def top_shapes(slide, name):
    """Devuelve (contenedor, [sp visibles]) del shape con ese nombre: sp simple o AlternateContent."""
    tree = slide._element.find('.//p:spTree', NS)
    for ch in tree:
        names = [e.get('name') for e in ch.iter(P + 'cNvPr')]
        if name in names:
            if ch.tag == MC + 'AlternateContent':
                return ch, ch.findall('.//p:sp', NS)
            return ch, [ch]
    raise KeyError(name)

def plain_par(p, segs):
    """Reescribe el párrafo con runs simples. segs: str o [(texto, 'n'|'i'|'s'|'si')]."""
    if isinstance(segs, str): segs = [(segs, 'n')]
    r0 = next((r for r in p.iter(A + 'r') if not in_fallback(r)), None)
    rpr = copy.deepcopy(r0.find(A + 'rPr')) if r0 is not None else etree.Element(A + 'rPr')
    for ch in list(p):
        if ch.tag not in (A + 'pPr', A + 'endParaRPr'): p.remove(ch)
    end = p.find(A + 'endParaRPr')
    for text, kind in segs:
        r = etree.Element(A + 'r'); rp = copy.deepcopy(rpr); r.append(rp)
        if 'i' in kind: rp.set('i', '1')
        else: rp.attrib.pop('i', None)
        if 's' in kind: rp.set('baseline', '-25000')
        else: rp.attrib.pop('baseline', None)
        etree.SubElement(r, A + 't').text = text
        (end.addprevious(r) if end is not None else p.append(r))

def unwrap(slide, name):
    """Si el shape está envuelto en AlternateContent, lo reemplaza por su copia Choice (texto real)."""
    cont, sps = top_shapes(slide, name)
    if cont.tag == MC + 'AlternateContent':
        sp = copy.deepcopy(sps[0]); cont.addprevious(sp); cont.getparent().remove(cont)
        return sp
    return cont

def set_title(n, start, segs):
    sp = unwrap(S(n), "Título")
    p = sp.find('.//a:p', NS)
    cur = ptext(p)
    assert cur.startswith(start), f"slide {n}: título «{cur[:60]}» no empieza con «{start}»"
    plain_par(p, segs)

def find_par(n, start):
    hits = [p for p in S(n)._element.iter(A + 'p') if not in_fallback(p) and ptext(p).strip().startswith(start)]
    assert hits, f"slide {n}: no hay párrafo que empiece con «{start}»"
    return hits

def set_par(n, start, segs):
    for p in find_par(n, start):
        sp = next(a for a in p.iterancestors() if a.tag == P + 'sp')
        name = next(sp.iter(P + 'cNvPr')).get('name')
        cont, _ = top_shapes(S(n), name)
        if cont.tag == MC + 'AlternateContent':
            sp = unwrap(S(n), name)
            p = next(q for q in sp.iter(A + 'p') if ptext(q).strip().startswith(start))
        plain_par(p, segs)

def del_par(n, start):
    for p in find_par(n, start):
        sp = next(a for a in p.iterancestors() if a.tag == P + 'sp')
        name = next(sp.iter(P + 'cNvPr')).get('name')
        cont, _ = top_shapes(S(n), name)
        if cont.tag == MC + 'AlternateContent':
            sp = unwrap(S(n), name)
            p = next(q for q in sp.iter(A + 'p') if ptext(q).strip().startswith(start))
        p.getparent().remove(p)

def replace(n, old, new):
    k = 0
    for t in S(n)._element.iter(A + 't'):
        if t.text and old in t.text: t.text = t.text.replace(old, new); k += 1
    assert k, f"slide {n}: no se encontró «{old}»"

def delete_shape(n, name):
    cont, _ = top_shapes(S(n), name); cont.getparent().remove(cont)

def xfrm(sp):
    return sp.find('.//a:xfrm', NS)

# ---------------- títulos: presentan; las viñetas profundizan ----------------
T = {
 4: ("Nos proponemos", "Se propone definir un método que mida el terreno y procese lo medido para obtener información útil"),
 6: ("SPT:", "SPT: ensayo de penetración estándar"),
 7: ("CPT/CPTu:", "CPT/CPTu: ensayo de penetración con cono"),
 8: ("Ventajas: resistencia", "Ventajas de los ensayos de penetración"),
 9: ("Limitaciones: puntuales", "Limitaciones de los ensayos de penetración"),
 10: ("Para medir la rigidez", "La otra familia de ensayos: la propagación de ondas"),
 11: ("Un golpe deforma", "Origen de las ondas en el terreno"),
 14: ("Onda P:", "Onda P: onda de compresión"),
 15: ("Onda S:", "Onda S: onda de corte"),
 17: ("En suelos, la relación", "En suelos, la relación esfuerzo-deformación depende del nivel de deformación"),
 18: ("Al crecer la deformación", "Fuera del tramo lineal: el modelo hiperbólico"),
 19: ("En pequeña señal", "De la velocidad de corte a la rigidez máxima"),
 20: ("Si conocemos", [("Conocida ", 'n'), ("V", 'i'), ("s", 'si'), (", se estima ", 'n'), ("G", 'i'), ("max", 's'),
                     (" con una incertidumbre razonable", 'n')]),
 21: ("Las ondas de cuerpo, al llegar", "Al llegar a una interfaz, la onda de cuerpo se divide"),
 23: ("Downhole:", "Ensayo downhole"),
 24: ("Crosshole:", "Ensayo crosshole"),
 25: ("Ventajas: miden", "Ventajas de downhole y crosshole"),
 26: ("Limitaciones: exigen", "Limitaciones de downhole y crosshole"),
 27: ("Refracción: a cierta", "Ensayo de refracción"),
 29: ("Refracción: simple", "Refracción: ventajas y limitaciones"),
 30: ("Reflexión: se registra", "Ensayo de reflexión"),
 31: ("Reflexión: alcanza", "Reflexión: ventajas y limitaciones"),
 32: ("La superficie libre es", "La superficie libre: una interfaz con su propia condición de frontera"),
 33: ("Respecto a la superficie libre", "Polarización de la onda S respecto de la superficie libre"),
 34: ("En la superficie libre, P y SV", "Conversión de modos en la superficie libre"),
 35: ("Las ondas Love solo existen", "Condición de existencia de las ondas Love"),
 36: ("Onda Love:", "Onda Love: origen y movimiento"),
 37: ("Onda Rayleigh:", "Onda Rayleigh: origen y movimiento"),
 38: ("Una fuente en superficie", "Reparto de la energía de una fuente vertical en superficie"),
 39: ("Las Rayleigh se atenúan", "Atenuación con la distancia: Rayleigh frente a ondas de cuerpo"),
 40: ("En un semiespacio homogéneo", "Velocidad de Rayleigh en un semiespacio homogéneo"),
 41: ("En un terreno estratificado", "Perfil de velocidad de corte de un terreno estratificado"),
 43: ("Como cada frecuencia", "Velocidad de fase y frecuencia en un terreno en capas"),
 45: ("La inversión tiene límites", "Límites de la inversión"),
 46: ("SASW: la diferencia", "Ensayo SASW"),
 47: ("SASW es simple", "SASW: ventajas y limitaciones"),
 49: ("El registro MASW es", "El registro MASW"),
 54: ("El SM-24 es un geófono", "El geófono SM-24"),
 55: ("La masa suspendida", "Modelo mecánico del geófono"),
 57: ("La pérdida cae", "Por qué importa la pérdida en baja frecuencia"),
 59: ("Invertir la respuesta", "Limitaciones de la compensación inversa"),
 60: ("La resistencia negativa", "Resistencia negativa y balance de fuerza"),
 61: ("La idea de Ma et al.", "El método de Ma et al."),
 62: ("Elegimos el método", "Se eligió el método de Ma et al. por tres razones"),
 63: ("El compensador sube", "Función de transferencia del compensador"),
 64: ("Implementación:", "Implementación del AFE"),
 65: ("La entrada es instrumental", "Etapa de entrada instrumental"),
 66: ("El pasabanda es un inversor", "Etapa pasabanda: cada quiebre se ajusta por separado"),
 67: ("Como el pasabanda ya invierte", "El pasabanda ya invierte la fase, y eso simplifica la etapa siguiente"),
 68: ("El antialias es", "Filtro antialias"),
 70: ("La ruta PGA–ADC", "Cómo se validó la cadena analógica"),
 71: ("El offset se acumula", "El problema del offset"),
 79: ("El ADC tiene cuatro", "Rangos de entrada del ADC"),
 80: ("Diezmamos", "Diezmado por media móvil"),
 83: ("Sin SD, el diezmado", "Duración del registro sin tarjeta SD"),
 84: ("Cada registro guarda", "Contenido de cada registro"),
 86: ("Elegimos ESP-NOW", "Se eligió ESP-NOW por costo y simplicidad, no por ser la opción más precisa"),
 90: ("El disparo va por broadcast", "Por qué el disparo va por broadcast"),
 91: ("El jitter se mide", "Medición del jitter del disparo"),
 92: ("Esta medición no incluye", "Alcance de la medición de jitter"),
 96: ("El nodo HAMMER registra", "El nodo HAMMER"),
 98: ("La interfaz web del maestro", "La interfaz web del maestro"),
 100: ("El arreglo: 21", "Geometría del arreglo"),
 102: ("Un receptor móvil", "Adquisición con un receptor móvil"),
 103: ("Una captura real", "Una captura real"),
 104: ("Cada posición se alinea", "Procesamiento de cada posición"),
 107: ("El servidor conserva", "Procesamiento en el servidor"),
 108: ("La SNR aparente compara", "Definición de la SNR aparente"),
 109: ("Por debajo de 10 Hz", "SNR aparente por banda de frecuencia"),
}
for n, (start, new) in T.items():
    set_title(n, start, new)

# ---------------- primera persona en el cuerpo ----------------
replace(41, "Si conocemos ", "Con ")
replace(41, ", estimamos el módulo de corte máximo:", " conocida, se estima el módulo de corte máximo:")
set_par(57, "Usamos el SM-24", "Con el SM-24, la respuesta en baja frecuencia se mejora con electrónica")
set_par(58, "Las comparamos", "Se comparan por complejidad, ruido y repetibilidad entre unidades.")
replace(63, "Buscamos que", "Se busca que")
set_par(78, "Nuestras señales", "Las señales de este trabajo son lentas: la velocidad no es el límite, la resolución sí.")
set_par(80, "Seguimos aprovechando", "Se sigue aprovechando el sobremuestreo del ΔΣ: el promedio reduce el ruido incorrelado")

# ---------------- un solo término: pequeña deformación ----------------
replace(19, "Solo en pequeña señal: el módulo de corte es ", "Solo en pequeña deformación: el módulo de corte es ")
set_par(19, "Relación buscada", "Relación buscada")

# ---------------- puntuales ----------------
set_par(22, "Vale para P y S", "Se aplica tanto a ondas P como S, cada una con su velocidad")
set_par(32, "El aire no transmite", "El aire no transmite esfuerzos, así que en la superficie el esfuerzo es cero")
set_par(36, "Sin componente vertical", "Sin componente vertical: la mayoría de los sensores, que miden en vertical, no la registran")
set_par(37, "Tiene componente vertical", "Tiene componente vertical: la registran los sensores verticales, que son la mayoría")
# 38: el supuesto va arriba, porque de él salen los porcentajes; la viñeta con los porcentajes repetía el gráfico
del_par(38, "Rayleigh 67")
replace(38, "Supone ", "Suponiendo ")
_, sup = top_shapes(S(38), "Supuestos"); _, cue = top_shapes(S(38), "Cuerpo")
y_sup = int(xfrm(cue[0]).find('a:off', NS).get('y'))
h_sup = int(xfrm(sup[0]).find('a:ext', NS).get('cy'))
for sp in sup: xfrm(sp).find('a:off', NS).set('y', str(y_sup))
for sp in cue: xfrm(sp).find('a:off', NS).set('y', str(y_sup + h_sup + 182880))
# 40: Vs ≈ cR/0,9 repetía cR ≈ 0,9·Vs; «dispersión» todavía no se presentó
delete_shape(40, "Fondo Vs cR"); delete_shape(40, "Ecuación E_vsc")
replace(40, "No hay dispersión: todas las frecuencias van a la misma ", "Todas las frecuencias viajan a la misma ")

prs.save(dst)
print("ok")
