import os, math, sys, subprocess, time, argparse
import cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont
W,H=1920,1080
OUT='/mnt/data/ondas_sismicas_remaster'
os.makedirs(OUT,exist_ok=True)
FONTS={'bold':'/usr/share/fonts/truetype/lato/Lato-Heavy.ttf', 'normal':'/usr/share/fonts/truetype/lato/Lato-Regular.ttf','semibold':'/usr/share/fonts/truetype/lato/Lato-Semibold.ttf'}
CFG={
 'P': dict(name='ONDA P',subtitle='Compresión y dilatación',type='ONDA DE CUERPO',desc='Movimiento paralelo a la propagación',rgb=(20,164,196),detail='Longitudinal'),
 'S': dict(name='ONDA S',subtitle='Deformación transversal',type='ONDA DE CUERPO',desc='Movimiento perpendicular a la propagación',rgb=(24,171,104),detail='Transversal vertical'),
 'Rayleigh': dict(name='ONDA RAYLEIGH',subtitle='Movimiento elíptico',type='ONDA SUPERFICIAL',desc='Desplazamiento vertical y longitudinal',rgb=(58,90,204),detail='Elíptico en el plano vertical'),
 'Love': dict(name='ONDA LOVE',subtitle='Cizallamiento horizontal',type='ONDA SUPERFICIAL',desc='Movimiento horizontal transversal',rgb=(173,76,194),detail='Transversal horizontal')}

# Color helpers
bgr=lambda c:tuple(map(int,c[::-1]))
def roundrect(draw,xy,r,fill,outline=None,width=1):
 draw.rounded_rectangle(xy,r,fill=fill,outline=outline,width=width)
def base_design(kind):
 c=CFG[kind]; acc=c['rgb']; img=Image.new('RGB',(W,H),(247,250,253)); d=ImageDraw.Draw(img)
 d.rectangle([0,0,W,11],fill=acc)
 d.rounded_rectangle([92,52,1320,278],radius=26,fill=(255,255,255),outline=(231,236,245),width=2)
 def font(n,style='normal'): return ImageFont.truetype(FONTS[style],n)
 d.text((138,73),c['type'],font=font(27,'bold'),fill=acc)
 d.text((136,114),c['name'],font=font(82,'bold'),fill=(26,40,64),stroke_width=0)
 d.text((140,218),c['subtitle'],font=font(32),fill=(94,111,131))
 # top info aligned right
 d.rounded_rectangle([1400,80,1807,215],radius=24,fill=(239,244,249))
 d.text((1434,103),'PROPAGACIÓN',font=font(24,'bold'),fill=(93,107,122))
 d.line([1435,170,1762,170],fill=acc,width=10)
 d.polygon([(1767,170),(1725,145),(1725,195)],fill=acc)
 # bottom card left
 d.rounded_rectangle([94,797,1826,994],radius=29,fill=(255,255,255),outline=(228,235,242),width=2)
 d.rounded_rectangle([122,825,138,970],radius=7,fill=acc)
 d.text((176,828),'MOVIMIENTO DE PARTÍCULAS',font=font(28,'bold'),fill=(89,107,124))
 d.text((176,880),c['desc'],font=font(38,'semibold'),fill=(24,42,60))
 d.text((178,942),c['detail'],font=font(24),fill=acc)
 d.text((100,1030),'Esquema ilustrativo · deformaciones ampliadas para facilitar su visualización',font=font(24),fill=(116,131,148))
 # legend particle glyph (right)
 ix,iy=1582,897
 if kind=='P':
  d.line([ix-98,iy,ix+97,iy],fill=acc,width=12)
  d.polygon([(ix-110,iy),(ix-73,iy-21),(ix-73,iy+21)],fill=acc)
  d.polygon([(ix+110,iy),(ix+73,iy-21),(ix+73,iy+21)],fill=acc)
 if kind=='S':
  d.line([ix,iy-63,ix,iy+64],fill=acc,width=12)
  d.polygon([(ix,iy-87),(ix-24,iy-47),(ix+24,iy-47)],fill=acc)
  d.polygon([(ix,iy+87),(ix-24,iy+47),(ix+24,iy+47)],fill=acc)
 if kind=='Rayleigh':
  d.ellipse([ix-92,iy-57,ix+92,iy+57],outline=acc,width=10)
  d.polygon([(ix-94,iy-15),(ix-61,iy-20),(ix-74,iy+12)],fill=acc)
 if kind=='Love':
  d.line([ix-83,iy+50,ix+81,iy-50],fill=acc,width=12)
  d.polygon([(ix+104,iy-64),(ix+49,iy-56),(ix+76,iy-23)],fill=acc)
  d.polygon([(ix-105,iy+64),(ix-52,iy+54),(ix-77,iy+22)],fill=acc)
 return cv2.cvtColor(np.array(img),cv2.COLOR_RGB2BGR)

