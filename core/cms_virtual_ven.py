"""
virtual_ven.py
Module utilitas Virtual Environment Python 3

Fungsi:
- cek virtual env
- buat virtual env
- aktifkan virtual env (secara subprocess / instruksi)
- matikan virtual env
"""

import os
import sys
import subprocess
from pathlib import Path


class VirtualVenv:
    def __init__(self, venv_path="venv"):
        self.venv_path = Path(venv_path).resolve()
        self.bin_dir = self.venv_path / ("Scripts" if os.name == "nt" else "bin")
        self.python_bin = self.bin_dir / ("python.exe" if os.name == "nt" else "python")

    # =====================================================
    # FUNGSI 1: CEK APAKAH SEDANG DI VENV
    # =====================================================

    @staticmethod
    def is_venv_active():
        """
        Return True jika Python saat ini berjalan di dalam virtualenv
        """
        return (
            hasattr(sys, "real_prefix")
            or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)
        )

    # =====================================================
    # FUNGSI 2: BUAT VIRTUAL ENV
    # =====================================================

    def create_venv(self, with_pip=True):
        """
        Membuat virtual environment
        """
        if self.venv_path.exists():
            return {
                "created": False,
                "path": str(self.venv_path),
                "reason": "virtual env sudah ada"
            }

        cmd = [
            sys.executable,
            "-m", "venv",
            str(self.venv_path)
        ]

        if with_pip:
            cmd.append("--upgrade-deps")

        subprocess.run(cmd, check=True)

        return {
            "created": True,
            "path": str(self.venv_path)
        }

    # =====================================================
    # FUNGSI 3: AKTIFKAN VENV (REALISTIS)
    # =====================================================

    def activate_info(self):
        """
        Mengembalikan command yang harus dijalankan user
        """
        if os.name == "nt":
            return f"{self.bin_dir}\\activate"
        return f"source {self.bin_dir}/activate"

    def run_in_venv(self, command):
        """
        Menjalankan perintah di dalam venv TANPA activate shell
        """
        if not self.python_bin.exists():
            raise FileNotFoundError("Virtual env belum dibuat")

        env = os.environ.copy()
        env["VIRTUAL_ENV"] = str(self.venv_path)
        env["PATH"] = f"{self.bin_dir}{os.pathsep}{env['PATH']}"

        return subprocess.run(
            command,
            env=env,
            check=True
        )

    # =====================================================
    # FUNGSI 4: MATIKAN VENV
    # =====================================================

    @staticmethod
    def deactivate_info():
        """
        Virtual env tidak bisa dimatikan dari Python.
        Ini hanya instruksi.
        """
        return "Ketik 'deactivate' di shell untuk keluar dari virtualenv"


# =====================================================
# CONTOH PAKAI JIKA DIJALANKAN LANGSUNG
# =====================================================

if __name__ == "__main__":
    venv = VirtualVenv("venv")

    print("Apakah sedang di venv?:", VirtualVenv.is_venv_active())

    result = venv.create_venv()
    print("Create venv:", result)

    print("Cara activate:")
    print(venv.activate_info())

    print("Cara deactivate:")
    print(VirtualVenv.deactivate_info())