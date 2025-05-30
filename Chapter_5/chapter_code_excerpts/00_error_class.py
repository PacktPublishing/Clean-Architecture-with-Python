from dataclasses import dataclass
from enum import Enum
from typing import Optional, Any, Self


class ErrorCode(Enum):
    NOT_FOUND = "NOT_FOUND"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    # Add other error codes as needed


@dataclass(frozen=True)
class Error:
    """Standardized error information"""

    code: ErrorCode
    message: str
    details: Optional[dict[str, Any]] = None

    @classmethod
    def not_found(cls, entity: str, entity_id: str) -> Self:
        return cls(
            code=ErrorCode.NOT_FOUND,
            message=f"{entity} with id {entity_id} not found",
        )

    @classmethod
    def validation_error(cls, message: str) -> Self:
        return cls(code=ErrorCode.VALIDATION_ERROR, message=message)
