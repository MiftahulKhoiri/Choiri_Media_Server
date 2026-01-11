from flask import Flask
from core.cms_bootstrap import bootstrap_system

def create_app():
    app = Flask(__name__)

    # secret key (nanti bisa pindah ke config)
    app.config["SECRET_KEY"] = "dev-secret-key"

    # bootstrap core CMS
    bootstrap_system()

    # register routes
    from app.routes.web import web_bp
    app.register_blueprint(web_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )