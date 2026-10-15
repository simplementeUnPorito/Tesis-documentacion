"""Helpers para editar slides con fórmulas (shapes envueltos en mc:AlternateContent).
Regla: el contenido visible está en mc:Choice; la Fallback que guarda PowerPoint es una imagen del texto."""
import copy
from lxml import etree

NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
      'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math'}
P = '{%s}' % NS['p']; A = '{%s}' % NS['a']; M = '{%s}' % NS['m']; MC = '{%s}' % NS['mc']


def in_fallback(el):
    return any(a.tag == MC + 'Fallback' for a in el.iterancestors())


def ptext(p):
    return "".join(t.text or "" for t in p.iter(A + 't', M + 't') if not in_fallback(t))


def top_shapes(slide, name):
    tree = slide._element.find('.//p:spTree', NS)
    for ch in tree:
        if name in [e.get('name') for e in ch.iter(P + 'cNvPr')]:
            if ch.tag == MC + 'AlternateContent':
                return ch, ch.findall('.//p:sp', NS)
            return ch, [ch]
    raise KeyError(name)


def unwrap(slide, name):
    cont, sps = top_shapes(slide, name)
    if cont.tag == MC + 'AlternateContent':
        sp = copy.deepcopy(sps[0]); cont.addprevious(sp); cont.getparent().remove(cont)
        return sp
    return cont


def plain_par(p, segs):
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


def body_par(slide, name, start):
    sp = unwrap(slide, name)
    hits = [p for p in sp.iter(A + 'p') if ptext(p).strip().startswith(start)]
    assert hits, f"«{name}»: no hay párrafo que empiece con «{start}»"
    return sp, hits[0]


def set_title(slide, segs):
    sp = unwrap(slide, "Título"); plain_par(sp.find('.//a:p', NS), segs)


def set_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text
