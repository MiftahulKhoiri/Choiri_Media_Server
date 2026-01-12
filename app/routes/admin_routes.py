from flask import Blueprint, render_template, request, redirect

from app.services.auth_decorators import root_required
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