import platform
import os

def detect():
    system = platform.system().lower()
    if os.path.exists("/data/data/com.termux/files/usr"):
        return "termux"
    return system