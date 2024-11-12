from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID

from Chapter_5.TodoApp.todo_app.domain.entities.entity import Entity
from Chapter_5.TodoApp.todo_app.domain.value_objects import (
    Deadline,
    Priority,
    TaskStatus,
)


@dataclass
class Task(Entity):
    """A task that needs to be completed."""

    title: str
    description: str
    due_date: Optional[Deadline] = None
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = field(default=TaskStatus.TODO, init=False)
    completed_at: Optional[datetime] = field(default=None, init=False)
    completion_notes: Optional[str] = field(default=None, init=False)
    project_id: Optional[UUID] = field(default=None, init=False)

    def start(self) -> None:
        """Mark the task as in progress."""
        if self.status != TaskStatus.TODO:
            raise ValueError("Only tasks with 'TODO' status can be started")
        self.status = TaskStatus.IN_PROGRESS

    def complete(self, notes: Optional[str] = None) -> None:
        """
        Mark the task as complete.

        Args:
            notes: Optional completion notes

        Raises:
            ValueError: If task is already completed
        """
        if self.status == TaskStatus.DONE:
            raise ValueError("Task is already completed")
        self.status = TaskStatus.DONE
        self.completed_at = datetime.now()
        self.completion_notes = notes

    def is_overdue(self) -> bool:
        """Check if the task is overdue."""
        return self.due_date is not None and self.due_date.is_overdue()
