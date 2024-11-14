"""
This module contains use cases for project operations.
"""

from copy import deepcopy
from dataclasses import dataclass

from Chapter_5.TodoApp.todo_app.application.common.result import Result, Error
from Chapter_5.TodoApp.todo_app.application.dtos.project_dtos import (
    CreateProjectRequest,
    ProjectResponse,
    CompleteProjectRequest,
    CompleteProjectResponse,
)
from Chapter_5.TodoApp.todo_app.application.ports.notifications import (
    NotificationPort,
)
from Chapter_5.TodoApp.todo_app.application.repositories.project_repository import (
    ProjectRepository,
)
from Chapter_5.TodoApp.todo_app.application.repositories.task_repository import (
    TaskRepository,
)
from Chapter_5.TodoApp.todo_app.domain.entities.project import Project
from Chapter_5.TodoApp.todo_app.domain.exceptions import (
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
    task_repository: TaskRepository
    notification_service: NotificationPort

    def execute(self, request: CompleteProjectRequest) -> Result:
        """Execute the use case."""
        try:
            params = request.to_execution_params()
            project = self.project_repository.get(params["project_id"])

            # Take snapshots of initial state
            project_snapshot = deepcopy(project)
            task_snapshots = {
                task.id: deepcopy(task) for task in project.incomplete_tasks
            }

            try:
                # Complete all outstanding tasks
                for task in project.incomplete_tasks:
                    task.complete()
                    self.task_repository.save(task)

                project.mark_completed(
                    notes=params["completion_notes"],
                )

                self.project_repository.save(project)
                for task in project_snapshot.incomplete_tasks:
                    self.notification_service.notify_task_completed(task.id)
                return Result.success(
                    CompleteProjectResponse.from_entity(project)
                )

            except (ValidationError, BusinessRuleViolation) as e:
                # Restore project state
                for task_id, task_snapshot in task_snapshots.items():
                    self.task_repository.save(task_snapshot)
                self.project_repository.save(project_snapshot)
                raise  # Re-raise the exception to be caught by outer try block

        except ProjectNotFoundError:
            return Result.failure(
                Error.not_found("Project", str(params["project_id"]))
            )
        except ValidationError as e:
            return Result.failure(Error.validation_error(str(e)))
        except BusinessRuleViolation as e:
            return Result.failure(Error.business_rule_violation(str(e)))
