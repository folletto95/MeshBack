# MeshBack

Utility to backup and restore Meshtastic device configuration and build
standalone executables for each platform.

## Building executables

Install dependencies and run the build script on the target platform:

```bash
pip install meshtastic pyinstaller
./build.sh
```

The resulting binary for the host OS will be placed under `dist/`.

## Usage

Once built, launch the executable. The GUI allows you to:

- View available serial ports and connect/disconnect
- Backup the connected device (files are stored under a folder named after the
  node as `<node>/<node>_<fw>_<timestamp>.bin`)
- Restore from a previously saved backup
