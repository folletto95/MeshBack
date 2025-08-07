# MeshBack

Utility to backup and restore Meshtastic device configuration and build
standalone executables for each platform.

## Building executables

Run the provided script on a Linux host. It sets up a Python virtual
environment, builds the native binary with PyInstaller and cross-compiles a
Windows `.exe` via Nuitka using the mingw-w64 toolchain—no Windows Python
download required:

```bash
./start_compile.sh
```

The resulting binaries are placed under `dist/` as `meshback` (Linux) and
`meshback.exe` (Windows).

## Usage

Once built, launch the `meshback` executable. The GUI allows you to:

- View available serial ports and connect/disconnect
- Backup the connected device (files are stored under a folder named after the
  node as `<node>/<node>_<fw>_<timestamp>.bin`)
- Restore from a previously saved backup

