"""
This module contains use cases for project operations.
"""

from copy import deepcopy
from dataclasses import dataclass
from uuid import UUID

from todo_app.domain.value_objects import ProjectType
from todo_app.application.common.result import Result, Error
from todo_app.application.dtos.project_dtos import (
    CreateProjectRequest,
    ProjectResponse,
    CompleteProjectRequest,
    CompleteProjectResponse,
    UpdateProjectRequest,
)
from todo_app.application.service_ports.notifications import (
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

import logging

logger = logging.getLogger(__name__)


@dataclass
class CreateProjectUseCase:
    """Use case for creating a new project."""

    project_repository: ProjectRepository

    def execute(self, request: CreateProjectRequest) -> Result:
        """Execute the use case."""
        try:
            params = request.to_execution_params()
            logger.info("Creating new project", extra={"context": {"name": params["name"]}})

            project = Project(name=params["name"], description=params["description"])
            self.project_repository.save(project)

            logger.info(
                "Project created successfully",
                extra={"context": {"project_id": str(project.id), "name": project.name}},
            )
            return Result.success(ProjectResponse.from_entity(project))

        except ValidationError as e:
            logger.error("Validation error creating project", extra={"context": {"error": str(e)}})
            return Result.failure(Error.validation_error(str(e)))
        except BusinessRuleViolation as e:
            logger.error("Business rule violation creating project", extra={"context": {"error": str(e)}})
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
            logger.info("Completing project", extra={"context": {"project_id": str(params["project_id"])}})
            project = self.project_repository.get(params["project_id"])

            # Take snapshots of initial state
            project_snapshot = deepcopy(project)
            task_snapshots = {task.id: deepcopy(task) for task in project.incomplete_tasks}

            try:
                # Complete all outstanding tasks
                for task in project.incomplete_tasks:
                    task.complete()
                    self.task_repository.save(task)

                project.mark_completed(notes=params["completion_notes"])
                self.project_repository.save(project)

                for task in project_snapshot.incomplete_tasks:
                    self.notification_service.notify_task_completed(task)

                logger.info(
                    "Project completed successfully",
                    extra={
                        "context": {
                            "project_id": str(project.id),
                            "tasks_completed": len(project_snapshot.incomplete_tasks),
                        }
                    },
                )
                return Result.success(CompleteProjectResponse.from_entity(project))

            except (ValidationError, BusinessRuleViolation) as e:
                # Restore project state
                logger.error(
                    "Failed to complete project",
                    extra={"context": {"project_id": str(project.id), "error": str(e)}},
                )
                for task_id, task_snapshot in task_snapshots.items():
                    self.task_repository.save(task_snapshot)
                self.project_repository.save(project_snapshot)
                raise  # Re-raise the exception to be caught by outer try block

        except ProjectNotFoundError:
            logger.error(
                "Project not found",
                extra={"context": {"project_id": str(params["project_id"])}},
            )
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
            logger.info("Retrieving project details", extra={"context": {"project_id": project_id}})
            project = self.project_repository.get(UUID(project_id))
            return Result.success(ProjectResponse.from_entity(project))
        except ProjectNotFoundError:
            logger.error("Project not found", extra={"context": {"project_id": project_id}})
            return Result.failure(Error.not_found("Project", project_id))


@dataclass
class ListProjectsUseCase:
    project_repository: ProjectRepository

    def execute(self) -> Result[list[ProjectResponse]]:
        """
        List all projects.

        Returns:
            Result containing either:
            - Success: List of ProjectResponse objects
            - Failure: Error information
        """
        try:
            logger.info("Retrieving all projects")
            projects = self.project_repository.get_all()
            logger.info("Projects retrieved successfully", extra={"context": {"count": len(projects)}})
            return Result.success([ProjectResponse.from_entity(p) for p in projects])
        except Exception as e:
            logger.error("Failed to retrieve projects", extra={"context": {"error": str(e)}})
            return Result.failure(Error.business_rule_violation(str(e)))


@dataclass
class UpdateProjectUseCase:
    """Use case for updating a project."""

    project_repository: ProjectRepository

    def execute(self, request: UpdateProjectRequest) -> Result:
        """Execute the use case."""
        try:
            params = request.to_execution_params()
            logger.info("Updating project", extra={"context": {"project_id": str(params["project_id"])}})
            project = self.project_repository.get(params["project_id"])

            # Prevent editing of INBOX project
            if project.project_type == ProjectType.INBOX:
                logger.warning(
                    "Attempted to modify INBOX project",
                    extra={"context": {"project_id": str(project.id)}},
                )
                return Result.failure(
                    Error.business_rule_violation("The INBOX project cannot be modified")
                )

            updated_fields = []
            if params["name"] is not None:
                project.name = params["name"]
                updated_fields.append("name")
            if params["description"] is not None:
                project.description = params["description"]
                updated_fields.append("description")

            self.project_repository.save(project)
            logger.info(
                "Project updated successfully",
                extra={
                    "context": {
                        "project_id": str(project.id),
                        "updated_fields": updated_fields,
                    }
                },
            )
            return Result.success(ProjectResponse.from_entity(project))

        except ProjectNotFoundError:
            logger.error(
                "Project not found",
                extra={"context": {"project_id": str(params["project_id"])}},
            )
            return Result.failure(Error.not_found("Project", str(params["project_id"])))
        except ValidationError as e:
            logger.error(
                "Validation error updating project",
                extra={"context": {"project_id": str(params["project_id"]), "error": str(e)}},
            )
            return Result.failure(Error.validation_error(str(e)))
        except BusinessRuleViolation as e:
            logger.error(
                "Business rule violation updating project",
                extra={"context": {"project_id": str(params["project_id"]), "error": str(e)}},
            )
            return Result.failure(Error.business_rule_violation(str(e)))
