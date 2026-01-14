from flask import Blueprint, jsonify, request

from app.services.api_token_service import generate_token
from app.services.api_auth_decorator import api_token_required
from app.services.session_service import current_user
from app.services.auth_decorators import login_required

api_bp = Blueprint("api", __name__, url_prefix="/api")


# -------------------------------
# GENERATE TOKEN (LOGIN REQUIRED)
# -------------------------------
@api_bp.route("/token", methods=["POST"])
@login_required
def create_token():
    token = generate_token(current_user())
    return jsonify({
        "token": token,
        "warning": "Simpan token ini, tidak akan ditampilkan lagi"
    })


# -------------------------------
# PROTECTED API EXAMPLE
# -------------------------------
@api_bp.route("/me")
@api_token_required
def api_me():
    return jsonify({
        "user": request.api_user,
        "status": "ok"
    })