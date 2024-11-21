from typing import Generic, TypeVar, Optional
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class ErrorViewModel:
    """Represents an error with an optional error code.
    
    Attributes:
        message: A human-readable error message
        code: An optional error code for programmatic error handling
    """
    message: str
    code: Optional[str] = None

@dataclass
class OperationResult(Generic[T]):
    """Represents the result of an operation that can either succeed with a value or fail with an error.
    
    This class implements the Either pattern, where a result can only be either a success
    or a failure, but never both or neither. This helps with explicit error handling and
    avoiding None checks.  It also enables type checking with Mypy and other static type checkers.
    
    Type Parameters:
        T: The type of the success value
        
    Attributes:
        _success: The success value if the operation succeeded
        _error: The error details if the operation failed
    """
    _success: Optional[T] = None
    _error: Optional[ErrorViewModel] = None

    def __init__(self, success: Optional[T] = None, error: Optional[ErrorViewModel] = None):
        """Initialize the result with either a success value or an error.
        
        Args:
            success: The success value if the operation succeeded
            error: The error details if the operation failed
            
        Raises:
            ValueError: If neither or both success and error are provided
        """
        if (success is None and error is None) or (success is not None and error is not None):
            raise ValueError("Either success or error must be provided, but not both")
        self._success = success
        self._error = error

    @property
    def is_success(self) -> bool:
        """Indicates whether the operation was successful."""
        return self._success is not None

    @property
    def success(self) -> T:
        """Returns the success value.
        
        Raises:
            ValueError: If accessing success value on an error result
        """
        if self._success is None:
            raise ValueError("Cannot access success value on error result")
        return self._success

    @property
    def error(self) -> ErrorViewModel:
        """Returns the error details.
        
        Raises:
            ValueError: If accessing error value on a success result
        """
        if self._error is None:
            raise ValueError("Cannot access error value on success result")
        return self._error

    @classmethod
    def succeed(cls, value: T) -> 'OperationResult[T]':
        """Creates a successful result with the given value.
        
        Args:
            value: The success value
            
        Returns:
            A new OperationResult instance representing success
        """
        return cls(success=value)

    @classmethod
    def fail(cls, message: str, code: Optional[str] = None) -> 'OperationResult[T]':
        """Creates a failed result with the given error message and optional code.
        
        Args:
            message: The error message
            code: An optional error code
            
        Returns:
            A new OperationResult instance representing failure
        """
        return cls(error=ErrorViewModel(message, code))
