from pathlib import Path
from math import atan2, cos, sin, pi
import zlib
from PIL import Image, ImageDraw, ImageFont


OUT = Path(__file__).resolve().parent


def load_font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\seguisb.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()


FONT_TITLE = load_font(42, True)
FONT_SUBTITLE = load_font(22, False)
FONT_BOX = load_font(22, True)
FONT_SMALL = load_font(18, False)
FONT_EDGE = load_font(17, False)


COLORS = {
    "bg": "#F7F9FC",
    "ink": "#1E293B",
    "muted": "#64748B",
    "line": "#334155",
    "start": "#E0F2FE",
    "start_border": "#0284C7",
    "bis": "#DBEAFE",
    "bis_border": "#2563EB",
    "verify": "#FEF3C7",
    "verify_border": "#D97706",
    "real": "#DCFCE7",
    "real_border": "#16A34A",
    "done": "#F3E8FF",
    "done_border": "#9333EA",
    "fail": "#FEE2E2",
    "fail_border": "#DC2626",
    "note": "#FFFFFF",
    "note_border": "#CBD5E1",
}


class Canvas:
    def __init__(self, width, height, title, subtitle=""):
        self.img = Image.new("RGB", (width, height), COLORS["bg"])
        self.draw = ImageDraw.Draw(self.img)
        self.width = width
        self.height = height
        self.nodes = {}
        self.draw.text((50, 34), title, font=FONT_TITLE, fill=COLORS["ink"])
        if subtitle:
            self.draw.text((52, 88), subtitle, font=FONT_SUBTITLE, fill=COLORS["muted"])

    def rounded_box(self, key, x, y, w, h, title, body="", fill="note", radius=22):
        border = COLORS.get(fill + "_border", COLORS["note_border"])
        self.draw.rounded_rectangle(
            [x, y, x + w, y + h],
            radius=radius,
            fill=COLORS[fill],
            outline=border,
            width=3,
        )
        self.nodes[key] = (x, y, w, h)
        self.centered_text(x, y + 16, w, title, FONT_BOX, COLORS["ink"])
        if body:
            self.centered_wrapped_text(x + 18, y + 50, w - 36, body, FONT_SMALL, COLORS["ink"], line_gap=6)

    def phase_label(self, x, y, text, color):
        self.draw.rounded_rectangle([x, y, x + 250, y + 38], radius=18, fill=color)
        self.centered_text(x, y + 7, 250, text, FONT_SMALL, "#FFFFFF")

    def centered_text(self, x, y, w, text, font, fill):
        bbox = self.draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        self.draw.text((x + (w - tw) / 2, y), text, font=font, fill=fill)

    def wrap_lines(self, text, font, max_w):
        words = text.split()
        lines = []
        cur = ""
        for word in words:
            trial = word if not cur else cur + " " + word
            bbox = self.draw.textbbox((0, 0), trial, font=font)
            if bbox[2] - bbox[0] <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines

    def centered_wrapped_text(self, x, y, w, text, font, fill, line_gap=4):
        lines = []
        for part in text.split("\n"):
            lines.extend(self.wrap_lines(part, font, w) if part else [""])
        yy = y
        for line in lines:
            bbox = self.draw.textbbox((0, 0), line, font=font)
            tw = bbox[2] - bbox[0]
            self.draw.text((x + (w - tw) / 2, yy), line, font=font, fill=fill)
            yy += (bbox[3] - bbox[1]) + line_gap

    def node_anchor(self, key, side):
        x, y, w, h = self.nodes[key]
        if side == "top":
            return x + w / 2, y
        if side == "bottom":
            return x + w / 2, y + h
        if side == "left":
            return x, y + h / 2
        if side == "right":
            return x + w, y + h / 2
        return x + w / 2, y + h / 2

    def arrow(self, a, b, aside="bottom", bside="top", label="", bend=None, color=None):
        color = color or COLORS["line"]
        p1 = self.node_anchor(a, aside)
        p2 = self.node_anchor(b, bside)
        points = [p1]
        if bend:
            points.extend(bend)
        points.append(p2)
        self.poly_arrow(points, color=color)
        if label:
            lx = sum(p[0] for p in points) / len(points)
            ly = sum(p[1] for p in points) / len(points)
            self.edge_label(lx, ly, label)

    def poly_arrow(self, points, color=None, width=3):
        color = color or COLORS["line"]
        self.draw.line(points, fill=color, width=width, joint="curve")
        x1, y1 = points[-2]
        x2, y2 = points[-1]
        ang = atan2(y2 - y1, x2 - x1)
        size = 14
        left = (x2 - size * cos(ang - pi / 7), y2 - size * sin(ang - pi / 7))
        right = (x2 - size * cos(ang + pi / 7), y2 - size * sin(ang + pi / 7))
        self.draw.polygon([(x2, y2), left, right], fill=color)

    def edge_label(self, x, y, text):
        lines = self.wrap_lines(text, FONT_EDGE, 190)
        line_h = 21
        w = max(self.draw.textbbox((0, 0), line, font=FONT_EDGE)[2] for line in lines) + 16
        h = line_h * len(lines) + 8
        self.draw.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], radius=8, fill="#FFFFFF", outline="#CBD5E1")
        yy = y - h / 2 + 5
        for line in lines:
            bbox = self.draw.textbbox((0, 0), line, font=FONT_EDGE)
            self.draw.text((x - (bbox[2] - bbox[0]) / 2, yy), line, font=FONT_EDGE, fill=COLORS["ink"])
            yy += line_h

    def save(self, name):
        path = OUT / name
        self.img.save(path)
        return path


