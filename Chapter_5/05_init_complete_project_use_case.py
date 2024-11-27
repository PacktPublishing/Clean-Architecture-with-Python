"""
This initial example of NotificationService from page 18
"""

from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from todo_app.application.common.result import Result, Error
from todo_app.application.repositories.project_repository import (
    ProjectRepository,
)
from todo_app.application.repositories.task_repository import (
    TaskRepository,
)
from todo_app.domain.exceptions import (
    ProjectNotFoundError,
    ValidationError,
)


class NotificationService:
    """Stub to make mypy happy"""

    def notify_task_completed(self, task_id: UUID) -> None:
        pass


@dataclass(frozen=True)
class CompleteProjectUseCase:
    project_repository: ProjectRepository
    task_repository: TaskRepository
    notification_service: NotificationService

    def execute(
        self, project_id: UUID, completion_notes: Optional[str] = None
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

            return Result.success({
                "id": str(project.id),
                "status": project.status,
                "completion_date": project.completed_at,
                "task_count": len(project.tasks),
                "completion_notes": project.completion_notes,
            })

        except ProjectNotFoundError:
            return Result.failure(Error.not_found("Project", str(project_id)))
        except ValidationError as e:
            return Result.failure(Error.validation_error(str(e)))
