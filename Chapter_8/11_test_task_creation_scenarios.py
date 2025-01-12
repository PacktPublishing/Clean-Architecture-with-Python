from uuid import UUID
import pytest
from unittest.mock import Mock


@pytest.mark.parametrize(
    "request_data,expected_behavior",
    [
        # Default priority task creation
        (
            {"title": "Test Task", "description": "Basic creation"},
            {"project_type": ProjectType.INBOX, "priority": Priority.MEDIUM},
        ),
        # High priority task
        (
            {"title": "Priority Task", "description": "High priority", "priority": "HIGH"},
            {"project_type": ProjectType.INBOX, "priority": Priority.HIGH},
        ),
    ],
    ids=["default-priority-task", "high-priority-task"],
)
def test_task_creation_scenarios(request_data, expected_behavior, tmp_path):
    """Test task creation use case handles various input scenarios correctly."""
    # Arrange
    task_repo = Mock(spec=TaskRepository)
    project_repo = FileProjectRepository(tmp_path)  # Real project repo for INBOX

    use_case = CreateTaskUseCase(task_repository=task_repo, project_repository=project_repo)

    # Act
    result = use_case.execute(CreateTaskRequest(**request_data))

    # Assert
    assert result.is_success
    created_task = result.value
    assert UUID(created_task.project_id) == project_repo.get_inbox().id
    assert created_task.priority == expected_behavior["priority"]
