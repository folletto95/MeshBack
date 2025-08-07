# MeshBack

Utility to backup and restore Meshtastic device configuration and build
standalone executables for each platform.

## Building executables


Run the provided script on a Linux host. It installs the required packages,
builds the native binary and cross-compiles a Windows `.exe` using Wine:

```bash
./start_compile.sh
```

The resulting binaries are placed under `dist/` as `backup_restore` (Linux) and
`backup_restore.exe` (Windows).

## Usage

Once built, launch the executable. The GUI allows you to:

- View available serial ports and connect/disconnect
- Backup the connected device (files are stored under a folder named after the
  node as `<node>/<node>_<fw>_<timestamp>.bin`)
- Restore from a previously saved backup
