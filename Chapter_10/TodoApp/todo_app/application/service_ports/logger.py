from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class Logger(ABC):
    """Interface for logging operations across architectural boundaries."""

    @abstractmethod
    def debug(self, msg: str, *, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log a debug-level message with optional structured data."""
        pass

    @abstractmethod
    def info(self, msg: str, *, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log an info-level message with optional structured data."""
        pass

    @abstractmethod
    def warning(self, msg: str, *, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log a warning-level message with optional structured data."""
        pass

    @abstractmethod
    def error(self, msg: str, *, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log an error-level message with optional structured data."""
        pass

    @abstractmethod
    def critical(self, msg: str, *, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log a critical-level message with optional structured data."""
        pass
