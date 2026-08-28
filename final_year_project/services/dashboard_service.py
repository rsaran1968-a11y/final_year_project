from __future__ import annotations

from datetime import datetime, timedelta

from models.dashboard import (
    CameraStatus,
    DashboardMetric,
    DashboardSnapshot,
    HourlyFlow,
    ModuleReadiness,
    TrackingEvent,
)


class DashboardService:
    """Build dashboard-ready read models from application state."""

    def build_snapshot(self, service_name: str, environment: str) -> DashboardSnapshot:
        now = datetime.now()
        cameras = self._camera_statuses(now)
        events = self._recent_events(now)
        hourly_flow = self._hourly_flow()
        entries_today = sum(flow.entries for flow in hourly_flow)
        exits_today = sum(flow.exits for flow in hourly_flow)
        occupancy = max(entries_today - exits_today, 0)
        pending_reviews = sum(1 for event in events if event.event_type == "review")
        active_cameras = sum(1 for camera in cameras if camera.status == "ready")
        average_confidence = self._average_confidence(cameras)

        return DashboardSnapshot(
            service=service_name,
            environment=environment,
            generated_at=now,
            system_status="degraded" if active_cameras == 0 else "ready",
            occupancy=occupancy,
            metrics=[
                DashboardMetric("Active Cameras", active_cameras, "feeds", "1 camera slot"),
                DashboardMetric("Entries Today", entries_today, "buses", "waiting for camera"),
                DashboardMetric("Exits Today", exits_today, "buses", "waiting for camera"),
                DashboardMetric("Pending Reviews", pending_reviews, "items", "none"),
                DashboardMetric("Current Yard Count", occupancy, "buses", "net flow"),
                DashboardMetric("Avg Confidence", round(average_confidence), "percent", "no frames"),
            ],
            cameras=cameras,
            events=events,
            modules=self._module_readiness(),
            hourly_flow=hourly_flow,
            alerts=self._alerts(cameras, pending_reviews),
        )

    def _camera_statuses(self, now: datetime) -> list[CameraStatus]:
        return [
            CameraStatus(
                "CAM-01",
                "Primary Camera",
                "Entry/Exit Point",
                "not_configured",
                0,
                0.0,
                "not connected",
            ),
        ]

    def _recent_events(self, now: datetime) -> list[TrackingEvent]:
        return []

    def _hourly_flow(self) -> list[HourlyFlow]:
        return [
            HourlyFlow("06:00", 0, 0),
            HourlyFlow("07:00", 0, 0),
            HourlyFlow("08:00", 0, 0),
            HourlyFlow("09:00", 0, 0),
            HourlyFlow("10:00", 0, 0),
            HourlyFlow("11:00", 0, 0),
            HourlyFlow("12:00", 0, 0),
            HourlyFlow("13:00", 0, 0),
        ]

    def _module_readiness(self) -> list[ModuleReadiness]:
        return [
            ModuleReadiness("Flask Backend", "ready", 100, "Application factory and health checks are active."),
            ModuleReadiness("Dashboard", "ready", 100, "Operational dashboard and JSON API are connected."),
            ModuleReadiness("Camera Ingestion", "pending", 35, "Service boundary is ready for stream adapters."),
            ModuleReadiness("Detection Pipeline", "pending", 25, "Model adapter contract is pending implementation."),
            ModuleReadiness("OCR Processing", "not_configured", 10, "OCR provider is intentionally not implemented yet."),
            ModuleReadiness("Database", "pending", 30, "Persistence adapter can be wired later."),
            ModuleReadiness("Cloud Storage", "not_configured", 10, "Storage provider credentials are not configured."),
        ]

    def _alerts(self, cameras: list[CameraStatus], pending_reviews: int) -> list[str]:
        alerts = []
        inactive_cameras = [camera.name for camera in cameras if camera.status != "ready"]

        if inactive_cameras:
            alerts.append("Primary camera is not configured. Tracking data will remain 0 until a camera source is connected.")
        if pending_reviews:
            alerts.append(f"{pending_reviews} event needs manual review.")
        if not alerts:
            alerts.append("All configured systems are operating normally.")

        return alerts

    def _average_confidence(self, cameras: list[CameraStatus]) -> float:
        confidence_values = [camera.confidence for camera in cameras if camera.confidence > 0]
        if not confidence_values:
            return 0.0
        return sum(confidence_values) / len(confidence_values)

    def _ago(self, now: datetime, minutes: int) -> str:
        return (now - timedelta(minutes=minutes)).strftime("%H:%M")
