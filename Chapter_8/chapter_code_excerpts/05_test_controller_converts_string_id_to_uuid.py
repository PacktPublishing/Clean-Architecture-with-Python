from uuid import UUID
from unittest.mock import Mock


def test_controller_converts_string_id_to_uuid():
    """Test that controller properly converts string IDs to UUIDs for use cases."""
    # Arrange
    task_id = "123e4567-e89b-12d3-a456-426614174000"
    complete_use_case = Mock()
    complete_use_case.execute.return_value = Result.success(
        TaskResponse.from_entity(
            Task(
                title="Test Task",
                description="Test Description",
                project_id=UUID("12345678-1234-5678-1234-567812345678"),
            )
        )
    )
    presenter = Mock(spec=TaskPresenter)

    controller = TaskController(
        complete_use_case=complete_use_case,
        presenter=presenter,
    )

    # Act
    controller.handle_complete(task_id=task_id)

    # Assert
    complete_use_case.execute.assert_called_once()
    called_request = complete_use_case.execute.call_args[0][0]
    assert isinstance(called_request.task_id, UUID)
