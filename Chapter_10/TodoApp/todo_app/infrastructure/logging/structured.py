from dataclasses import dataclass
import json
import logging
from typing import Any, Dict, Optional

from todo_app.infrastructure.config import Config
from .base import ApplicationLogger


class JsonFormatter(logging.Formatter):
    """Custom formatter that outputs everything as JSON."""

    def format(self, record: logging.LogRecord) -> str:
        """Format the record as a JSON string."""
        # Get the log message (our JSON context) from the record
        try:
            # Parse our JSON context from the message
            log_data = json.loads(record.msg)
            # Add logging-specific fields
            log_data["log_level"] = record.levelname
            return json.dumps(log_data)
        except json.JSONDecodeError:
            # Fallback if message isn't JSON
            return json.dumps({"log_level": record.levelname, "message": record.msg})


@dataclass
class StructuredLogger(ApplicationLogger):
    """JSON structured logging implementation."""

    def __post_init__(self) -> None:
        self._logger = self._get_configured_logger()

    @staticmethod
    def _get_configured_logger() -> logging.Logger:
        """Get or create configured logger instance."""
        logger = logging.getLogger("todo_app")

        # Only configure if not already configured
        if not logger.handlers:
            # Create and add handlers with JSON formatter
            handlers = StructuredLogger._create_handlers(None)  # formatter not needed

            for handler in handlers:
                logger.addHandler(handler)

            logger.setLevel(logging.INFO)

        return logger

    @staticmethod
    def _create_handlers(formatter: Optional[logging.Formatter] = None) -> list[logging.Handler]:
        """Create handlers with JSON formatting."""
        handlers = []
        json_formatter = JsonFormatter()

        # File handler
        try:
            log_path = Config.get_log_file_path()
            file_handler = logging.FileHandler(log_path)
            file_handler.setFormatter(json_formatter)
            handlers.append(file_handler)
        except Exception as e:
            # Log setup error through console
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(json_formatter)
            handlers.append(console_handler)

        # Always add console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(json_formatter)
        handlers.append(console_handler)

        return handlers

    def _log(self, level: int, msg: str, *, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log with JSON formatting."""
        context = self._format_context(msg, extra)
        # Send as JSON string that our formatter will parse
        self._logger.log(level, json.dumps(context))
