# Folder utama cms_bash_folder

import os
from cms_detect_os import detect


def detect_cms_base():
    # ========================================================
    # 0. ENV OVERRIDE (PALING PRIORITAS)
    # ========================================================
    env_base = os.environ.get("CMS_BASE")
    if env_base:
        return os.path.abspath(env_base)

    # ========================================================
    # 1. DETEKSI OS
    # ========================================================
    system = detect()
    home = os.path.expanduser("~")

    # ========================================================
    # 2. TERMUX
    # ========================================================
    if system == "linux Termux":
        return os.path.join(
            home, "storage", "downloads", "BMS"
        )

    # ========================================================
    # 3. WINDOWS
    # ========================================================
    if system == "windows":
        return os.path.join(home, "BMS")

    # ========================================================
    # 4. macOS
    # ========================================================
    if system == "darwin":
        return os.path.join(home, "BMS")

    # ========================================================
    # 5. LINUX (Raspberry Pi / Desktop / Server)
    # ========================================================
    if system.startswith("linux" or "linux raspabery pi"):
        return os.path.join(home, "BMS")

    # ========================================================
    # 6. FALLBACK TERAKHIR (SANGAT JARANG TERPAKAI)
    # ========================================================
    return os.path.abspath(
        os.path.join(os.getcwd(), "BMS")
    )


# ============================================================
# BASE PATH UTAMA
# ============================================================
BASE = detect_cms_base()


# ============================================================
# DEFINISI FOLDER APLIKASI
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
for folder in (
    BASE,
    DB_FOLDER,
    LOG_FOLDER,
    PICTURES_FOLDER,
    MUSIC_FOLDER,
    VIDEO_FOLDER,
    UPLOAD_FOLDER,
):
    os.makedirs(folder, exist_ok=True)