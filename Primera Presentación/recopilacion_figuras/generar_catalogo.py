"""Genera el catálogo de selección; no modifica la tesis ni las imágenes fuente."""
from pathlib import Path
import json, html, base64, io
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor

HERE=Path(__file__).resolve().parent
ITEMS=json.loads((HERE/'inventario.json').read_text(encoding='utf-8'))
ITEMS.sort(key=lambda x:(min(x['sections']),x['id']))
SECTIONS={
1:'Importancia de la caracterización',2:'Métodos tradicionales',
3:'Fundamentos sísmicos',4:'Uso de ondas superficiales',5:'Selección del método',
6:'Requerimientos',7:'Diseño electrónico',8:'Validación experimental',
9:'Resultados',10:'Trabajos futuros'}
pdfmetrics.registerFont(TTFont('Arial','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold','C:/Windows/Fonts/arialbd.ttf'))
W,H=landscape(A4)
ACCENT=HexColor('#104b55')
styles={
 'text':ParagraphStyle('text',fontName='Arial',fontSize=10,leading=14,textColor=HexColor('#263844')),
 'small':ParagraphStyle('small',fontName='Arial',fontSize=8,leading=11,textColor=HexColor('#4b5960')),
 'tiny':ParagraphStyle('tiny',fontName='Arial',fontSize=7,leading=9,textColor=HexColor('#4b5960')),
}
def para(c,text,x,top,width,style='text'):
    p=Paragraph(text,styles[style]); _,h=p.wrap(width,H)
    p.drawOn(c,x,top-h)
    return top-h

def image_bytes(item,maxsize=2200):
    with Image.open(item['preview']) as source:
        source.thumbnail((maxsize,maxsize))
        im=Image.new('RGB',source.size,'white')
        if source.mode=='RGBA':im.paste(source,mask=source.getchannel('A'))
        else:im.paste(source.convert('RGB'))
        buf=io.BytesIO(); im.save(buf,format='PNG')
        return buf.getvalue(),im.size

c=canvas.Canvas(str(HERE/'Catalogo_figuras.pdf'),pagesize=(W,H))
c.setTitle('Figuras candidatas por sección - Primera Presentación')
c.setAuthor('Recopilación para revisión de Elías Álvarez')
c.setFillColor(ACCENT);c.setFont('ArialBold',24)
c.drawString(36,H-45,'Figuras candidatas por sección')
top=para(c,'37 candidatos: 14 páginas del Draw.io y 23 imágenes o páginas bibliográficas. Ninguna figura se insertó en la tesis. Los identificadores permiten elegir por mensaje, por ejemplo: D04, D09, F12 y F16.',36,H-65,W-72)
top-=15
for n,title in SECTIONS.items():
    ids=', '.join(i['id'] for i in ITEMS if n in i['sections'])
    top=para(c,f'<b>{n}. {html.escape(title)}</b> — {ids}',36,top,W-72)-9
top-=7
top=para(c,'<b>Estados:</b> Prioritario = aporta al relato actual; Alternativa/Apoyo = opcional; Revisar/Rehacer/No usar tal cual = necesita cambios antes de insertarse; Bibliografía = material ajeno con cita. Las observaciones indican comprobaciones concretas, no una aprobación automática.',36,top,W-72)-10
para(c,'Los originales permanecen intactos. El archivo HTML permite filtrar por sección, ampliar y marcar candidatos. El PDF exportado del Draw.io conserva las 14 páginas completas.',36,top,W-72,'small')
c.showPage()
for k,item in enumerate(ITEMS,2):
    id=item['id']
    c.bookmarkPage(id); c.addOutlineEntry(id+' · '+item['title'],id,0,False)
    c.setFillColor(ACCENT);c.setFont('ArialBold',18)
    c.drawString(36,H-34,id+' · '+item['title'])
    sections=', '.join(str(n) for n in item['sections'])
    c.setFont('Arial',10);c.setFillColor(HexColor('#4b5960'))
    c.drawString(36,H-55,'Secciones '+sections+'  |  '+item['status'])
    data,(iw,ih)=image_bytes(item)
    (HERE/'vistas'/f'{id}-catalogo.png').write_bytes(data)
    bottom=139; available_h=H-218; available_w=W-72
    scale=min(available_w/iw,available_h/ih)
    dw,dh=iw*scale,ih*scale
    c.drawImage(ImageReader(io.BytesIO(data)),(W-dw)/2,bottom+(available_h-dh)/2,width=dw,height=dh,mask='auto')
    top=para(c,html.escape(item['note']),36,121,W-72,'text')-8
    source=item['path'].replace('\\','/')
    if item.get('page'):source+=' — página '+str(item['page'])
    top=para(c,'<b>Original:</b> '+html.escape(source),36,top,W-72,'tiny')-4
    if item.get('source'):para(c,'<b>Fuente:</b> '+html.escape(item['source']),36,top,W-72,'tiny')
    c.setFont('Arial',8);c.setFillColor(HexColor('#4b5960'))
    c.drawString(36,20,'Sólo selección: no insertado en el documento')
    c.drawRightString(W-36,20,str(k))
    c.showPage()
