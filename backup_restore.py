#!/usr/bin/env python3
"""GUI utility to backup and restore Meshtastic device configuration."""

from __future__ import annotations

import datetime as _dt
import re
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import serial.tools.list_ports
from meshtastic.serial_interface import SerialInterface
from meshtastic.protobuf import admin_pb2, config_pb2


def _list_ports() -> list[str]:
    """Return available serial port device names."""
    return [p.device for p in serial.tools.list_ports.comports()]


def _fetch_firmware_version(iface: SerialInterface) -> str | None:
    """Query the device for firmware version using an admin request."""
    result: dict[str, str] = {}

    def _on_response(packet: dict) -> None:
        try:
            resp = packet["decoded"]["admin"]["raw"].get_device_metadata_response
            result["fw"] = resp.firmware_version
        except Exception:  # pragma: no cover - best effort only
            pass

    msg = admin_pb2.AdminMessage()
    msg.get_device_metadata_request = True
    iface.localNode._sendAdmin(msg, wantResponse=True, onResponse=_on_response)
    iface.waitForAckNak()
    return result.get("fw")


def _sanitize(text: str) -> str:
    return re.sub(r"\W+", "_", text)


def backup(iface: SerialInterface) -> Path:
    """Create a backup file and return its path."""
    node_name = iface.getLongName() or "node"
    fw = _fetch_firmware_version(iface) or "fw"
    timestamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = _sanitize(node_name)
    safe_fw = _sanitize(fw)
    filename = f"{safe_name}_{safe_fw}_{timestamp}.bin"

    node_dir = Path(safe_name)
    node_dir.mkdir(parents=True, exist_ok=True)

    config = iface.getConfig()
    path = node_dir / filename
    path.write_bytes(config.SerializeToString())
    return path


def restore(iface: SerialInterface, file_path: str | Path) -> None:
    """Restore configuration from *file_path* to *iface*."""
    data = Path(file_path).read_bytes()
    config = config_pb2.Config()
    config.ParseFromString(data)
    iface.writeConfig(config)


class App(tk.Tk):
    """Tkinter based UI for backing up and restoring devices."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Meshtastic Backup/Restore")
        self.iface: SerialInterface | None = None

        self.port_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Not connected")

        frm = ttk.Frame(self, padding=10)
        frm.grid()

        ttk.Label(frm, text="Serial Port:").grid(column=0, row=0, sticky="w")
        self.port_combo = ttk.Combobox(frm, textvariable=self.port_var, values=_list_ports(), width=25)
        self.port_combo.grid(column=1, row=0)
        ttk.Button(frm, text="Refresh", command=self.refresh_ports).grid(column=2, row=0)

        ttk.Button(frm, text="Connect", command=self.connect).grid(column=0, row=1)
        ttk.Button(frm, text="Disconnect", command=self.disconnect).grid(column=1, row=1)

        ttk.Button(frm, text="Backup", command=self.do_backup).grid(column=0, row=2, pady=(10, 0))
        ttk.Button(frm, text="Restore", command=self.do_restore).grid(column=1, row=2, pady=(10, 0))

        ttk.Label(frm, textvariable=self.status_var).grid(column=0, row=3, columnspan=3, sticky="w", pady=(10, 0))

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def refresh_ports(self) -> None:
        self.port_combo["values"] = _list_ports()

    def connect(self) -> None:
        port = self.port_var.get()
        if not port:
            messagebox.showerror("Error", "Select a serial port")
            return
        try:
            self.iface = SerialInterface(port)
            name = self.iface.getLongName() or "Unknown"
            fw = _fetch_firmware_version(self.iface) or "Unknown"
            self.status_var.set(f"Connected: {name} ({fw})")
        except Exception as exc:  # pragma: no cover - runtime failure
            self.iface = None
            messagebox.showerror("Error", str(exc))

    def disconnect(self) -> None:
        if self.iface:
            self.iface.close()
            self.iface = None
        self.status_var.set("Not connected")

    def do_backup(self) -> None:
        if not self.iface:
            messagebox.showerror("Error", "Not connected")
            return
        try:
            path = backup(self.iface)
            messagebox.showinfo("Backup", f"Saved to {path}")
        except Exception as exc:  # pragma: no cover - runtime failure
            messagebox.showerror("Error", str(exc))

    def do_restore(self) -> None:
        if not self.iface:
            messagebox.showerror("Error", "Not connected")
            return
        file = filedialog.askopenfilename(filetypes=[("Binary", "*.bin"), ("All files", "*")])
        if not file:
            return
        try:
            restore(self.iface, file)
            messagebox.showinfo("Restore", "Restore complete")
        except Exception as exc:  # pragma: no cover - runtime failure
            messagebox.showerror("Error", str(exc))

    def on_close(self) -> None:
        self.disconnect()
        self.destroy()


if __name__ == "__main__":
    App().mainloop()
