from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def _get_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"Environment variable {name} must be an integer.") from exc


@dataclass(frozen=True, slots=True)
class AppConfig:
    app_name: str
    environment: str
    debug: bool
    host: str
    port: int
    secret_key: str
    log_level: str
    log_file: Path
    database_url: str
    storage_path: Path

    def to_flask_config(self) -> dict[str, object]:
        return {
            "APP_NAME": self.app_name,
            "ENVIRONMENT": self.environment,
            "DEBUG": self.debug,
            "HOST": self.host,
            "PORT": self.port,
            "SECRET_KEY": self.secret_key,
            "DATABASE_URL": self.database_url,
            "STORAGE_PATH": self.storage_path,
        }


@lru_cache(maxsize=1)
def get_config() -> AppConfig:
    return AppConfig(
        app_name=os.getenv("APP_NAME", "Bus Entry Exit Tracking System"),
        environment=os.getenv("APP_ENV", "development"),
        debug=_get_bool("FLASK_DEBUG", False),
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=_get_int("APP_PORT", 5000),
        secret_key=os.getenv("SECRET_KEY", "change-me-in-production"),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        log_file=BASE_DIR / os.getenv("LOG_FILE", "logs/app.log"),
        database_url=os.getenv("DATABASE_URL", "sqlite:///database/app.db"),
        storage_path=BASE_DIR / os.getenv("STORAGE_PATH", "storage"),
    )
