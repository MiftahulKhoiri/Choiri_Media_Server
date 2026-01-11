"""
cms_bootstrap.py
Bootstrap / inisialisasi sistem CMS
(Menggunakan logger & custom error)
"""

import os

from core.cms_logger import get_logger
from core.cms_errors import (
    CMSBootstrapError,
    CMSDependencyError,
    CMSVirtualEnvError,
    CMSPermissionError,
)

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
# LOGGER
# =====================================================

log = get_logger("CMS_BOOTSTRAP")


# =====================================================
# BOOTSTRAP SEQUENCE
# =====================================================

def bootstrap_system(
    ensure_git: bool = True,
    ensure_venv: bool = True,
    install_requirements: bool = True,
):
    """
    Menjalankan inisialisasi sistem CMS secara lengkap
    """

    log.info("=" * 60)
    log.info(" CMS SYSTEM BOOTSTRAP ")
    log.info("=" * 60)

    try:
        # -------------------------------------------------
        # 1️⃣ Deteksi OS
        # -------------------------------------------------
        os_info = detect()
        log.info(f"[OS] {os_info}")

        # -------------------------------------------------
        # 2️⃣ Permission check (non-Termux)
        # -------------------------------------------------
        if os_info != "Linux Termux" and os.geteuid() != 0:
            raise CMSPermissionError(
                "Bootstrap di Linux non-Termux harus dijalankan sebagai root (sudo)"
            )

        # -------------------------------------------------
        # 3️⃣ Setup folder system (core)
        # -------------------------------------------------
        ensure_directories()
        log.info("[OK] Folder system siap")

        # -------------------------------------------------
        # 4️⃣ Setup folder aplikasi (BMS)
        # -------------------------------------------------
        ensure_app_folders()
        log.info("[OK] Folder aplikasi siap")

        # -------------------------------------------------
        # 5️⃣ Pastikan Git
        # -------------------------------------------------
        if ensure_git:
            log.info("[STEP] Cek / Update Git")
            git_result = GitAutoUpdater().update()

            if git_result.get("updated"):
                log.info(
                    f"[OK] Git diupdate → {git_result.get('new_version')}"
                )
            else:
                log.info("[OK] Git sudah versi terbaru")

        # -------------------------------------------------
        # 6️⃣ Virtual Environment
        # -------------------------------------------------
        if ensure_venv:
            log.info("[STEP] Virtual Environment")
            venv = VirtualVenv(VENV_DIR)
            venv.create_venv()
            log.info("[OK] Virtualenv siap")

        # -------------------------------------------------
        # 7️⃣ Install requirements
        # -------------------------------------------------
        if install_requirements:
            if REQUIREMENTS_FILE.exists():
                log.info("[STEP] Install requirements.txt")
                installer = RequirementsInstaller(
                    python_bin=str(VENV_PYTHON)
                )
                installer.install_requirements(
                    str(REQUIREMENTS_FILE)
                )
                log.info("[OK] Requirements terpenuhi")
            else:
                log.warning(
                    "[SKIP] requirements.txt tidak ditemukan"
                )

        log.info("[DONE] Bootstrap selesai")

    except CMSPermissionError:
        log.exception("Permission error saat bootstrap")
        raise

    except CMSVirtualEnvError:
        log.exception("Virtual environment error")
        raise

    except CMSDependencyError:
        log.exception("Dependency error")
        raise

    except Exception as e:
        log.exception("Bootstrap gagal")
        raise CMSBootstrapError(str(e)) from e


# =====================================================
# ENTRY POINT (OPSIONAL)
# =====================================================

if __name__ == "__main__":
    bootstrap_system()