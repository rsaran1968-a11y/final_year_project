from __future__ import annotations

from flask import Flask, Response, jsonify

from config import AppConfig, get_config
from dashboard.routes import dashboard_bp
from services.logging_service import configure_logging


def create_app(config: AppConfig | None = None) -> Flask:
    """Application factory for the Bus Entry & Exit Tracking System."""
    app_config = config or get_config()
    configure_logging(app_config)

    app = Flask(__name__)
    app.config.from_mapping(app_config.to_flask_config())
    app.register_blueprint(dashboard_bp)

    @app.get("/health")
    def health_check() -> tuple[Response, int]:
        return jsonify({"status": "ok", "service": app_config.app_name}), 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host=app.config["HOST"],
        port=app.config["PORT"],
        debug=app.config["DEBUG"],
    )
