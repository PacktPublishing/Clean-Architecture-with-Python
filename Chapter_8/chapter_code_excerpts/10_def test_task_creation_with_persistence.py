from uuid import UUID
from unittest.mock import Mock


def test_task_creation_with_persistence(tmp_path):
    """Test task creation use case with real persistence."""
    # Arrange
    task_repo = FileTaskRepository(tmp_path)
    project_repo = FileProjectRepository(tmp_path)
    project_repo.set_task_repository(task_repo)

    use_case = CreateTaskUseCase(
        task_repository=task_repo,
        project_repository=project_repo,
        notification_service=Mock(),  # Still mock non-persistence concerns
    )

    # Act
    result = use_case.execute(CreateTaskRequest(title="Test Task", description="Integration test"))

    # Assert - Task was persisted
    assert result.is_success
    created_task = task_repo.get(UUID(result.value.id))
    assert created_task.project_id == project_repo.get_inbox().id
