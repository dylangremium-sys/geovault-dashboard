#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

PYTHON_BIN="${PYTHON_BIN:-python3}"
APP_NAME="${APP_NAME:-DriedFruitLedger}"
ENTRYPOINT="${ENTRYPOINT:-dried_fruit_ledger.py}"
DIST_DIR="${DIST_DIR:-dist}"
BUILD_DIR="${BUILD_DIR:-build}"

echo "==> Using Python: ${PYTHON_BIN}"
echo "==> Project root: ${PROJECT_ROOT}"

OS_NAME="$(uname -s)"
if [[ "${OS_NAME}" != "Darwin" ]]; then
  echo "ERROR: macOS build script must run on macOS (Darwin). Current OS: ${OS_NAME}."
  exit 1
fi

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "ERROR: Python binary '${PYTHON_BIN}' not found."
  exit 1
fi

if [[ ! -f "${ENTRYPOINT}" ]]; then
  echo "ERROR: Entry file '${ENTRYPOINT}' not found in ${PROJECT_ROOT}."
  exit 1
fi

if ! "${PYTHON_BIN}" - <<'PY' >/dev/null 2>&1
import tkinter
PY
then
  echo "ERROR: Tkinter is unavailable in '${PYTHON_BIN}'. Install a Python build with Tk support."
  exit 1
fi

echo "==> Installing/refreshing build tools"
"${PYTHON_BIN}" -m pip install --upgrade pip pyinstaller

echo "==> Cleaning previous build output"
rm -rf "${DIST_DIR}" "${BUILD_DIR}" "${APP_NAME}.spec"

echo "==> Building macOS app bundle"
"${PYTHON_BIN}" -m PyInstaller \
  --noconfirm \
  --clean \
  --windowed \
  --name "${APP_NAME}" \
  --add-data "DRIED_FRUIT_LEDGER_MANUAL.md:." \
  "${ENTRYPOINT}"

APP_BUNDLE="${DIST_DIR}/${APP_NAME}.app"
ZIP_OUTPUT="${DIST_DIR}/${APP_NAME}-macOS.zip"

if [[ -d "${APP_BUNDLE}" ]]; then
  echo "==> Creating distributable ZIP"
  ditto -c -k --sequesterRsrc --keepParent "${APP_BUNDLE}" "${ZIP_OUTPUT}"
  echo "Done."
  echo "App bundle: ${APP_BUNDLE}"
  echo "ZIP package: ${ZIP_OUTPUT}"
else
  echo "ERROR: Build finished but app bundle was not created."
  exit 1
fi
