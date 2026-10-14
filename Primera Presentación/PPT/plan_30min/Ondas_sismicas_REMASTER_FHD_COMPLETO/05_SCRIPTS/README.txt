VERSIONES DE LOS SCRIPTS

01_CON_TEXTO
  Copia de los scripts originales. No modificar esta carpeta si se necesita conservar la versión actual.
  Los cuatro MP4 con texto están en ../01_REDIBUJADOS_FULL_HD.

02_SIN_TEXTO
  render_waves_sin_texto.py genera únicamente la animación visual: bloque, malla, deformación, onda y marcador.
  No agrega títulos, subtítulos, tarjetas, leyendas ni etiquetas de ejes.
  Los cuatro MP4 sin texto están en ../07_REDIBUJADOS_SIN_TEXTO.

La versión sin texto escribe sus resultados en:
  ../07_REDIBUJADOS_SIN_TEXTO

Ejemplo:
  python render_waves_sin_texto.py --kind all
  python render_waves_sin_texto.py --preview --kind P

Dependencias: Python, OpenCV, NumPy y ffmpeg. Si imageio-ffmpeg está instalado,
el script usa su ejecutable ffmpeg automáticamente.
