"""
This module contains request and response data transfer objects (DTOs) for project operations.
These DTOs handle data transformation between the outer layers and the application core.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Sequence, Self
from uuid import UUID

from todo_app.domain.exceptions import BusinessRuleViolation
from todo_app.domain.value_objects import ProjectStatus
from todo_app.application.dtos.task_dtos import TaskResponse
from todo_app.domain.entities.project import Project


@dataclass(frozen=True)
class CreateProjectRequest:
    """Request data for creating a new project."""

    name: str
    description: str = ""

    def __post_init__(self) -> None:
        """Validate request data"""
        if not self.name.strip():
            raise ValueError("Project name is required")
        if len(self.name) > 100:
            raise ValueError("Project name cannot exceed 100 characters")
        if len(self.description) > 2000:
            raise ValueError("Description cannot exceed 2000 characters")

    def to_execution_params(self) -> dict:
        """Convert request data to use case parameters."""
        return {
            "name": self.name.strip(),
            "description": self.description.strip(),
        }


@dataclass(frozen=True)
class CompleteProjectRequest:
    """Request data for completing a project."""

    project_id: str
    completion_notes: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate request data"""
        if not self.project_id.strip():
            raise ValueError("Project ID is required")
        if self.completion_notes and len(self.completion_notes) > 1000:
            raise ValueError("Completion notes cannot exceed 1000 characters")
        try:
            UUID(self.project_id)
        except ValueError:
            raise ValueError("Invalid project ID format")

    def to_execution_params(self) -> dict:
        """Convert request data to use case parameters."""
        return {
            "project_id": UUID(self.project_id),
            "completion_notes": self.completion_notes,
        }


@dataclass(frozen=True)
class ProjectResponse:
    """Response data for basic project operations."""

    id: str
    name: str
    description: str
    status: ProjectStatus
    completion_date: Optional[datetime]
    tasks: Sequence[TaskResponse]

    @classmethod
    def from_entity(cls, project: Project) -> Self:
        """Create response from a Project entity."""
        return cls(
            id=str(project.id),
            name=project.name,
            description=project.description,
            status=project.status,
            completion_date=project.completed_at if project.completed_at else None,
            tasks=[TaskResponse.from_entity(task) for task in project.tasks],
        )


@dataclass(frozen=True)
class CompleteProjectResponse:
    """Response data specific to project completion."""

    id: str
    status: ProjectStatus
    completion_date: datetime
    task_count: int
    completion_notes: Optional[str]

    @classmethod
    def from_entity(cls, project: Project) -> Self:
        """Create response from a Project entity."""
        if project.completed_at is None:
            raise BusinessRuleViolation("Project does not have a completion date")
        return cls(
            id=str(project.id),
            status=project.status,
            completion_date=project.completed_at,
            task_count=len(project.tasks),
            completion_notes=project.completion_notes,
        )
