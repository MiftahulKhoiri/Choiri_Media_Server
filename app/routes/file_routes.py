from flask import (
    Blueprint, render_template, request,
    redirect, flash, send_from_directory
)

from app.services.auth_decorators import login_required, root_required
from app.services.session_service import current_user, is_root
from app.services.file_service import (
    save_user_file,
    list_user_files,
    list_all_files,
    get_user_upload_dir
)

file_bp = Blueprint("files", __name__, url_prefix="/files")


@file_bp.route("/", methods=["GET", "POST"])
@login_required
def user_files():
    username = current_user()

    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            flash("Tidak ada file dipilih", "error")
            return redirect("/files")

        try:
            save_user_file(file, username)
            flash("File berhasil diupload", "success")
        except ValueError as e:
            flash(str(e), "error")

        return redirect("/files")

    files = list_user_files(username)
    return render_template("files.html", files=files)


@file_bp.route("/download/<filename>")
@login_required
def download_file(filename):
    username = current_user()
    directory = get_user_upload_dir(username)
    return send_from_directory(directory, filename, as_attachment=True)


@file_bp.route("/admin")
@root_required
def admin_files():
    return render_template(
        "admin_files.html",
        files=list_all_files()
    )