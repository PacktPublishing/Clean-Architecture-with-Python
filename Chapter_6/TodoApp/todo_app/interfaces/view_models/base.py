from dataclasses import dataclass
from typing import Optional, Self


@dataclass(frozen=True)
class ErrorViewModel:
    """View-specific representation of an error."""
    message: str
    code: Optional[str] = None  # For categorizing errors if needed

@dataclass(frozen=True)
class OperationResult[T]:
    """Container for operation results."""
    success: Optional[T] = None
    error: Optional[ErrorViewModel] = None

    @property
    def is_success(self) -> bool:
        return self.success is not None

    @classmethod
    def succeed(cls, task: T) -> "OperationResult[T]":
        return cls(success=task)

    @classmethod
    def fail(cls, message: str, code: Optional[str] = None) -> "OperationResult[T]":
        return cls(error=ErrorViewModel(message=message, code=code))