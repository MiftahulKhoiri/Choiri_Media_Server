from flask import Blueprint, render_template, request, redirect, flash

from app.services.admin_audit_service import log_admin_action
from app.services.session_service import current_user
from app.services.auth_decorators import root_required
from app.services.audit_reader_service import read_auth_logs
from app.services.auth_service import create_user_by_admin

from app.repositories.user_repository import (
    list_users,
    delete_user,
    update_user_role,
    set_user_active,
)

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

ALLOWED_ROLES = {"user", "root"}


@admin_bp.route("/users")
@root_required
def users():
    return render_template("admin_users.html", users=list_users())


@admin_bp.route("/delete/<username>", methods=["POST"])
@root_required
def delete(username):
    if username == "root":
        flash("User root tidak boleh dihapus", "error")
        return redirect("/admin/users")

    delete_user(username)
    log_admin_action(current_user(), "delete_user", username)
    return redirect("/admin/users")


@admin_bp.route("/role", methods=["POST"])
@root_required
def change_role():
    username = request.form["username"]
    role = request.form["role"]

    if role not in ALLOWED_ROLES:
        flash("Role tidak valid", "error")
        return redirect("/admin/users")

    update_user_role(username, role)
    log_admin_action(current_user(), "change_role", f"{username}:{role}")
    return redirect("/admin/users")


@admin_bp.route("/add-user", methods=["GET", "POST"])
@root_required
def add_user():
    if request.method == "POST":
        try:
            create_user_by_admin(
                request.form["username"],
                request.form["password"],
                request.form["role"]
            )
            log_admin_action(current_user(), "create_user", request.form["username"])
            flash("User berhasil dibuat", "success")
            return redirect("/admin/users")
        except ValueError as e:
            flash(str(e), "error")

    return render_template("admin_add_user.html")


@admin_bp.route("/login-history")
@root_required
def login_history():
    log_admin_action(current_user(), "view_login_history")
    return render_template(
        "admin_login_history.html",
        logs=read_auth_logs()
    )

@admin_bp.route("/lock/<username>", methods=["POST"])
@root_required
def lock_user(username):
    if username == "root":
        flash("User root tidak boleh dikunci", "error")
        return redirect("/admin/users")

    set_user_active(username, False)
    log_admin_action(current_user(), "lock_user", username)

    flash("User berhasil dikunci", "success")
    return redirect("/admin/users")

@admin_bp.route("/unlock/<username>", methods=["POST"])
@root_required
def unlock_user(username):
    set_user_active(username, True)
    log_admin_action(current_user(), "unlock_user", username)

    flash("User berhasil dibuka", "success")
    return redirect("/admin/users")