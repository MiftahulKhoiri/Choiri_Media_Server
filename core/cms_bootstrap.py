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

from core.cms_detect_os import detect_os
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
    os_info = detect_os()
    print(f"[OS] {os_info}")

    # 2️⃣ Setup folder
    ensure_directories()
    print("[OK] Folder system siap")

    # 3️⃣ Pastikan Git
    if ensure_git:
        print("[STEP] Cek Git")
        GitAutoUpdater().update()

    # 4️⃣ Virtual Environment
    if ensure_venv:
        print("[STEP] Virtual Environment")
        venv = VirtualVenv(VENV_DIR)
        venv.create_venv()

    # 5️⃣ Install requirements
    if install_requirements and REQUIREMENTS_FILE.exists():
        print("[STEP] Install requirements")
        installer = RequirementsInstaller(
            python_bin=str(VENV_PYTHON)
        )
        installer.install_requirements(str(REQUIREMENTS_FILE))

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