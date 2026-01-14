from flask import Blueprint, request, render_template, redirect, flash
from werkzeug.security import generate_password_hash

from app.services.auth_decorators import login_required
from app.repositories.user_repository import update_password
from app.services.session_service import current_user

password_bp = Blueprint("password", __name__)


@password_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        password = request.form["password"]
        confirm = request.form["confirm"]

        if len(password) < 8:
            flash("Password minimal 8 karakter", "error")
            return redirect("/change-password")

        if password != confirm:
            flash("Password tidak cocok", "error")
            return redirect("/change-password")

        password_hash = generate_password_hash(password)

        update_password(
            current_user(),
            password_hash,
            force_change=0
        )

        flash("Password berhasil diganti", "success")
        return redirect("/dashboard")

    return render_template("change_password.html")