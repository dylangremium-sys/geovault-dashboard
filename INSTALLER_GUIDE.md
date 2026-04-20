# Dried Fruit Ledger - Installer Guide

This guide explains how to package the app into distributable binaries.

## What gets built

- **macOS**: `.app` bundle + `.zip` in `dist/`
- **Windows**: one-folder app bundle + `.zip` in `dist\`

The app uses local files only:

- `ledger.db` (SQLite backend)
- `ledger_data.csv` (exported snapshot)

No internet connection is required for runtime.

---

## 1) macOS build

Run from project root:

```bash
bash scripts/build-macos.sh
```

Build outputs:

- `dist/DriedFruitLedger.app`
- `dist/DriedFruitLedger-macOS.zip`

If macOS blocks launch on another machine:

1. Right-click app -> Open (first run)
2. Or sign/notarize in your Apple Developer workflow for frictionless distribution.

---

## 2) Windows build

### Option A: Command Prompt

```bat
scripts\build-windows.bat
```

### Option B: PowerShell

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-windows.ps1
```

Build outputs:

- `dist\DriedFruitLedger\` (folder bundle)
- `dist\DriedFruitLedger-Windows.zip`

---

## 3) Build prerequisites

- Python 3.11+
- Tkinter available in your Python install
- `pip` available

Packaging dependency is installed by scripts:

- `pyinstaller` (from `scripts/requirements-packaging.txt`)

---

## 4) Distribution checklist

1. Build on target OS (Mac build on Mac, Windows build on Windows).
2. Open packaged app once locally and test:
   - Process order
   - Save product (Code/SKU/Weight)
   - Weekly report
   - CSV export
3. Share zipped artifact from `dist/`.

---

## 5) Notes

- Backend database (`ledger.db`) is created at first launch in app working directory.
- Export snapshot (`ledger_data.csv`) is generated after order save and via Export button.
- If you need a single-file EXE on Windows, change `--onedir` to `--onefile` in scripts (startup may be slower).

