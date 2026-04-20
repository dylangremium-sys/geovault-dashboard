param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"

Write-Host "==> Using Python executable: $Python"

$venvPath = ".venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "==> Creating virtual environment"
    & $Python -m venv $venvPath
}

$venvPython = Join-Path $venvPath "Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    throw "Virtualenv Python not found at $venvPython"
}

Write-Host "==> Upgrading pip"
& $venvPython -m pip install --upgrade pip

Write-Host "==> Installing PyInstaller"
& $venvPython -m pip install -r "scripts/requirements-packaging.txt"

Write-Host "==> Cleaning previous build outputs"
if (Test-Path "build") { Remove-Item "build" -Recurse -Force }
if (Test-Path "dist") { Remove-Item "dist" -Recurse -Force }
if (Test-Path "DriedFruitLedger.spec") { Remove-Item "DriedFruitLedger.spec" -Force }

Write-Host "==> Building Dried Fruit Ledger executable"
& $venvPython -m PyInstaller `
  --noconfirm `
  --clean `
  --windowed `
  --name "DriedFruitLedger" `
  --add-data "DRIED_FRUIT_LEDGER_MANUAL.md;." `
  --hidden-import "tkinter" `
  --hidden-import "sqlite3" `
  "dried_fruit_ledger.py"

Write-Host ""
Write-Host "Build complete."
Write-Host "Windows executable folder: dist\DriedFruitLedger\"
Write-Host "Creating ZIP package..."
$zipPath = "dist\DriedFruitLedger-Windows.zip"
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }
Compress-Archive -Path "dist\DriedFruitLedger" -DestinationPath $zipPath -Force
Write-Host "Windows ZIP package: $zipPath"
