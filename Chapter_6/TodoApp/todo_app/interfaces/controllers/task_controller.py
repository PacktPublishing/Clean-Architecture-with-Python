from dataclasses import dataclass
from typing import Optional

from todo_app.interfaces.presenters.base import TaskPresenter
from todo_app.application.dtos.task_dtos import CompleteTaskRequest
from todo_app.application.common.result import Result
from todo_app.application.dtos.task_dtos import CreateTaskRequest
from todo_app.application.use_cases.task_use_cases import CompleteTaskUseCase, CreateTaskUseCase


@dataclass
class TaskController:
    """Controller for task-related operations."""
    create_use_case: CreateTaskUseCase
    complete_use_case: CompleteTaskUseCase
    presenter: TaskPresenter

    def handle_create(self, title: str, description: str, **kwargs) -> Result:
        """Handle task creation request."""
        request = CreateTaskRequest(title=title, description=description)
        result = self.create_use_case.execute(request)
        return result

    def handle_complete(self, task_id: str, notes: Optional[str] = None) -> Result:
        """Handle task completion request."""
        request = CompleteTaskRequest(task_id=task_id, completion_notes=notes)
        result = self.complete_use_case.execute(request)
        return result

