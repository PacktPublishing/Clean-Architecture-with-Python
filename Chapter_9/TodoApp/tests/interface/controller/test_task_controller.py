from unittest.mock import Mock
from uuid import UUID
from todo_app.application.use_cases.task_use_cases import CompleteTaskUseCase
from todo_app.application.common.result import Result
from todo_app.domain.entities.task import Task
from todo_app.interfaces.controllers.task_controller import TaskController
from todo_app.interfaces.presenters.base import TaskPresenter
from todo_app.application.dtos.task_dtos import TaskResponse


def test_controller_sends_uuid_to_repository():
    """Test that repository receives UUID for task operations."""
    # Arrange
    task_id = "123e4567-e89b-12d3-a456-426614174000"
    expected_uuid = UUID(task_id)
    mock_repo = Mock()
    mock_repo.get.return_value = Task(
        title="Test Task",
        description="Test Description",
        project_id=UUID("12345678-1234-5678-1234-567812345678"),
    )
    complete_use_case = CompleteTaskUseCase(task_repository=mock_repo, notification_service=Mock())

    controller = TaskController(
        complete_use_case=complete_use_case,
        get_use_case=Mock(),
        create_use_case=Mock(),
        update_use_case=Mock(),
        delete_use_case=Mock(),
        presenter=Mock(spec=TaskPresenter),
    )

    # Act
    controller.handle_complete(task_id=task_id)

    # Assert
    mock_repo.get.assert_called_once()
    actual_uuid = mock_repo.get.call_args[0][0]
    assert isinstance(actual_uuid, UUID)
    assert actual_uuid == expected_uuid
