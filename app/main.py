from flask import Flask
from flask_wtf.csrf import CSRFProtect

# =====================================================
# CORE BOOTSTRAP
# =====================================================

from core.cms_bootstrap import bootstrap_system

# =====================================================
# SERVICES
# =====================================================

from app.services.auth_service import init_auth, bootstrap_root_user
from app.services.api_token_service import init_api_token
from app.repositories.user_repository import init_user_table

# =====================================================
# ROUTES
# =====================================================

from app.routes.web import web_bp
from app.routes.admin_routes import admin_bp
from app.routes.auth_routes import auth_bp
from app.routes.file_routes import file_bp
from app.routes.dashboard_routes import dashboard_bp
from app.routes.api_routes import api_bp
from app.routes.password_routes import password_bp


# =====================================================
# APP FACTORY
# =====================================================

def create_app():
    app = Flask(__name__)
    

    # -------------------------------------------------
    # SECRET KEY (NANTI PINDAH KE CONFIG)
    # -------------------------------------------------
    app.config["SECRET_KEY"] = "dev-secret-key"
    csrf = CSRFProtect(app)

    # -------------------------------------------------
    # BOOTSTRAP CORE SYSTEM
    # (folder, git, venv, dll)
    # -------------------------------------------------
    bootstrap_system()

    # -------------------------------------------------
    # INIT AUTH SYSTEM (DB, TABLE)
    # -------------------------------------------------
    init_auth()
    init_user_table()
    init_api_token()
    bootstrap_root_user()

    # -------------------------------------------------
    # REGISTER BLUEPRINTS
    # -------------------------------------------------
    app.register_blueprint(web_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(file_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(password_bp)

    return app


# =====================================================
# ENTRY POINT (DEV MODE)
# =====================================================

if __name__ == "__main__":
    app = create_app()
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )