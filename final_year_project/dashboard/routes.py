from __future__ import annotations

from flask import Blueprint, Response, current_app, jsonify, render_template

from services.dashboard_service import DashboardService


dashboard_bp = Blueprint("dashboard", __name__)
dashboard_service = DashboardService()


@dashboard_bp.get("/")
@dashboard_bp.get("/dashboard")
def dashboard() -> str:
    return render_template(
        "dashboard.html",
        app_name=current_app.config["APP_NAME"],
        environment=current_app.config["ENVIRONMENT"],
    )


@dashboard_bp.get("/api/dashboard/summary")
def dashboard_summary() -> tuple[Response, int]:
    snapshot = dashboard_service.build_snapshot(
        service_name=current_app.config["APP_NAME"],
        environment=current_app.config["ENVIRONMENT"],
    )
    return jsonify(snapshot.to_dict()), 200
