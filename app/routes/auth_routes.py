from flask import Blueprint, request, redirect, render_template, flash

from app.services.auth_service import (
    verify_login,
    login_user,
    must_change_password,
)

from app.repositories.user_repository import get_user_by_username

from app.services.audit_service import log_logout

from app.services.rate_limit_service import (
    can_attempt,
    register_fail,
    reset_fail,
)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        ip = request.remote_addr

        if not can_attempt(ip):
            flash("Terlalu banyak percobaan login. Coba lagi nanti.", "error")
            return redirect("/login")

        if verify_login(username, password):
            reset_fail(ip)
            login_user(username, ip)

            # =================================================
            # FORCE CHANGE PASSWORD (PALING PRIORITAS)
            # =================================================
            if must_change_password(username):
                flash(
                    "Anda wajib mengganti password sebelum melanjutkan",
                    "warning"
                )
                return redirect("/change-password")

            # =================================================
            # ROLE-BASED REDIRECT
            # =================================================
            user = get_user_by_username(username)

            if user.role == "root":
                flash("Selamat datang Admin", "success")
                return redirect("/admin/users")

            # default user
            flash("Login berhasil", "success")
            return redirect("/dashboard")

        register_fail(ip)
        flash("Username atau password salah", "error")
        return redirect("/login")

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
    user = current_user()
    logout_session()
    if user:
        log_logout(user, request.remote_addr)
    return redirect("/")