import os
from cms_detect_os import detect


# ============================================================
# Fungsi untuk menentukan BASE folder aplikasi CMS 
# ============================================================
def detect_cms_base():

    # --------------------------------------------------------
    # 0. ENV OVERRIDE (PALING PRIORITAS)
    # --------------------------------------------------------
    # Cek apakah ada environment variable bernama CMS_BASE
    # Kalau ADA → kita pakai ini, tidak peduli OS apa pun
    #
    # Contoh:
    # export CMS_BASE=/sdcard/BMS
    #
    env_base = os.environ.get("CMS_BASE")

    if env_base:
        # os.path.abspath() memastikan path jadi absolut
        # supaya aman dipakai di mana pun
        return os.path.abspath(env_base)

    # --------------------------------------------------------
    # 1. DETEKSI OS / ENVIRONMENT
    # --------------------------------------------------------
    # detect() mengembalikan string:
    # "termux", "windows", "linux", "darwin"
    #
    system = detect()

    # --------------------------------------------------------
    # 2. TERMUX
    # --------------------------------------------------------
    # Jika dijalankan di Android lewat Termux
    if system == "termux":
        return "/data/data/com.termux/files/home/storage/downloads/BMS"

    # --------------------------------------------------------
    # 3. WINDOWS
    # --------------------------------------------------------
    # Folder cmS akan dibuat di HOME user
    if system == "windows":
        return os.path.join(os.path.expanduser("~"), "BMS")

    # --------------------------------------------------------
    # 4. macOS
    # --------------------------------------------------------
    # Sama seperti Windows, pakai HOME user
    if system == "darwin":
        return os.path.join(os.path.expanduser("~"), "BMS")

    # --------------------------------------------------------
    # 5. LINUX / SERVER
    # --------------------------------------------------------
    # Default fallback:
    # ambil folder project (1 level di atas file ini)
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )


# ============================================================
# BASE PATH UTAMA APLIKASI
# ============================================================
# Semua folder lain akan mengikuti BASE ini
BASE = detect_cms_base()


# ============================================================
# DEFINISI FOLDER-FOLDER APLIKASI
# ============================================================
DB_FOLDER        = os.path.join(BASE, "database")   # database
LOG_FOLDER       = os.path.join(BASE, "logs")       # log sistem
PICTURES_FOLDER  = os.path.join(BASE, "Pictures")   # gambar
MUSIC_FOLDER     = os.path.join(BASE, "music")      # musik
VIDEO_FOLDER     = os.path.join(BASE, "video")      # video
UPLOAD_FOLDER    = os.path.join(BASE, "upload")     # upload file

# File penting
DB_PATH  = os.path.join(DB_FOLDER, "users.db")
LOG_PATH = os.path.join(LOG_FOLDER, "system.log")


# ============================================================
# BUAT FOLDER OTOMATIS JIKA BELUM ADA
# ============================================================
# Loop semua folder → buat kalau belum ada
for folder in [
    BASE,
    DB_FOLDER,
    LOG_FOLDER,
    PICTURES_FOLDER,
    MUSIC_FOLDER,
    VIDEO_FOLDER,
    UPLOAD_FOLDER
]:
    os.makedirs(folder, exist_ok=True)