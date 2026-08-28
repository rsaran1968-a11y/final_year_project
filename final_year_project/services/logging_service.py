from __future__ import annotations

import logging
from logging.config import dictConfig
from pathlib import Path

from config import AppConfig


def configure_logging(config: AppConfig) -> None:
    """Configure application logging for console and file output."""
    log_file = Path(config.log_file)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                    "level": config.log_level,
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "standard",
                    "level": config.log_level,
                    "filename": str(log_file),
                    "maxBytes": 10_485_760,
                    "backupCount": 5,
                    "encoding": "utf-8",
                },
            },
            "root": {
                "handlers": ["console", "file"],
                "level": config.log_level,
            },
        }
    )

    logging.getLogger(__name__).info("Logging configured for %s", config.app_name)
