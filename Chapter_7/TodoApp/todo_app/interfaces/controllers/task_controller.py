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

from todo_app.domain.value_objects import TaskStatus
from todo_app.interfaces.presenters.base import TaskPresenter
from todo_app.interfaces.view_models.task_vm import TaskViewModel
from todo_app.interfaces.view_models.base import OperationResult
from todo_app.application.dtos.task_dtos import (
    CompleteTaskRequest,
    CreateTaskRequest,
    SetTaskPriorityRequest,
)
from todo_app.application.use_cases.task_use_cases import (
    CompleteTaskUseCase,
    CreateTaskUseCase,
    GetTaskUseCase,
    SetTaskPriorityUseCase,
    UpdateTaskStatusUseCase,
)


@dataclass
class TaskController:
    """
    Controller for task-related operations, demonstrating Clean Architecture principles.

    This controller adheres to Clean Architecture by:
    - Depending only on abstractions (use cases and presenters)
    - Converting external input into use case request models
    - Ensuring business rules remain in the use cases
    - Using presenters to format output appropriately for the interface

    The clear separation of concerns allows:
    - Easy testing through dependency injection
    - Addition of new interfaces without changing business logic
    - Modification of presentation logic without affecting core functionality

    Attributes:
        create_use_case: Use case for creating tasks
        complete_use_case: Use case for completing tasks
        presenter: Handles formatting of task data for the interface
    """

    create_use_case: CreateTaskUseCase
    get_use_case: GetTaskUseCase
    update_status_use_case: UpdateTaskStatusUseCase
    set_priority_use_case: SetTaskPriorityUseCase
    complete_use_case: CompleteTaskUseCase
    presenter: TaskPresenter

    def handle_create(self, title: str, description: str) -> OperationResult[TaskViewModel]:
        """
        Handle task creation requests from any interface.

        This method demonstrates Clean Architecture's separation of concerns by:
        1. Accepting primitive types as input (making it interface-agnostic)
        2. Converting input into the use case's required format
        3. Executing the use case without knowing its implementation details
        4. Using a presenter to format the response appropriately

        Args:
            title: The task title
            description: The task description

        Returns:
            OperationResult containing either:
            - Success: TaskViewModel formatted for the interface
            - Failure: Error information formatted for the interface
        """
        try:
            # Convert primitive input to use case request model specifically designed for the
            # Interface->Application boundary crossing
            # It contains validation specific to application needs
            # Ensures data entering the application layer is properly formatted and validated
            request = CreateTaskRequest(title=title, description=description)

            # Execute use case and get domain-oriented result
            result = self.create_use_case.execute(request)

            if result.is_success:
                # Convert domain response to view model
                view_model = self.presenter.present_task(result.value)
                return OperationResult.succeed(view_model)

            # Handle domain errors
            error_vm = self.presenter.present_error(
                result.error.message, str(result.error.code.name)
            )
            return OperationResult.fail(error_vm.message, error_vm.code)

        except ValueError as e:
            # Handle validation errors
            error_vm = self.presenter.present_error(str(e), "VALIDATION_ERROR")
            return OperationResult.fail(error_vm.message, error_vm.code)

    def handle_complete(
        self, task_id: str, notes: Optional[str] = None
    ) -> OperationResult[TaskViewModel]:
        """
        Handle task completion requests from any interface.

        Following Clean Architecture principles, this method:
        1. Remains ignorant of the interface details (CLI, web, etc.)
        2. Uses use cases for business logic
        3. Returns interface-appropriate view models

        Args:
            task_id: The unique identifier of the task
            notes: Optional completion notes

        Returns:
            OperationResult containing either:
            - Success: TaskViewModel with completion information
            - Failure: Error information formatted for the interface
        """
        try:
            request = CompleteTaskRequest(task_id=task_id, completion_notes=notes)
            result = self.complete_use_case.execute(request)

            if result.is_success:
                view_model = self.presenter.present_task(result.value)
                return OperationResult.succeed(view_model)

            error_vm = self.presenter.present_error(
                result.error.message, str(result.error.code.name)
            )
            return OperationResult.fail(error_vm.message, error_vm.code)

        except ValueError as e:
            error_vm = self.presenter.present_error(str(e), "VALIDATION_ERROR")
            return OperationResult.fail(error_vm.message, error_vm.code)

    def handle_get(self, task_id: str) -> OperationResult[TaskViewModel]:
        """
        Handle task retrieval requests.

        Args:
            task_id: The unique identifier of the task

        Returns:
            OperationResult containing either:
            - Success: TaskViewModel with task details
            - Failure: Error information
        """
        try:
            result = self.get_use_case.execute(UUID(task_id))

            if result.is_success:
                view_model = self.presenter.present_task(result.value)
                return OperationResult.succeed(view_model)

            error_vm = self.presenter.present_error(
                result.error.message, str(result.error.code.name)
            )
            return OperationResult.fail(error_vm.message, error_vm.code)

        except ValueError as e:
            error_vm = self.presenter.present_error(str(e), "VALIDATION_ERROR")
            return OperationResult.fail(error_vm.message, error_vm.code)

    def handle_update_status(
        self, task_id: str, status: TaskStatus
    ) -> OperationResult[TaskViewModel]:
        """
        Handle task status update requests.

        Args:
            task_id: The unique identifier of the task
            status: The new status to set

        Returns:
            OperationResult containing either:
            - Success: TaskViewModel with updated task details
            - Failure: Error information
        """
        try:
            result = self.update_status_use_case.execute(UUID(task_id), status)

            if result.is_success:
                view_model = self.presenter.present_task(result.value)
                return OperationResult.succeed(view_model)

            error_vm = self.presenter.present_error(
                result.error.message, str(result.error.code.name)
            )
            return OperationResult.fail(error_vm.message, error_vm.code)

        except ValueError as e:
            error_vm = self.presenter.present_error(str(e), "VALIDATION_ERROR")
            return OperationResult.fail(error_vm.message, error_vm.code)

    def handle_set_priority(self, task_id: str, priority: str) -> OperationResult[TaskViewModel]:
        """
        Handle task priority update requests from any interface.

        Args:
            task_id: The unique identifier of the task
            priority: The new priority value (HIGH, MEDIUM, or LOW)

        Returns:
            OperationResult containing either:
            - Success: TaskViewModel with updated priority
            - Failure: Error information formatted for the interface
        """
        try:
            request = SetTaskPriorityRequest(task_id=task_id, priority=priority)
            result = self.set_priority_use_case.execute(request)

            if result.is_success:
                view_model = self.presenter.present_task(result.value)
                return OperationResult.succeed(view_model)

            error_vm = self.presenter.present_error(
                result.error.message, str(result.error.code.name)
            )
            return OperationResult.fail(error_vm.message, error_vm.code)

        except ValueError as e:
            error_vm = self.presenter.present_error(str(e), "VALIDATION_ERROR")
            return OperationResult.fail(error_vm.message, error_vm.code)
