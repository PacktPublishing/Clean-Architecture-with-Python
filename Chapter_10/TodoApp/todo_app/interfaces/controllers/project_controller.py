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
from todo_app.application.dtos.project_dtos import CompleteProjectRequest, CreateProjectRequest, UpdateProjectRequest
from todo_app.application.use_cases.project_use_cases import (
    CompleteProjectUseCase,
    CreateProjectUseCase,
    GetProjectUseCase,
    ListProjectsUseCase,
    UpdateProjectUseCase,
)

import logging

logger = logging.getLogger(__name__)

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
        update_use_case: Use case for updating projects
    """

    create_use_case: CreateProjectUseCase
    complete_use_case: CompleteProjectUseCase
    presenter: ProjectPresenter
    get_use_case: GetProjectUseCase
    list_use_case: ListProjectsUseCase
    update_use_case: UpdateProjectUseCase

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
            logger.info(
                "Handling project creation request",
                extra={"context": {"name": name}},
            )
            request = CreateProjectRequest(name=name, description=description)
            result = self.create_use_case.execute(request)

            if result.is_success:
                view_model = self.presenter.present_project(result.value)
                logger.info(
                    "Project creation handled successfully",
                    extra={"context": {"project_id": str(result.value.id)}},
                )
                return OperationResult.succeed(view_model)

            logger.error(
                "Project creation failed",
                extra={
                    "context": {
                        "name": name,
                        "error": result.error.message,
                        "error_code": str(result.error.code.name),
                    }
                },
            )
            error_vm = self.presenter.present_error(
                result.error.message, str(result.error.code.name)
            )
            return OperationResult.fail(error_vm.message, error_vm.code)

        except ValueError as e:
            logger.error(
                "Validation error in project creation",
                extra={"context": {"name": name, "error": str(e)}},
            )
            error_vm = self.presenter.present_error(str(e), "VALIDATION_ERROR")
            return OperationResult.fail(error_vm.message, error_vm.code)

    def handle_complete(self, project_id: str, notes: Optional[str] = None) -> OperationResult:
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
            logger.info(
                "Handling project completion request",
                extra={"context": {"project_id": project_id}},
            )
            request = CompleteProjectRequest(project_id=project_id, completion_notes=notes)
            result = self.complete_use_case.execute(request)

            if result.is_success:
                view_model = self.presenter.present_project(result.value)
                logger.info(
                    "Project completion handled successfully",
                    extra={"context": {"project_id": project_id}},
                )
                return OperationResult.succeed(view_model)

            logger.error(
                "Project completion failed",
                extra={
                    "context": {
                        "project_id": project_id,
                        "error": result.error.message,
                        "error_code": str(result.error.code.name),
                    }
                },
            )
            error_vm = self.presenter.present_error(
                result.error.message, str(result.error.code.name)
            )
            return OperationResult.fail(error_vm.message, error_vm.code)

        except ValueError as e:
            logger.error(
                "Validation error in project completion",
                extra={"context": {"project_id": project_id, "error": str(e)}},
            )
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
            logger.info(
                "Handling project retrieval request",
                extra={"context": {"project_id": project_id}},
            )
            result = self.get_use_case.execute(project_id)

            if result.is_success:
                view_model = self.presenter.present_project(result.value)
                logger.info(
                    "Project retrieval handled successfully",
                    extra={"context": {"project_id": project_id}},
                )
                return OperationResult.succeed(view_model)

            logger.error(
                "Project retrieval failed",
                extra={
                    "context": {
                        "project_id": project_id,
                        "error": result.error.message,
                        "error_code": str(result.error.code.name),
                    }
                },
            )
            error_vm = self.presenter.present_error(
                result.error.message, str(result.error.code.name)
            )
            return OperationResult.fail(error_vm.message, error_vm.code)

        except ValueError as e:
            logger.error(
                "Validation error in project retrieval",
                extra={"context": {"project_id": project_id, "error": str(e)}},
            )
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
        logger.info("Handling project list request")
        result = self.list_use_case.execute()

        if result.is_success:
            view_models = [self.presenter.present_project(proj) for proj in result.value]
            logger.info(
                "Project list handled successfully",
                extra={"context": {"count": len(view_models)}},
            )
            return OperationResult.succeed(view_models)

        logger.error(
            "Project list failed",
            extra={
                "context": {
                    "error": result.error.message,
                    "error_code": str(result.error.code.name),
                }
            },
        )
        error_vm = self.presenter.present_error(result.error.message, str(result.error.code.name))
        return OperationResult.fail(error_vm.message, error_vm.code)

    def handle_update(
        self, 
        project_id: str, 
        name: Optional[str] = None, 
        description: Optional[str] = None
    ) -> OperationResult:
        """
        Handle project update requests.

        Args:
            project_id: The unique identifier of the project
            name: Optional new name for the project
            description: Optional new description for the project

        Returns:
            OperationResult containing either:
            - Success: Updated ProjectViewModel
            - Failure: Error information
        """
        try:
            logger.info(
                "Handling project update request",
                extra={
                    "context": {
                        "project_id": project_id,
                        "update_fields": [f for f, v in [("name", name), ("description", description)] if v is not None],
                    }
                },
            )
            request = UpdateProjectRequest(
                project_id=project_id,
                name=name,
                description=description
            )
            result = self.update_use_case.execute(request)

            if result.is_success:
                view_model = self.presenter.present_project(result.value)
                logger.info(
                    "Project update handled successfully",
                    extra={"context": {"project_id": project_id}},
                )
                return OperationResult.succeed(view_model)

            logger.error(
                "Project update failed",
                extra={
                    "context": {
                        "project_id": project_id,
                        "error": result.error.message,
                        "error_code": str(result.error.code.name),
                    }
                },
            )
            error_vm = self.presenter.present_error(
                result.error.message, str(result.error.code.name)
            )
            return OperationResult.fail(error_vm.message, error_vm.code)

        except ValueError as e:
            logger.error(
                "Validation error in project update",
                extra={"context": {"project_id": project_id, "error": str(e)}},
            )
            error_vm = self.presenter.present_error(str(e), "VALIDATION_ERROR")
            return OperationResult.fail(error_vm.message, error_vm.code)
