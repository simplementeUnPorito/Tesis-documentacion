[CmdletBinding()]
param([string]$StoreRoot = $env:GITHUB_LFS_ROOT)
$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
& (Join-Path $PSScriptRoot 'configure-lfs-folderstore.ps1') -StoreRoot $StoreRoot
& git -C $repoRoot lfs checkout '*.zip' '*.drawio'
if ($LASTEXITCODE -ne 0) { throw 'No se pudieron hidratar los documentos LFS.' }
