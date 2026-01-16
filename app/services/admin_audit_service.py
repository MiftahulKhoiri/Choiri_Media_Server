"""
admin_audit_service.py
Audit log untuk aksi admin (root)
"""

from datetime import datetime
from pathlib import Path

from core.cms_bash_folder import LOG_FOLDER

ADMIN_LOG = Path(LOG_FOLDER) / "admin_actions.log"


def log_admin_action(admin, action, target=None):
    timestamp = datetime.utcnow().isoformat()

    line = f"{timestamp} | admin={admin} | action={action}"

    if target:
        line += f" | target={target}"

    with open(ADMIN_LOG, "a") as f:
        f.write(line + "\n")