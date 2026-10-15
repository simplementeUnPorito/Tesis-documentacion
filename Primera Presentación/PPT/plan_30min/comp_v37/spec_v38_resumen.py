"""Comprimida v37: un tema por slide. ('old', slide_comp29, escena, opciones) reutiliza la coreografía original;
('new', slide_larga_v37) arma la escena con el contenido de la larga; ('keys', chips) cierra el tema con palabras clave.
Opciones de 'old': larga (nº de la larga v37 para las notas), drop (tags a quitar), img (tag -> imagen nueva),
head (tag -> texto de encabezado)."""
import os
FIG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figuras_es_v25")
PALETTE = ["1F4E79", "C55A11", "2E75B6", "548235", "7F6000", "843C0C"]

def chip_xml(tag, kw, det, color, r, EMU):
    x, y, w, h = (int(v * EMU) for v in r)
    esc = lambda s: s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return (f'<p:sp xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
            f'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            f'<p:nvSpPr><p:cNvPr id="{tag}" name="Chip [o{tag}]"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>'
            f'<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 14000"/></a:avLst></a:prstGeom>'
            f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" lIns="91440" tIns="45720" rIns="91440" bIns="45720" anchor="ctr"><a:normAutofit/></a:bodyPr><a:lstStyle/>'
            f'<a:p><a:pPr algn="ctr"/><a:r><a:rPr lang="es-ES" sz="1800" b="1"><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>'
            f'<a:latin typeface="Arial"/></a:rPr><a:t>{esc(kw)}</a:t></a:r>'
            + (f'<a:br><a:rPr lang="es-ES" sz="1300"/></a:br><a:r><a:rPr lang="es-ES" sz="1300"><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>'
               f'<a:latin typeface="Arial"/></a:rPr><a:t>{esc(det)}</a:t></a:r>' if det else '')
            + '</a:p></p:txBody></p:sp>')

FIXES = {}
o = lambda c, s, larga, **kw: ('old', c, s, dict(larga=larga, **kw))
n = lambda ln, **kw: ('new', ln, kw)
k = lambda *chips: ('keys', list(chips))

