param(
    [ValidateSet('pyinstaller', 'nuitka')][string]$Builder = 'pyinstaller',
    [string]$Python = "$PSScriptRoot\.venv-gui\Scripts\python.exe",
    [ValidatePattern('^[A-Za-z0-9_-]+$')][string]$OutputName = 'BDOChestStudio',
    [switch]$Incremental
)
$ErrorActionPreference = 'Stop'
$buildOriginalPath = $env:PATH
$buildOriginalName = $env:BDO_BUILD_NAME
Push-Location $PSScriptRoot
try {
    # Avoid harvesting unrelated DLLs from media tools or other Qt installs.
    $env:PATH = "$(Split-Path $Python);$env:SystemRoot\System32;$env:SystemRoot"
    $env:BDO_BUILD_NAME = $OutputName
    if ($Builder -eq 'nuitka') {
        & $Python -m nuitka --mode=onefile --enable-plugin=pyside6 --windows-console-mode=disable --include-data-dir=src/bdo_sim/assets=bdo_sim/assets --include-data-files=LICENSE=licenses/LICENSE --include-data-files=THIRD_PARTY_NOTICES.md=licenses/THIRD_PARTY_NOTICES.md --output-dir=dist "--output-filename=$OutputName.exe" src/launcher.py
    } else {
        $buildArguments = @('-m', 'PyInstaller', '--noconfirm')
        if (-not $Incremental) { $buildArguments += '--clean' }
        & $Python @buildArguments scripts/BDOChestStudio.spec
    }
    if ($LASTEXITCODE -ne 0) { throw "Сборка завершилась с кодом $LASTEXITCODE" }
} finally {
    $env:PATH = $buildOriginalPath
    $env:BDO_BUILD_NAME = $buildOriginalName
    Pop-Location
}
