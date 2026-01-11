"""
cms_config.py
Manajemen konfigurasi global CMS
"""

import os
from pathlib import Path

from core.cms_paths import BASE_DIR
from core.cms_logger import get_logger
from core.cms_errors import CMSConfigError

# =====================================================
# LOGGER
# =====================================================

log = get_logger("CMS_CONFIG")

# =====================================================
# DEFAULT CONFIG
# =====================================================

DEFAULT_CONFIG = {
    "CMS_ENV": "PROD",          # DEV | PROD
    "CMS_DEBUG": "0",           # 1 = debug
    "CMS_NAME": "CMS_SYSTEM",
    "CMS_VERSION": "1.0.0",
    "CMS_TIMEZONE": "Asia/Jakarta",
}

# =====================================================
# INTERNAL STORAGE
# =====================================================

_config = {}
_loaded = False


# =====================================================
# ENV FILE LOADER
# =====================================================

def _load_env_file(env_path: Path):
    """
    Load file .env secara manual (tanpa dependency)
    """
    if not env_path.exists():
        log.debug(".env tidak ditemukan (skip)")
        return

    log.info(f"Load env file: {env_path}")

    for line in env_path.read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(
            key.strip(),
            value.strip().strip('"').strip("'"),
        )


# =====================================================
# LOAD CONFIG (PUBLIC API)
# =====================================================

def load_config(env_file: str = ".env") -> dict:
    """
    Load konfigurasi CMS (idempotent)
    """
    global _loaded, _config

    if _loaded:
        return _config

    env_path = Path(env_file)
    if not env_path.is_absolute():
        env_path = BASE_DIR / env_path

    _load_env_file(env_path)

    # Merge default + env
    config = DEFAULT_CONFIG.copy()
    for key in config:
        config[key] = os.environ.get(
            key, config[key]
        )

    # Validasi ENV
    if config["CMS_ENV"] not in ("DEV", "PROD"):
        raise CMSConfigError(
            "CMS_ENV harus DEV atau PROD"
        )

    _config = config
    _loaded = True

    log.info(
        f"Config loaded (ENV={config['CMS_ENV']}, DEBUG={config['CMS_DEBUG']})"
    )

    return _config


# =====================================================
# GETTER API
# =====================================================

def get(key: str, default=None):
    """
    Ambil nilai config
    """
    if not _loaded:
        load_config()
    return _config.get(key, default)


def is_debug() -> bool:
    return get("CMS_DEBUG") == "1"


def is_dev() -> bool:
    return get("CMS_ENV") == "DEV"


def is_prod() -> bool:
    return get("CMS_ENV") == "PROD"