c.save()

cards=[]
for item in ITEMS:
    id=item['id']
    data=(HERE/'vistas'/f'{id}-catalogo.png').read_bytes()
    src='data:image/png;base64,'+base64.b64encode(data).decode()
    source=Path(item['path']).as_uri()
    label=' · '.join('§'+str(s) for s in item['sections'])
    cards.append(f'''<article id="{id}" data-sections="{' '.join(map(str,item['sections']))}">
<header><label><input type="checkbox" value="{id}"> <strong>{id}</strong></label><span>{html.escape(item['status'])}</span></header>
<h2>{html.escape(item['title'])}</h2><p class="section">{label}</p>
<button class="preview" aria-label="Ampliar {id}"><img src="{src}" alt="{html.escape(item['title'])}" loading="lazy"></button>
<p>{html.escape(item['note'])}</p><a href="{html.escape(source)}" target="_blank">Abrir original{(' · página '+str(item['page'])) if item.get('page') else ''}</a>
<details><summary>Ruta y procedencia</summary><p class="path">{html.escape(item['path'])}</p>{html.escape(item.get('source') or '')}</details></article>''')
options=''.join(f'<option value="{n}">{n}. {html.escape(title)}</option>' for n,title in SECTIONS.items())
html_doc='''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Figuras candidatas · Primera Presentación</title>
<style>
:root{font-family:Arial,sans-serif;color:#22363d;background:#f2f5f5}body{margin:0}main{max-width:1350px;margin:auto;padding:24px}
h1{font-size:32px;margin-bottom:8px}h2{font-size:19px;line-height:1.3}.intro{max-width:950px;line-height:1.5}
.toolbar{position:sticky;top:0;background:#104b55;color:white;padding:14px 24px;display:flex;gap:12px;align-items:center;flex-wrap:wrap;z-index:2}
select,button,textarea{font:inherit}select,button{padding:8px 12px;border-radius:6px;border:1px solid #bdcbcd;cursor:pointer}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(350px,1fr));gap:20px}article{background:white;border:1px solid #d5dfe0;border-radius:10px;padding:18px;box-shadow:0 3px 12px #00000007}
article header{display:flex;justify-content:space-between;align-items:center}article header span{font-size:12px;background:#e9f0f1;padding:5px 8px;border-radius:4px}
input[type=checkbox]{width:18px;height:18px;vertical-align:middle}p{font-size:14px;line-height:1.45}.section{color:#607079}.preview{width:100%;height:260px;background:#fbfbfb;padding:6px;border:1px solid #e4eaea;cursor:zoom-in}.preview img{width:100%;height:100%;object-fit:contain}
a{color:#126578}details{margin-top:12px;font-size:12px}.path{overflow-wrap:anywhere;font-size:12px}
textarea{box-sizing:border-box;width:100%;min-height:70px;margin:16px 0;padding:12px;border:1px solid #bdcbcd;border-radius:8px}
dialog{border:0;border-radius:8px;max-width:95vw;max-height:94vh;padding:10px}dialog::backdrop{background:#000b}dialog img{display:block;max-width:91vw;max-height:80vh;object-fit:contain}
dialog button{float:right;margin-bottom:5px}[hidden]{display:none!important}
@media(max-width:500px){main{padding:12px}.grid{grid-template-columns:1fr}.toolbar{padding:10px}h1{font-size:25px}}
</style>
<div class="toolbar"><strong>Recopilación · 37 candidatos</strong><select id="filter" aria-label="Filtrar por sección"><option value="">Todas las secciones</option>OPTIONS</select><button id="chosen">Sólo elegidas</button><button id="download">Descargar selección</button><span id="count">0 elegidas</span></div>
<main><h1>Elegí las figuras que querés incorporar</h1><p class="intro">No se insertó ninguna en la tesis. Marcá los identificadores que te interesan; las notas indican qué necesita ajuste antes de usarse. Los diagramas se exportaron del Draw.io sin modificar el original. Las figuras bibliográficas están identificadas como tales.</p>
<textarea id="selection" readonly aria-label="Selección para enviar por mensaje" placeholder="Los identificadores elegidos aparecerán acá."></textarea>
<div class="grid">CARDS</div></main><dialog id="zoom"><button id="close">Cerrar</button><img alt=""></dialog>
<script>
const checks=[...document.querySelectorAll('input[type=checkbox]')],filter=document.querySelector('#filter');let onlyChosen=false;
try{const saved=JSON.parse(localStorage.getItem('tesis_figuras_20260830')||'[]');checks.forEach(c=>c.checked=saved.includes(c.value));}catch(e){}
function refresh(){const ids=checks.filter(c=>c.checked).map(c=>c.value);document.querySelector('#selection').value=ids.length?'Figuras elegidas: '+ids.join(', '):'';document.querySelector('#count').textContent=ids.length+' elegidas';try{localStorage.setItem('tesis_figuras_20260830',JSON.stringify(ids));}catch(e){}document.querySelectorAll('article').forEach(a=>{a.hidden=(filter.value&&!a.dataset.sections.split(' ').includes(filter.value))||(onlyChosen&&!a.querySelector('input').checked);});}
checks.forEach(c=>c.addEventListener('change',refresh));filter.addEventListener('change',refresh);
document.querySelector('#chosen').onclick=function(){onlyChosen=!onlyChosen;this.textContent=onlyChosen?'Ver todas':'Sólo elegidas';refresh();};
document.querySelector('#download').onclick=()=>{const blob=new Blob([document.querySelector('#selection').value+'\\n'],{type:'text/plain;charset=utf-8'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='seleccion_figuras.txt';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);};
const dialog=document.querySelector('#zoom');document.querySelectorAll('.preview').forEach(b=>b.onclick=()=>{const im=dialog.querySelector('img');im.src=b.querySelector('img').src;im.alt=b.querySelector('img').alt;dialog.showModal();});
document.querySelector('#close').onclick=()=>dialog.close();dialog.onclick=e=>{if(e.target===dialog)dialog.close();};refresh();
</script></html>'''
(HERE/'catalogo_figuras.html').write_text(html_doc.replace('OPTIONS',options).replace('CARDS',''.join(cards)),encoding='utf-8')

