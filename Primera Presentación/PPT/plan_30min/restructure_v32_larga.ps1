param([string]$deck)
# v32 larga (numeración de la v31 editada por el autor, 123 slides al entrar).
# Nuevas: FTM y martillete (copias de la 61) tras el trabajo futuro (113); divisor «Anexo» (copia de la 117) antes de la 123.
# Se borran 114 (UWB) y 115 (riesgo watchdog). Se mueven: 104 (error de posición) tras 93 (receptor móvil);
# 95 (descarga por lotes) y 96 (pares) tras 103 (deriva), al cerrar la sincronización.
$app = New-Object -ComObject PowerPoint.Application
$p = $app.Presentations.Open($deck, 0, 0, 0)
$n0 = $p.Slides.Count
if ($n0 -ne 123) { throw "se esperaban 123 slides y hay $n0" }
$id = @{}; for ($i = 1; $i -le $n0; $i++) { $id[$i] = $p.Slides($i).SlideID }
$id['F'] = $p.Slides(61).Duplicate().Item(1).SlideID
$id['D'] = $p.Slides(61).Duplicate().Item(1).SlideID
$id['A'] = $p.Slides.FindBySlideID($id[117]).Duplicate().Item(1).SlideID
$p.Slides.FindBySlideID($id[114]).Delete(); $p.Slides.FindBySlideID($id[115]).Delete()

$order = @(); $order += 1..93; $order += 104, 94; $order += 97..103; $order += 95, 96
$order += 105..113; $order += 'F', 'D'; $order += 116..122; $order += 'A', 123
if ($order.Count -ne $p.Slides.Count) { throw "orden con $($order.Count), hay $($p.Slides.Count)" }
for ($k = 0; $k -lt $order.Count; $k++) { $p.Slides.FindBySlideID($id[$order[$k]]).MoveTo($k + 1) }
"FTM={0} martillete={1} anexo={2} total={3}" -f $p.Slides.FindBySlideID($id['F']).SlideIndex, $p.Slides.FindBySlideID($id['D']).SlideIndex, $p.Slides.FindBySlideID($id['A']).SlideIndex, $p.Slides.Count
$p.Save(); $p.Close()
