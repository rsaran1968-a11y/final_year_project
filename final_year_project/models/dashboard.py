from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Literal


HealthStatus = Literal["ready", "degraded", "offline"]
ModuleStatus = Literal["ready", "pending", "not_configured"]
Severity = Literal["info", "warning", "critical"]


@dataclass(frozen=True, slots=True)
class DashboardMetric:
    label: str
    value: int
    unit: str
    trend: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CameraStatus:
    camera_id: str
    name: str
    location: str
    status: ModuleStatus
    fps: int
    confidence: float
    last_seen: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TrackingEvent:
    event_id: str
    event_type: Literal["entry", "exit", "system", "review"]
    bus_number: str
    gate: str
    confidence: float
    occurred_at: str
    severity: Severity

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ModuleReadiness:
    name: str
    status: ModuleStatus
    progress: int
    detail: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class HourlyFlow:
    hour: str
    entries: int
    exits: int

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class DashboardSnapshot:
    service: str
    environment: str
    generated_at: datetime
    system_status: HealthStatus
    occupancy: int
    metrics: list[DashboardMetric]
    cameras: list[CameraStatus]
    events: list[TrackingEvent]
    modules: list[ModuleReadiness]
    hourly_flow: list[HourlyFlow]
    alerts: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "service": self.service,
            "environment": self.environment,
            "generated_at": self.generated_at.isoformat(timespec="seconds"),
            "system_status": self.system_status,
            "occupancy": self.occupancy,
            "metrics": [metric.to_dict() for metric in self.metrics],
            "cameras": [camera.to_dict() for camera in self.cameras],
            "events": [event.to_dict() for event in self.events],
            "modules": [module.to_dict() for module in self.modules],
            "hourly_flow": [flow.to_dict() for flow in self.hourly_flow],
            "alerts": self.alerts,
        }
