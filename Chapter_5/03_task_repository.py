from abc import abstractmethod, ABC
from uuid import UUID

from Chapter_5.TodoApp.todo_app.domain.entities.task import Task


class TaskRepository(ABC):
    """Repository interface defined by the Application Layer"""

    @abstractmethod
    def get(self, task_id: UUID) -> Task:
        """Retrieve a task by its ID"""
        pass

    @abstractmethod
    def save(self, task: Task) -> None:
        """Save a task to the repository"""
        pass

    @abstractmethod
    def delete(self, task_id: UUID) -> None:
        """Delete a task from the repository"""
        pass


class NotificationService(ABC):
    """Service interface for sending notifications"""

    @abstractmethod
    def notify_task_assigned(self, task_id: UUID) -> None:
        """Notify when a task is assigned"""
        pass

    @abstractmethod
    def notify_task_completed(self, task_id: UUID) -> None:
        """Notify when a task is completed"""
        pass
