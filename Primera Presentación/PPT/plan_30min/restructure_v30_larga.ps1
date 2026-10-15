param([string]$deck)
# v30 larga (numeración v29 al entrar): capas (copia de la 21), sensores (copia de la 86, tras la 52),
# SM-24 (54) antes de la plataforma (53), y una quinta slide de referencias. Todo por SlideID.
$app = New-Object -ComObject PowerPoint.Application
$p = $app.Presentations.Open($deck, 0, 0, 0)
$id = @{}; foreach ($n in 21, 52, 53, 54, 86) { $id[$n] = $p.Slides($n).SlideID }
$lastRef = $p.Slides($p.Slides.Count).SlideID
function Idx($sid) { $p.Slides.FindBySlideID($sid).SlideIndex }

$capas = $p.Slides((Idx $id[21])).Duplicate().Item(1)          # queda en 22; la 21 pasa a ser «capas»
$sens = $p.Slides((Idx $id[86])).Duplicate().Item(1)
$sens.MoveTo((Idx $id[53]))                                     # hacia atrás: ocupa el lugar de la plataforma
$p.Slides((Idx $id[54])).MoveTo((Idx $id[53]))                  # SM-24 justo antes de la plataforma
$ref5 = $p.Slides((Idx $lastRef)).Duplicate().Item(1)

"capas={0} interfaces={1} sensores={2} sm24={3} plataforma={4} ref5={5} total={6}" -f (Idx $id[21]), $capas.SlideIndex, $sens.SlideIndex, (Idx $id[54]), (Idx $id[53]), $ref5.SlideIndex, $p.Slides.Count
$p.Save(); $p.Close()