md=['# Figuras candidatas por sección','','Ninguna figura se ha insertado en la tesis. Se preservan las fuentes y el Draw.io original.','','[Catálogo visual PDF](<'+str(HERE/'Catalogo_figuras.pdf').replace('\\','/')+'>) · [Galería con selección](<'+str(HERE/'catalogo_figuras.html').replace('\\','/')+'>)','','## Mapa por sección','','| Sección | Candidatos |','|---|---|']
for n,title in SECTIONS.items():md.append('| '+str(n)+'. '+title+' | '+', '.join(i['id'] for i in ITEMS if n in i['sections'])+' |')
md+=['','## Candidatos','','El estado «Prioritario» indica interés editorial, no aprobación de inserción. «Rehacer» y «No usar tal cual» señalan incompatibilidades concretas.']
for i in ITEMS:
    src=i['path'].replace('\\','/')
    md+=['','### '+i['id']+' · '+i['title'],'','Secciones: '+', '.join(map(str,i['sections']))+'. Estado: '+i['status']+'.','',i['note'],'','[Abrir fuente](<'+src+'>)'+(' — página '+str(i['page']) if i.get('page') else '')]
    if i.get('source'):md+=['','[Procedencia bibliográfica]('+i['source']+')']
md+=['','## Criterios de conservación','','- Los esquemáticos se presentan completos, sin recortar componentes.','- Se exportaron las catorce páginas del Draw.io, sin alterar su contenido.','- No se utiliza la exportación histórica de nueve capas y 82,6 m como resultado actual.','- No se deduce energía entre bandas a partir de imágenes de dispersión normalizadas.','- La fuente periódica de período variable se presenta como idea a ensayar.','- Las figuras de libros y artículos requieren cita y revisión de las condiciones de reproducción.']
(HERE/'RECOPILACION_FIGURAS.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print('Generated PDF, HTML and Markdown:',len(ITEMS),'candidates')
