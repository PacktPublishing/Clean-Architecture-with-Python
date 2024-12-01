from datetime import datetime, timedelta
from uuid import UUID, uuid4

from freezegun import freeze_time

from todo_app.infrastructure.notifications.recorder import NotificationRecorder
from todo_app.infrastructure.persistence.memory import InMemoryTaskRepository
from todo_app.application.common.result import ErrorCode
from todo_app.application.use_cases.deadline_use_cases import (
    CheckDeadlinesUseCase,
)
from todo_app.domain.entities.task import Task
from todo_app.domain.exceptions import (
    BusinessRuleViolation,
    ValidationError,
    TaskNotFoundError,
)
from todo_app.domain.value_objects import Deadline


def test_check_deadlines_empty_repository():
    """Test checking deadlines with no tasks."""
    repo = InMemoryTaskRepository()
    notifications = NotificationRecorder()
    use_case = CheckDeadlinesUseCase(repo, notifications)

    result = use_case.execute()

    assert result.is_success
    assert result.value["notifications_sent"] == 0
    assert not notifications.deadline_warnings


@freeze_time("2024-01-01 12:00:00")
def test_check_deadlines_no_approaching_deadlines():
    """Test checking deadlines when no tasks have approaching deadlines."""
    repo = InMemoryTaskRepository()
    notifications = NotificationRecorder()
    use_case = CheckDeadlinesUseCase(repo, notifications)

    # Create tasks with deadlines well in the future
    far_future_date = datetime.now() + timedelta(days=10)
    task1 = Task(
        title="Future Task 1",
        description="Test",
        project_id=uuid4(),
        due_date=Deadline(far_future_date),
    )
    task2 = Task(
        title="Future Task 2",
        description="Test",
        project_id=uuid4(),
        due_date=Deadline(far_future_date + timedelta(days=1)),
    )

    repo.save(task1)
    repo.save(task2)

    result = use_case.execute()

    assert result.is_success
    assert result.value["notifications_sent"] == 0
    assert not notifications.deadline_warnings


@freeze_time("2024-01-01 12:00:00")
def test_check_deadlines_approaching_deadlines():
    """Test checking deadlines with tasks approaching their deadlines."""
    repo = InMemoryTaskRepository()
    notifications = NotificationRecorder()
    use_case = CheckDeadlinesUseCase(repo, notifications)

    # Create tasks with various deadlines
    approaching_date = datetime.now() + timedelta(hours=23)  # Within 1 day
    future_date = datetime.now() + timedelta(days=5)  # Not approaching

    task1 = Task(
        title="Approaching Task",
        description="Test",
        project_id=uuid4(),
        due_date=Deadline(approaching_date),
    )
    task2 = Task(
        title="Future Task",
        description="Test",
        project_id=uuid4(),
        due_date=Deadline(future_date),
    )

    repo.save(task1)
    repo.save(task2)

    result = use_case.execute()

    assert result.is_success
    assert result.value["notifications_sent"] == 1
    assert len(notifications.deadline_warnings) == 1
    assert notifications.deadline_warnings[0][0] == task1.id  # First task should be warned
    assert notifications.deadline_warnings[0][1] == 0  # Less than 1 day remaining


@freeze_time("2024-01-01 12:00:00")
def test_check_deadlines_custom_threshold():
    """Test checking deadlines with a custom warning threshold."""
    repo = InMemoryTaskRepository()
    notifications = NotificationRecorder()
    use_case = CheckDeadlinesUseCase(repo, notifications, warning_threshold=timedelta(days=3))

    # Create tasks with various deadlines
    two_days = Task(
        title="Two Days Task",
        description="Test",
        project_id=uuid4(),
        due_date=Deadline(datetime.now() + timedelta(days=2)),
    )
    four_days = Task(
        title="Four Days Task",
        description="Test",
        project_id=uuid4(),
        due_date=Deadline(datetime.now() + timedelta(days=4)),
    )

    repo.save(two_days)
    repo.save(four_days)

    result = use_case.execute()

    assert result.is_success
    assert result.value["notifications_sent"] == 1
    assert len(notifications.deadline_warnings) == 1
    assert notifications.deadline_warnings[0][0] == two_days.id
    assert notifications.deadline_warnings[0][1] == 2  # 2 days remaining


