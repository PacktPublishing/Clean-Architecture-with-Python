"""
This module contains use cases for project operations.
"""

from dataclasses import dataclass

from Chapter_5.ToDoApp.todo_app.application.common.result import Result, Error
from Chapter_5.ToDoApp.todo_app.application.dtos.project_dtos import (
    CreateProjectRequest,
    ProjectResponse,
    CompleteProjectRequest,
    ProjectCompletionResponse,
)
from Chapter_5.ToDoApp.todo_app.application.repositories.project_repository import (
    ProjectRepository,
)
from Chapter_5.ToDoApp.todo_app.domain.entities.project import Project
from Chapter_5.ToDoApp.todo_app.domain.exceptions import (
    ValidationError,
    BusinessRuleViolation,
    ProjectNotFoundError,
)


@dataclass
class CreateProjectUseCase:
    """Use case for creating a new project."""

    project_repository: ProjectRepository

    def execute(self, request: CreateProjectRequest) -> Result:
        """Execute the use case."""
        try:
            params = request.to_execution_params()

            project = Project(
                name=params["name"], description=params["description"]
            )

            self.project_repository.save(project)

            return Result.success(ProjectResponse.from_entity(project))

        except ValidationError as e:
            return Result.failure(Error.validation_error(str(e)))
        except BusinessRuleViolation as e:
            return Result.failure(Error.business_rule_violation(str(e)))


@dataclass
class CompleteProjectUseCase:
    """Use case for marking a project as complete."""

    project_repository: ProjectRepository

    def execute(self, request: CompleteProjectRequest) -> Result:
        """Execute the use case."""
        try:
            params = request.to_execution_params()

            project = self.project_repository.get(params["project_id"])
            project.mark_completed(
                notes=params["completion_notes"],
            )

            self.project_repository.save(project)

            return Result.success(
                ProjectCompletionResponse.from_entity(project)
            )

        except ProjectNotFoundError:
            return Result.failure(
                Error.not_found("Project", str(params["project_id"]))
            )
        except ValidationError as e:
            return Result.failure(Error.validation_error(str(e)))
        except BusinessRuleViolation as e:
            return Result.failure(Error.business_rule_violation(str(e)))
