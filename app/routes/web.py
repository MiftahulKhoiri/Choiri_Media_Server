from flask import Blueprint, render_template

web_bp = Blueprint(
    "web",
    __name__,
)

@web_bp.route("/")
def index():
    return render_template("index.html")


@web_bp.route("/login")
def login():
    return render_template("login.html")


@web_bp.route("/register")
def register():
    return render_template("register.html")