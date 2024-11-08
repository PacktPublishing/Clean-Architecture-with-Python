"""
This module contains use cases for task operations.
"""

from dataclasses import dataclass

from Chapter_5.ToDoApp.todo_app.application.common.result import Result, Error
from Chapter_5.ToDoApp.todo_app.application.dtos.task_dtos import (
    CompleteTaskRequest,
    CreateTaskRequest,
    TaskResponse,
)
from Chapter_5.ToDoApp.todo_app.application.ports.notifications import (
    NotificationPort,
)
from Chapter_5.ToDoApp.todo_app.application.repositories.project_repository import (
    ProjectRepository,
)
from Chapter_5.ToDoApp.todo_app.application.repositories.task_repository import (
    TaskRepository,
)
from Chapter_5.ToDoApp.todo_app.domain.entities.task import Task
from Chapter_5.ToDoApp.todo_app.domain.exceptions import (
    TaskNotFoundError,
    ProjectNotFoundError,
    ValidationError,
    BusinessRuleViolation,
)
from Chapter_5.ToDoApp.todo_app.domain.value_objects import Priority


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
            task.complete(notes=params["completion_notes"])

            self.task_repository.save(task)
            self.notification_service.notify_task_completed(task.id)

            return Result.success(TaskResponse.from_entity(task))

        except TaskNotFoundError:
            return Result.failure(
                Error.not_found("Task", str(params["task_id"]))
            )
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
            if project_id := params.get("project_id"):
                self.project_repository.get(project_id)

            task = Task(
                title=params["title"],
                description=params["description"],
                due_date=params.get("deadline"),
                priority=params.get("priority", Priority.MEDIUM),
            )

            self.task_repository.save(task)

            return Result.success(TaskResponse.from_entity(task))

        except ProjectNotFoundError:
            if project_id := params.get("project_id"):
                return Result.failure(
                    Error.not_found("Project", str(project_id))
                )
            return Result.failure(Error.validation_error("Invalid project ID"))
        except ValidationError as e:
            return Result.failure(Error.validation_error(str(e)))
        except BusinessRuleViolation as e:
            return Result.failure(Error.business_rule_violation(str(e)))
