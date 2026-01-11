"""
cms_requirements_installer.py
Module installer requirements.txt yang cerdas & aman
"""

import sys
import subprocess
from pathlib import Path
from packaging.requirements import Requirement
from packaging.version import Version


class RequirementsInstaller:
    def __init__(self, python_bin=None, verbose=True):
        self.python = python_bin or sys.executable
        self.verbose = verbose

    # =====================================================
    # UTIL
    # =====================================================

    def _log(self, msg):
        if self.verbose:
            print(msg)

    def _run(self, cmd):
        self._log(f">> {' '.join(cmd)}")
        subprocess.run(cmd, check=True)

    def _cmd_out(self, cmd):
        return subprocess.check_output(cmd, text=True).strip()

    # =====================================================
    # CORE
    # =====================================================

    def pip(self, args):
        return [self.python, "-m", "pip"] + args

    def read_requirements(self, path="requirements.txt"):
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"{path} tidak ditemukan")

        requirements = []
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            requirements.append(Requirement(line))

        return requirements

    def get_installed_version(self, package_name):
        try:
            out = self._cmd_out(
                self.pip(["show", package_name])
            )
            for line in out.splitlines():
                if line.startswith("Version:"):
                    return Version(line.split(":", 1)[1].strip())
        except subprocess.CalledProcessError:
            return None

    def requirement_satisfied(self, requirement: Requirement):
        installed = self.get_installed_version(requirement.name)

        if not installed:
            return False

        if not requirement.specifier:
            return True

        return installed in requirement.specifier

    # =====================================================
    # PUBLIC API
    # =====================================================

    def install_requirements(self, requirements_file="requirements.txt"):
        reqs = self.read_requirements(requirements_file)

        installed = []
        skipped = []
        updated = []

        for req in reqs:
            if self.requirement_satisfied(req):
                self._log(f"✔ SKIP   {req}")
                skipped.append(str(req))
                continue

            self._log(f"↻ INSTALL {req}")
            self._run(self.pip(["install", str(req)]))

            if self.get_installed_version(req.name):
                updated.append(str(req))
            else:
                installed.append(str(req))

        return {
            "installed": installed,
            "updated": updated,
            "skipped": skipped,
            "total": len(reqs)
        }