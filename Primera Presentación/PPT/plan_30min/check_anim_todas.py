#!/usr/bin/env python3
"""check_anim.py deck.pptx : comprobaciones semánticas del timing que validate.py (XSD) no hace."""
import zipfile, re, sys
z = zipfile.ZipFile(sys.argv[1]); problems = 0; nslides = 0
import re as _re
_ns = sorted({int(m.group(1)) for m in (_re.match(r'ppt/slides/slide(\d+)\.xml$', q) for q in z.namelist()) if m})
for n in _ns:
    x = z.read(f'ppt/slides/slide{n}.xml').decode()
    if '<p:timing>' not in x: continue
    nslides += 1
    body = x[:x.find('<p:timing>')]; t = x[x.find('<p:timing>'):]
    # ids únicos (Choice/Fallback comparten id): quitar fallback antes de contar
    b2 = re.sub(r'<mc:Fallback[^>]*>.*?</mc:Fallback>', '', body, flags=re.S)
    ids = re.findall(r'<p:cNvPr id="(\d+)"', b2)
    errs = []
    d = {i for i in ids if ids.count(i) > 1}
    if d: errs.append(('ids duplicados', sorted(d)[:5]))
    cnt = {}
    for m in re.finditer(r'<p:sp>.*?</p:sp>', b2, re.S):
        s = m.group(0); i = re.search(r'<p:cNvPr id="(\d+)"', s).group(1)
        tb = re.search(r'<p:txBody>.*?</p:txBody>', s, re.S); cnt[i] = len(re.findall(r'<a:p>|<a:p ', tb.group(0))) if tb else 0
    sp = set(re.findall(r'spid="(\d+)"', t)); miss = sp - set(ids)
    if miss: errs.append(('spid inexistente', sorted(miss)[:5]))
    oor = [m.groups() for m in re.finditer(r'spid="(\d+)"><p:txEl><p:pRg st="(\d+)" end="(\d+)"', t) if int(m.group(3)) >= cnt.get(m.group(1), 0)]
    if oor: errs.append(('párrafo fuera de rango', oor[:3]))
    bl = set(re.findall(r'<p:bldP spid="(\d+)"', t)); pt = set(re.findall(r'spid="(\d+)"><p:txEl', t))
    whole = set(re.findall(r'<p:spTgt spid="(\d+)"/>', t))
    if bl ^ pt: errs.append(('bldP vs párrafos', sorted(bl ^ pt)[:5]))
    if pt & whole: errs.append(('efectos mixtos', sorted(pt & whole)[:5]))
    ctn = re.findall(r'<p:cTn id="(\d+)"', t)
    if len(ctn) != len(set(ctn)): errs.append(('cTn duplicados', ''))
    if re.search(r'nan|inf', t): errs.append(('nan/inf', ''))
    if errs: problems += 1; print('slide', n, errs)
print('slides con timing:', nslides, '| con problemas:', problems)
sys.exit(1 if problems else 0)
