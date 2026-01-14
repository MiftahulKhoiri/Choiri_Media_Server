"""
file_service.py
Business logic upload & akses file user
"""

import os
from werkzeug.utils import secure_filename

from core.cms_bash_folder import UPLOAD_FOLDER


ALLOWED_EXTENSIONS = {
    "png", "jpg", "jpeg", "gif",
    "pdf", "txt", "zip"
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def get_user_upload_dir(username):
    path = os.path.join(UPLOAD_FOLDER, "users", username)
    os.makedirs(path, exist_ok=True)
    return path


def save_user_file(file_storage, username):
    if not allowed_file(file_storage.filename):
        raise ValueError("Tipe file tidak diizinkan")

    file_storage.stream.seek(0, os.SEEK_END)
    size = file_storage.stream.tell()
    file_storage.stream.seek(0)

    if size > MAX_FILE_SIZE:
        raise ValueError("Ukuran file terlalu besar (maks 10MB)")

    filename = secure_filename(file_storage.filename)
    user_dir = get_user_upload_dir(username)

    filepath = os.path.join(user_dir, filename)

    if os.path.exists(filepath):
        raise ValueError("File dengan nama yang sama sudah ada")

    file_storage.save(filepath)
    return filename


def list_user_files(username):
    user_dir = get_user_upload_dir(username)
    return sorted(os.listdir(user_dir))


def list_all_files():
    base = os.path.join(UPLOAD_FOLDER, "users")
    result = {}

    if not os.path.exists(base):
        return result

    for user in os.listdir(base):
        user_path = os.path.join(base, user)
        if os.path.isdir(user_path):
            result[user] = os.listdir(user_path)

    return result