def draw_detailed():
    c = Canvas(
        1850,
        2480,
        "Maquina de estados detallada - calibracion PSoC GEO",
        "Biseccion por etapa -> verify -> realcheck -> restore capture path",
    )

    c.phase_label(70, 150, "Entrada / salida", "#0284C7")
    c.phase_label(70, 430, "Biseccion por etapa", "#2563EB")
    c.phase_label(70, 1345, "Verify", "#D97706")
    c.phase_label(70, 1690, "Realcheck", "#16A34A")

    x1, x2, x3 = 120, 700, 1280
    w, h = 390, 118

    c.rounded_box("idle", x1, 215, w, h, "PSOC_IDLE", "Espera boton fisico o comando web calibrar", "start")
    c.rounded_box("start", x2, 215, w, h, "start_calibration_if_idle", "Aborta servo, limpia captura, manda CAL_START", "start")
    c.rounded_box("stage_begin", x2, 455, w, h, "CAL_ASYNC_STAGE_BEGIN", "Selecciona AMux de la etapa y mide DAC center", "bis")

    c.rounded_box("measure_center", x2, 645, w, h, "CAL_ASYNC_MEASURE", "Descarta settle_samples y promedia center", "bis")
    c.rounded_box("eval_init", x2, 835, w, h, "EVAL_INIT", "Guarda base, registra mejor candidato", "bis")
    c.rounded_box("probe", x1, 1010, w, h, "MEASURE probe", "Mide center +/- PROBE_STEP para saber pendiente", "bis")
    c.rounded_box("eval_probe", x1, 1190, w, h, "EVAL_PROBE", "Detecta si subir DAC sube o baja la medicion", "bis")
    c.rounded_box("plan", x2, 1190, w, h, "PLAN_ITER", "Actualiza lo/hi, revisa DEADBAND, elige midpoint", "bis")
    c.rounded_box("measure_iter", x3, 1010, w, h, "MEASURE iter", "Mide el DAC medio de la biseccion", "bis")
    c.rounded_box("eval_iter", x3, 1190, w, h, "EVAL_ITER", "Registra candidato; si no llega a TOL vuelve a plan", "bis")
    c.rounded_box("finish_stage", x2, 1435, w, h, "finish_stage", "Escribe mejor DAC, loguea OK/FAIL, stage++", "bis")

    c.rounded_box("verify_begin", x2, 1620, w, h, "VERIFY_BEGIN", "Relee cada etapa usando su final_dac", "verify")
    c.rounded_box("eval_verify", x2, 1800, w, h, "EVAL_VERIFY", "ok = !saturado && error <= TOL", "verify")

    c.rounded_box("real_switch", x2, 1980, w, h, "REALCHECK_SWITCH", "ADC stop, stage=0, cambia a entrada real", "real")
    c.rounded_box("real_begin", x1, 2160, w, h, "REALCHECK_BEGIN", "Si enable=0 salta; si enable=1 mide final_dac", "real")
    c.rounded_box("eval_real", x2, 2160, w, h, "EVAL_REALCHECK", "Evalua error real y decide nudge", "real")
    c.rounded_box("nudge", x3, 2160, w, h, "MEASURE nudge", "Prueba DAC +/- nudge_step", "real")
    c.rounded_box("complete", x2, 2325, w, 92, "COMPLETE / CAL_DONE", "Restaura captura y vuelve a IDLE", "done", radius=18)

    c.arrow("idle", "start", "right", "left", "boton o web")
    c.arrow("start", "stage_begin", "bottom", "top", "busy=1")
    c.arrow("stage_begin", "measure_center", "bottom", "top")
    c.arrow("measure_center", "eval_init", "bottom", "top", "promedio listo")
    c.arrow("eval_init", "finish_stage", "bottom", "top", "error <= TOL", bend=[(1130, 1030), (1130, 1395)])
    c.arrow("eval_init", "probe", "left", "right", "si no llega")
    c.arrow("probe", "eval_probe", "bottom", "top")
    c.arrow("eval_probe", "plan", "right", "left", "pendiente OK")
    c.arrow("plan", "finish_stage", "bottom", "top", "DEADBAND / max_iter / sin rango")
    c.arrow("plan", "measure_iter", "right", "bottom", "midpoint")
    c.arrow("measure_iter", "eval_iter", "bottom", "top")
    c.arrow("eval_iter", "finish_stage", "left", "right", "mejor <= TOL")
    c.arrow("eval_iter", "plan", "left", "right", "sigue", bend=[(1190, 1300), (1190, 1260)])
    c.arrow("finish_stage", "stage_begin", "left", "left", "stage++ < 4", bend=[(610, 1490), (560, 1490), (560, 505)])
    c.arrow("finish_stage", "verify_begin", "bottom", "top", "stage == 4")
    c.arrow("verify_begin", "eval_verify", "bottom", "top", "measure verify")
    c.arrow("eval_verify", "verify_begin", "left", "left", "stage++ < 4", bend=[(650, 1860), (600, 1860), (600, 1680)])
    c.arrow("eval_verify", "real_switch", "bottom", "top", "stage == 4")
    c.arrow("real_switch", "real_begin", "left", "top")
    c.arrow("real_begin", "eval_real", "right", "left", "enable=1")
    c.arrow("real_begin", "real_begin", "left", "left", "enable=0: stage++", bend=[(80, 2220), (80, 2150), (200, 2150)])
    c.arrow("eval_real", "nudge", "right", "left", "puede mejorar")
    c.arrow("nudge", "eval_real", "left", "right", "mide nudge", bend=[(1220, 2225)])
    c.arrow("eval_real", "real_begin", "left", "right", "OK / empeora / max nudges", bend=[(640, 2220)])
    c.arrow("real_begin", "complete", "bottom", "left", "stage == 4", bend=[(315, 2370), (650, 2370)])

    # Legend
    c.rounded_box("legend", 1260, 220, 470, 210, "Lectura rapida", "TOL = criterio de OK.\nDEADBAND = dejar de mover DAC cerca del objetivo.\nMEASURE siempre descarta muestras y promedia.", "note")

    return c.save("calibration_fsm_detailed.png")


