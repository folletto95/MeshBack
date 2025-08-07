#!/usr/bin/env bash

# Compile native Linux and Windows executables without downloading Windows Python.

set -e

# Install system dependencies
sudo apt-get update

sudo apt-get install -y python3-venv mingw-w64

# Create and activate virtual environment

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

pip install pyinstaller nuitka

# Build Linux executable with PyInstaller
pyinstaller --onefile -n meshback meshback.py

# Cross-compile Windows executable using Nuitka + mingw
python -m nuitka \
  --mingw64 \
  --onefile \
  --enable-plugin=tk-inter \
  --output-dir=dist \
  --output-filename=meshback.exe \
  meshback.py

deactivate

echo "Executables stored in dist/: meshback (Linux) and meshback.exe (Windows)"