SLIDES = [
 dict(host=1, title=None, scenes=[]),
 dict(host=2, title="Por qué medir el terreno", scenes=[o(2, 0, 2), o(2, 1, 3), o(2, 2, 4),
      k(("Conocer el suelo", "antes, durante y después de la obra"), ("Sin alterar lo construido", "evaluar cambios y daños"),
        ("Método propuesto", "fenómeno → transductor → procesamiento"), ("Este trabajo", "la plataforma que mide"))]),
 dict(host=3, title="Ensayos de penetración", scenes=[o(3, 0, 5), o(3, 1, 6), o(3, 2, 7), o(3, 3, 8), o(3, 4, 9),
      o(3, 5, 10, head={67: "La otra familia de ensayos: la propagación de ondas"}),
      k(("SPT", "golpes N para hincar la cuchara"), ("CPT / CPTu", "perfil continuo de punta y fricción"),
        ("Resistencia, no rigidez", "la rigidez sale de correlaciones"), ("Ondas", "su velocidad depende de la rigidez"))]),
 dict(host=4, title="Del golpe a las ondas P y S", scenes=[o(4, 0, 11), o(4, 1, 12), o(4, 2, 13),
      k(("Golpe", "la deformación se propaga"), ("Primera aproximación", "homogéneo, isótropo, elástico lineal"),
        ("Navier", "solo dos ondas: P y S"))]),
 dict(host=5, title="Velocidad de corte y rigidez", scenes=[o(5, 0, 14), o(5, 1, 15), o(5, 2, 16), o(5, 3, 17), n(18),
      o(5, 4, 19), o(5, 5, 20),
      k(("Onda P", "compresión, Vp"), ("Onda S", "corte, Vs"), ("Pequeña deformación", "G ≈ Gmax"),
        ("Gmax = ρ·Vs²", "la relación buscada"), ("Error", "Vs pesa el doble que ρ"))]),
 dict(host=8, title="Capas e interfaces", scenes=[n(21), o(8, 1, 22, drop=[216], head={214: "En cada interfaz, la onda se refleja y se transmite"}), o(8, 4, 23),
      k(("Modelo en capas", "ρ, Vp y Vs por capa"), ("Interfaz", "se refleja y se transmite"),
        ("Snell", "ángulo crítico: sin θc = V1/V2"))]),
 dict(host=6, title="Ensayos dentro del terreno", scenes=[o(6, 0, 24), o(6, 1, 24), o(6, 2, 25), o(6, 3, 26), o(6, 4, 27), o(6, 5, 27),
      k(("Downhole", "un pozo, Vs por tramo"), ("Crosshole", "dos pozos, Vs por capa"),
        ("Directos", "pero perforan y son puntuales"))]),
 dict(host=7, title="Ensayos desde la superficie", scenes=[o(7, 0, 28), o(7, 1, 28), o(7, 2, 29), o(7, 3, 30), o(7, 4, 31),
      o(7, 5, 32), o(7, 6, 32),
      k(("Refracción", "onda de cabeza: la velocidad debe crecer con z"), ("Reflexión", "ida y vuelta: poca resolución arriba"))]),
 dict(host=8, title="La superficie libre", scenes=[o(8, 0, 33), o(8, 2, 33), o(8, 3, 34), n(35), o(8, 5, 36),
      k(("Superficie libre", "esfuerzo nulo"), ("SV y SH", "polarización de la onda S"), ("Conversión", "P ↔ SV; SH queda aparte"))]),
 dict(host=9, title="Ondas Love y Rayleigh", scenes=[o(9, 0, 37), o(9, 1, 38), n(39), o(9, 2, 40), o(9, 3, 41), o(9, 4, 42),
      o(9, 5, 43, drop=[281, 282]),
      k(("Love", "necesita una capa blanda; horizontal"), ("Rayleigh", "siempre existe; componente vertical"),
        ("Energía", "dos tercios van a Rayleigh"), ("Atenuación", "1/√r: domina lejos"), ("cR ≈ 0,9·Vs", "sin dispersión en un medio homogéneo"))]),
 dict(host=10, title="Dispersión e inversión", scenes=[o(10, 0, 44), o(10, 1, 45), o(10, 2, 46), o(10, 3, 47), o(10, 4, 48),
      k(("Capas", "cada λ ve otra profundidad"), ("Dispersión", "la velocidad de fase depende de f"),
        ("Inversión", "un modelo que reproduce la curva"), ("Límites", "supuestos y no unicidad"))]),
 dict(host=11, title="SASW y MASW", scenes=[o(11, 0, 49), o(11, 1, 50), o(11, 2, 51), o(11, 3, 52), o(11, 4, 53),
      k(("SASW", "dos receptores, Δφ"), ("MASW", "muchas posiciones: redundancia"), ("Registro", "matriz espacio–tiempo"),
        ("Adquisición sucesiva", "menos canales"))]),
 dict(host=12, title="De la medición al diseño", scenes=[o(12, 0, 54), o(12, 1, 55), n(56),
      k(("Tres requerimientos", "tiempo y posición, referencia, forma de onda"), ("Cinco condiciones", "del diseño del sistema"),
        ("SM-24", "elegido por disponibilidad"))]),
 dict(host=13, title="El geófono SM-24", scenes=[o(13, 0, 57), o(13, 1, 58), o(13, 2, 59), n(60),
      k(("SM-24", "10 Hz, 28,8 V·s/m"), ("Modelo", "masa, resorte y bobina"), ("Bajo 10 Hz", "−40 dB a 1 Hz"),
        ("Baja frecuencia", "es la que llega más profundo"))]),
 dict(host=14, title="Cómo extender la baja frecuencia", scenes=[o(14, 0, 61), o(14, 1, 62), n(63), n(64), n(65),
      k(("Cuatro familias", "carga, inversa, activas, forma"), ("Compensación inversa", "satura"),
        ("Resistencia negativa", "realimentación positiva"), ("Balance de fuerza", "4,5 Hz → 0,16 Hz, pero complejo"))]),
 dict(host=14, title="El método de Ma et al.", scenes=[o(14, 3, 66), o(14, 4, 67), o(14, 5, 68),
      k(("Bajar el pico", "no levantar el fondo"), ("Estable y simple", "filtro en serie, sin lazo"), ("Hcomp = 1 − HBP", "camino directo menos un pasabanda"))]),
 dict(host=15, title="El frente analógico (AFE)", scenes=[n(69), o(15, 1, 70), o(15, 2, 71), o(15, 3, 72), o(15, 4, 73), o(15, 5, 74),
      k(("Cadena", "entrada dif., PGA, pasabanda, sumador, Bessel"), ("Hasta ×1800", "recupera la atenuación 2ζ1"),
        ("Inversor y sumador", "menos componentes"))]),
 dict(host=16, title="Validación y offset", scenes=[o(16, 0, 75), o(16, 1, 76), o(16, 2, 77), o(16, 3, 78), o(16, 4, 79),
      k(("Validación", "barridos de 10 mHz a 200 kHz"), ("Offset", "hasta 45,8 % del fondo de escala"), ("Calibración", "lo baja a 0,4–3,9 %"))]),
 dict(host=12, title="El HAMMER y la plataforma", scenes=[n(80), o(12, 2, 81),
      k(("HAMMER", "marca el instante del impacto"), ("Plataforma", "un maestro y nodos por ESP-NOW"))]),
 dict(host=17, title="Digitalización en el PSoC", scenes=[o(17, 3, 82, img={629: os.path.join(FIG, "fig_delta_sigma_es.png")}),
      o(18, 0, 83), o(17, 1, 84), o(17, 0, 85), o(17, 2, 86),
      k(("ΔΣ", "resolución para señales lentas"), ("Rangos", "de ±0,512 a ±2,5 V"), ("Hardware decide cuándo", "el software, qué valores"))]),
 dict(host=18, title="Captura y almacenamiento", scenes=[o(18, 2, 87), o(18, 3, 88),
      o(18, 1, 89, img={642: os.path.join(FIG, "fig_media_movil_es.png")}, drop=[646]), o(18, 4, 90), o(18, 5, 91),
      k(("Máquina de estados", "dispara, cuenta y cierra"), ("RAM o SD", "512 lotes o el tamaño de la tarjeta"),
        ("Diezmado", "D muestras → 1"), ("Registro", "metadatos, CRC y original"))]),
 dict(host=22, title="Operación en campo", scenes=[o(22, 1, 92), o(22, 2, 93), o(23, 0, 94), o(23, 2, 95), o(23, 3, 96),
      k(("Interfaz web", "configura, revisa y decide"), ("Sesión de campo", "sin infraestructura"), ("Geometría", "21 posiciones, 40 m"),
        ("Posición", "10 cm de error = 5 % en c"))]),
 dict(host=19, title="Sincronización: por qué importa", scenes=[o(19, 1, 97), o(19, 2, 98), o(19, 3, 99),
      k(("ESP-NOW", "costo y simplicidad"), ("Δφ = 360°·f·Δt", "el error crece con f"), ("400 µs", "5° hasta unos 35 Hz"))]),
 dict(host=20, title="El disparo y su jitter", scenes=[o(20, 0, 100), o(20, 1, 101), o(20, 2, 102), o(20, 3, 103), o(20, 4, 104),
      k(("Broadcast", "una emisión para todos"), ("Jitter", "200–400 µs con 3 nodos"), ("Falta medir", "inicio del ADC y deriva"))]),
 dict(host=21, title="Descarga y flujo completo", scenes=[o(21, 0, 105), o(21, 1, 106), o(22, 0, 107),
      k(("Lotes con CRC", "reintento si algo falla"), ("Escala", "≈19 nodos por maestro"), ("Flujo", "del impacto al perfil Vs(z)"))]),
 dict(host=24, title="Procesamiento", scenes=[o(24, 3, 108), o(24, 1, 109), o(24, 2, 110),
      k(("Servidor", "el original no se toca"), ("Alineación y promedio", "unos 30 golpes por posición"), ("Resultado", "21 trazas espacio–tiempo"))]),
 dict(host=25, title="SNR aparente", scenes=[o(25, 0, 111), o(25, 1, 112), o(25, 2, 113),
      k(("Bajo 10 Hz", "0,5–2,1 dB"), ("Sobre 10 Hz", "16,7–24,4 dB"), ("Causas", "fuente, acople, geófono y electrónica"))]),
 dict(host=26, title="Estado y trabajo en curso", scenes=[o(26, 0, 114), o(26, 1, 115), n(116), n(117),
      k(("Demostrado", "la adquisición secuencial"), ("Falta", "simultánea, sincronía e inversión"), ("Wi-Fi FTM", "≈150 ns (preliminar)"),
        ("Martillete", "una fuente repetible"))]),
 dict(host=27, title=None, scenes=[]),
 dict(host=28, title=None, scenes=[]),
 dict(host=29, title="Referencias", scenes=[n(120), n(121), n(122), n(123), n(124)]),
 dict(host=23, title="Anexo: geometría del arreglo", scenes=[o(23, 1, 126)]),
]
