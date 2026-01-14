"""
audit_reader_service.py
Membaca audit log autentikasi
"""

import json
import os

from core.cms_bash_folder import LOG_FOLDER

AUDIT_LOG_FILE = os.path.join(LOG_FOLDER, "auth_audit.log")


def read_auth_logs(limit=100):
    if not os.path.exists(AUDIT_LOG_FILE):
        return []

    with open(AUDIT_LOG_FILE) as f:
        lines = f.readlines()

    entries = [json.loads(line) for line in lines]
    return entries[-limit:][::-1]  # terbaru dulu