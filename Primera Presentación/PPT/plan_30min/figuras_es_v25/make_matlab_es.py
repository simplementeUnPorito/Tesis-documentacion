# Crea copias en español de los scripts de MATLAB de la figura de calibración (el repo no se toca).
import io, re
S = r'C:\Github\Tesis\docs\Propuesta Urucom\scripts'
W = r'C:\Users\elias\AppData\Local\trabajo\fig_es'
a = io.open(S + r'\agressive.m', encoding='utf8').read()
a, n1 = re.subn(r"inputFile = fullfile\(.*?'autocalibracionExampleOscilloscope.csv'\);",
                lambda m: "inputFile = 'C:/Github/Tesis/docs/Propuesta Urucom/Imagenes/autocalibracionExampleOscilloscope.csv';",
                a, flags=re.S)
old_out = r"'C:\Github\Tesis\docs\Propuesta Urucom\Imagenes\autocalibration_scope_sum.png'"
assert n1 == 1 and a.count(old_out) == 1
a = a.replace(old_out, "'" + W + r"\agressive_es_scope.png'")
a = a.replace("'Time (s)'", "'Tiempo (s)'").replace("'Stage output relative to V_{ref} (V)'", "'Salida de la etapa respecto de V_{ref} (V)'")
io.open(W + r'\agressive_es.m', 'w', encoding='utf8').write(a)

f = io.open(S + r'\format_agressive_calibration_panels.m', encoding='utf8').read()
old_run = r"run('C:\Github\Tesis\docs\Propuesta Urucom\scripts\agressive.m');"
old_png = r"'C:\Github\Tesis\docs\Urucom_2026_compact\imagenes\autocalibration_stage_outputs_agressive.png'"
assert f.count(old_run) == 1 and f.count(old_png) == 1 and f.count("xlabel(panelAx, 'Time (s)');") == 1
f = f.replace(old_run, "run('" + W + r"\agressive_es.m');")
f = f.replace(old_png, "'" + W + r"\g6_cal_ejemplo_es.png'")
f = f.replace("xlabel(panelAx, 'Time (s)');", "xlabel(panelAx, 'Tiempo (s)');")
io.open(W + r'\panels_es.m', 'w', encoding='utf8').write(f)
print('ok')
