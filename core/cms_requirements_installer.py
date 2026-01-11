"""
cms_requirements_installer.py
Installer requirements.txt CMS (cerdas & aman)
"""

import sys
import subprocess
from pathlib import Path

from packaging.requirements import Requirement
from packaging.version import Version

from core.cms_logger import get_logger
from core.cms_errors import CMSDependencyError

# =====================================================
# LOGGER
# =====================================================

log = get_logger("CMS_REQUIREMENTS")


class RequirementsInstaller:
    """
    Installer requirements.txt dengan skip & update logic
    """

    def __init__(self, python_bin=None):
        self.python = python_bin or sys.executable

    # =================================================
    # UTIL
    # =================================================

    def _run(self, cmd):
        log.debug(f">> {' '.join(cmd)}")
        subprocess.run(cmd, check=True)

    def _cmd_out(self, cmd):
        return subprocess.check_output(
            cmd, text=True
        ).strip()

    def pip(self, args):
        return [self.python, "-m", "pip"] + args

    # =================================================
    # REQUIREMENTS
    # =================================================

    def _read_requirements(self, path):
        path = Path(path)
        if not path.exists():
            raise CMSDependencyError(
                f"{path} tidak ditemukan"
            )

        requirements = []
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            requirements.append(Requirement(line))

        return requirements

    def _installed_version(self, package):
        try:
            out = self._cmd_out(
                self.pip(["show", package])
            )
            for line in out.splitlines():
                if line.startswith("Version:"):
                    return Version(
                        line.split(":", 1)[1].strip()
                    )
        except subprocess.CalledProcessError:
            return None

    def _is_satisfied(self, requirement: Requirement):
        installed = self._installed_version(
            requirement.name
        )

        if not installed:
            return False

        if not requirement.specifier:
            return True

        return installed in requirement.specifier

    # =================================================
    # PUBLIC API
    # =================================================

    def install_requirements(self, requirements_file):
        """
        Install requirements.txt dengan auto skip
        """
        reqs = self._read_requirements(
            requirements_file
        )

        installed = []
        skipped = []
        updated = []

        log.info(
            f"Memproses {len(reqs)} dependency"
        )

        for req in reqs:
            if self._is_satisfied(req):
                log.info(f"SKIP   {req}")
                skipped.append(str(req))
                continue

            log.info(f"INSTALL {req}")
            try:
                self._run(
                    self.pip(["install", str(req)])
                )
            except Exception as e:
                raise CMSDependencyError(
                    f"Gagal install {req}: {e}"
                ) from e

            if self._installed_version(req.name):
                updated.append(str(req))
            else:
                installed.append(str(req))

        return {
            "installed": installed,
            "updated": updated,
            "skipped": skipped,
            "total": len(reqs),
        }