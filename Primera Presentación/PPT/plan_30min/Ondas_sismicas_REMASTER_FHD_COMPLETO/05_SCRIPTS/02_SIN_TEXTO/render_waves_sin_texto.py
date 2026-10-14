import os, math, sys, subprocess, time, argparse
import cv2, numpy as np
from pathlib import Path

W, H = 1920, 1080
OUT = Path(__file__).resolve().parents[2] / '07_REDIBUJADOS_SIN_TEXTO'
CFG = {
    'P': dict(rgb=(20, 164, 196)),
    'S': dict(rgb=(24, 171, 104)),
    'Rayleigh': dict(rgb=(58, 90, 204)),
    'Love': dict(rgb=(173, 76, 194)),
}

bgr = lambda c: tuple(map(int, c[::-1]))

def base_design(kind):
    return np.full((H, W, 3), (253, 253, 253), dtype=np.uint8)

PX0, PY0 = 205.0, 637.0
SX, SY, SZ = 94., 58., 93.
L, D, Z = 12.0, 2.45, 2.12

def deform(kind, x, y, z, t):
    x = np.asarray(x, dtype=np.float64); y = np.asarray(y, dtype=np.float64); z = np.asarray(z, dtype=np.float64)
    center = -1.9 + (L + 3.8) * (t / 8.8)
    u = x - center
    env = np.exp(-0.5 * (u / 1.60) ** 2)
    phi = (2 * np.pi / 2.85) * u
    if kind == 'P': dx, dy, dz = 0.48 * env * np.sin(phi), 0, 0
    elif kind == 'S': dx, dy, dz = 0, 0, 0.59 * env * np.sin(phi)
    elif kind == 'Rayleigh':
        dep = np.exp(-1.85 * (Z - z)); dx, dy, dz = 0.37 * dep * env * np.cos(phi), 0, 0.49 * dep * env * np.sin(phi)
    else:
        dep = np.exp(-1.8 * (Z - z)); dx, dy, dz = 0, 0.78 * dep * env * np.sin(phi), 0
    return x + dx, y + dy, z + dz

def project(kind, x, y, z, t):
    a, b, c = deform(kind, x, y, z, t)
    return np.column_stack([PX0 + SX * a + SY * b, PY0 + 15.0 * a - 44.0 * b - SZ * c]).round().astype(np.int32)

def path(kind, xyz, t):
    ar = np.array(xyz, dtype=np.float64).reshape((-1, 3))
    return project(kind, ar[:, 0], ar[:, 1], ar[:, 2], t)

def polygon(img, pts, color): cv2.fillPoly(img, [pts.reshape(-1, 1, 2)], bgr(color), lineType=cv2.LINE_AA)
def line(img, pts, color, w=2): cv2.polylines(img, [pts.reshape(-1, 1, 2)], False, bgr(color), w, cv2.LINE_AA)

