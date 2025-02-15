import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from todo_app.application.service_ports.logger import Logger
from todo_app.infrastructure.config import Config


@dataclass
class ApplicationLogger(Logger):
    """Base logger implementation using stdlib logging.

    Provides consistent formatting that can evolve to structured logging
    or OpenTelemetry without changing call sites.
    """

    app_context: str  # e.g., "WEB" or "CLI"

    def __post_init__(self) -> None:
        self._logger = self._get_configured_logger()

    @staticmethod
    def _get_configured_logger() -> logging.Logger:
        """Get or create configured logger instance."""
        logger = logging.getLogger("todo_app")

        # Only configure if not already configured
        if not logger.handlers:
            # Extract handler configuration to make format changes easier
            default_format = "%(asctime)s [%(levelname)s] %(message)s"
            default_datefmt = "%Y-%m-%d %H:%M:%S"

            # Create and add new handlers
            handlers = ApplicationLogger._create_handlers(
                formatter=logging.Formatter(default_format, datefmt=default_datefmt)
            )

            for handler in handlers:
                logger.addHandler(handler)

            logger.setLevel(logging.INFO)

        return logger

    @staticmethod
    def _create_handlers(formatter: logging.Formatter) -> list[logging.Handler]:
        """Create and configure all handlers.

        Separating handler creation makes it easier to:
        1. Add new handler types
        2. Modify formatting for all handlers
        3. Evolution to structured logging
        """
        handlers = []

        # Console handler (always enabled)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        handlers.append(console_handler)

        # File handler
        try:
            log_path = Config.get_log_file_path()
            file_handler = logging.FileHandler(log_path)
            file_handler.setFormatter(formatter)
            handlers.append(file_handler)
        except Exception as e:
            # Log through console handler since logger isn't set up yet
            console_handler.handle(
                logging.LogRecord(
                    "todo_app",
                    logging.ERROR,
                    "",
                    0,
                    f"Failed to set up file logging: {str(e)}",
                    (),
                    None,
                )
            )

        return handlers

    def _format_context(self, msg: str, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Prepare structured context for all log messages."""
        context = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "app_context": self.app_context,
            "message": msg,
        }
        if extra:
            context.update(extra)
        return context

    def _log(self, level: int, msg: str, *, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log with formatting."""
        context = self._format_context(msg, extra)
        log_msg = f"{context['timestamp']} [{context['app_context']}] {msg} | {extra}"
        self._logger.log(level, log_msg)

    def debug(self, msg: str, *, extra: Optional[Dict[str, Any]] = None) -> None:
        self._log(logging.DEBUG, msg, extra=extra)

    def info(self, msg: str, *, extra: Optional[Dict[str, Any]] = None) -> None:
        self._log(logging.INFO, msg, extra=extra)

    def warning(self, msg: str, *, extra: Optional[Dict[str, Any]] = None) -> None:
        self._log(logging.WARNING, msg, extra=extra)

    def error(self, msg: str, *, extra: Optional[Dict[str, Any]] = None) -> None:
        self._log(logging.ERROR, msg, extra=extra)

    def critical(self, msg: str, *, extra: Optional[Dict[str, Any]] = None) -> None:
        self._log(logging.CRITICAL, msg, extra=extra)
