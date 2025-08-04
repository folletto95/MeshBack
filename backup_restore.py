#!/usr/bin/env python3
"""Utility to backup and restore Meshtastic device configuration.

This module exposes a small CLI that talks to a Meshtastic device via
`meshtastic.serial_interface.SerialInterface` and serializes the
configuration to a binary file.  It is intentionally minimal so it can
be bundled with PyInstaller for distribution as a standalone executable
on multiple platforms.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from meshtastic.serial_interface import SerialInterface
from meshtastic.protobuf import config_pb2


def backup(device_port: str, output_file: Path) -> None:
    """Read configuration from *device_port* and write it to *output_file*."""
    iface = SerialInterface(device_port)
    try:
        config = iface.getConfig()
        with output_file.open("wb") as fh:
            fh.write(config.SerializeToString())
    finally:
        iface.close()


def restore(device_port: str, input_file: Path) -> None:
    """Write configuration from *input_file* to *device_port*."""
    data = input_file.read_bytes()
    config = config_pb2.Config()
    config.ParseFromString(data)

    iface = SerialInterface(device_port)
    try:
        iface.writeConfig(config)
    finally:
        iface.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Backup or restore a Meshtastic device")
    parser.add_argument("action", choices=["backup", "restore"], help="Operation to perform")
    parser.add_argument("port", help="Serial port of the device, e.g. /dev/ttyUSB0 or COM3")
    parser.add_argument("file", type=Path, help="File to read from or write to")

    args = parser.parse_args()

    if args.action == "backup":
        backup(args.port, args.file)
    else:
        restore(args.port, args.file)


if __name__ == "__main__":
    main()
