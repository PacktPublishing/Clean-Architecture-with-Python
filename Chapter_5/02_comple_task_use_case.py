from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from Chapter_5.ToDoApp.todo_app.application.common.result import Result, Error
from Chapter_5.ToDoApp.todo_app.application.repositories.task_repository import (
    TaskRepository,
)
from Chapter_5.ToDoApp.todo_app.domain.exceptions import (
    TaskNotFoundError,
    ValidationError,
)


@dataclass(frozen=True)
class CompleteTaskUseCase:
    """Use case for marking a task as complete and notifying stakeholders"""

    task_repository: TaskRepository

    def execute(
        self,
        task_id: UUID,
        completion_notes: Optional[str] = None,
    ) -> Result:

        try:
            # Input validation
            task = self.task_repository.get(task_id)
            task.complete(notes=completion_notes)
            self.task_repository.save(task)

            # Return simplified task data
            return Result.success(
                {
                    "id": str(task.id),
                    "status": "completed",
                    "completion_date": task.completed_at.isoformat(),
                }
            )

        except TaskNotFoundError:
            return Result.failure(Error.not_found("Task", str(task_id)))
        except ValidationError as e:
            return Result.failure(Error.validation_error(str(e)))
