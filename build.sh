#!/usr/bin/env bash
# Build a standalone executable for the host platform using PyInstaller.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP="$SCRIPT_DIR/backup_restore.py"
DIST_DIR="$SCRIPT_DIR/dist"

# Ensure dependencies exist
if ! command -v pyinstaller >/dev/null 2>&1; then
  echo "pyinstaller is required. Install with: pip install pyinstaller" >&2
  exit 1
fi

pyinstaller --onefile "$APP" \
  --distpath "$DIST_DIR" \
  --workpath "$SCRIPT_DIR/build" \
  --name meshback