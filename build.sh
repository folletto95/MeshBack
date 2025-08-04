#!/usr/bin/env bash
# Build standalone executables for Linux and Windows using PyInstaller.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP="backup_restore.py"
DIST_DIR="$SCRIPT_DIR/dist"

# Ensure dependencies exist
if ! command -v pyinstaller >/dev/null 2>&1; then
  echo "pyinstaller is required. Install with: pip install pyinstaller" >&2
  exit 1
fi

mkdir -p "$DIST_DIR"

# Build native executable
pyinstaller --onefile "$SCRIPT_DIR/$APP" \
  --distpath "$DIST_DIR/linux" \
  --workpath "$SCRIPT_DIR/build/linux" \
  --name meshback

# Build Windows executable via wine if available
if command -v wine >/dev/null 2>&1; then
  wine pyinstaller --onefile "$SCRIPT_DIR/$APP" \
    --distpath "$DIST_DIR/windows" \
    --workpath "$SCRIPT_DIR/build/windows" \
    --name meshback
else
  echo "wine not found; skipping Windows build" >&2
fi
