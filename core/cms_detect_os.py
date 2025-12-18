import platform
import os

def detect():
    # Termux detection
    if os.path.exists("/data/data/com.termux/files/usr/bin"):
        return "termux"

    # OS umum
    return platform.system().lower()