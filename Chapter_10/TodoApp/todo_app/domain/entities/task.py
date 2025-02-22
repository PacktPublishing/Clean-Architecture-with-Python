from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID

from todo_app.domain.entities.entity import Entity
from todo_app.domain.value_objects import (
    Deadline,
    Priority,
    TaskStatus,
)

import logging

logger = logging.getLogger(__name__)


@dataclass
class Task(Entity):
    """A task that needs to be completed."""

    title: str
    description: str
    project_id: UUID
    due_date: Optional[Deadline] = None
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = field(default=TaskStatus.TODO, init=False)
    completed_at: Optional[datetime] = field(default=None, init=False)
    completion_notes: Optional[str] = field(default=None, init=False)

    def start(self) -> None:
        """Mark the task as in progress."""
        if self.status != TaskStatus.TODO:
            logger.error(
                "Attempted to start task with invalid status",
                extra={
                    "context": {
                        "task_id": str(self.id),
                        "task_title": self.title,
                        "current_status": self.status.name,
                    }
                },
            )
            raise ValueError("Only tasks with 'TODO' status can be started")
            
        logger.info(
            "Starting task",
            extra={
                "context": {
                    "task_id": str(self.id),
                    "task_title": self.title,
                    "project_id": str(self.project_id),
                }
            },
        )
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
            logger.error(
                "Attempted to complete already completed task",
                extra={
                    "context": {
                        "task_id": str(self.id),
                        "task_title": self.title,
                        "completed_at": str(self.completed_at),
                    }
                },
            )
            raise ValueError("Task is already completed")
            
        logger.info(
            "Completing task",
            extra={
                "context": {
                    "task_id": str(self.id),
                    "task_title": self.title,
                    "project_id": str(self.project_id),
                    "previous_status": self.status.name,
                }
            },
        )
        self.status = TaskStatus.DONE
        self.completed_at = datetime.now()
        self.completion_notes = notes

    def is_overdue(self) -> bool:
        """Check if the task is overdue."""
        is_overdue = self.due_date is not None and self.due_date.is_overdue()
        if is_overdue:
            logger.warning(
                "Task is overdue",
                extra={
                    "context": {
                        "task_id": str(self.id),
                        "task_title": self.title,
                        "due_date": str(self.due_date),
                        "days_overdue": self.due_date.days_overdue(),
                    }
                },
            )
        return is_overdue
