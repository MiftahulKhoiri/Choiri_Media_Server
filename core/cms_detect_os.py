"""
cms_detec_os.py
Modul pendeteksi OS dan environment lintas platform.
Kompatibel: Termux, Raspberry Pi, Linux PC, Windows, macOS, dll.
"""

import os
import platform


def detect_os() -> str:
    """
    Mengembalikan string deskripsi OS/environment.
    """

    system = platform.system().lower()
    machine = platform.machine().lower()
    processor = platform.processor().lower()

    # ===============================
    # WINDOWS
    # ===============================
    if system == "windows":
        return "linux windows"

    # ===============================
    # LINUX FAMILY
    # ===============================
    if system == "linux":

        # ---- TERMUX ----
        # Termux selalu punya PREFIX dengan path com.termux
        prefix = os.environ.get("PREFIX", "")
        if "com.termux" in prefix:
            return "linux Termux"

        # ---- RASPBERRY PI ----
        try:
            with open("/proc/cpuinfo", "r") as f:
                cpuinfo = f.read().lower()
                if "raspberry pi" in cpuinfo or "bcm" in cpuinfo:
                    return "linux raspabery pi"
        except Exception:
            pass

        # ---- AMD PC ----
        if "amd" in processor or "amd" in machine:
            return "linux AMD"

        # ---- GENERIC LINUX ----
        return "linux generic"

    # ===============================
    # MACOS
    # ===============================
    if system == "darwin":
        return "macos"

    # ===============================
    # UNKNOWN
    # ===============================
    return f"unknown os ({system})"


def detect_detail() -> dict:
    """
    Mengembalikan detail OS dalam bentuk dictionary.
    Cocok untuk logging atau JSON.
    """

    return {
        "os_result": detect_os(),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
    }