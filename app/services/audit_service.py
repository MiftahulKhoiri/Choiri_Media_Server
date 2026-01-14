"""
audit_service.py
Audit log untuk autentikasi
"""

import os
import json
from datetime import datetime

from core.cms_bash_folder import LOG_FOLDER


AUDIT_LOG_FILE = os.path.join(LOG_FOLDER, "auth_audit.log")


def _write_log(action, username, ip=None):
    os.makedirs(LOG_FOLDER, exist_ok=True)

    entry = {
        "time": datetime.utcnow().isoformat(),
        "action": action,
        "user": username,
        "ip": ip,
    }

    with open(AUDIT_LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


def log_login(username, ip):
    _write_log("login", username, ip)


def log_logout(username, ip=None):
    _write_log("logout", username, ip)