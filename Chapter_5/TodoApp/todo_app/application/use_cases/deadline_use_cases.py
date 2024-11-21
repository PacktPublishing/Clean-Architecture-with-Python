from dataclasses import field, dataclass
from datetime import timedelta

from todo_app.application.common.result import Result, Error
from todo_app.application.ports.notifications import (
    NotificationPort,
)
from todo_app.application.repositories.task_repository import (
    TaskRepository,
)
from todo_app.domain.exceptions import (
    TaskNotFoundError,
    ValidationError,
    BusinessRuleViolation,
)


@dataclass
class CheckDeadlinesUseCase:
    """Use case for checking and notifying about approaching task deadlines."""

    task_repository: TaskRepository
    notification_service: NotificationPort
    warning_threshold: timedelta = field(default=timedelta(days=1))

    def execute(self) -> Result:
        """Check all tasks and notify about approaching deadlines."""
        try:
            tasks = self.task_repository.get_active_tasks()
            notifications_sent = 0

            for task in tasks:
                if task.due_date and task.due_date.is_approaching(
                    self.warning_threshold
                ):
                    remaining_days = int(
                        task.due_date.time_remaining().total_seconds()
                        / (24 * 3600)
                    )
                    self.notification_service.notify_task_deadline_approaching(
                        task.id, remaining_days
                    )
                    notifications_sent += 1

            return Result.success({"notifications_sent": notifications_sent})

        except TaskNotFoundError as e:
            return Result.failure(Error.not_found("Task", str(e)))
        except ValidationError as e:
            return Result.failure(Error.validation_error(str(e)))
        except BusinessRuleViolation as e:
            return Result.failure(Error.business_rule_violation(str(e)))
