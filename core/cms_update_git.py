import os
import shutil
import subprocess
import tempfile
from pathlib import Path


class GitAutoUpdater:
    """
    Git Auto Updater
    - Auto skip jika Git sudah versi terbaru
    - Support Termux, Raspberry Pi, Linux
    """

    REPO_URL = "https://github.com/git/git.git"

    def __init__(self, prefix=None, verbose=True):
        self.verbose = verbose
        self.is_termux = self._detect_termux()
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
    # ENV DETECTION
    # =====================================================

    def _detect_termux(self):
        return os.environ.get("PREFIX", "").startswith("/data/data/com.termux")

    def _detect_prefix(self):
        return os.environ["PREFIX"] if self._detect_termux() else "/usr/local"

    def _detect_distro(self):
        if not os.path.exists("/etc/os-release"):
            return "unknown"
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("ID="):
                    return line.strip().split("=")[1].strip('"')
        return "unknown"

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
        self._run([
            "git", "clone",
            "--depth", "1",
            "--filter=blob:none",
            self.REPO_URL,
            str(self.source_dir)
        ])

        tags = self._cmd_out(
            ["git", "-C", str(self.source_dir), "tag"]
        ).splitlines()

        versions = sorted(
            (t[1:] for t in tags if t.startswith("v")),
            key=lambda s: list(map(int, s.split(".")))
        )

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

        distro = self._detect_distro()

        if distro in ("ubuntu", "debian", "raspbian", "linuxmint", "pop"):
            self._run(["apt-get", "update"])
            self._run([
                "apt-get", "install", "-y",
                "build-essential", "libssl-dev",
                "libcurl4-gnutls-dev", "libexpat1-dev",
                "gettext", "zlib1g-dev", "autoconf"
            ])
            return

        raise RuntimeError(f"Distro tidak didukung: {distro}")

    # =====================================================
    # BUILD
    # =====================================================

    def build_and_install(self):
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
            shutil.rmtree(self.workdir)

    # =====================================================
    # PUBLIC API
    # =====================================================

    def update(self):
        """
        Jalankan update Git.
        Return dict status agar mudah dipakai di aplikasi lain.
        """
        result = {
            "installed": self.current_version,
            "latest": None,
            "updated": False,
            "prefix": self.prefix
        }

        self._log("=== Git Auto Updater ===")
        self._log(f"Installed Git : {self.current_version or 'not installed'}")

        latest = self.get_latest_git_version()
        result["latest"] = latest
        self._log(f"Latest Git    : {latest}")

        if self.current_version and self.is_latest(self.current_version, latest):
            self._log("✔ Git sudah versi terbaru (skip)")
            self.cleanup()
            return result

        self._log("↻ Update diperlukan")
        self.install_dependencies()
        self.build_and_install()

        new_ver = self._cmd_out([f"{self.prefix}/bin/git", "--version"])
        result["updated"] = True
        result["new_version"] = new_ver

        self._log(f"✔ Git berhasil diupdate → {new_ver}")
        self.cleanup()
        return result