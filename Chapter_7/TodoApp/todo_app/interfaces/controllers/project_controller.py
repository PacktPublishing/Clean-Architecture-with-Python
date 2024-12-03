"""
This module contains the project controller implementing Clean Architecture's Interface Adapters layer.

The project controller demonstrates:
1. How controllers route between interfaces and use cases
2. Clean conversion between external and internal data formats
3. Proper error handling and formatting for interfaces
4. Adherence to the Dependency Rule
"""

from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from todo_app.interfaces.view_models.project_vm import ProjectViewModel
from todo_app.interfaces.presenters.base import ProjectPresenter
from todo_app.interfaces.view_models.base import OperationResult
from todo_app.application.dtos.project_dtos import CompleteProjectRequest, CreateProjectRequest
from todo_app.application.use_cases.project_use_cases import (
    CompleteProjectUseCase,
    CreateProjectUseCase,
    GetProjectUseCase,
    ListProjectsUseCase,
)


@dataclass
class ProjectController:
    """
    Controller for project-related operations, implementing Clean Architecture patterns.

    This controller demonstrates key Clean Architecture principles:
    - Controllers exist in the Interface Adapters layer
    - They depend inward on use cases (Dependency Rule)
    - They handle data conversion between layers
    - They isolate interface concerns from business logic

    Benefits of this Clean Architecture implementation:
    - Business logic remains protected in use cases
    - New interfaces can be added without changing core logic
    - Testing is simplified through dependency injection
    - Presentation concerns are properly separated

    Attributes:
        create_use_case: Use case for creating projects
        complete_use_case: Use case for completing projects
        presenter: Handles formatting of project data for the interface
    """

    create_use_case: CreateProjectUseCase
    complete_use_case: CompleteProjectUseCase
    presenter: ProjectPresenter
    get_use_case: GetProjectUseCase
    list_use_case: ListProjectsUseCase

    def handle_create(self, name: str, description: str = "") -> OperationResult:
        """
        Handle project creation requests from any interface.

        This method follows Clean Architecture by:
        1. Accepting primitive types (making it interface-agnostic)
        2. Converting data to use case format
        3. Executing business logic through use cases
        4. Converting responses to interface-appropriate format

        Args:
            name: The project name
            description: Optional project description

        Returns:
            OperationResult containing either:
            - Success: ProjectViewModel formatted for the interface
            - Failure: Error information formatted for the interface
        """
        try:
            request = CreateProjectRequest(name=name, description=description)
            result = self.create_use_case.execute(request)

            if result.is_success:
                view_model = self.presenter.present_project(result.value)
                return OperationResult.succeed(view_model)

            error_vm = self.presenter.present_error(
                result.error.message, str(result.error.code.name)
            )
            return OperationResult.fail(error_vm.message, error_vm.code)

        except ValueError as e:
            error_vm = self.presenter.present_error(str(e), "VALIDATION_ERROR")
            return OperationResult.fail(error_vm.message, error_vm.code)

    def handle_complete(self, project_id: UUID, notes: Optional[str] = None) -> OperationResult:
        """
        Handle project completion requests from any interface.

        Demonstrates Clean Architecture benefits:
        1. Interface agnostic - same method works for any interface
        2. Business logic isolation in use cases
        3. Proper error handling and formatting for interfaces

        Args:
            project_id: The unique identifier of the project
            notes: Optional completion notes

        Returns:
            OperationResult containing either:
            - Success: ProjectViewModel with completion information
            - Failure: Error information formatted for the interface
        """
        try:
            request = CompleteProjectRequest(project_id=str(project_id), completion_notes=notes)
            result = self.complete_use_case.execute(request)

            if result.is_success:
                view_model = self.presenter.present_project(result.value)
                return OperationResult.succeed(view_model)

            error_vm = self.presenter.present_error(
                result.error.message, str(result.error.code.name)
            )
            return OperationResult.fail(error_vm.message, error_vm.code)

        except ValueError as e:
            error_vm = self.presenter.present_error(str(e), "VALIDATION_ERROR")
            return OperationResult.fail(error_vm.message, error_vm.code)

    def handle_get(self, project_id: str) -> OperationResult[ProjectViewModel]:
        """
        Handle project retrieval requests.

        Args:
            project_id: The unique identifier of the project

        Returns:
            OperationResult containing either:
            - Success: ProjectViewModel with project details
            - Failure: Error information
        """
        try:
            result = self.get_use_case.execute(project_id)

            if result.is_success:
                view_model = self.presenter.present_project(result.value)
                return OperationResult.succeed(view_model)

            error_vm = self.presenter.present_error(
                result.error.message, str(result.error.code.name)
            )
            return OperationResult.fail(error_vm.message, error_vm.code)

        except ValueError as e:
            error_vm = self.presenter.present_error(str(e), "VALIDATION_ERROR")
            return OperationResult.fail(error_vm.message, error_vm.code)

    def handle_list(self) -> OperationResult[list[ProjectViewModel]]:
        """
        Handle project listing requests.

        Returns:
            OperationResult containing either:
            - Success: List of ProjectViewModel objects
            - Failure: Error information
        """
        result = self.list_use_case.execute()

        if result.is_success:
            view_models = [self.presenter.present_project(proj) for proj in result.value]
            return OperationResult.succeed(view_models)

        error_vm = self.presenter.present_error(result.error.message, str(result.error.code.name))
        return OperationResult.fail(error_vm.message, error_vm.code)
