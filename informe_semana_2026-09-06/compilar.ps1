# Compila el informe. Se corre desde esta carpeta:  .\compilar.ps1
#
# DOS COSAS QUE HAY QUE SABER ANTES DE PELEARSE CON ESTO:
#
# 1. MiKTeX se cae con "cannot retrieve attributes for the directory
#    'C:\Program Files\MATLAB\...\matlab.exe\'". No es un problema de LaTeX: hay
#    una entrada del PATH que apunta a un EJECUTABLE donde MiKTeX espera una
#    carpeta, y al recorrer el PATH se atraganta. Este script saca esa entrada
#    solo para su propio proceso; el PATH del sistema no se toca.
#
# 2. Va con LUALATEX y no con pdflatex, porque el preambulo usa fontspec. Y por
#    eso mismo NO lleva inputenc ni fontenc: con ellos los caracteres de un byte
#    alto se remapean mal y en el PDF aparece '£' donde va '¿' y 'Œ' donde va
#    '×'. Compila limpio y sale mal, que es la peor combinacion.
#
# Corre dos veces porque las referencias a figuras y secciones necesitan la
# segunda pasada para resolverse.

$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    $env:PATH = ($env:PATH -split ';' | Where-Object { $_ -and ($_ -notlike '*matlab.exe*') }) -join ';'

    Write-Host "[informe] regenerando las figuras desde los datos crudos..."
    $py = Join-Path $PSScriptRoot '..\..\src\interfaces\python'
    Push-Location $py
    try { & python figuras_semana.py } finally { Pop-Location }

    foreach ($pasada in 1, 2) {
        Write-Host "[informe] lualatex, pasada $pasada de 2..."
        & lualatex -interaction=nonstopmode informe.tex *> compilacion.log
    }

    if (-not (Test-Path informe.pdf)) {
        Get-Content compilacion.log | Select-String -Pattern "^!" | Select-Object -First 10
        throw "no se genero el PDF; ver compilacion.log"
    }

    $faltan = (Get-Content compilacion.log | Select-String 'Missing character').Count
    if ($faltan -gt 0) {
        Write-Warning "$faltan caracteres no existen en la fuente y SE PERDIERON del PDF."
        Write-Warning "Buscar 'Missing character' en compilacion.log para ver cuales."
    }

    $paginas = (Get-Content informe.log | Select-String 'Output written').ToString().Trim()
    Write-Host "[informe] OK: $paginas"
} finally { Pop-Location }
