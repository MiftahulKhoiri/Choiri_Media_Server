"""
cms_bash_folder.py
Manajemen folder aplikasi BMS
Mengikuti hasil detect() custom
"""

import os
from core.cms_detect_os import detect


# ============================================================
# DETEKSI BASE FOLDER CMS
# ============================================================

def detect_cms_base():
    # --------------------------------------------------------
    # 0. ENV OVERRIDE (PALING PRIORITAS)
    # --------------------------------------------------------
    env_base = os.environ.get("CMS_BASE")
    if env_base:
        return os.path.abspath(env_base)

    # --------------------------------------------------------
    # 1. DETEKSI OS
    # --------------------------------------------------------
    system = detect()
    home = os.path.expanduser("~")

    # --------------------------------------------------------
    # 2. TERMUX (KHUSUS)
    # --------------------------------------------------------
    if system == "Linux Termux":
        return os.path.join(
            home, "storage", "downloads", "BMS"
        )

    # --------------------------------------------------------
    # 3. SEMUA OS LAIN (STANDAR)
    # --------------------------------------------------------
    # Linux PC, Linux Raspberry Pi, Windows, macOS
    return os.path.join(home, "BMS")


# ============================================================
# BASE PATH UTAMA
# ============================================================

BASE = detect_cms_base()


# ============================================================
# DEFINISI FOLDER APLIKASI
# ============================================================

DB_FOLDER        = os.path.join(BASE, "database")
LOG_FOLDER       = os.path.join(BASE, "logs")
PICTURES_FOLDER  = os.path.join(BASE, "pictures")
MUSIC_FOLDER     = os.path.join(BASE, "music")
VIDEO_FOLDER     = os.path.join(BASE, "video")
UPLOAD_FOLDER    = os.path.join(BASE, "upload")

DB_PATH  = os.path.join(DB_FOLDER, "users.db")
LOG_PATH = os.path.join(LOG_FOLDER, "system.log")


# ============================================================
# AUTO CREATE FOLDER (IDEMPOTENT)
# ============================================================

def ensure_app_folders():
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


# ============================================================
# AUTO INIT SAAT IMPORT (OPSIONAL)
# ============================================================

ensure_app_folders()