def frame(kind, t, background):
    img = background.copy(); a = CFG[kind]['rgb']
    cv2.ellipse(img, (995, 758), (665, 20), 0, 0, 360, (235, 229, 222), -1, cv2.LINE_AA)
    coords = [(L, 0, 0), (L, D, 0), (L, D, Z), (L, 0, Z)]
    polygon(img, path(kind, coords, t), (222, 232, 240))
    xs = np.linspace(0, L, 180)
    polygon(img, path(kind, [(x, 0, Z) for x in xs] + [(x, 0, 0) for x in xs[::-1]], t), (240, 246, 250))
    polygon(img, path(kind, [(x, 0, Z) for x in xs] + [(x, D, Z) for x in xs[::-1]], t), (228, 238, 245))
    gridtop, gridfront, outline = (151, 171, 188), (138, 155, 170), (76, 100, 123)
    for yy in np.linspace(0, D, 9): line(img, path(kind, [(x, yy, Z) for x in xs], t), gridtop, 2)
    for xx in np.linspace(0, L, 65):
        line(img, path(kind, [(xx, y, Z) for y in np.linspace(0, D, 17)], t), gridtop, 1)
        line(img, path(kind, [(xx, 0, z) for z in np.linspace(0, Z, 12)], t), gridfront, 1)
    for z in np.linspace(0, Z, 10): line(img, path(kind, [(x, 0, z) for x in xs], t), gridfront, 2 if z in (0, Z) else 1)
    for y in np.linspace(0, D, 9): line(img, path(kind, [(L, y, z) for z in np.linspace(0, Z, 12)], t), gridtop, 1)
    for z in np.linspace(0, Z, 10): line(img, path(kind, [(L, y, z) for y in np.linspace(0, D, 20)], t), gridtop, 1)
    for xyz in [[(x, 0, Z) for x in xs], [(x, 0, 0) for x in xs], [(0, 0, z) for z in np.linspace(0, Z, 12)], [(L, 0, z) for z in np.linspace(0, Z, 12)], [(0, y, Z) for y in np.linspace(0, D, 17)], [(L, y, Z) for y in np.linspace(0, D, 17)], [(L, y, 0) for y in np.linspace(0, D, 17)]]:
        line(img, path(kind, xyz, t), outline, 3)
    center = -1.9 + (L + 3.8) * (t / 8.8)
    for x in np.linspace(max(0, center - 1.8), min(L, center + 1.8), 13) if 0 < center + 1.8 and center - 1.8 < L else []:
        alpha = math.exp(-0.5 * ((x - center) / 1.25) ** 2)
        if alpha >= .4:
            tinted = tuple(int(gridtop[i] * (1 - alpha * .56) + a[i] * alpha * .56) for i in range(3))
            line(img, path(kind, [(x, y, Z) for y in np.linspace(0, D, 17)], t), tinted, 2)
    if kind == 'P': xx, zz = 6.5, 1.04
    elif kind == 'S': xx, zz = 6.5, 1.04
    elif kind == 'Rayleigh': xx, zz = 6.5, 1.85
    else: xx, zz = 6.5, 1.89
    u, v = path(kind, [(xx, 0, zz)], t)[0]
    cv2.rectangle(img, (u - 8, v - 8), (u + 8, v + 8), (15, 25, 40), -1, cv2.LINE_AA)
    return img

def encode(kind, fps=24, dur=8.8, preview=False):
    OUT.mkdir(parents=True, exist_ok=True)
    bg = base_design(kind)
    if preview:
        pathh = OUT / ('vista_previa_' + kind + '.png')
        ok, encoded = cv2.imencode('.png', frame(kind, 3.4, bg))
        if not ok: raise RuntimeError('No se pudo crear la vista previa')
        pathh.write_bytes(encoded.tobytes())
        return pathh
    out = OUT / (kind + '_SIN_TEXTO_FHD.mp4')
    try:
        import imageio_ffmpeg
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        ffmpeg = 'ffmpeg'
    ff = [ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo', '-s', f'{W}x{H}', '-pix_fmt', 'bgr24', '-r', str(fps), '-i', '-', '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(out)]
    proc = subprocess.Popen(ff, stdin=subprocess.PIPE, stderr=subprocess.PIPE); start = time.time()
    try:
        for fi in range(round(fps * dur)): proc.stdin.write(frame(kind, fi / fps, bg).tobytes())
    finally:
        proc.stdin.close()
    code = proc.wait(); print(kind, 'DONE', code, round(time.time() - start, 1), 'sec', out, flush=True)
    if code: raise Exception('ffmpeg encoder error')
    return out

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--preview', action='store_true'); p.add_argument('--kind', default='all'); p.add_argument('--fps', type=int, default=24); args = p.parse_args()
    for k in list(CFG) if args.kind == 'all' else [args.kind]: print(encode(k, preview=args.preview, fps=args.fps), flush=True)
