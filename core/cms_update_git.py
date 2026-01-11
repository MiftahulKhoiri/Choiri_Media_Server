"""
cms_update_git.py
Git Auto Updater (production-ready)
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from packaging.version import Version

from core.cms_detect_os import detect
from core.cms_logger import get_logger
from core.cms_errors import (
    CMSDependencyError,
    CMSPermissionError,
)

# =====================================================
# LOGGER
# =====================================================

log = get_logger("CMS_GIT")


class GitAutoUpdater:
    """
    Git Auto Updater
    - Auto skip jika Git sudah versi terbaru
    - Support Termux, Raspberry Pi, Linux PC
    """

    REPO_URL = "https://github.com/git/git.git"

    def __init__(self, prefix=None):
        self.os_name = detect()
        self.is_termux = self.os_name == "Linux Termux"
        self.prefix = prefix or self._detect_prefix()
        self.workdir = Path(tempfile.mkdtemp(prefix="git_auto_"))
        self.source_dir = self.workdir / "git"
        self.current_version = self._get_installed_git_version()

    # =====================================================
    # UTIL
    # =====================================================

    def _run(self, cmd, cwd=None):
        log.debug(f">> {' '.join(cmd)}")
        subprocess.run(cmd, cwd=cwd, check=True)

    def _cmd_out(self, cmd):
        return subprocess.check_output(cmd, text=True).strip()

    # =====================================================
    # PREFIX
    # =====================================================

    def _detect_prefix(self):
        if self.is_termux:
            return os.environ.get(
                "PREFIX",
                "/data/data/com.termux/files/usr"
            )
        return "/usr/local"

    # =====================================================
    # VERSION
    # =====================================================

    def _get_installed_git_version(self):
        try:
            out = self._cmd_out(["git", "--version"])
            return out.split()[-1]
        except Exception:
            return None

    def _get_latest_git_version(self):
        """
        Ambil versi Git terbaru TANPA clone repo
        Aman untuk tag non-numeric (rc, alpha, dll)
        """
        try:
            out = self._cmd_out([
                "git", "ls-remote",
                "--tags", "--refs",
                self.REPO_URL
            ])
        except Exception as e:
            raise CMSDependencyError(
                "Gagal mengambil versi Git terbaru"
            ) from e

        versions = []

        for line in out.splitlines():
            ref = line.split()[-1]
            if not ref.startswith("refs/tags/v"):
                continue

            raw_version = ref.split("/")[-1][1:]  # hapus 'v'

            try:
                versions.append(Version(raw_version))
            except Exception:
                # skip tag aneh (rc, windows, dll)
                continue

        if not versions:
            raise CMSDependencyError(
                "Tidak ditemukan versi Git valid"
            )

        return str(max(versions))

    def _is_latest(self, installed, latest):
        return installed == latest

    # =====================================================
    # DEPENDENCIES
    # =====================================================

    def _install_dependencies(self):
        if self.is_termux:
            log.info("Install dependency Git (Termux)")
            self._run([
                "pkg", "install", "-y",
                "git", "make", "clang",
                "openssl", "libcurl",
                "zlib", "gettext"
            ])
            return

        # Linux non-Termux wajib root
        if os.geteuid() != 0:
            raise CMSPermissionError(
                "Update Git membutuhkan akses root (sudo)"
            )

        log.info("Install dependency Git (Linux)")
        self._run(["apt-get", "update"])
        self._run([
            "apt-get", "install", "-y",
            "build-essential",
            "libssl-dev",
            "libcurl4-gnutls-dev",
            "libexpat1-dev",
            "gettext",
            "zlib1g-dev",
            "autoconf"
        ])

    # =====================================================
    # BUILD
    # =====================================================

    def _build_and_install(self):
        log.info("Clone source Git")
        self._run([
            "git", "clone", "--depth", "1",
            self.REPO_URL,
            str(self.source_dir)
        ])

        if (self.source_dir / "configure.ac").exists():
            self._run(
                ["make", "configure"],
                cwd=self.source_dir
            )

        log.info("Build Git")
        self._run(
            ["./configure", f"--prefix={self.prefix}"],
            cwd=self.source_dir
        )
        self._run(
            ["make", f"-j{os.cpu_count()}"],
            cwd=self.source_dir
        )

        log.info("Install Git")
        self._run(
            ["make", "install"],
            cwd=self.source_dir
        )

    # =====================================================
    # CLEANUP
    # =====================================================

    def _cleanup(self):
        if self.workdir.exists():
            shutil.rmtree(self.workdir, ignore_errors=True)

    # =====================================================
    # PUBLIC API
    # =====================================================

    def update(self) -> dict:
        """
        Update Git jika perlu.
        Return dict status.
        """
        result = {
            "installed": self.current_version,
            "latest": None,
            "updated": False,
            "prefix": self.prefix,
        }

        log.info("Cek versi Git")

        try:
            latest = self._get_latest_git_version()
            result["latest"] = latest

            log.info(
                f"Git installed : {self.current_version or 'not installed'}"
            )
            log.info(f"Git latest    : {latest}")

            if self.current_version and self._is_latest(
                self.current_version, latest
            ):
                log.info("Git sudah versi terbaru (skip)")
                return result

            log.info("Update Git diperlukan")
            self._install_dependencies()
            self._build_and_install()

            new_ver = self._cmd_out(
                [f"{self.prefix}/bin/git", "--version"]
            )
            result["updated"] = True
            result["new_version"] = new_ver

            log.info(f"Git berhasil diupdate → {new_ver}")
            return result

        finally:
            self._cleanup()