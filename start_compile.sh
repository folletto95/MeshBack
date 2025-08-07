#!/usr/bin/env bash
# Compile native Linux binary and Windows .exe using Wine.
set -e

# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3-venv wine wget

# Build Linux executable
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

pyinstaller --onefile -n meshback meshback.py

deactivate

# Build Windows executable via Wine
PY_VERSION=3.11.6
PY_INSTALLER=python-${PY_VERSION}-amd64.exe
if [ ! -f "$PY_INSTALLER" ]; then
  wget https://www.python.org/ftp/python/${PY_VERSION}/${PY_INSTALLER}
fi
wine "$PY_INSTALLER" /quiet InstallAllUsers=1 PrependPath=1
wine pip install --upgrade pip
wine pip install meshtastic pyinstaller
WIN_SCRIPT=$(winepath -w "$(pwd)/meshback.py")
wine pyinstaller --onefile -n meshback "$WIN_SCRIPT"

echo "Executables stored in dist/: meshback (Linux) and meshback.exe (Windows)"

