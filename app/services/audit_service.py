"""
audit_service.py
Audit log untuk autentikasi
"""

import os
import json
from datetime import datetime

from core.cms_bash_folder import LOG_FOLDER


AUDIT_LOG_FILE = os.path.join(LOG_FOLDER, "auth_audit.log")


def _write_log(action, username):
    os.makedirs(LOG_FOLDER, exist_ok=True)

    entry = {
        "time": datetime.utcnow().isoformat(),
        "action": action,
        "user": username,
    }

    with open(AUDIT_LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


def log_login(username):
    _write_log("login", username)


def log_logout(username):
    _write_log("logout", username)