from datetime import timedelta, timezone
from uuid import UUID
from freezegun import freeze_time
from unittest.mock import Mock


def test_task_deadline_approaching():
    """Test deadline notifications respect time boundaries."""
    # Arrange
    with freeze_time("2024-01-14 12:00:00"):
        task = Task(
            title="Time-sensitive task",
            description="Testing deadlines",
            project_id=UUID("12345678-1234-5678-1234-567812345678"),
            due_date=Deadline(datetime(2024, 1, 15, 12, 0, tzinfo=timezone.utc)),
        )
    notification_service = Mock(spec=NotificationPort)
    use_case = CheckDeadlinesUseCase(
        task_repository=Mock(spec=TaskRepository),
        notification_service=notification_service,
        warning_threshold=timedelta(days=1),
    )

    # Act
    with freeze_time("2024-01-14 13:00:00"):
        result = use_case.execute()

    # Assert
    assert result.is_success
    notification_service.notify_task_deadline_approaching.assert_called_once()
