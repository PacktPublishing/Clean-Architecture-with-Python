# todo_app/infrastructure/logging/config.py
from logging.config import dictConfig
from pathlib import Path
import json
import logging
from datetime import datetime, timezone
from typing import Literal


class JsonFormatter(logging.Formatter):
    """Formats log records as JSON."""

    def __init__(self, app_context: str):
        super().__init__()
        self.app_context = app_context

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "source": self.app_context,
        }

        # Add extra context if present
        if hasattr(record, "extra"):
            log_data.update(record.extra)

        return json.dumps(log_data)


def configure_logging(app_context: Literal["CLI", "WEB"]) -> None:
    """
    Configure application logging with sensible defaults.

    Args:
        app_context: Whether this is CLI or WEB context
    """
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    config = {
        "version": 1,
        "formatters": {
            "json": {"()": JsonFormatter, "app_context": app_context},
            "standard": {"format": "%(message)s"},
        },
        "handlers": {
            # Standard console output (for Flask)
            "standard_console": {"class": "logging.StreamHandler", "formatter": "standard"},
            # JSON console output (for our app)
            "json_console": {"class": "logging.StreamHandler", "formatter": "json"},
            # File handlers
            "app_file": {
                "class": "logging.FileHandler",
                "filename": log_dir / "app.log",
                "formatter": "json",
            },
            "access_file": {
                "class": "logging.FileHandler",
                "filename": log_dir / "access.log",
                "formatter": "standard",
            },
        },
        "loggers": {
            # Application logger
            "todo_app": {
                "handlers": ["app_file"] if app_context == "CLI" else ["json_console", "app_file"],
                "level": "INFO",
            },
            # Flask's werkzeug logger
            "werkzeug": {
                "handlers": ["standard_console", "access_file"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }

    dictConfig(config)
