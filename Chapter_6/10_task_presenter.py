from abc import ABC, abstractmethod
from typing import Optional


class TaskPresenter(ABC):
    """Abstract base presenter for task-related output."""

    @abstractmethod
    def present_task(self, task_response: TaskResponse) -> TaskViewModel:
        """Convert task response to view model."""

        pass

    @abstractmethod
    def present_error(self, error_msg: str, code: Optional[str] = None) -> ErrorViewModel:
        """Format error message for display."""

        pass