def draw_simple():
    c = Canvas(
        1500,
        1500,
        "Maquina funcional simplificada",
        "La misma logica, vista como fases de trabajo",
    )
    x = 480
    w, h = 540, 120
    ys = [170, 350, 530, 710, 890, 1070, 1250]

    c.rounded_box("trigger", x, ys[0], w, h, "1. Trigger", "Boton fisico o boton web pide calibrar", "start")
    c.rounded_box("prep", x, ys[1], w, h, "2. Preparar hardware", "Aborta servo, limpia buffers, entra a CALIBRATING", "start")
    c.rounded_box("search", x, ys[2], w, h, "3. Buscar DAC por etapa", "Para PGA, BP, Adder y LP: center -> probe -> biseccion", "bis")
    c.rounded_box("best", x, ys[3], w, h, "4. Guardar mejor candidato", "Aunque no sea perfecto, deja el mejor DAC no saturado", "bis")
    c.rounded_box("verify", x, ys[4], w, h, "5. Verify", "Relee cada final_dac y marca ok si error <= TOL", "verify")
    c.rounded_box("real", x, ys[5], w, h, "6. Realcheck", "Con entrada real, nudges finos +/-1 LSB si esta habilitado", "real")
    c.rounded_box("done", x, ys[6], w, h, "7. Restaurar y avisar", "Vuelve a camino de captura y manda CAL_DONE", "done")

    for a, b in zip(["trigger", "prep", "search", "best", "verify", "real"], ["prep", "search", "best", "verify", "real", "done"]):
        c.arrow(a, b, "bottom", "top")

    c.rounded_box("loop", 80, 530, 310, 305, "Loop interno", "La fase 3 se repite para 4 etapas:\nGEO_PGA\nGEO_BP\nGEO_ADDER\nGEO_LP", "note")
    c.arrow("loop", "search", "right", "left")

    c.rounded_box("fast", 1085, 530, 330, 370, "Que lo hace lento", "Cada medicion hace:\n1) descartar settle\n2) promediar N*WINDOW\n3) esperar estabilidad\n\nRealcheck suele ser el mayor costo.", "note")
    c.arrow("search", "fast", "right", "left")
    c.arrow("real", "fast", "right", "left")

    c.rounded_box("tol", 80, 930, 330, 250, "TOL vs DEADBAND", "TOL: define OK formal.\nDEADBAND: corta movimiento cerca del objetivo para no perseguir ruido.", "note")
    c.arrow("tol", "search", "right", "left", bend=[(420, 1060), (420, 590)])

    return c.save("calibration_fsm_simplified.png")


