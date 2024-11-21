from dataclasses import dataclass
from typing import Optional

from todo_app.interfaces.view_models.task_vm import TaskViewModel
from todo_app.interfaces.view_models.base import OperationResult
from todo_app.interfaces.presenters.base import TaskPresenter
from todo_app.application.dtos.task_dtos import CompleteTaskRequest
from todo_app.application.dtos.task_dtos import CreateTaskRequest
from todo_app.application.use_cases.task_use_cases import CompleteTaskUseCase, CreateTaskUseCase


@dataclass
class TaskController:
    create_use_case: CreateTaskUseCase
    complete_use_case: CompleteTaskUseCase
    presenter: TaskPresenter

    def handle_create(
        self, 
        title: str, 
        description: str, 
        **kwargs
    ) -> OperationResult:
        try:
            request = CreateTaskRequest(title=title, description=description)
            result = self.create_use_case.execute(request)
            
            if result.is_success:
                view_model = self.presenter.present_task(result.value)
                return OperationResult.succeed(view_model)
            
            error_vm = self.presenter.present_error(
                result.error.message,
                str(result.error.code)
            )
            return OperationResult.fail(error_vm.message, error_vm.code)
            
        except ValueError as e:
            error_vm = self.presenter.present_error(str(e), "VALIDATION_ERROR")
            return OperationResult.fail(error_vm.message, error_vm.code)

    def handle_complete(
        self, 
        task_id: str, 
        notes: Optional[str] = None
    ) -> OperationResult:
        try:
            request = CompleteTaskRequest(task_id=task_id, completion_notes=notes)
            result = self.complete_use_case.execute(request)
            
            if result.is_success:
                view_model = self.presenter.present_task(result.value)
                return OperationResult.succeed(view_model)
            
            error_vm = self.presenter.present_error(
                result.error.message,
                str(result.error.code)
            )
            return OperationResult.fail(error_vm.message, error_vm.code)
            
        except ValueError as e:
            error_vm = self.presenter.present_error(str(e), "VALIDATION_ERROR")
            return OperationResult.fail(error_vm.message, error_vm.code)

