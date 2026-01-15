#!/usr/bin/env python3
"""
cms.py
Script utama untuk menjalankan CMS
"""

import os
import sys
import subprocess
from pathlib import Path

# =====================================================
# PATH DASAR
# =====================================================

BASE_DIR = Path(__file__).resolve().parent
CORE_DIR = BASE_DIR / "core"
APP_DIR = BASE_DIR / "app"

sys.path.insert(0, str(BASE_DIR))

# =====================================================
# IMPORT CORE
# =====================================================

from core.cms_detect_os import detect
from core.cms_logger import get_logger
from core.cms_paths import VENV_DIR, VENV_PYTHON
from core.cms_virtual_ven import VirtualVenv
from core.cms_update_git.py import SelfUpdater
from core.cms_requirements_installer import RequirementsInstaller

# =====================================================
# LOGGER
# =====================================================

log = get_logger("CMS_MAIN")


# =====================================================
# UTIL
# =====================================================

def restart_self():
    """
    Restart cms.py (dipakai setelah update Git)
    """
    log.info("Restart CMS setelah update Git")
    os.execv(sys.executable, [sys.executable] + sys.argv)


def run(cmd, env=None):
    log.info(f"RUN: {' '.join(cmd)}")
    subprocess.run(cmd, env=env, check=True)


# =====================================================
# MAIN FLOW
# =====================================================

def main():
    log.info("=" * 60)
    log.info(" CMS START ")
    log.info("=" * 60)

    # -------------------------------------------------
    # 1️⃣ Cek sistem
    # -------------------------------------------------
    os_info = detect()
    log.info(f"OS Detected: {os_info}")

    # -------------------------------------------------
    # 2️⃣ Cek / Buat Virtualenv
    # -------------------------------------------------
    venv = VirtualVenv(VENV_DIR)
    venv.create_venv()

    if not VENV_PYTHON.exists():
        log.error("Python virtualenv tidak ditemukan")
        sys.exit(1)

    # -------------------------------------------------
    # 3️⃣ Update Git
    # -------------------------------------------------
    updater = SelfUpdater(BASE_DIR)

if updater.update_if_needed():
    log.info("Restart CMS untuk pakai kode terbaru")
    os.execv(sys.executable, [sys.executable] + sys.argv)

    # -------------------------------------------------
    # 4️⃣ Install requirements.txt
    # -------------------------------------------------
    req_file = BASE_DIR / "requirements.txt"
    if req_file.exists():
        installer = RequirementsInstaller(
            python_bin=str(VENV_PYTHON)
        )
        installer.install_requirements(req_file)
    else:
        log.warning("requirements.txt tidak ditemukan (skip)")

    # -------------------------------------------------
    # 5️⃣ Jalankan Flask app
    # -------------------------------------------------
    main_app = APP_DIR / "main.py"
    if not main_app.exists():
        log.error("app/main.py tidak ditemukan")
        sys.exit(1)

    log.info("Menjalankan Web Server Flask")

    env = os.environ.copy()

    # 🔑 INI KUNCI UTAMA (FIX ERROR core)
    env["PYTHONPATH"] = str(BASE_DIR)

    # virtualenv context
    env["VIRTUAL_ENV"] = str(VENV_DIR)
    env["PATH"] = (
        str(VENV_PYTHON.parent)
        + os.pathsep
        + env.get("PATH", "")
    )

    run(
        [str(VENV_PYTHON), str(main_app)],
        env=env
    )


# =====================================================
# ENTRY POINT
# =====================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.info("CMS dihentikan oleh user")