param([string]$deck)
# v31 larga (numeración v30 al entrar). Slides nuevas: N1 reflexión en la superficie libre (copia de la 29)
# antes de la 35, y N2 condición de Rayleigh (copia de la 36) después de la 37. Reordena la parte de sistema:
# GEO digital → HAMMER → interfaz web → sesión → geometría → receptor móvil → comunicación y sincronización →
# flujo completo → análisis. Todo por SlideID: el orden final se escribe como lista de índices de la v30.
$app = New-Object -ComObject PowerPoint.Application
$p = $app.Presentations.Open($deck, 0, 0, 0)
$n0 = $p.Slides.Count
$id = @{}; for ($i = 1; $i -le $n0; $i++) { $id[$i] = $p.Slides($i).SlideID }
$id['N1'] = $p.Slides(29).Duplicate().Item(1).SlideID
$id['N2'] = $p.Slides((36 + 1)).Duplicate().Item(1).SlideID   # la 36 corrió a 37 por la copia de la 29

$order = @()
$order += 1..34; $order += 'N1'; $order += 35, 36, 37; $order += 'N2'; $order += 38..86
$order += 98, 100, 101, 102, 104                      # HAMMER, interfaz web, sesión, geometría, receptor móvil
$order += 87, 88, 96, 97                              # cómo llega la información al maestro
$order += 89, 90, 91, 92, 93, 94, 95                  # sincronización: por qué, cómo, cuánto, deriva
$order += 99, 103, 105, 106, 107, 108, 109            # flujo completo y análisis
$order += 110..$n0
if ($order.Count -ne $n0 + 2) { throw "orden con $($order.Count) entradas, se esperaban $($n0 + 2)" }
for ($k = 0; $k -lt $order.Count; $k++) { $p.Slides.FindBySlideID($id[$order[$k]]).MoveTo($k + 1) }

"N1={0} N2={1} HAMMER={2} total={3}" -f $p.Slides.FindBySlideID($id['N1']).SlideIndex, $p.Slides.FindBySlideID($id['N2']).SlideIndex, $p.Slides.FindBySlideID($id[98]).SlideIndex, $p.Slides.Count
$p.Save(); $p.Close()