PX0,PY0=205.0,637.0
SX,SY,SZ=94.,58.,93.
L,D,Z=12.0,2.45,2.12

def deform(kind,x,y,z,t):
 x=np.asarray(x,dtype=np.float64); y=np.asarray(y,dtype=np.float64); z=np.asarray(z,dtype=np.float64)
 # travelling wave packet, 0.3--8.6 s passage with 1.55 wavelengths inside
 center=-1.9 + (L+3.8)*(t/8.8)
 u=x-center
 env=np.exp(-0.5*(u/1.60)**2)
 phi=(2*np.pi/2.85)*u
 if kind=='P':
  dx=0.48*env*np.sin(phi); dy=0; dz=0
 elif kind=='S':
  dx=0;dy=0;dz=0.59*env*np.sin(phi)
 elif kind=='Rayleigh':
  dep=np.exp(-1.85*(Z-z))
  dx=0.37*dep*env*np.cos(phi); dy=0;dz=0.49*dep*env*np.sin(phi)
 else:  # Love, horizontal transverse motion and surface attenuation
  dep=np.exp(-1.8*(Z-z));dx=0;dy=0.78*dep*env*np.sin(phi);dz=0
 return x+dx, y+dy, z+dz

def project(kind,x,y,z,t):
 a,b,c=deform(kind,x,y,z,t)
 px=PX0+SX*a+SY*b
 py=PY0+15.0*a-44.0*b-SZ*c
 return np.column_stack([px,py]).round().astype(np.int32)

def path(kind,xyz,t):
 ar=np.array(xyz, dtype=np.float64).reshape((-1,3))
 return project(kind,ar[:,0],ar[:,1],ar[:,2],t)

def polygon(img,pts,color): cv2.fillPoly(img,[pts.reshape(-1,1,2)],bgr(color),lineType=cv2.LINE_AA)
def line(img,pts,color,w=2): cv2.polylines(img,[pts.reshape(-1,1,2)],False,bgr(color),w,cv2.LINE_AA)

