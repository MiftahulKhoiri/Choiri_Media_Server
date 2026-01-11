"""
cms_bootstrap.py
Bootstrap / inisialisasi sistem CMS
"""

import os

from core.cms_paths import (
    ensure_directories,
    VENV_DIR,
    VENV_PYTHON,
    REQUIREMENTS_FILE,
)

from core.cms_detect_os import detect
from core.cms_bash_folder import ensure_app_folders
from core.cms_virtual_ven import VirtualVenv
from core.cms_requirements_installer import RequirementsInstaller
from core.cms_update_git import GitAutoUpdater


# =====================================================
# BOOTSTRAP SEQUENCE
# =====================================================

def bootstrap_system(
    ensure_git=True,
    ensure_venv=True,
    install_requirements=True,
):
    """
    Menjalankan inisialisasi sistem CMS secara lengkap
    """

    print("=" * 60)
    print(" CMS SYSTEM BOOTSTRAP ")
    print("=" * 60)

    # 1️⃣ Deteksi OS
    os_info = detect()
    print(f"[OS] {os_info}")

    # 2️⃣ Setup folder system (core)
    ensure_directories()
    print("[OK] Folder system siap")

    # 3️⃣ Setup folder aplikasi (BMS)
    ensure_app_folders()
    print("[OK] Folder aplikasi siap")

    # 4️⃣ Pastikan Git
    if ensure_git:
        print("[STEP] Cek / Update Git")
        git_result = GitAutoUpdater().update()
        if git_result.get("updated"):
            print(f"[OK] Git diupdate → {git_result.get('new_version')}")
        else:
            print("[OK] Git sudah versi terbaru")

    # 5️⃣ Virtual Environment
    if ensure_venv:
        print("[STEP] Virtual Environment")
        venv = VirtualVenv(VENV_DIR)
        venv.create_venv()
        print("[OK] Virtualenv siap")

    # 6️⃣ Install requirements
    if install_requirements:
        if REQUIREMENTS_FILE.exists():
            print("[STEP] Install requirements.txt")
            installer = RequirementsInstaller(
                python_bin=str(VENV_PYTHON)
            )
            installer.install_requirements(str(REQUIREMENTS_FILE))
            print("[OK] Requirements terpenuhi")
        else:
            print("[SKIP] requirements.txt tidak ditemukan")

    print("[DONE] Bootstrap selesai")


# =====================================================
# ENTRY POINT (OPSIONAL)
# =====================================================

if __name__ == "__main__":
    # Termux tidak butuh root
    if not os.environ.get("PREFIX") and os.geteuid() != 0:
        print("ERROR: Jalankan sebagai root (sudo)")
        raise SystemExit(1)

    bootstrap_system()