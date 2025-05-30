"""
This module contains controllers that implement the Interface Adapters layer of Clean Architecture.

Controllers are responsible for:
1. Accepting input from external sources (CLI, web, etc.)
2. Converting that input into the format required by use cases
3. Executing the appropriate use case
4. Converting the result into a view model suitable for the interface
5. Handling and formatting any errors that occur

Key Clean Architecture benefits demonstrated in these controllers:
- Dependency Rule is followed: controllers depend inward towards use cases
- Separation of Concerns: controllers handle routing and data conversion only
- Independence: business logic remains isolated in use cases
- Flexibility: new interfaces can be added without changing use cases
"""

from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from todo_app.application.dtos.operations import DeletionOutcome
from todo_app.domain.value_objects import Priority
from todo_app.application.dtos.task_dtos import CompleteTaskRequest, CreateTaskRequest
from todo_app.application.use_cases.task_use_cases import CompleteTaskUseCase, CreateTaskUseCase
from todo_app.domain.value_objects import TaskStatus
from todo_app.interfaces.presenters.base import TaskPresenter
from todo_app.interfaces.view_models.base import OperationResult
from todo_app.application.dtos.task_dtos import UpdateTaskRequest
from todo_app.application.use_cases.task_use_cases import (
    DeleteTaskUseCase,
    GetTaskUseCase,
    UpdateTaskUseCase,
)
from todo_app.interfaces.view_models.task_vm import TaskViewModel

import logging

logger = logging.getLogger(__name__)


@dataclass
class TaskController:
    """Controller for task-related operations."""

    create_use_case: CreateTaskUseCase
    get_use_case: GetTaskUseCase
    complete_use_case: CompleteTaskUseCase
    update_use_case: UpdateTaskUseCase
    delete_use_case: DeleteTaskUseCase
    presenter: TaskPresenter

    def handle_create(
        self,
        title: str,
        description: str,
        project_id: Optional[str] = None,
        priority: Optional[str] = None,
        due_date: Optional[str] = None,
    ) -> OperationResult[TaskViewModel]:
        try:
            logger.info(
                "Handling task creation request",
                extra={
                    "context": {
                        "title": title,
                        "project_id": project_id,
                        "priority": priority,
                    }
                },
            )
            request = CreateTaskRequest(
                title=title,
                description=description,
                project_id=project_id,
                priority=priority,
                due_date=due_date,
            )
            result = self.create_use_case.execute(request)
            if result.is_success:
                view_model = self.presenter.present_task(result.value)
                logger.info(
                    "Task creation handled successfully",
                    extra={"context": {"task_id": str(result.value.id)}},
                )
                return OperationResult.succeed(view_model)

            logger.error(
                "Task creation failed",
                extra={
                    "context": {
                        "title": title,
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
                "Validation error in task creation",
                extra={"context": {"title": title, "error": str(e)}},
            )
            error_vm = self.presenter.present_error(str(e), "VALIDATION_ERROR")
            return OperationResult.fail(error_vm.message, error_vm.code)

    def handle_get(self, task_id: str) -> OperationResult[TaskViewModel]:
        try:
            logger.info(
                "Handling task retrieval request",
                extra={"context": {"task_id": task_id}},
            )
            result = self.get_use_case.execute(UUID(task_id))
            if result.is_success:
                view_model = self.presenter.present_task(result.value)
                logger.info(
                    "Task retrieval handled successfully",
                    extra={"context": {"task_id": task_id}},
                )
                return OperationResult.succeed(view_model)

            logger.error(
                "Task retrieval failed",
                extra={
                    "context": {
                        "task_id": task_id,
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
                "Validation error in task retrieval",
                extra={"context": {"task_id": task_id, "error": str(e)}},
            )
            error_vm = self.presenter.present_error(str(e), "VALIDATION_ERROR")
            return OperationResult.fail(error_vm.message, error_vm.code)

    def handle_complete(
        self, task_id: str, notes: Optional[str] = None
    ) -> OperationResult[TaskViewModel]:
        """Handle task completion requests."""
        try:
            logger.info(
                "Handling task completion request",
                extra={"context": {"task_id": task_id}},
            )
            request = CompleteTaskRequest(task_id=task_id, completion_notes=notes)
            result = self.complete_use_case.execute(request)

            if result.is_success:
                view_model = self.presenter.present_task(result.value)
                logger.info(
                    "Task completion handled successfully",
                    extra={"context": {"task_id": task_id}},
                )
                return OperationResult.succeed(view_model)

            logger.error(
                "Task completion failed",
                extra={
                    "context": {
                        "task_id": task_id,
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
                "Validation error in task completion",
                extra={"context": {"task_id": task_id, "error": str(e)}},
            )
            error_vm = self.presenter.present_error(str(e), "VALIDATION_ERROR")
            return OperationResult.fail(error_vm.message, error_vm.code)

    def handle_update(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        due_date: Optional[str] = None,
    ) -> OperationResult[TaskViewModel]:
        try:
            logger.info(
                "Handling task update request",
                extra={
                    "context": {
                        "task_id": task_id,
                        "update_fields": [
                            f for f, v in [
                                ("title", title),
                                ("description", description),
                                ("status", status),
                                ("priority", priority),
                                ("due_date", due_date),
                            ] if v is not None
                        ],
                    }
                },
            )
            # Convert string status/priority to enums if provided
            status_enum = TaskStatus[status.upper()] if status else None
            priority_enum = Priority[priority.upper()] if priority else None

            request = UpdateTaskRequest(
                task_id=task_id,
                title=title,
                description=description,
                status=status_enum,
                priority=priority_enum,
                due_date=due_date,
            )
            result = self.update_use_case.execute(request)
            if result.is_success:
                view_model = self.presenter.present_task(result.value)
                logger.info(
                    "Task update handled successfully",
                    extra={"context": {"task_id": task_id}},
                )
                return OperationResult.succeed(view_model)

            logger.error(
                "Task update failed",
                extra={
                    "context": {
                        "task_id": task_id,
                        "error": result.error.message,
                        "error_code": str(result.error.code.name),
                    }
                },
            )
            error_vm = self.presenter.present_error(
                result.error.message, str(result.error.code.name)
            )
            return OperationResult.fail(error_vm.message, error_vm.code)
        except (ValueError, KeyError) as e:
            logger.error(
                "Validation error in task update",
                extra={"context": {"task_id": task_id, "error": str(e)}},
            )
            error_vm = self.presenter.present_error(str(e), "VALIDATION_ERROR")
            return OperationResult.fail(error_vm.message, error_vm.code)

    def handle_delete(self, task_id: str) -> OperationResult[DeletionOutcome]:
        """
        Handle task deletion requests from any interface.

        Args:
            task_id: The task's unique identifier

        Returns:
            OperationResult containing either:
            - Success: DeletionResult with details of the deleted task
            - Failure: Error information formatted for the interface
        """
        try:
            logger.info(
                "Handling task deletion request",
                extra={"context": {"task_id": task_id}},
            )
            result = self.delete_use_case.execute(UUID(task_id))
            if result.is_success:
                logger.info(
                    "Task deletion handled successfully",
                    extra={"context": {"task_id": task_id}},
                )
                return OperationResult.succeed(result.value)

            logger.error(
                "Task deletion failed",
                extra={
                    "context": {
                        "task_id": task_id,
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
                "Validation error in task deletion",
                extra={"context": {"task_id": task_id, "error": str(e)}},
            )
            error_vm = self.presenter.present_error(str(e), "VALIDATION_ERROR")
            return OperationResult.fail(error_vm.message, error_vm.code)
