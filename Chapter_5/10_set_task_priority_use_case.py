from dataclasses import dataclass

from Chapter_5.TodoApp.todo_app.application.common.result import Result, Error
from Chapter_5.TodoApp.todo_app.application.dtos.task_dtos import (
    TaskResponse,
    SetTaskPriorityRequest,
)
from Chapter_5.TodoApp.todo_app.application.ports.notifications import (
    NotificationPort,
)
from Chapter_5.TodoApp.todo_app.application.repositories.task_repository import (
    TaskRepository,
)
from Chapter_5.TodoApp.todo_app.domain.exceptions import ValidationError
from Chapter_5.TodoApp.todo_app.domain.value_objects import Priority


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
                self.notification_service.notify_task_high_priority(task.id)

            return Result.success(TaskResponse.from_entity(task))
        except ValidationError as e:
            return Result.failure(Error.validation_error(str(e)))
