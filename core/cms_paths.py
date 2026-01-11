"""
cms_paths.py
Manajemen path global CMS (Single Source of Truth)
"""

import os
from pathlib import Path


# =====================================================
# ENV DETECTION
# =====================================================

def is_termux():
    return os.environ.get("PREFIX", "").startswith("/data/data/com.termux")


# =====================================================
# BASE DIRECTORIES
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if is_termux():
    SYSTEM_PREFIX = Path(os.environ["PREFIX"])
    BASE_DIR = SYSTEM_PREFIX / "share" / "cms_system"
else:
    SYSTEM_PREFIX = Path("/usr/local")
    BASE_DIR = SYSTEM_PREFIX / "cms_system"

# =====================================================
# CORE PATHS
# =====================================================

CORE_DIR = PROJECT_ROOT / "core"
ENV_DIR = BASE_DIR / "env"
BIN_DIR = BASE_DIR / "bin"
LOG_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data"
TMP_DIR = BASE_DIR / "tmp"

# =====================================================
# VIRTUAL ENV
# =====================================================

VENV_DIR = ENV_DIR / "venv"
VENV_BIN = VENV_DIR / ("Scripts" if os.name == "nt" else "bin")
VENV_PYTHON = VENV_BIN / ("python.exe" if os.name == "nt" else "python")

# =====================================================
# FILE PATHS
# =====================================================

REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"

# =====================================================
# HELPERS
# =====================================================

def ensure_directories():
    """
    Membuat semua folder inti jika belum ada
    Idempotent (aman dipanggil berulang)
    """
    for path in [
        BASE_DIR,
        ENV_DIR,
        BIN_DIR,
        LOG_DIR,
        DATA_DIR,
        TMP_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)