def frame(kind,t,background):
 img=background.copy(); a=CFG[kind]['rgb']
 # Soft soft shadow under block
 cv2.ellipse(img,(995,758),(665,20),0,0,360,(235,229,222),-1,cv2.LINE_AA)
 # Back right side x=L, y in [0,D]
 coords=[(L,0,0),(L,D,0),(L,D,Z),(L,0,Z)]
 polygon(img,path(kind,coords,t),(222,232,240))
 # front face, x=0->L, z=0->Z; visible shaded face
 xs=np.linspace(0,L,180)
 frontpoly=[(x,0,Z) for x in xs]+[(x,0,0) for x in xs[::-1]]
 polygon(img,path(kind,frontpoly,t),(240,246,250))
 # top face, y depth 0->D
 toppoly=[(x,0,Z) for x in xs]+[(x,D,Z) for x in xs[::-1]]
 polygon(img,path(kind,toppoly,t),(228,238,245))
 # top grid depth channels and x sections
 gridtop=(151,171,188); gridfront=(138,155,170); big=(92,111,131)
 for yy in np.linspace(0,D,9):
  xyz=[(x,yy,Z) for x in xs]
  line(img,path(kind,xyz,t),gridtop,2)
 for xx in np.linspace(0,L,65):
  zz=[(xx,y,Z) for y in np.linspace(0,D,17)]
  line(img,path(kind,zz,t),gridtop,1)
 # mesh front along vertical grid planes x
 for xx in np.linspace(0,L,65):
  line(img,path(kind,[(xx,0,z) for z in np.linspace(0,Z,12)],t),gridfront,1)
 # front horizontal lines
 for z in np.linspace(0,Z,10):
  line(img,path(kind,[(x,0,z) for x in xs],t),gridfront,2 if z in (0,Z) else 1)
 # right end cross grid
 for y in np.linspace(0,D,9):
  line(img,path(kind,[(L,y,z) for z in np.linspace(0,Z,12)],t),gridtop,1)
 for z in np.linspace(0,Z,10):
  line(img,path(kind,[(L,y,z) for y in np.linspace(0,D,20)],t),gridtop,1)
 # outlines near/front/top contours
 outline=(76,100,123)
 for xyz in [[(x,0,Z) for x in xs],[(x,0,0) for x in xs],[(0,0,z) for z in np.linspace(0,Z,12)], [(L,0,z) for z in np.linspace(0,Z,12)],[(0,y,Z) for y in np.linspace(0,D,17)],[(L,y,Z) for y in np.linspace(0,D,17)],[(L,y,0) for y in np.linspace(0,D,17)]]:
  line(img,path(kind,xyz,t),outline,3)
 # highlight some cross-sections in passing packet (moving tint on wave envelope)
 center=-1.9 +(L+3.8)*(t/8.8)
 for x in np.linspace(max(0,center-1.8),min(L,center+1.8),13) if .0<center+1.8 and center-1.8<L else []:
  alpha=math.exp(-0.5*((x-center)/1.25)**2)
  if alpha <.4: continue
  tinted=tuple(int(gridtop[i]*(1-alpha*.56)+a[i]*alpha*.56) for i in range(3))
  line(img,path(kind,[(x,y,Z) for y in np.linspace(0,D,17)],t),tinted,2)
 # tracking marker one at surface front face (square black)
 if kind=='P': xx,zz=6.5,1.04
 elif kind=='S':xx,zz=6.5,1.04
 elif kind=='Rayleigh':xx,zz=6.5,1.85
 else:xx,zz=6.5,1.89
 center_point=path(kind,[(xx,0,zz)],t)[0]; u,v=center_point
 cv2.rectangle(img,(u-8,v-8),(u+8,v+8),(15,25,40),-1,cv2.LINE_AA)
 # transverse direction reference
 ox,oy=1620,698
 cv2.arrowedLine(img,(ox,oy),(ox+133,oy+20),bgr((235,94,70)),4,cv2.LINE_AA,tipLength=.16)
 cv2.arrowedLine(img,(ox,oy),(ox+63,oy-61),bgr((235,94,70)),4,cv2.LINE_AA,tipLength=.20)
 cv2.arrowedLine(img,(ox,oy),(ox,oy-113),bgr((235,94,70)),4,cv2.LINE_AA,tipLength=.15)
 cv2.putText(img,'x',(ox+141,oy+29),cv2.FONT_HERSHEY_SIMPLEX,0.95,bgr((235,94,70)),2,cv2.LINE_AA)
 cv2.putText(img,'y',(ox+69,oy-68),cv2.FONT_HERSHEY_SIMPLEX,0.95,bgr((235,94,70)),2,cv2.LINE_AA)
 cv2.putText(img,'z',(ox-34,oy-118),cv2.FONT_HERSHEY_SIMPLEX,0.95,bgr((235,94,70)),2,cv2.LINE_AA)
 return img

def encode(kind,fps=24,dur=8.8,preview=False):
 bg=base_design(kind)
 if preview:
  im=frame(kind,3.4,bg)
  pathh=os.path.join(OUT,'vista_previa_'+kind+'.png')
  cv2.imwrite(pathh,im)
  return pathh
 out=os.path.join(OUT,kind+'_REDIBUJADO_FHD.mp4')
 ff=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-vcodec','rawvideo','-s',f'{W}x{H}', '-pix_fmt','bgr24','-r',str(fps),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',out]
 proc=subprocess.Popen(ff,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
 start=time.time()
 try:
  for fi in range(round(fps*dur)):
   b=frame(kind,fi/fps,bg)
   proc.stdin.write(b.tobytes())
 except BrokenPipeError:
  print(proc.stderr.read().decode(),file=sys.stderr); raise
 finally:
  try:proc.stdin.close()
  except:pass
 code=proc.wait()
 print(kind,'DONE',code,round(time.time()-start,1),'sec',out,flush=True)
 if code:raise Exception('ffmpeg encoder error')
 return out

if __name__=='__main__':
 p=argparse.ArgumentParser(); p.add_argument('--preview',action='store_true');p.add_argument('--kind',default='all');p.add_argument('--fps',type=int,default=24);args=p.parse_args()
 if args.kind=='all': ks=list(CFG)
 else:ks=[args.kind]
 for k in ks:print(encode(k,preview=args.preview,fps=args.fps),flush=True)
