"""Mapa de textos larga v29 -> larga v37 (párrafo viejo -> párrafo nuevo), para actualizar la comprimida.
Empareja slides por SlideID y shapes por nombre; dentro de cada shape alinea párrafos con difflib.
Salida: JSON con {"pairs": [[viejo, nuevo_segs]], "deleted": [viejo]} donde nuevo_segs = [[texto, tipo]]
(tipo: n normal, i cursiva, s subíndice, si ambos), para conservar subíndices y cursivas."""
import sys, json, difflib
import pptx
from lxml import etree
sys.path.insert(0, __file__.rsplit('\\', 2)[0] if '\\' in __file__ else '..')
from pptx_helpers_v30 import NS, P, A, M, MC, in_fallback, ptext

def shapes_paras(slide):
    out = {}
    tree = slide._element.find('.//p:spTree', NS)
    for el in tree.iter(P + 'sp', P + 'graphicFrame'):
        if in_fallback(el): continue
        nm = next(el.iter(P + 'cNvPr')).get('name')
        ps = [p for p in el.iter(A + 'p') if not in_fallback(p)]
        out.setdefault(nm, [])
        out[nm] += [p for p in ps if ptext(p).strip()]
    return out

def segs(p):
    res = []
    for r in p.iter(A + 'r'):
        if in_fallback(r): continue
        t = r.find(A + 't'); rp = r.find(A + 'rPr')
        if t is None or not t.text: continue
        k = ''
        if rp is not None and rp.get('i') == '1': k += 'i'
        if rp is not None and rp.get('baseline', '0').startswith('-'): k += 's'
        res.append([t.text, k or 'n'])
    # párrafo con fórmulas: si hay m:t fuera de runs, se usa el texto plano
    if any(True for _ in p.iter(M + 't')) and not res: res = [[ptext(p), 'n']]
    return res

old, new = pptx.Presentation(sys.argv[1]), pptx.Presentation(sys.argv[2])
by_id = {s.slide_id: s for s in new.slides}
pairs, deleted, xmls = {}, set(), {}
for so in old.slides:
    sn = by_id.get(so.slide_id)
    if sn is None: continue
    po, pn = shapes_paras(so), shapes_paras(sn)
    for nm, plo in po.items():
        pln = pn.get(nm)
        if pln is None:
            for p in plo: deleted.add(ptext(p).strip())
            continue
        to = [ptext(p).strip() for p in plo]; tn = [ptext(p).strip() for p in pln]
        sm = difflib.SequenceMatcher(a=to, b=tn, autojunk=False)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == 'replace':
                for k in range(max(i2 - i1, j2 - j1)):
                    a = to[i1 + k] if i1 + k < i2 else None
                    b = pln[j1 + k] if j1 + k < j2 else None
                    if a and b is not None: pairs[a] = segs(b) or [[ptext(b), 'n']]; xmls[a] = etree.tostring(b, encoding='unicode')
                    elif a: deleted.add(a)
            elif op == 'delete':
                for k in range(i1, i2): deleted.add(to[k])
json.dump({"pairs": [[k, v] for k, v in pairs.items()], "deleted": sorted(deleted - set(pairs)), "xml": xmls},
          open(sys.argv[3], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(pairs), "reemplazos;", len(deleted - set(pairs)), "borrados")
