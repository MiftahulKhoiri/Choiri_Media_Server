"""
dashboard_routes.py
Route dashboard (login wajib)
"""

from flask import Blueprint, render_template

from app.services.auth_decorators import login_required
from app.services.session_service import current_user, is_root

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)


@dashboard_bp.route("/")
@login_required
def dashboard_home():
    return render_template(
        "dashboard.html",
        user=current_user(),
        is_root=is_root()
    )