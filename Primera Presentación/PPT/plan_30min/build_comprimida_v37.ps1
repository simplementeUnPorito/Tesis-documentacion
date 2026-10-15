param([string]$larga, [string]$out)
# Comprimida v37: cada slide comprimida reúne varias slides de la larga v37 como escenas, una por clic.
# Escena 0 visible al entrar; en cada clic salen (fundido) los objetos de la escena anterior y entran los de la siguiente.
# Las notas de cada slide comprimida concatenan las de sus escenas con el rótulo «[Slide larga NN: título]».
# Grupos por tema sobre el orden de la larga v37 (que es el orden de Elías).
$groups = @(
  @(1), @(2,3,4), @(5,6,7,8,9,10), @(11,12,13), @(14,15,16,17,18,19,20), @(21,22,23), @(24,25,26,27),
  @(28,29,30,31,32), @(33,34,35,36), @(37,38,39,40,41,42,43), @(44,45,46,47,48), @(49,50,51,52,53),
  @(54,55,56), @(57,58,59,60), @(61,62,63,64,65), @(66,67,68), @(69,70,71,72,73,74), @(75,76,77,78,79),
  @(80,81), @(82,83,84,85,86), @(87,88,89,90,91), @(92,93,94,95,96), @(97,98,99), @(100,101,102,103,104),
  @(105,106,107), @(108,109,110), @(111,112,113), @(114,115,116,117), @(118), @(119), @(120,121,122,123,124), @(125,126)
)
$all = @(); foreach ($g in $groups) { $all += $g }
if ($all.Count -ne 126 -or (($all | Sort-Object -Unique).Count) -ne 126) { throw "los grupos no cubren 1..126 exactamente una vez" }

$app = New-Object -ComObject PowerPoint.Application
$src = $app.Presentations.Open($larga, -1, 0, 0)
$src.SaveCopyAs($out); $src.Close()
$p = $app.Presentations.Open($out, 0, 0, -1)          # con ventana: Paste falla sin ella
$app.Visible = -1
$win = $p.Windows(1); $win.ViewType = 1          # vista de una slide: View.Paste pega shapes, no slides
$id = @{}; for ($i = 1; $i -le $p.Slides.Count; $i++) { $id[$i] = $p.Slides($i).SlideID }

function TitleOf($s) {
  foreach ($sh in $s.Shapes) { if ($sh.Name -eq "Título" -and $sh.HasTextFrame) { return $sh.TextFrame.TextRange.Text } }
  foreach ($sh in $s.Shapes) { if ($sh.HasTextFrame -and $sh.TextFrame.HasText) { return $sh.TextFrame.TextRange.Text } }
  return ""
}
function NotesOf($s) { try { return $s.NotesPage.Shapes.Placeholders(2).TextFrame.TextRange.Text } catch { return "" } }

$log = @()
foreach ($g in $groups) {
  $base = $p.Slides.FindBySlideID($id[$g[0]])
  $notes = @("[Slide larga $($g[0]): $(TitleOf $base)] $(NotesOf $base)")
  $scenes = @()
  $sc0 = @(); foreach ($sh in $base.Shapes) { if ($sh.Type -ne 14) { $sc0 += $sh.Name } }
  $scenes += ,$sc0
  for ($k = 1; $k -lt $g.Count; $k++) {
    $m = $p.Slides.FindBySlideID($id[$g[$k]])
    $notes += "[Slide larga $($g[$k]): $(TitleOf $m)] $(NotesOf $m)"
    $idx = @(); for ($j = 1; $j -le $m.Shapes.Count; $j++) { if ($m.Shapes($j).Type -ne 14) { $idx += $j } }
    $pos = @{}; foreach ($j in $idx) { $pos[$j] = @($m.Shapes($j).Left, $m.Shapes($j).Top) }
    $ok = $false
    for ($try = 0; $try -lt 4 -and -not $ok; $try++) {
      try {
        $m.Shapes.Range([object[]]$idx).Copy(); Start-Sleep -Milliseconds 200
        $win.View.GotoSlide($base.SlideIndex); $before = $base.Shapes.Count
        $win.View.Paste(); Start-Sleep -Milliseconds 200
        if ($base.Shapes.Count - $before -ne $idx.Count) { throw "se pegaron $($base.Shapes.Count - $before) de $($idx.Count)" }
        $ok = $true
      }
      catch { $err = $_.Exception.Message; Start-Sleep -Milliseconds 400 }
    }
    if (-not $ok) { $p.Close(); throw "no se pudo copiar la slide larga $($g[$k]): $err" }
    $names = @(); $n = 0
    foreach ($j in $idx) {
      $n++; $sh = $base.Shapes($before + $n)
      $sh.Left = $pos[$j][0]; $sh.Top = $pos[$j][1]          # misma posición que en la larga
      $sh.Name = "E$k " + $sh.Name
      $names += $sh.Name
    }
    $scenes += ,$names
  }
  # animaciones: en el clic k salen los de la escena k-1 y entran los de la k
  $seq = $base.TimeLine.MainSequence
  for ($k = 1; $k -lt $scenes.Count; $k++) {
    $first = $true
    foreach ($nm in $scenes[$k - 1]) {
      $trig = if ($first) { 1 } else { 2 }                      # 1: al hacer clic, 2: con la anterior
      $e = $seq.AddEffect($base.Shapes($nm), 10, 0, $trig); $e.Exit = -1; $e.Timing.Duration = 0.25; $first = $false
    }
    foreach ($nm in $scenes[$k]) {
      $e = $seq.AddEffect($base.Shapes($nm), 10, 0, 2); $e.Timing.Duration = 0.3; $e.Timing.TriggerDelayTime = 0.25
    }
  }
  try { $base.NotesPage.Shapes.Placeholders(2).TextFrame.TextRange.Text = ($notes -join "`r`r") } catch {}
  for ($k = $g.Count - 1; $k -ge 1; $k--) { $p.Slides.FindBySlideID($id[$g[$k]]).Delete() }
  $log += "{0,2}: larga {1} ({2} escenas)" -f $base.SlideIndex, ($g -join ","), $g.Count
}
$log
"total: $($p.Slides.Count) slides"
$p.Save(); $p.Close()
