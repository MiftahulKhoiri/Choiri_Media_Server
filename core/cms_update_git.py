"""
cms_update_git.py
Auto update source code CMS dari GitHub
"""

import os
import subprocess
import sys

from core.cms_logger import get_logger

log = get_logger("CMS_SELF_UPDATE")


class SelfUpdater:
    def __init__(self, repo_dir):
        self.repo_dir = repo_dir

    def _run(self, cmd):
        return subprocess.check_output(
            cmd,
            cwd=self.repo_dir,
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()

    def get_local_commit(self):
        return self._run(["git", "rev-parse", "HEAD"])

    def get_remote_commit(self):
        self._run(["git", "fetch", "origin"])
        return self._run(["git", "rev-parse", "origin/main"])

    def update_if_needed(self) -> bool:
        """
        Return True jika update terjadi
        """
        try:
            local = self.get_local_commit()
            remote = self.get_remote_commit()

            log.info(f"Local commit  : {local[:8]}")
            log.info(f"Remote commit : {remote[:8]}")

            if local == remote:
                log.info("Kode sudah terbaru (skip)")
                return False

            log.warning("Update kode terdeteksi, pull dari GitHub")
            subprocess.run(
                ["git", "pull", "--rebase"],
                cwd=self.repo_dir,
                check=True
            )

            log.info("Update kode selesai")
            return True

        except Exception as e:
            log.error(f"Gagal auto update kode: {e}")
            return False