def write_explanation():
    text = """# Maquina de estados de calibracion PSoC GEO

Archivos generados:

- `calibration_fsm_detailed.png`: maquina de estados completa del firmware.
- `calibration_fsm_simplified.png`: vista funcional simplificada.
- `calibration_fsm_diagrams.pdf`: los dos diagramas en un solo PDF.

## Lectura rapida

La calibracion tiene tres fases grandes:

1. **Busqueda por biseccion**: para cada etapa GEO (`GEO_PGA`, `GEO_BP`, `GEO_ADDER`, `GEO_LP`) mide un DAC inicial, hace un probe para saber el sentido de la pendiente, y luego usa biseccion para encontrar el mejor codigo DAC.
2. **Verify**: vuelve a medir el `final_dac` elegido por cada etapa. Aca se decide si el resultado formalmente cumple `TOL`.
3. **Realcheck**: mide con la entrada real del geofono y puede hacer nudges finos de `+/-1 LSB` si esta habilitado para esa etapa.

Al final restaura el camino normal de captura y manda `CAL_DONE`.

## Estados internos

`CAL_ASYNC_STAGE_BEGIN` prepara la etapa actual: selecciona `AMux_ADC`, arranca ADC y mide `dac_center`.

`CAL_ASYNC_MEASURE` es un estado comun. No decide nada por si solo: escribe DAC, descarta muestras de asentamiento, promedia y vuelve al estado evaluador que lo llamo.

`CAL_ASYNC_EVAL_INIT` mira la medicion del centro. Si ya esta dentro de `TOL`, termina la etapa. Si no, manda a medir el probe.

`CAL_ASYNC_EVAL_PROBE` compara centro contra probe para deducir si subir DAC sube o baja la medicion. Con eso inicializa el rango `[lo, hi]`.

`CAL_ASYNC_PLAN_ITER` decide el siguiente DAC de biseccion. Corta si llega a `DEADBAND`, si se queda sin rango, o si llega a `MAX_ITER`.

`CAL_ASYNC_EVAL_ITER` registra el punto medido, actualiza el mejor candidato, y vuelve a `PLAN_ITER` si todavia no llego a `TOL`.

`CAL_ASYNC_VERIFY_BEGIN` y `CAL_ASYNC_EVAL_VERIFY` releen cada etapa usando su `final_dac`. El resultado formal de verify es `!saturado && error <= TOL`.

`CAL_ASYNC_REALCHECK_SWITCH` cambia hacia la fase de entrada real.

`CAL_ASYNC_REALCHECK_BEGIN` inicia realcheck de cada etapa. Si `CAL_REALCHECK_ENABLE_*` es 0, salta esa etapa.

`CAL_ASYNC_EVAL_REALCHECK` decide si el punto real ya esta OK, si conviene hacer un nudge, o si el nudge empeoro/saturo y hay que terminar.

`CAL_ASYNC_DONE` queda cuando se restaura el camino de captura y `busy=0`.

## TOL vs DEADBAND

`TOL` es el criterio formal de exito: si `abs(medido - target) <= TOL`, ese punto puede considerarse OK.

`DEADBAND` es un criterio de control: si el error actual ya entro en esa zona, deja de mover el DAC para no perseguir ruido o alternar entre codigos vecinos.

Si `DEADBAND == TOL`, el corte de movimiento coincide con el criterio formal.

Si `DEADBAND > TOL`, la biseccion puede terminar antes, pero luego `verify` podria marcar esa etapa como no OK.

Si `DEADBAND < TOL`, va a perseguir mas fino que el criterio formal, normalmente mas lento y mas sensible al ruido.

## Donde mirar en codigo

- `calibration.c`: enum `PsocCalAsyncState` y `psoc_calibration_service_async()`.
- `calibration_tables_geo_*.h`: parametros por etapa.
- `calibration.h`: structs y factor global `CAL_SETTLE_FACTOR`.
"""
    path = OUT / "calibration_fsm_explanation.md"
    path.write_text(text, encoding="utf-8")
    return path


