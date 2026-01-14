from flask import Blueprint, render_template, request, redirect

from app.services.auth_decorators import root_required
from app.services.audit_reader_service import read_auth_logs

from app.repositories.user_repository import (
    list_users,
    delete_user,
    update_user_role,
)

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


@admin_bp.route("/users")
@root_required
def users():
    return render_template(
        "admin_users.html",
        users=list_users()
    )


@admin_bp.route("/delete/<username>")
@root_required
def delete(username):
    delete_user(username)
    return redirect("/admin/users")


@admin_bp.route("/role", methods=["POST"])
@root_required
def change_role():
    update_user_role(
        request.form["username"],
        request.form["role"]
    )
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
            flash("User berhasil dibuat", "success")
            return redirect("/admin/users")
        except ValueError as e:
            flash(str(e), "error")

    return render_template("admin_add_user.html")

@admin_bp.route("/login-history")
@root_required
def login_history():
    return render_template(
        "admin_login_history.html",
        logs=read_auth_logs()
    )