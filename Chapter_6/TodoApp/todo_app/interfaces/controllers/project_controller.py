from dataclasses import dataclass
from typing import Optional

from todo_app.interfaces.presenters.base import ProjectPresenter
from todo_app.application.common.result import Result
from todo_app.application.dtos.project_dtos import CompleteProjectRequest, CreateProjectRequest
from todo_app.application.use_cases.project_use_cases import CompleteProjectUseCase, CreateProjectUseCase


@dataclass
class ProjectController:
    """Controller for project-related operations."""
    create_use_case: CreateProjectUseCase
    complete_use_case: CompleteProjectUseCase
    presenter: ProjectPresenter

    def handle_create(self, name: str, description: str = "") -> Result:
        """Handle project creation request."""
        request = CreateProjectRequest(name=name, description=description)
        result = self.create_use_case.execute(request)
        return result

    def handle_complete(self, project_id: str, notes: Optional[str] = None) -> Result:
        """Handle project completion request."""
        request = CompleteProjectRequest(project_id=project_id, completion_notes=notes)
        result = self.complete_use_case.execute(request)
        return result