"""
cms_logger.py
Logger terpusat untuk CMS
"""

import logging
import sys
from pathlib import Path

from core.cms_paths import LOG_DIR


# =====================================================
# KONFIGURASI DASAR
# =====================================================

LOG_NAME = "CMS"
LOG_FILE = LOG_DIR / "cms.log"

LOG_LEVEL = logging.INFO
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# =====================================================
# INITIALIZE LOGGER (SINGLETON)
# =====================================================

_logger = None


def get_logger(name: str = LOG_NAME) -> logging.Logger:
    """
    Mengembalikan instance logger CMS (singleton).
    """
    global _logger

    if _logger:
        return _logger

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    logger.propagate = False

    # Hindari double handler
    if logger.handlers:
        return logger

    # ---- Console Handler ----
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

    # ---- File Handler ----
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    _logger = logger
    return logger