@freeze_time("2024-01-01 12:00:00")
def test_check_deadlines_completed_tasks():
    """Test that completed tasks are not checked for deadlines."""
    repo = InMemoryTaskRepository()
    notifications = NotificationRecorder()
    use_case = CheckDeadlinesUseCase(repo, notifications)

    # Create a completed task with an approaching deadline
    approaching_date = datetime.now() + timedelta(hours=12)
    task = Task(
        title="Completed Task",
        description="Test",
        project_id=uuid4(),
        due_date=Deadline(approaching_date),
    )
    task.complete()  # Mark as complete
    repo.save(task)

    result = use_case.execute()

    assert result.is_success
    assert result.value["notifications_sent"] == 0
    assert not notifications.deadline_warnings


@freeze_time("2024-01-01 12:00:00")
def test_check_deadlines_multiple_notifications():
    """Test checking multiple tasks with approaching deadlines."""
    repo = InMemoryTaskRepository()
    notifications = NotificationRecorder()
    use_case = CheckDeadlinesUseCase(repo, notifications)

    # Create multiple tasks with approaching deadlines
    base_time = datetime.now()
    tasks = []
    for hours in [12, 18, 22]:  # All within 24 hours
        task = Task(
            title=f"Task due in {hours} hours",
            description="Test",
            project_id=uuid4(),
            due_date=Deadline(base_time + timedelta(hours=hours)),
        )
        tasks.append(task)
        repo.save(task)

    result = use_case.execute()

    assert result.is_success
    assert result.value["notifications_sent"] == 3
    assert len(notifications.deadline_warnings) == 3
    # Verify each task got a warning
    task_ids = {warning[0] for warning in notifications.deadline_warnings}
    assert task_ids == {task.id for task in tasks}


@freeze_time("2024-01-01 12:00:00")
def test_check_deadlines_handles_repository_errors():
    """Test handling of repository errors during deadline check."""

    class ErroringTaskRepository(InMemoryTaskRepository):
        def get_active_tasks(self):
            raise BusinessRuleViolation("Repository error")

    repo = ErroringTaskRepository()
    notifications = NotificationRecorder()
    use_case = CheckDeadlinesUseCase(repo, notifications)

    result = use_case.execute()

    assert not result.is_success
    assert result.error.code == ErrorCode.BUSINESS_RULE_VIOLATION
    assert "Repository error" in result.error.message
    assert not notifications.deadline_warnings  # No notifications should be sent


@freeze_time("2024-01-01 12:00:00")
def test_check_deadlines_handles_notification_errors():
    """Test handling of notification service errors."""

    class ErroringNotificationService(NotificationRecorder):
        def notify_task_deadline_approaching(self, task_id, days_remaining):
            raise ValidationError("Notification error")

    repo = InMemoryTaskRepository()
    notifications = ErroringNotificationService()
    use_case = CheckDeadlinesUseCase(repo, notifications)

    # Create a task with approaching deadline
    due_date = datetime.now() + timedelta(hours=12)
    task = Task(
        title="Test Task",
        description="Test",
        project_id=uuid4(),
        due_date=Deadline(due_date),
    )
    repo.save(task)

    result = use_case.execute()

    assert not result.is_success
    assert result.error.code == ErrorCode.VALIDATION_ERROR
    assert "Notification error" in result.error.message


@freeze_time("2024-01-01 12:00:00")
def test_check_deadlines_handles_task_not_found():
    """Test handling of TaskNotFoundError during deadline check."""

    class TaskNotFoundRepository(InMemoryTaskRepository):
        def get_active_tasks(self):
            raise TaskNotFoundError(UUID("123e4567-e89b-12d3-a456-426614174000"))

    repo = TaskNotFoundRepository()
    notifications = NotificationRecorder()
    use_case = CheckDeadlinesUseCase(repo, notifications)

    result = use_case.execute()

    assert not result.is_success
    assert result.error.code == ErrorCode.NOT_FOUND
    assert "Task" in result.error.message
    assert not notifications.deadline_warnings
