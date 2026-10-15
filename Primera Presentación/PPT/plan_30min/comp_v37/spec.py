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
 dict(host=2, title="Por qué medir el terreno", scenes=[o(2, 0, 2), o(2, 1, 3), o(2, 2, 4)]),
 dict(host=3, title="Ensayos de penetración", scenes=[o(3, 0, 5), o(3, 1, 6), o(3, 2, 7), o(3, 3, 8), o(3, 4, 9),
      o(3, 5, 10, head={67: "La otra familia de ensayos: la propagación de ondas"})]),
 dict(host=4, title="Del golpe a las ondas P y S", scenes=[o(4, 0, 11), o(4, 1, 12), o(4, 2, 13)]),
 dict(host=5, title="Velocidad de corte y rigidez", scenes=[o(5, 0, 14), o(5, 1, 15), o(5, 2, 16), o(5, 3, 17), n(18),
      o(5, 4, 19), o(5, 5, 20)]),
 dict(host=8, title="Capas e interfaces", scenes=[n(21), o(8, 1, 22, drop=[216], head={214: "En cada interfaz, la onda se refleja y se transmite"}), o(8, 3, 34), o(8, 4, 23)]),
 dict(host=6, title="Ensayos dentro del terreno", scenes=[o(6, 0, 24), o(6, 1, 24), o(6, 2, 25), o(6, 3, 26), o(6, 4, 27), o(6, 5, 27)]),
 dict(host=7, title="Ensayos desde la superficie", scenes=[o(7, 0, 28), o(7, 1, 28), o(7, 2, 29), o(7, 3, 30), o(7, 4, 31),
      o(7, 5, 32), o(7, 6, 32)]),
 dict(host=8, title="La superficie libre", scenes=[o(8, 0, 33), o(8, 2, 33), o(8, 3, 34), n(35), o(8, 5, 36)]),
 dict(host=9, title="Ondas Love y Rayleigh", scenes=[o(9, 0, 37), o(9, 1, 38), n(39), o(9, 2, 40), o(9, 3, 41), o(9, 4, 42),
      o(9, 5, 43, drop=[281, 282])]),
 dict(host=10, title="Dispersión e inversión", scenes=[o(10, 0, 44), o(10, 1, 45), o(10, 2, 46), o(10, 3, 47), o(10, 4, 48)]),
 dict(host=11, title="SASW y MASW", scenes=[o(11, 0, 49), o(11, 1, 50), o(11, 2, 51), o(11, 3, 52), o(11, 4, 53)]),
 dict(host=12, title="De la medición al diseño", scenes=[o(12, 0, 54), o(12, 1, 55), n(56)]),
 dict(host=13, title="El geófono SM-24", scenes=[o(13, 0, 57), o(13, 1, 58), o(13, 2, 59), n(60)]),
 dict(host=14, title="Cómo extender la baja frecuencia", scenes=[o(14, 0, 61), o(14, 1, 62), n(63), n(64), n(65)]),
 dict(host=14, title="El método de Ma et al.", scenes=[o(14, 3, 66), o(14, 4, 67), o(14, 5, 68)]),
 dict(host=15, title="El frente analógico (AFE)", scenes=[n(69), o(15, 1, 70), o(15, 2, 71), o(15, 3, 72), o(15, 4, 73), o(15, 5, 74)]),
 dict(host=16, title="Validación y offset", scenes=[o(16, 0, 75), o(16, 1, 76), o(16, 2, 77), o(16, 3, 78), o(16, 4, 79)]),
 dict(host=12, title="El HAMMER y la plataforma", scenes=[n(80), o(12, 2, 81)]),
 dict(host=17, title="Digitalización en el PSoC", scenes=[o(17, 3, 82, img={629: os.path.join(FIG, "fig_delta_sigma_es.png")}),
      o(18, 0, 83), o(17, 1, 84), o(17, 0, 85), o(17, 2, 86)]),
 dict(host=18, title="Captura y almacenamiento", scenes=[o(18, 2, 87), o(18, 3, 88),
      o(18, 1, 89, img={642: os.path.join(FIG, "fig_media_movil_es.png")}, drop=[646]), o(18, 4, 90), o(18, 5, 91)]),
 dict(host=22, title="Operación en campo", scenes=[o(22, 1, 92), o(22, 2, 93), o(23, 0, 94), o(23, 2, 95), o(23, 3, 96)]),
 dict(host=19, title="Sincronización: por qué importa", scenes=[o(19, 1, 97), o(19, 2, 98), o(19, 3, 99)]),
 dict(host=20, title="El disparo y su jitter", scenes=[o(20, 0, 100), o(20, 1, 101), o(20, 2, 102), o(20, 3, 103), o(20, 4, 104)]),
 dict(host=21, title="Descarga y flujo completo", scenes=[o(21, 0, 105), o(21, 1, 106), o(22, 0, 107)]),
 dict(host=24, title="Procesamiento", scenes=[o(24, 3, 108), o(24, 1, 109), o(24, 2, 110)]),
 dict(host=25, title="SNR aparente", scenes=[o(25, 0, 111), o(25, 1, 112), o(25, 2, 113)]),
 dict(host=26, title="Estado y trabajo en curso", scenes=[o(26, 0, 114), o(26, 1, 115), n(116), n(117)]),
 dict(host=27, title=None, scenes=[]),
 dict(host=28, title=None, scenes=[]),
 dict(host=29, title="Referencias", scenes=[n(120), n(121), n(122), n(123), n(124)]),
 dict(host=23, title="Anexo: geometría del arreglo", scenes=[o(23, 1, 126)]),
]

