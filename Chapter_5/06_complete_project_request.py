from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from Chapter_5.ToDoApp.todo_app.domain.exceptions import ValidationError


@dataclass(frozen=True)
class CompleteProjectRequest:
    """Data structure for project completion requests"""

    project_id: str  # From API (will be converted to UUID)
    completion_notes: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate request data"""
        if not self.project_id.strip():
            raise ValidationError("Project ID is required")

        if self.completion_notes and len(self.completion_notes) > 1000:
            raise ValidationError(
                "Completion notes cannot exceed 1000 characters"
            )

    def to_execution_params(self) -> dict:
        """Convert validated request data to use case parameters"""
        return {
            "project_id": UUID(self.project_id),
            "completion_notes": self.completion_notes,
        }
