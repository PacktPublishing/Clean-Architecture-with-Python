# todo_app/application/service_ports/notifications.py
"""
This module defines the notification interface (port) for external notification services.
"""

from abc import ABC, abstractmethod

from todo_app.domain.entities.task import Task


class NotificationPort(ABC):
    """Interface for sending notifications about task events."""

    @abstractmethod
    def notify_task_completed(self, task: Task) -> None:
        """Notify when a task is completed."""
        pass

    @abstractmethod
    def notify_task_high_priority(self, task: Task) -> None:
        """Notify when a task is set to high priority."""
        pass

    @abstractmethod
    def notify_task_deadline_approaching(self, task: Task, days_remaining: int) -> None:
        """Notify when a task's deadline is approaching."""
        pass