# Palabras clave del riel lateral: (escena en la que entran, texto). Quedan visibles hasta el final del tema.
KEYS = {
 "Por qué medir el terreno": [(0, "Conocer el suelo"), (1, "Sin alterar lo construido"), (2, "Fenómeno → transductor → procesamiento")],
 "Ensayos de penetración": [(1, "SPT: golpes N"), (2, "CPT: perfil continuo"), (4, "Resistencia, no rigidez"), (5, "Ondas → rigidez")],
 "Del golpe a las ondas P y S": [(0, "Golpe → ondas"), (1, "Medio elástico lineal"), (2, "Navier: solo P y S")],
 "Velocidad de corte y rigidez": [(1, "Ondas P y S"), (3, "Pequeña deformación"), (5, "Gmax = ρ·Vs²"), (6, "Vs pesa el doble")],
 "Capas e interfaces": [(0, "Capas: ρ, Vp, Vs"), (1, "Reflexión y transmisión"), (3, "Ley de Snell")],
 "Ensayos dentro del terreno": [(1, "Downhole: un pozo"), (2, "Crosshole: dos pozos"), (4, "Directos, pero perforan")],
 "Ensayos desde la superficie": [(1, "Refracción: onda de cabeza"), (3, "Vs debe crecer con z"), (4, "Reflexión: ida y vuelta"), (5, "Poca resolución arriba")],
 "La superficie libre": [(1, "Esfuerzo nulo"), (2, "SV y SH"), (4, "P ↔ SV; SH aparte")],
 "Ondas Love y Rayleigh": [(0, "Love: capa blanda"), (2, "Rayleigh: siempre existe"), (4, "67 % de la energía"), (5, "Atenúa 1/√r"), (6, "cR ≈ 0,9·Vs")],
 "Dispersión e inversión": [(1, "Cada λ, otra profundidad"), (2, "Dispersión"), (3, "Inversión"), (4, "No unicidad")],
 "SASW y MASW": [(0, "SASW: Δφ entre dos"), (2, "MASW: redundancia"), (3, "Registro espacio–tiempo"), (4, "Adquisición sucesiva")],
 "De la medición al diseño": [(0, "3 requerimientos"), (1, "5 condiciones"), (2, "SM-24 por disponibilidad")],
 "El geófono SM-24": [(0, "SM-24: 10 Hz"), (1, "Masa, resorte y bobina"), (2, "−40 dB a 1 Hz"), (3, "Baja f llega más hondo")],
 "Cómo extender la baja frecuencia": [(0, "Cuatro familias"), (1, "Inversa: satura"), (2, "R negativa: inestable"), (4, "Balance: 0,16 Hz, complejo")],
 "El método de Ma et al.": [(0, "Bajar el pico"), (1, "Estable y simple"), (2, "Hcomp = 1 − HBP")],
 "El frente analógico (AFE)": [(0, "Hasta ×1800"), (1, "Entrada diferencial"), (3, "Inversor + sumador"), (4, "Bessel antialias")],
 "Validación y offset": [(0, "10 mHz – 200 kHz"), (1, "Offset hasta 45,8 %"), (4, "Calibrado: 0,4–3,9 %")],
 "El HAMMER y la plataforma": [(0, "HAMMER: instante del golpe"), (1, "Maestro + nodos ESP-NOW")],
 "Digitalización en el PSoC": [(0, "ΔΣ: resolución"), (1, "±0,512 a ±2,5 V"), (3, "Hardware: cuándo"), (3, "Software: qué valores")],
 "Captura y almacenamiento": [(0, "Máquina de estados"), (1, "RAM o SD"), (2, "Diezmado: D → 1"), (4, "CRC y original intacto")],
 "Operación en campo": [(0, "Interfaz web"), (1, "Sin infraestructura"), (2, "21 posiciones, 40 m"), (4, "10 cm → 5 % en c")],
 "Sincronización: por qué importa": [(0, "ESP-NOW: costo"), (1, "Δφ = 360°·f·Δt"), (1, "400 µs: 5° hasta 35 Hz"), (2, "Δc/c = c·Δt/Δx")],
 "El disparo y su jitter": [(1, "Broadcast"), (2, "Jitter: 200–400 µs"), (4, "Deriva sin medir")],
 "Descarga y flujo completo": [(0, "Lotes con CRC"), (1, "≈19 nodos por maestro"), (2, "Impacto → Vs(z)")],
 "Procesamiento": [(0, "Original intacto"), (1, "~30 golpes promediados"), (2, "21 trazas")],
 "SNR aparente": [(0, "< 10 Hz: 0,5–2,1 dB"), (1, "> 10 Hz: 16,7–24,4 dB"), (2, "Fuente, acople, sensor")],
 "Estado y trabajo en curso": [(0, "Secuencial: demostrado"), (1, "Falta: simultánea"), (2, "Wi-Fi FTM ≈150 ns"), (3, "Martillete repetible")],
}
