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
    subdir = request.args.get("dir", "")

    if request.method == "POST":
        file = request.files.get("file")
        try:
            save_user_file(file, username, subdir)
            flash("File berhasil diupload", "success")
        except Exception as e:
            flash(str(e), "error")

        return redirect(f"/files?dir={subdir}")

    files = list_user_files(username, subdir)
    return render_template(
        "files.html",
        files=files,
        subdir=subdir
    )


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

@file_bp.route("/preview/<filename>")
@login_required
def preview_file(filename):
    username = current_user()
    directory = get_user_upload_dir(username)

    return send_from_directory(
        directory,
        filename,
        as_attachment=False
    )

@file_bp.route("/delete/<filename>")
@login_required
def delete_file(filename):
    try:
        delete_user_file(current_user(), filename)
        flash("File dihapus", "success")
    except Exception as e:
        flash(str(e), "error")

    return redirect("/files")

@file_bp.route("/rename/<filename>", methods=["GET", "POST"])
@login_required
def rename_file(filename):
    if request.method == "POST":
        new_name = request.form["new_name"]
        try:
            rename_user_file(
                current_user(),
                filename,
                new_name
            )
            flash("File berhasil di-rename", "success")
            return redirect("/files")
        except Exception as e:
            flash(str(e), "error")

    return render_template(
        "rename_file.html",
        filename=filename
    )