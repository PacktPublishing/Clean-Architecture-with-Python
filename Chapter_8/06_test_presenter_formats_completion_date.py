from datetime import datetime, timezone
from uuid import UUID


def test_presenter_formats_completion_date():
    """Test that presenter formats dates according to interface requirements."""
    # Arrange
    completion_time = datetime(2024, 1, 15, 14, 30, tzinfo=timezone.utc)
    task = Task(
        title="Test Task",
        description="Test Description",
        project_id=UUID("12345678-1234-5678-1234-567812345678"),
    )
    task.complete()
    # Override completion time for deterministic testing
    task.completed_at = completion_time
    task_response = TaskResponse.from_entity(task)
    presenter = CliTaskPresenter()
    # Act
    view_model = presenter.present_task(task_response)
    # Assert
    expected_format = "2024-01-15 14:30"
    assert view_model.completion_info is not None and expected_format in view_model.completion_info
