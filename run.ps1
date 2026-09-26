param([string]$Python = "$PSScriptRoot\.venv-gui\Scripts\python.exe")
$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    & $Python "$PSScriptRoot\src\launcher.py"
    if ($LASTEXITCODE -ne 0) { throw "Application exited with code $LASTEXITCODE" }
} finally {
    Pop-Location
}
