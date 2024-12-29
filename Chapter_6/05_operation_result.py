"""
At our architectural boundaries, we need clear, consistent ways to handle 
both successful operations and failures. Operations can fail for many 
reasons - invalid input, business rule violations, or system errors - and 
each type of failure might need different handling by the external interface. 
Similarly, successful operations need to provide their results in a format 
suitable for the interface that requested them. We've seen this mechanism 
in play in the controller examples shown earlier. 

class TaskController: 
     
    def handle_create( 
        self,  
        title: str,  
        description: str 
    ) -> OperationResult[TaskViewModel]:
"""

from dataclasses import dataclass


@dataclass
class OperationResult(Generic[T]):
    """Represents the outcome of controller operations."""

    _success: Optional[T] = None

    _error: Optional[ErrorViewModel] = None

    @classmethod
    def succeed(cls, value: T) -> "OperationResult[T]":
        """Create a successful result with the given view model."""

        return cls(_success=value)

    @classmethod
    def fail(cls, message: str, code: Optional[str] = None) -> "OperationResult[T]":
        """Create a failed result with error details."""

        return cls(_error=ErrorViewModel(message, code))
