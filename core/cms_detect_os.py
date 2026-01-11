"""
cms_detect_os.py
Modul pendeteksi OS dan environment lintas platform.
Single Source of Truth untuk seluruh CMS.
"""

import os
import platform


def detect() -> str:
    """
    Mengembalikan string OS/environment terstandarisasi.
    """

    system = platform.system().lower()
    machine = platform.machine().lower()
    processor = platform.processor().lower()

    # ===============================
    # WINDOWS
    # ===============================
    if system == "windows":
        return "Windows"

    # ===============================
    # MACOS
    # ===============================
    if system == "darwin":
        return "macOS"

    # ===============================
    # LINUX FAMILY
    # ===============================
    if system == "linux":

        # ---- TERMUX ----
        prefix = os.environ.get("PREFIX", "")
        if "com.termux" in prefix:
            return "Linux Termux"

        # ---- RASPBERRY PI ----
        try:
            with open("/proc/cpuinfo", "r") as f:
                cpuinfo = f.read().lower()
                if "raspberry pi" in cpuinfo or "bcm270" in cpuinfo or "bcm271" in cpuinfo:
                    return "Linux RaspberryPi"
        except Exception:
            pass

        # ---- AMD PC ----
        if "amd" in processor or "amd" in machine:
            return "Linux AMD"

        # ---- GENERIC LINUX ----
        return "Linux Generic"

    # ===============================
    # UNKNOWN
    # ===============================
    return "Unknown"


def detect_detail() -> dict:
    """
    Mengembalikan detail OS dalam bentuk dictionary.
    Aman untuk logging / JSON.
    """

    return {
        "os_result": detect(),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
    }