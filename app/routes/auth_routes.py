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
        username = request.form["username"]
        password = request.form["password"]
        ip = request.remote_addr

        # -----------------------------------------
        # RATE LIMIT (ANTI BRUTE FORCE)
        # -----------------------------------------
        if not can_attempt(ip):
            return "Terlalu banyak percobaan login. Coba lagi nanti.", 429

        # -----------------------------------------
        # VERIFIKASI LOGIN
        # -----------------------------------------
        if verify_login(username, password):
            reset_fail(ip)
            login_user(username)

            # 🔴 INI BAGIAN PENTING (2.3)
            if must_change_password(username):
                return redirect("/change-password")

            return redirect("/dashboard")

        # LOGIN GAGAL
        register_fail(ip)
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