"""
This module contains use cases for task operations.
"""

from copy import deepcopy
from dataclasses import dataclass

from todo_app.application.common.result import Result, Error
from todo_app.application.dtos.task_dtos import (
    CompleteTaskRequest,
    CreateTaskRequest,
    TaskResponse,
    SetTaskPriorityRequest,
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
from todo_app.domain.entities.task import Task
from todo_app.domain.exceptions import (
    TaskNotFoundError,
    ProjectNotFoundError,
    ValidationError,
    BusinessRuleViolation,
)
from todo_app.domain.value_objects import Priority


@dataclass
class CompleteTaskUseCase:
    """Use case for marking a task as complete and notifying stakeholders."""

    task_repository: TaskRepository
    notification_service: NotificationPort

    def execute(self, request: CompleteTaskRequest) -> Result:
        """Execute the use case."""
        try:
            params = request.to_execution_params()
            task = self.task_repository.get(params["task_id"])

            # Take snapshot of initial state
            task_snapshot = deepcopy(task)

            try:
                task.complete(notes=params["completion_notes"])
                self.task_repository.save(task)
                self.notification_service.notify_task_completed(task)

                return Result.success(TaskResponse.from_entity(task))

            except (ValidationError, BusinessRuleViolation) as e:
                # Restore task state
                self.task_repository.save(task_snapshot)
                raise  # Re-raise the exception to be caught by outer try block

        except TaskNotFoundError:
            return Result.failure(Error.not_found("Task", str(params["task_id"])))
        except ValidationError as e:
            return Result.failure(Error.validation_error(str(e)))
        except BusinessRuleViolation as e:
            return Result.failure(Error.business_rule_violation(str(e)))


@dataclass
class CreateTaskUseCase:
    """Use case for creating a new task."""

    task_repository: TaskRepository
    project_repository: ProjectRepository

    def execute(self, request: CreateTaskRequest) -> Result:
        """Execute the use case."""
        try:
            params = request.to_execution_params()

            # If task is part of a project, verify project exists
            project_id = params.get("project_id")
            if project_id:
                self.project_repository.get(project_id)

            task = Task(
                title=params["title"],
                description=params["description"],
                due_date=params.get("deadline"),
                priority=params.get("priority", Priority.MEDIUM),
            )

            # Set the project_id if one was provided
            if project_id:
                task.project_id = project_id

            self.task_repository.save(task)

            return Result.success(TaskResponse.from_entity(task))

        except ProjectNotFoundError:
            return Result.failure(Error.not_found("Project", str(params.get("project_id"))))
        except ValidationError as e:
            return Result.failure(Error.validation_error(str(e)))
        except BusinessRuleViolation as e:
            return Result.failure(Error.business_rule_violation(str(e)))


@dataclass
class SetTaskPriorityUseCase:
    task_repository: TaskRepository
    notification_service: NotificationPort  # Depends on capability interface

    def execute(self, request: SetTaskPriorityRequest) -> Result:
        try:
            params = request.to_execution_params()

            task = self.task_repository.get(params["task_id"])
            task.priority = params["priority"]

            self.task_repository.save(task)

            if task.priority == Priority.HIGH:
                self.notification_service.notify_task_high_priority(task)

            return Result.success(TaskResponse.from_entity(task))
        except ValidationError as e:
            return Result.failure(Error.validation_error(str(e)))
