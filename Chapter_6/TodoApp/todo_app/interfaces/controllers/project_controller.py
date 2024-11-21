from dataclasses import dataclass
from typing import Optional

from todo_app.interfaces.presenters.base import ProjectPresenter
from todo_app.interfaces.view_models.base import OperationResult
from todo_app.application.dtos.project_dtos import CompleteProjectRequest, CreateProjectRequest
from todo_app.application.use_cases.project_use_cases import CompleteProjectUseCase, CreateProjectUseCase


@dataclass
class ProjectController:
    """Controller for project-related operations."""
    create_use_case: CreateProjectUseCase
    complete_use_case: CompleteProjectUseCase
    presenter: ProjectPresenter

    def handle_create(self, name: str, description: str = "") -> OperationResult:
        """Handle project creation request."""
        try:
            request = CreateProjectRequest(name=name, description=description)
            result = self.create_use_case.execute(request)
            
            if result.is_success:
                view_model = self.presenter.present_project(result.value)
                return OperationResult.succeed(view_model)
            
            error_vm = self.presenter.present_error(
                result.error.message,
                str(result.error.code)
            )
            return OperationResult.fail(error_vm.message, error_vm.code)
            
        except ValueError as e:
            error_vm = self.presenter.present_error(str(e), "VALIDATION_ERROR")
            return OperationResult.fail(error_vm.message, error_vm.code)

    def handle_complete(self, project_id: str, notes: Optional[str] = None) -> OperationResult:
        """Handle project completion request."""
        try:
            request = CompleteProjectRequest(project_id=project_id, completion_notes=notes)
            result = self.complete_use_case.execute(request)
            
            if result.is_success:
                view_model = self.presenter.present_project(result.value)
                return OperationResult.succeed(view_model)
            
            error_vm = self.presenter.present_error(
                result.error.message,
                str(result.error.code)
            )
            return OperationResult.fail(error_vm.message, error_vm.code)
            
        except ValueError as e:
            error_vm = self.presenter.present_error(str(e), "VALIDATION_ERROR")
            return OperationResult.fail(error_vm.message, error_vm.code)