"""
cms_virtual_ven.py
Manajemen Python Virtual Environment CMS
"""

import os
import sys
import subprocess
from pathlib import Path

from core.cms_logger import get_logger
from core.cms_errors import CMSVirtualEnvError

# =====================================================
# LOGGER
# =====================================================

log = get_logger("CMS_VENV")


class VirtualVenv:
    """
    Manager Virtual Environment Python
    """

    def __init__(self, venv_path):
        self.venv_path = Path(venv_path).resolve()
        self.bin_dir = self.venv_path / (
            "Scripts" if os.name == "nt" else "bin"
        )
        self.python_bin = self.bin_dir / (
            "python.exe" if os.name == "nt" else "python"
        )

    # =================================================
    # UTIL
    # =================================================

    @staticmethod
    def is_active() -> bool:
        """
        Cek apakah Python saat ini berjalan di dalam venv
        """
        return (
            hasattr(sys, "real_prefix")
            or (
                hasattr(sys, "base_prefix")
                and sys.base_prefix != sys.prefix
            )
        )

    # =================================================
    # CREATE
    # =================================================

    def create_venv(self):
        """
        Membuat virtualenv jika belum ada
        """
        if self.venv_path.exists():
            log.info("Virtualenv sudah ada (skip)")
            return

        log.info(f"Membuat virtualenv di {self.venv_path}")

        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "venv",
                    str(self.venv_path),
                ],
                check=True,
            )
        except Exception as e:
            raise CMSVirtualEnvError(
                f"Gagal membuat virtualenv: {e}"
            ) from e

        if not self.python_bin.exists():
            raise CMSVirtualEnvError(
                "Virtualenv dibuat tapi python binary tidak ditemukan"
            )

        log.info("Virtualenv berhasil dibuat")

    # =================================================
    # RUN IN VENV
    # =================================================

    def run(self, command: list):
        """
        Menjalankan command di dalam environment venv
        (tanpa activate shell)
        """
        if not self.python_bin.exists():
            raise CMSVirtualEnvError(
                "Virtualenv belum tersedia"
            )

        env = os.environ.copy()
        env["VIRTUAL_ENV"] = str(self.venv_path)
        env["PATH"] = (
            str(self.bin_dir)
            + os.pathsep
            + env.get("PATH", "")
        )

        log.debug(
            f"Run in venv: {' '.join(command)}"
        )

        try:
            subprocess.run(
                command,
                env=env,
                check=True,
            )
        except Exception as e:
            raise CMSVirtualEnvError(
                f"Gagal menjalankan perintah di venv: {e}"
            ) from e