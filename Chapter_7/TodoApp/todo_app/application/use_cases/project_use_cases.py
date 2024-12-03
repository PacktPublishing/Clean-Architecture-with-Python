"""
This module contains use cases for project operations.
"""

from copy import deepcopy
from dataclasses import dataclass
from uuid import UUID

from todo_app.application.common.result import Result, Error
from todo_app.application.dtos.project_dtos import (
    CreateProjectRequest,
    ProjectResponse,
    CompleteProjectRequest,
    CompleteProjectResponse,
)
from todo_app.application.ports.notifications import (
    NotificationPort,
)
from todo_app.application.repositories.project_repository import (
    ProjectRepository,
)
from todo_app.application.repositories.task_repository import (
    TaskRepository,
)
from todo_app.domain.entities.project import Project
from todo_app.domain.exceptions import (
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

            project = Project(name=params["name"], description=params["description"])

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
            task_snapshots = {task.id: deepcopy(task) for task in project.incomplete_tasks}

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
                return Result.success(CompleteProjectResponse.from_entity(project))

            except (ValidationError, BusinessRuleViolation) as e:
                # Restore project state
                for task_id, task_snapshot in task_snapshots.items():
                    self.task_repository.save(task_snapshot)
                self.project_repository.save(project_snapshot)
                raise  # Re-raise the exception to be caught by outer try block

        except ProjectNotFoundError:
            return Result.failure(Error.not_found("Project", str(params["project_id"])))
        except ValidationError as e:
            return Result.failure(Error.validation_error(str(e)))
        except BusinessRuleViolation as e:
            return Result.failure(Error.business_rule_violation(str(e)))


@dataclass
class GetProjectUseCase:
    """Use case for retrieving project details."""

    project_repository: ProjectRepository

    def execute(self, project_id: str) -> Result[ProjectResponse]:
        """
        Get details for a specific project.

        Args:
            project_id: The unique identifier of the project

        Returns:
            Result containing either:
            - Success: ProjectResponse with project details
            - Failure: Error information
        """
        try:
            project = self.project_repository.get(UUID(project_id))
            return Result.success(ProjectResponse.from_entity(project))
        except ProjectNotFoundError:
            return Result.failure(Error.not_found("Project", project_id))


@dataclass
class ListProjectsUseCase:
    """Use case for listing all projects."""

    project_repository: ProjectRepository
    task_repository: TaskRepository

    def execute(self) -> Result[list[ProjectResponse]]:
        """
        List all projects with their associated tasks.

        Returns:
            Result containing either:
            - Success: List of ProjectResponse objects
            - Failure: Error information
        """
        try:
            # Get or create INBOX if it doesn't exist
            try:
                inbox = self.project_repository.get_inbox("INBOX")
            except Exception:
                inbox = None

            # Get all tasks that aren't assigned to a project
            if inbox:
                unassigned_tasks = self.task_repository.find_by_project(inbox.id)
                for task in unassigned_tasks:
                    inbox.add_task(task)

            projects = []

            # Add inbox first if it exists
            if inbox:
                projects.append(ProjectResponse.from_entity(inbox))

            return Result.success(projects)

        except Exception as e:
            return Result.failure(Error.business_rule_violation(str(e)))
