from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from Chapter_5.ToDoApp.todo_app.application.common.result import Result, Error
from Chapter_5.ToDoApp.todo_app.application.dtos.project_dtos import (
    ProjectResponse,
)
from Chapter_5.ToDoApp.todo_app.application.repositories.project_repository import (
    ProjectRepository,
)
from Chapter_5.ToDoApp.todo_app.application.repositories.task_repository import (
    TaskRepository,
)
from Chapter_5.ToDoApp.todo_app.domain.exceptions import (
    ProjectNotFoundError,
    ValidationError,
)


class NotificationService:
    """Stub to make mypy happy"""

    def notify_task_completed(self, task_id: UUID) -> None:
        pass


@dataclass(frozen=True)
class ProjectCompletionUseCase:
    project_repository: ProjectRepository
    task_repository: TaskRepository
    notification_service: NotificationService

    def execute(
        self,
        project_id: UUID,
        completion_notes: Optional[str] = None,
    ) -> Result:
        try:
            # Validate project exists
            project = self.project_repository.get(project_id)

            # Complete all outstanding tasks
            for task in project.incomplete_tasks:
                task.complete()
                self.task_repository.save(task)
                self.notification_service.notify_task_completed(task.id)

            # Complete the project itself
            project.mark_completed(notes=completion_notes)
            self.project_repository.save(project)

            return Result.success(ProjectResponse.from_entity(project))

        except ProjectNotFoundError:
            return Result.failure(Error.not_found("Project", str(project_id)))
        except ValidationError as e:
            return Result.failure(Error.validation_error(str(e)))
