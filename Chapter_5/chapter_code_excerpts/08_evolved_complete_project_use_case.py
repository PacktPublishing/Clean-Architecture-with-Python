from dataclasses import dataclass

from todo_app.application.common.result import Result, Error
from todo_app.application.dtos.project_dtos import (
    CompleteProjectRequest,
    CompleteProjectResponse,
)
from todo_app.application.repositories.project_repository import (
    ProjectRepository,
)
from todo_app.application.repositories.task_repository import (
    TaskRepository,
)
from todo_app.domain.exceptions import (
    ValidationError,
    ProjectNotFoundError,
)


class NotificationService:
    """Stub to make mypy happy"""

    def notify_task_completed(self, task: Task) -> None:
        pass


@dataclass(frozen=True)
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
