@echo off
setlocal ENABLEDELAYEDEXPANSION

REM Build Windows distributable with PyInstaller.
REM Run this on a Windows machine with Python installed.

echo [1/4] Validating Python...
python --version >nul 2>&1
if errorlevel 1 (
  echo ERROR: Python not found in PATH.
  exit /b 1
)

echo [2/4] Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 exit /b 1

echo [3/4] Installing packaging dependencies...
python -m pip install -r scripts\requirements-packaging.txt
if errorlevel 1 exit /b 1

echo [4/4] Building executable...
python -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --onedir ^
  --windowed ^
  --name "DriedFruitLedger" ^
  --add-data "DRIED_FRUIT_LEDGER_MANUAL.md;." ^
  --hidden-import "tkinter" ^
  --hidden-import "sqlite3" ^
  dried_fruit_ledger.py
if errorlevel 1 exit /b 1

if exist dist\DriedFruitLedger-Windows.zip del /f /q dist\DriedFruitLedger-Windows.zip
powershell -NoProfile -Command "Compress-Archive -Path 'dist\DriedFruitLedger' -DestinationPath 'dist\DriedFruitLedger-Windows.zip' -Force"
if errorlevel 1 exit /b 1

echo.
echo Build complete.
echo App folder: dist\DriedFruitLedger
echo ZIP package: dist\DriedFruitLedger-Windows.zip
echo Include these files in the same folder when sharing:
echo - dist\DriedFruitLedger\DriedFruitLedger.exe
echo - dist\DriedFruitLedger\ledger.db  (generated on first run)
echo - dist\DriedFruitLedger\ledger_data.csv (exported by app)
echo - dist\DriedFruitLedger\DRIED_FRUIT_LEDGER_MANUAL.md
echo.
echo Optional single-file build:
echo python -m PyInstaller --noconfirm --clean --onefile --windowed --name "DriedFruitLedger" dried_fruit_ledger.py

endlocal
