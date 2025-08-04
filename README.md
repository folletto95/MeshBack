# MeshBack

Utility to backup and restore Meshtastic device configuration and build
standalone executables for multiple platforms.

## Building executables

Install dependencies and run the build script:

```bash
pip install meshtastic pyinstaller
./build.sh
```

The resulting binaries will be placed under `dist/linux` and
`dist/windows` (the latter requires `wine`).

## Usage

Once built, run the executable with:

```bash
./meshback backup /dev/ttyUSB0 config.bin
./meshback restore /dev/ttyUSB0 config.bin
```

Replace the serial port and file paths as needed.
