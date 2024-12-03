from dataclasses import dataclass, field
from datetime import datetime
from inspect import stack
from typing import Optional
from uuid import UUID

from todo_app.domain.exceptions import BusinessRuleViolation
from todo_app.domain.entities.entity import Entity
from todo_app.domain.entities.task import Task
from todo_app.domain.value_objects import (
    ProjectType,
    TaskStatus,
    ProjectStatus,
)


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

    def __post_init__(self) -> None:
        # Only allow INBOX_NAME as project name if created via create_inbox()
        if self.name == self.INBOX_NAME:
            caller_frames = stack()
            create_inbox_called = any(frame.function == "create_inbox" for frame in caller_frames)
            if not create_inbox_called:
                raise BusinessRuleViolation(f"'{self.INBOX_NAME}' is a reserved name.")

    @classmethod
    def create_inbox(cls) -> "Project":
        return cls(
            name="INBOX",
            description="Default project for unassigned tasks",
            project_type=ProjectType.INBOX,
        )

    def add_task(self, task: Task) -> None:
        """Add a task to the project."""
        if self.status == ProjectStatus.COMPLETED:
            raise ValueError("Cannot add tasks to a completed project")
        self._tasks[task.id] = task
        task.project_id = self.id

    def get_task(self, task_id: UUID) -> Optional[Task]:
        """Get a task by its ID."""
        return self._tasks.get(task_id)

    @property
    def tasks(self) -> list[Task]:
        """Get all tasks in the project."""
        return list(self._tasks.values())

    @property
    def incomplete_tasks(self) -> list[Task]:
        """Get all incomplete tasks in the project."""
        return [task for task in self.tasks if task.status != TaskStatus.DONE]

    def mark_completed(self, notes: Optional[str] = None) -> None:
        """
        Mark the project as completed.

        Args:
            notes: Optional completion notes
        """
        if self.name == self.INBOX_NAME:
            raise BusinessRuleViolation("The INBOX project cannot be completed")
        self.status = ProjectStatus.COMPLETED
        self.completed_at = datetime.now()
        self.completion_notes = notes
