from unittest.mock import Mock
from uuid import UUID


def test_successful_task_completion():
    """Test task completion using mock dependencies."""
    # Arrange
    task = Task(
        title="Test task",
        description="Test description",
        project_id=UUID("12345678-1234-5678-1234-567812345678"),
    )
    task_repo = Mock()
    task_repo.get.return_value = task
    notification_service = Mock()

    use_case = CompleteTaskUseCase(
        task_repository=task_repo, notification_service=notification_service
    )
    request = CompleteTaskRequest(task_id=str(task.id))
    # Act
    result = use_case.execute(request)

    # Assert
    assert result.is_success
    task_repo.save.assert_called_once_with(task)
    notification_service.notify_task_completed.assert_called_once_with(task)
