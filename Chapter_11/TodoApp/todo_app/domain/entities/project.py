from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID

from todo_app.domain.entities.entity import Entity
from todo_app.domain.entities.task import Task
from todo_app.domain.exceptions import BusinessRuleViolation
from todo_app.domain.value_objects import (
    ProjectType,
    TaskStatus,
    ProjectStatus,
)

import logging

logger = logging.getLogger(__name__)


@dataclass
class Project(Entity):
    """A project containing multiple tasks."""

    INBOX_NAME = "INBOX"  # Class constant for the special inbox name

    name: str
    description: str = ""
    project_type: ProjectType = field(default=ProjectType.REGULAR)
    status: ProjectStatus = field(default=ProjectStatus.ACTIVE, init=False)
    completed_at: Optional[datetime] = field(default=None, init=False)
    completion_notes: Optional[str] = field(default=None, init=False)
    _tasks: dict[UUID, Task] = field(default_factory=dict, init=False)

    @classmethod
    def create_inbox(cls) -> "Project":
        logger.info("Creating INBOX project")
        return cls(
            name="INBOX",
            description="Default project for unassigned tasks",
            project_type=ProjectType.INBOX,
        )

    def add_task(self, task: Task) -> None:
        """Add a task to the project."""
        if self.status == ProjectStatus.COMPLETED:
            logger.error(
                "Attempted to add task to completed project",
                extra={
                    "context": {
                        "project_id": str(self.id),
                        "project_name": self.name,
                        "task_id": str(task.id),
                    }
                },
            )
            raise ValueError("Cannot add tasks to a completed project")
            
        logger.info(
            "Adding task to project",
            extra={
                "context": {
                    "project_id": str(self.id),
                    "project_name": self.name,
                    "task_id": str(task.id),
                    "task_title": task.title,
                }
            },
        )
        self._tasks[task.id] = task
        task.project_id = self.id

    def get_task(self, task_id: UUID) -> Optional[Task]:
        """Get a task by its ID."""
        task = self._tasks.get(task_id)
        if task is None:
            logger.warning(
                "Task not found in project",
                extra={
                    "context": {
                        "project_id": str(self.id),
                        "project_name": self.name,
                        "task_id": str(task_id),
                    }
                },
            )
        return task

    @property
    def tasks(self) -> list[Task]:
        """Get all tasks in the project."""
        logger.debug(
            "Retrieving all tasks from project",
            extra={
                "context": {
                    "project_id": str(self.id),
                    "project_name": self.name,
                    "task_count": len(self._tasks),
                }
            },
        )
        return list(self._tasks.values())

    @property
    def incomplete_tasks(self) -> list[Task]:
        """Get all incomplete tasks in the project."""
        incomplete = [task for task in self.tasks if task.status != TaskStatus.DONE]
        logger.debug(
            "Retrieving incomplete tasks from project",
            extra={
                "context": {
                    "project_id": str(self.id),
                    "project_name": self.name,
                    "incomplete_count": len(incomplete),
                    "total_count": len(self._tasks),
                }
            },
        )
        return incomplete

    def mark_completed(self, notes: Optional[str] = None) -> None:
        """
        Mark the project as completed.

        Args:
            notes: Optional completion notes
        """
        if self.project_type == ProjectType.INBOX:
            logger.error(
                "Attempted to complete INBOX project",
                extra={
                    "context": {
                        "project_id": str(self.id),
                        "project_name": self.name,
                    }
                },
            )
            raise BusinessRuleViolation("The INBOX project cannot be completed")
            
        logger.info(
            "Marking project as completed",
            extra={
                "context": {
                    "project_id": str(self.id),
                    "project_name": self.name,
                    "incomplete_tasks": len(self.incomplete_tasks),
                }
            },
        )
        self.status = ProjectStatus.COMPLETED
        self.completed_at = datetime.now()
        self.completion_notes = notes
