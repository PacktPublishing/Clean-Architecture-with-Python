# todo_app/infrastructure/logging/config.py
from logging.config import dictConfig
from pathlib import Path
import json
import logging
from datetime import datetime, timezone
from typing import Literal
from uuid import UUID
from todo_app.infrastructure.logging.trace import get_trace_id


class JsonLogEncoder(json.JSONEncoder):
    """Custom JSON encoder for log records."""

    def default(self, o):
        # Handle common types that json.dumps can't handle natively
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, UUID):
            return str(o)
        if isinstance(o, set):
            return list(o)
        if isinstance(o, Exception):
            return str(o)
        # Let the base class handle anything else
        return super().default(o)


class JsonFormatter(logging.Formatter):
    """Formats log records as JSON."""

    def __init__(self, app_context: str):
        super().__init__()
        self.app_context = app_context
        self.encoder = JsonLogEncoder()

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.now(timezone.utc),  # Let encoder handle datetime
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "app_context": self.app_context,
            "trace_id": get_trace_id(),
        }

        if hasattr(record, "extra"):
            log_data.update(record.extra)

        return self.encoder.encode(log_data)


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
            "standard": {
                "format": "%(asctime)s [%(trace_id)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
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
