"""
This module contains request and response data transfer objects (DTOs) for task operations.
These DTOs handle data transformation between the outer layers and the application core.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Self
from uuid import UUID

from todo_app.domain.entities.task import Task
from todo_app.domain.value_objects import Deadline, Priority, TaskStatus


@dataclass(frozen=True)
class CompleteTaskRequest:
    """Request data for completing a task."""

    task_id: str
    completion_notes: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate request data"""
        if not self.task_id.strip():
            raise ValueError("Task ID is required")
        if self.completion_notes and len(self.completion_notes) > 1000:
            raise ValueError("Completion notes cannot exceed 1000 characters")
        try:
            UUID(self.task_id)
        except ValueError:
            raise ValueError("Invalid task ID format")

    def to_execution_params(self) -> dict:
        """Convert request data to use case parameters."""
        return {
            "task_id": UUID(self.task_id),
            "completion_notes": self.completion_notes,
        }


@dataclass(frozen=True)
class CreateTaskRequest:
    """Request data for creating a new task."""

    title: str
    description: str
    due_date: Optional[str] = None
    priority: Optional[str] = None
    project_id: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate request data"""
        if not self.title.strip():
            raise ValueError("Title is required")
        if len(self.title) > 200:
            raise ValueError("Title cannot exceed 200 characters")
        if len(self.description) > 2000:
            raise ValueError("Description cannot exceed 2000 characters")
        if self.project_id:
            try:
                UUID(self.project_id)
            except ValueError:
                raise ValueError("Invalid project ID format")

    def to_execution_params(self) -> dict:
        """Convert request data to use case parameters."""
        params = {
            "title": self.title.strip(),
            "description": self.description.strip(),
        }

        if self.due_date:
            params["deadline"] = Deadline(datetime.fromisoformat(self.due_date))

        if self.priority:
            params["priority"] = Priority[self.priority.upper()]

        if self.project_id:
            params["project_id"] = UUID(self.project_id)

        return params


@dataclass(frozen=True)
class TaskResponse:
    """Response data for crossing Domain->Application boundary."""
    id: str  # UUID conversion needed for boundary crossing
    title: str
    description: str
    status: TaskStatus
    priority: Priority
    due_date: Optional[datetime] = None
    project_id: Optional[UUID] = None
    completion_date: Optional[datetime] = None
    completion_notes: Optional[str] = None

    @classmethod
    def from_entity(cls, task: Task) -> Self:
        """Create response from a Task entity."""
        return cls(
            id=str(task.id),  # Basic conversion for boundary crossing
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            due_date=task.due_date.due_date if task.due_date else None,
            project_id=task.project_id,
            completion_date=task.completed_at,
            completion_notes=task.completion_notes,
        )


@dataclass(frozen=True)
class SetTaskPriorityRequest:
    """Request data for updating task priority."""

    task_id: str
    priority: str

    def __post_init__(self) -> None:
        """Validate request data"""
        if not self.task_id.strip():
            raise ValueError("Task ID is required")

        try:
            priority_value = self.priority.strip().upper()
            if not priority_value:
                raise ValueError
            if priority_value not in [p.name for p in Priority]:
                raise ValueError
        except (AttributeError, ValueError):
            raise ValueError(
                f"Priority must be one of: {', '.join(p.name for p in Priority)}"
            )
        try:
            UUID(self.task_id)
        except ValueError:
            raise ValueError("Invalid task ID format")

    def to_execution_params(self) -> dict:
        """Convert request data to use case parameters."""
        return {
            "task_id": UUID(self.task_id),
            "priority": Priority[self.priority.upper()],
        }
