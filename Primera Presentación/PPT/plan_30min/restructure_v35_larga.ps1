param([string]$deck)
# v35 larga: orden del bloque de comunicación (numeración v34 al entrar):
# 96 ESP-NOW → 104 desfase→fase → 105 velocidad de fase → 97 disparo → 100 por qué broadcast →
# 101 jitter → 103 alcance → 102 deriva → 98 descarga por lotes → 99 pares.
$app = New-Object -ComObject PowerPoint.Application
$p = $app.Presentations.Open($deck, 0, 0, 0)
$expect = @{ 96 = 'Se eligió ESP-NOW'; 97 = 'El disparo se prepara'; 98 = 'Los registros se descargan'; 99 = 'Los pares de ESP-NOW';
             100 = 'Por qué el disparo'; 101 = 'Medición del jitter'; 102 = 'Tras el disparo'; 103 = 'Alcance de la medición';
             104 = 'Un desfase de tiempo'; 105 = 'En velocidad de fase' }
$id = @{}
foreach ($n in $expect.Keys) {
  $t = $p.Slides($n).Shapes("Título").TextFrame.TextRange.Text
  if (-not $t.StartsWith($expect[$n])) { throw "slide $n es «$t»" }
  $id[$n] = $p.Slides($n).SlideID
}
$order = 96, 104, 105, 97, 100, 101, 103, 102, 98, 99
for ($k = 0; $k -lt $order.Count; $k++) { $p.Slides.FindBySlideID($id[$order[$k]]).MoveTo(96 + $k) }
96..105 | ForEach-Object { "{0}: {1}" -f $_, $p.Slides($_).Shapes("Título").TextFrame.TextRange.Text }
$p.Save(); $p.Close()
