import os,cv2,numpy as np,subprocess,time
OUT='/mnt/data/ondas_sismicas_remaster'
files={'P':'/mnt/data/A_006A_seismicP-Wave_braile.mp4','S':'/mnt/data/A_006B_seismicS-Wave_braile.mp4','Rayleigh':'/mnt/data/A_006C_RaleighWave_braile.mp4','Love':'/mnt/data/A_006D_LoveWave_braile.mp4'}
# Grey conversion LUT: transform grey background and face to neutral white, preserve dark contours
xp=np.array([0,40,90,120,145,165,185,201,210,216,228,242,255],float)
yp=np.array([0,28,57,77,99,133,173,217,245,249,252,254,255],float)
lut=np.interp(np.arange(256),xp,yp).astype(np.uint8)

def clean(src):
    # RGB almost neutral? neutralize MPEG quantization colored pixel noise
    f=cv2.bilateralFilter(src,3,18,2)
    f=cv2.LUT(f,lut)
    hh,ss,vv=cv2.split(cv2.cvtColor(src,cv2.COLOR_BGR2HSV))
    # On saturated lettering, restore stronger, solid colored inks
    satmask=(ss.astype(np.float32)/100.0).clip(0,1)
    satmask=satmask[:,:,None]
    cleanhsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
    ch,cs,cv=cv2.split(cleanhsv)
    ss2=(cs.astype(np.float32) + 25*satmask[:,:,0]).clip(0,255).astype('uint8')
    cv=np.maximum(cv,(cv.astype(np.float32)*satmask[:,:,0]).astype(np.uint8))
    col=cv2.cvtColor(cv2.merge([hh,ss2,cv]),cv2.COLOR_HSV2BGR)
    f=np.clip(f.astype(np.float32)*(1-satmask*.7)+col.astype(np.float32)*satmask*.7,0,255).astype('uint8')
    high=cv2.resize(f,(1280,960),interpolation=cv2.INTER_LANCZOS4)
    blur=cv2.GaussianBlur(high,(0,0),1.1)
    sharp=cv2.addWeighted(high,1.26,blur,-.26,0)
    return sharp

def run(k,p):
    c=cv2.VideoCapture(p)
    fps=c.get(cv2.CAP_PROP_FPS); dur=c.get(cv2.CAP_PROP_FRAME_COUNT)/fps
    target=os.path.join(OUT,f'{k}_ORIGINAL_RESTAURADO_1280x960.mp4')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24','-video_size','1280x960','-framerate',f'{fps:.5f}','-i','-', '-an','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',target]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    count=0
    while True:
      ok,f=c.read()
      if not ok:break
      enhanced=clean(f)
      if count==round(fps*2.8):cv2.imwrite(os.path.join(OUT,f'preview_original_restaurado_{k}.png'), enhanced)
      proc.stdin.write(enhanced.tobytes())
      count+=1
    proc.stdin.close();proc.wait(); c.release()
    print(k, 'original restored',count,'frames, dur',round(dur,2), 'out',target,flush=True)

if __name__=='__main__':
 import sys
 keys=list(files) if len(sys.argv)==1 else sys.argv[1:]
 for k in keys:run(k,files[k])
