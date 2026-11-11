$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$rscript = Get-ChildItem "$env:ProgramFiles\R" -Recurse -Filter Rscript.exe |
    Where-Object { $_.FullName -match '\\bin\\Rscript\.exe$' } |
    Sort-Object FullName -Descending |
    Select-Object -First 1

if (-not $rscript) {
    throw "Rscript.exe was not found under $env:ProgramFiles\R"
}

$renvPlatformRoot = Join-Path $projectRoot "renv\library\windows"
$rVersionLibrary = Get-ChildItem $renvPlatformRoot -Directory |
    Sort-Object Name -Descending |
    Select-Object -First 1
$architectureLibrary = Get-ChildItem $rVersionLibrary.FullName -Directory |
    Select-Object -First 1

if (-not $architectureLibrary) {
    throw "The project renv library is missing. Run renv::restore() first."
}

$env:R_LIBS_USER = $architectureLibrary.FullName
Push-Location $projectRoot
try {
    & $rscript.FullName --vanilla analysis/figures/generate_research_figures.R
    if ($LASTEXITCODE -ne 0) {
        throw "R figure generation failed with exit code $LASTEXITCODE"
    }
}
finally {
    Pop-Location
}
