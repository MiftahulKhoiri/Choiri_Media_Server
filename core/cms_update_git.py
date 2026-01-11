import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from core.cms_detect_os import detect


class GitAutoUpdater:
    """
    Git Auto Updater
    - Auto skip jika Git sudah versi terbaru
    - Support Termux, Raspberry Pi, Linux PC
    - Konsisten dengan cms_detect_os
    """

    REPO_URL = "https://github.com/git/git.git"

    def __init__(self, prefix=None, verbose=True):
        self.verbose = verbose
        self.os_name = detect()
        self.is_termux = self.os_name == "Linux Termux"
        self.prefix = prefix or self._detect_prefix()
        self.workdir = Path(tempfile.mkdtemp(prefix="git_auto_"))
        self.source_dir = self.workdir / "git"
        self.current_version = self.get_installed_git_version()

    # =====================================================
    # UTIL
    # =====================================================

    def _log(self, msg):
        if self.verbose:
            print(msg)

    def _run(self, cmd, cwd=None):
        self._log(f">> {' '.join(cmd)}")
        subprocess.run(cmd, cwd=cwd, check=True)

    def _cmd_out(self, cmd):
        return subprocess.check_output(cmd, text=True).strip()

    # =====================================================
    # PREFIX
    # =====================================================

    def _detect_prefix(self):
        if self.is_termux:
            return os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
        return "/usr/local"

    # =====================================================
    # VERSION
    # =====================================================

    def get_installed_git_version(self):
        try:
            out = self._cmd_out(["git", "--version"])
            return out.split()[-1]
        except Exception:
            return None

    def get_latest_git_version(self):
        """
        Ambil versi Git terbaru TANPA clone repository
        """
        out = self._cmd_out([
            "git", "ls-remote", "--tags", "--refs", self.REPO_URL
        ])

        versions = []
        for line in out.splitlines():
            ref = line.split()[-1]
            if ref.startswith("refs/tags/v"):
                versions.append(ref.split("/")[-1][1:])

        versions.sort(key=lambda s: list(map(int, s.split("."))))
        return versions[-1] if versions else None

    def is_latest(self, installed, latest):
        return installed == latest

    # =====================================================
    # DEPENDENCIES
    # =====================================================

    def install_dependencies(self):
        if self.is_termux:
            self._run([
                "pkg", "install", "-y",
                "git", "make", "clang",
                "openssl", "libcurl",
                "zlib", "gettext"
            ])
            return

        # Linux non-Termux wajib root
        if os.geteuid() != 0:
            raise PermissionError("Update Git membutuhkan akses root")

        self._run(["apt-get", "update"])
        self._run([
            "apt-get", "install", "-y",
            "build-essential", "libssl-dev",
            "libcurl4-gnutls-dev", "libexpat1-dev",
            "gettext", "zlib1g-dev", "autoconf"
        ])

    # =====================================================
    # BUILD
    # =====================================================

    def build_and_install(self):
        self._run([
            "git", "clone", "--depth", "1",
            self.REPO_URL, str(self.source_dir)
        ])

        if (self.source_dir / "configure.ac").exists():
            self._run(["make", "configure"], cwd=self.source_dir)

        self._run(["./configure", f"--prefix={self.prefix}"], cwd=self.source_dir)
        self._run(["make", f"-j{os.cpu_count()}"], cwd=self.source_dir)
        self._run(["make", "install"], cwd=self.source_dir)

    # =====================================================
    # CLEANUP
    # =====================================================

    def cleanup(self):
        if self.workdir.exists():
            shutil.rmtree(self.workdir, ignore_errors=True)

    # =====================================================
    # PUBLIC API
    # =====================================================

    def update(self):
        result = {
            "installed": self.current_version,
            "latest": None,
            "updated": False,
            "prefix": self.prefix
        }

        self._log("=== Git Auto Updater ===")
        self._log(f"Installed Git : {self.current_version or 'not installed'}")

        try:
            latest = self.get_latest_git_version()
            result["latest"] = latest
            self._log(f"Latest Git    : {latest}")

            if self.current_version and self.is_latest(self.current_version, latest):
                self._log("✔ Git sudah versi terbaru (skip)")
                return result

            self._log("↻ Update diperlukan")
            self.install_dependencies()
            self.build_and_install()

            new_ver = self._cmd_out([f"{self.prefix}/bin/git", "--version"])
            result["updated"] = True
            result["new_version"] = new_ver

            self._log(f"✔ Git berhasil diupdate → {new_ver}")
            return result

        finally:
            self.cleanup()