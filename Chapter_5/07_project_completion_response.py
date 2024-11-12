from dataclasses import dataclass
from typing import Optional, Self

from Chapter_5.TodoApp.todo_app.domain.entities.project import Project


class UserService:
    """Stub to make mypy happy"""

    ...


@dataclass(frozen=True)
class ProjectCompletionResponse:
    """Data structure for project completion responses"""

    id: str
    status: str
    completion_date: str
    task_count: int
    completion_notes: Optional[str]

    @classmethod
    def from_entity(cls, project: Project, user_service: UserService) -> Self:
        """Create response from domain entities"""
        return cls(
            id=str(project.id),
            status=project.status.value,
            completion_date=project.completed_at.isoformat(),
            task_count=len(project.tasks),
            completion_notes=project.completion_notes,
        )
