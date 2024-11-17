"""
This module contains the core error handling and result types for the application layer.
These types provide a consistent way to handle success and failure cases across all use cases.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Self


class ErrorCode(Enum):
    """Enumeration of possible error codes in the application layer."""

    NOT_FOUND = "NOT_FOUND"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    BUSINESS_RULE_VIOLATION = "BUSINESS_RULE_VIOLATION"
    UNAUTHORIZED = "UNAUTHORIZED"
    CONFLICT = "CONFLICT"


@dataclass(frozen=True)
class Error:
    """
    Represents an error that occurred during use case execution.

    This class provides a standardized way to represent errors across the application layer,
    including the specific type of error (via ErrorCode) and any additional context.

    Attributes:
        code: The type of error that occurred
        message: A human-readable description of the error
        details: Optional additional context about the error
    """

    code: ErrorCode
    message: str
    details: Optional[dict[str, Any]] = None

    @classmethod
    def not_found(cls, entity: str, entity_id: str) -> Self:
        """Create a NOT_FOUND error for a specific entity."""
        return cls(
            code=ErrorCode.NOT_FOUND,
            message=f"{entity} with id {entity_id} not found",
        )

    @classmethod
    def validation_error(cls, message: str) -> Self:
        """Create a VALIDATION_ERROR with the specified message."""
        return cls(code=ErrorCode.VALIDATION_ERROR, message=message)

    @classmethod
    def business_rule_violation(cls, message: str) -> Self:
        """Create a BUSINESS_RULE_VIOLATION error with the specified message."""
        return cls(code=ErrorCode.BUSINESS_RULE_VIOLATION, message=message)


@dataclass(frozen=True)
class Result:
    """
    Represents the outcome of a use case execution, either success or failure.

    This class provides a way to handle both successful and failed outcomes,
    ensuring that error handling is explicit and consistent across the application layer.

    Attributes:
        value: The success value (if successful)
        error: The error details (if failed)
    """

    value: Any = None
    error: Optional[Error] = None

    @property
    def is_success(self) -> bool:
        """Check if the result represents a successful operation."""
        return self.error is None

    @classmethod
    def success(cls, value: Any) -> Self:
        """Create a successful result with the given value."""
        return cls(value=value)

    @classmethod
    def failure(cls, error: Error) -> Self:
        """Create a failed result with the given error."""
        return cls(error=error)
