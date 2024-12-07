from dataclasses import field, dataclass
from typing import Any
from uuid import UUID

from todo_app.application.common.result import Result, Error
from todo_app.application.dtos.task_dtos import TaskResponse
from todo_app.application.serviceports.notifications import (
    NotificationPort,
)
from todo_app.application.repositories.task_repository import (
    TaskRepository,
)
from todo_app.domain.exceptions import ValidationError


@dataclass(frozen=True)
class TaskManagementUseCase:
    task_repository: TaskRepository
    notification_service: NotificationPort
    _optional_services: dict[str, Any] = field(default_factory=dict)

    def register_service(self, name: str, service: Any) -> None:
        """Register an optional service"""
        self._optional_services[name] = service

    def complete_task(self, task_id: UUID) -> Result:
        try:
            task = self.task_repository.get(task_id)
            task.complete()
            self.task_repository.save(task)

            # Required notification
            self.notification_service.notify_task_completed(task.id)

            # Optional integrations
            if analytics := self._optional_services.get("analytics"):
                analytics.track_task_completion(task.id)
            if audit := self._optional_services.get("audit"):
                audit.log_task_completion(task.id)

            return Result.success(TaskResponse.from_entity(task))
        except ValidationError as e:
            return Result.failure(Error.validation_error(str(e)))
