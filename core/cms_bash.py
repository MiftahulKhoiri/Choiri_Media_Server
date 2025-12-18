import os
from cms_detect_os import detect

# ============================================================
# Deteksi BASE Folder
# ============================================================
def detect_cms_base():
    system = detect()

    # 1. TERMUX
    if system == "termux":
        return "/data/data/com.termux/files/home/storage/downloads/BMS"

    # 2. ANDROID (non-Termux)
    android_paths = [
        "/storage/emulated/0/Download/BMS",
        "/sdcard/Download/BMS"
    ]
    for p in android_paths:
        if os.path.exists(p):
            return p

    # 3. WINDOWS
    if system == "windows":
        return os.path.join(os.path.expanduser("~"), "BMS")

    # 4. macOS
    if system == "darwin":
        return os.path.join(os.path.expanduser("~"), "BMS")

    # 5. LINUX / SERVER
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )


# ============================================================
# BASE PATH
# ============================================================
BASE = detect_cms_base()


# ============================================================
# FOLDER DEFINISI
# ============================================================
DB_FOLDER        = os.path.join(BASE, "database")
LOG_FOLDER       = os.path.join(BASE, "logs")
PICTURES_FOLDER  = os.path.join(BASE, "Pictures")
MUSIC_FOLDER     = os.path.join(BASE, "music")
VIDEO_FOLDER     = os.path.join(BASE, "video")
UPLOAD_FOLDER    = os.path.join(BASE, "upload")

DB_PATH  = os.path.join(DB_FOLDER, "users.db")
LOG_PATH = os.path.join(LOG_FOLDER, "system.log")


# ============================================================
# AUTO CREATE FOLDER
# ============================================================
for folder in [
    BASE, DB_FOLDER, LOG_FOLDER,
    PICTURES_FOLDER, MUSIC_FOLDER,
    VIDEO_FOLDER, UPLOAD_FOLDER
]:
    os.makedirs(folder, exist_ok=True)