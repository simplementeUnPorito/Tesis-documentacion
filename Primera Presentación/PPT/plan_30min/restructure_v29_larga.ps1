param([string]$deck)
# Larga v29: puente tras la 9 (copia de la 5), slide nueva tras la 16 (copia de la 16),
# y 28 (interfaces) + 31 (Snell) movidas antes del downhole (19). Se trabaja por SlideID.
$app = New-Object -ComObject PowerPoint.Application
$p = $app.Presentations.Open($deck, 0, 0, 0)
$id = @{}; foreach ($n in 5, 9, 16, 18, 28, 31) { $id[$n] = $p.Slides($n).SlideID }
function Idx($sid) { $p.Slides.FindBySlideID($sid).SlideIndex }

$br = $p.Slides(5).Duplicate().Item(1); $br.MoveTo((Idx $id[9]))  # hacia adelante: la posición final es la de la 9 antes de quitar el duplicado
$nw = $p.Slides((Idx $id[16])).Duplicate().Item(1)   # queda justo después de la 16
$p.Slides((Idx $id[28])).MoveTo((Idx $id[18]) + 1)
$p.Slides((Idx $id[31])).MoveTo((Idx $id[28]) + 1)

"puente={0} nueva={1} interfaces={2} snell={3} total={4}" -f $br.SlideIndex, $nw.SlideIndex, (Idx $id[28]), (Idx $id[31]), $p.Slides.Count
$p.Save(); $p.Close()
