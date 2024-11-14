from dataclasses import dataclass
from uuid import UUID

from Chapter_5.TodoApp.todo_app.application.common.result import Result, Error
from Chapter_5.TodoApp.todo_app.application.dtos.project_dtos import (
    CompleteProjectRequest,
    CompleteProjectResponse,
)
from Chapter_5.TodoApp.todo_app.application.repositories.project_repository import (
    ProjectRepository,
)
from Chapter_5.TodoApp.todo_app.application.repositories.task_repository import (
    TaskRepository,
)
from Chapter_5.TodoApp.todo_app.domain.exceptions import (
    ValidationError,
    ProjectNotFoundError,
)


class NotificationService:
    """Stub to make mypy happy"""

    def notify_task_completed(self, task_id: UUID) -> None:
        pass


@dataclass
class CompleteProjectUseCase:
    project_repository: ProjectRepository
    task_repository: TaskRepository
    notification_service: NotificationService

    def execute(self, request: CompleteProjectRequest) -> Result:
        try:
            params = request.to_execution_params()
            project = self.project_repository.get(params["project_id"])
            project.mark_completed(notes=params["completion_notes"])

            # Complete all outstanding tasks
            # ... Truncated for brevity

            self.project_repository.save(project)

            response = CompleteProjectResponse.from_entity(project)
            return Result.success(response)

        except ProjectNotFoundError:
            return Result.failure(
                Error.not_found("Project", str(params["project_id"]))
            )
        except ValidationError as e:
            return Result.failure(Error.validation_error(str(e)))
