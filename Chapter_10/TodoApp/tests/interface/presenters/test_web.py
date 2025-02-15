from datetime import datetime, timedelta, timezone
from todo_app.application.dtos.task_dtos import TaskResponse
from todo_app.interfaces.presenters.web import WebTaskPresenter
from todo_app.domain.value_objects import TaskStatus, Priority


def test_web_presenter_formats_overdue_date():
    """Test that presenter properly formats overdue dates."""
    # Arrange
    past_date = datetime.now(timezone.utc) - timedelta(days=1)
    task_response = TaskResponse(
        id="123",
        title="Test Task",
        description="Test Description",
        status=TaskStatus.TODO,
        priority=Priority.MEDIUM,
        project_id="456",
        due_date=past_date,
    )
    presenter = WebTaskPresenter()

    # Act
    view_model = presenter.present_task(task_response)

    # Assert
    assert view_model.due_date_display is not None
    assert "Overdue" in view_model.due_date_display
    assert past_date.strftime("%Y-%m-%d") in view_model.due_date_display


def test_web_presenter_formats_future_date():
    """Test that presenter properly formats future dates."""
    # Arrange
    future_date = datetime.now(timezone.utc) + timedelta(days=1)
    task_response = TaskResponse(
        id="123",
        title="Test Task",
        description="Test Description",
        status=TaskStatus.TODO,
        priority=Priority.MEDIUM,
        project_id="456",
        due_date=future_date,
    )
    presenter = WebTaskPresenter()

    # Act
    view_model = presenter.present_task(task_response)

    # Assert
    assert view_model.due_date_display is not None
    assert "Overdue" not in view_model.due_date_display
    assert future_date.strftime("%Y-%m-%d") in view_model.due_date_display
