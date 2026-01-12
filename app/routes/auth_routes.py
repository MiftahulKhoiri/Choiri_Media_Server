from flask import Blueprint, request, redirect, render_template

from app.services.auth_service import (
    verify_login,
    login_user,
    register_user,
)

from app.services.session_service import (
    is_logged_in,
    logout_session,
)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if verify_login(
            request.form["username"],
            request.form["password"]
        ):
            login_user(request.form["username"])
            return redirect("/dashboard")

        return "Login gagal"

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        register_user(
            request.form["username"],
            request.form["password"]
        )
        return redirect("/login")

    return render_template("register.html")


@auth_bp.route("/logout")
def logout():
    logout_session()
    return redirect("/")