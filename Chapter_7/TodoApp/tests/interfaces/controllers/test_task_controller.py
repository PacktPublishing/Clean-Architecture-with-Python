from datetime import datetime, timezone
import pytest
from uuid import uuid4
from todo_app.interfaces.view_models.base import ErrorViewModel
from todo_app.domain.value_objects import TaskStatus, Priority
from todo_app.application.dtos.task_dtos import TaskResponse
from todo_app.application.common.result import Result, Error, ErrorCode
from todo_app.interfaces.controllers.task_controller import TaskController
from todo_app.interfaces.view_models.task_vm import TaskViewModel


@pytest.fixture
def mock_create_use_case():
    class MockCreateUseCase:
        def execute(self, request):
            if request.title == "error":
                return Result.failure(
                    Error(code=ErrorCode.VALIDATION_ERROR, message="Invalid title")
                )
            return Result.success(
                TaskResponse(
                    id=str(uuid4()),
                    title=request.title,
                    project_id=str(uuid4()),
                    description=request.description,
                    status=TaskStatus.TODO,
                    priority=Priority.MEDIUM,
                )
            )

    return MockCreateUseCase()


@pytest.fixture
def mock_complete_use_case():
    class MockCompleteUseCase:
        def execute(self, request):
            # Specific UUID that we'll use to test "not found" scenario
            not_found_id = "550e8400-e29b-41d4-a716-446655440000"

            if request.task_id == not_found_id:
                return Result.failure(Error(code=ErrorCode.NOT_FOUND, message="Task not found"))
            return Result.success(
                TaskResponse(
                    id=request.task_id,
                    title="Test Task",
                    project_id=str(uuid4()),
                    description="Description",
                    status=TaskStatus.DONE,
                    priority=Priority.MEDIUM,
                    completion_date=datetime.now(timezone.utc),
                    completion_notes=request.completion_notes,
                )
            )

    return MockCompleteUseCase()


@pytest.fixture
def mock_presenter():
    class MockPresenter:
        def present_task(self, task_response):
            return TaskViewModel(
                id=task_response.id,
                title=task_response.title,
                description=task_response.description,
                status_display=f"[{task_response.status.name}]",
                priority_display=str(task_response.priority.value),
                due_date_display="",
                project_display="",
                completion_info="",
            )

        def present_error(self, message, code):
            return ErrorViewModel(message=message, code=code)

    return MockPresenter()


@pytest.fixture
def task_controller(mock_create_use_case, mock_complete_use_case, mock_presenter):
    return TaskController(
        create_use_case=mock_create_use_case,
        complete_use_case=mock_complete_use_case,  # Make sure we're using the mock
        presenter=mock_presenter,
    )


def test_handle_create_success(task_controller):
    """Test successful task creation."""
    result = task_controller.handle_create(title="Test Task", description="Test Description")

    assert result.is_success
    assert isinstance(result.success, TaskViewModel)
    assert result.success.title == "Test Task"
    assert result.success.status_display == "[TODO]"


def test_handle_create_failure(task_controller):
    """Test failed task creation."""
    result = task_controller.handle_create(title="error", description="Test Description")

    assert not result.is_success
    assert result.error.message == "Invalid title"
    assert result.error.code == "VALIDATION_ERROR"


def test_handle_create_validation_error(task_controller):
    """Test validation error handling."""
    result = task_controller.handle_create(
        title="", description="Test Description"  # Empty title should raise ValueError
    )

    assert not result.is_success
    assert "Title is required" in result.error.message
    assert result.error.code == "VALIDATION_ERROR"


def test_handle_complete_success(task_controller):
    """Test successful task completion."""
    task_id = str(uuid4())
    result = task_controller.handle_complete(task_id=task_id, notes="Completed successfully")

    assert result.is_success
    assert result.success.id == task_id
    assert isinstance(result.success, TaskViewModel)
    assert result.success.status_display == "[DONE]"


def test_handle_complete_invalid_id_format(task_controller):
    """Test completion with invalid task ID format."""
    result = task_controller.handle_complete(
        task_id="not-a-uuid", notes="Will fail"  # Invalid UUID format
    )

    assert not result.is_success
    assert "Invalid task ID format" in result.error.message
    assert result.error.code == "VALIDATION_ERROR"


def test_handle_complete_task_not_found(task_controller):
    """Test completion of non-existent task."""
    result = task_controller.handle_complete(
        task_id="550e8400-e29b-41d4-a716-446655440000",  # This UUID will trigger the not found case
        notes="Will fail",
    )

    assert not result.is_success
    assert "Task not found" in result.error.message
    assert result.error.code == "NOT_FOUND"