def pdf_stream(data):
    return (
        f"<< /Length {len(data)} >>\nstream\n".encode("ascii")
        + data
        + b"\nendstream"
    )


def write_pdf(image_paths, pdf_path):
    objects = {1: b"<< /Type /Catalog /Pages 2 0 R >>"}
    page_ids = []
    next_id = 3

    for idx, path in enumerate(image_paths):
        img = Image.open(path).convert("RGB")
        width_px, height_px = img.size
        scale = 0.5
        page_w = width_px * scale
        page_h = height_px * scale

        raw = zlib.compress(img.tobytes(), level=6)
        image_id = next_id
        next_id += 1
        objects[image_id] = (
            f"<< /Type /XObject /Subtype /Image /Width {width_px} /Height {height_px} "
            f"/ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /FlateDecode "
            f"/Length {len(raw)} >>\nstream\n"
        ).encode("ascii") + raw + b"\nendstream"

        content = f"q {page_w:.2f} 0 0 {page_h:.2f} 0 0 cm /Im{idx} Do Q\n".encode("ascii")
        content_id = next_id
        next_id += 1
        objects[content_id] = pdf_stream(content)

        page_id = next_id
        next_id += 1
        page_ids.append(page_id)
        objects[page_id] = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {page_w:.2f} {page_h:.2f}] "
            f"/Resources << /XObject << /Im{idx} {image_id} 0 R >> >> "
            f"/Contents {content_id} 0 R >>"
        ).encode("ascii")

    kids = " ".join(f"{pid} 0 R" for pid in page_ids)
    objects[2] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode("ascii")

    with open(pdf_path, "wb") as f:
        f.write(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = {}
        for obj_id in sorted(objects):
            offsets[obj_id] = f.tell()
            f.write(f"{obj_id} 0 obj\n".encode("ascii"))
            f.write(objects[obj_id])
            f.write(b"\nendobj\n")
        xref_pos = f.tell()
        max_id = max(objects)
        f.write(f"xref\n0 {max_id + 1}\n".encode("ascii"))
        f.write(b"0000000000 65535 f \n")
        for obj_id in range(1, max_id + 1):
            f.write(f"{offsets[obj_id]:010d} 00000 n \n".encode("ascii"))
        f.write(
            f"trailer\n<< /Size {max_id + 1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode("ascii")
        )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    detailed = draw_detailed()
    simple = draw_simple()
    explanation = write_explanation()

    pdf = OUT / "calibration_fsm_diagrams.pdf"
    write_pdf([detailed, simple], pdf)

    print(detailed)
    print(simple)
    print(pdf)
    print(explanation)


if __name__ == "__main__":
    main()
