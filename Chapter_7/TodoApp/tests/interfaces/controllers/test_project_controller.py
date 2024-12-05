from datetime import datetime, timezone
from uuid import uuid4
import pytest

from todo_app.domain.value_objects import ProjectStatus, ProjectType
from todo_app.application.dtos.project_dtos import ProjectResponse, CompleteProjectResponse
from todo_app.application.common.result import Result, Error, ErrorCode
from todo_app.interfaces.controllers.project_controller import ProjectController
from todo_app.interfaces.view_models.project_vm import ProjectViewModel
from todo_app.interfaces.view_models.base import ErrorViewModel


@pytest.fixture
def mock_create_use_case():
    class MockCreateUseCase:
        def execute(self, request):
            if request.name == "error":
                return Result.failure(
                    Error(code=ErrorCode.VALIDATION_ERROR, message="Invalid project name")
                )
            return Result.success(
                ProjectResponse(
                    id=str(uuid4()),
                    name=request.name,
                    description=request.description,
                    project_type=ProjectType.REGULAR,
                    status=ProjectStatus.ACTIVE,
                    completion_date=None,
                    tasks=[],
                )
            )

    return MockCreateUseCase()


@pytest.fixture
def mock_complete_use_case():
    class MockCompleteUseCase:
        def execute(self, request):
            not_found_id = "550e8400-e29b-41d4-a716-446655440000"

            if request.project_id == not_found_id:
                return Result.failure(Error(code=ErrorCode.NOT_FOUND, message="Project not found"))
            return Result.success(
                ProjectResponse(
                    id=request.project_id,
                    name="Test Project",
                    description="Description",
                    project_type=ProjectType.REGULAR,
                    status=ProjectStatus.COMPLETED,
                    completion_date=datetime.now(timezone.utc),
                    tasks=[],
                )
            )

    return MockCompleteUseCase()


@pytest.fixture
def mock_presenter():
    class MockPresenter:
        def present_project(self, project_response):
            return ProjectViewModel(
                id=project_response.id,
                name=project_response.name,
                description=project_response.description,
                project_type=project_response.project_type,
                status_display=f"[{project_response.status.name}]",
                task_count=len(project_response.tasks),
                completed_task_count=0,
                completion_info=(
                    "Not completed" if not project_response.completion_date else "Completed"
                ),
                tasks=[],
            )

        def present_error(self, message, code):
            return ErrorViewModel(message=message, code=code)

    return MockPresenter()


@pytest.fixture
def mock_get_use_case():
    pass


@pytest.fixture
def mock_list_use_case():
    pass


@pytest.fixture
def mock_update_use_case():
    pass


@pytest.fixture
def project_controller(
    mock_create_use_case,
    mock_complete_use_case,
    mock_presenter,
    mock_get_use_case,
    mock_list_use_case,
    mock_update_use_case,
):
    return ProjectController(
        create_use_case=mock_create_use_case,
        complete_use_case=mock_complete_use_case,
        presenter=mock_presenter,
        get_use_case=mock_get_use_case,
        list_use_case=mock_list_use_case,
        update_use_case=mock_update_use_case,
    )


def test_handle_create_success(project_controller):
    """Test successful project creation."""
    result = project_controller.handle_create(name="Test Project", description="Test Description")

    assert result.is_success
    assert isinstance(result.success, ProjectViewModel)
    assert result.success.name == "Test Project"
    assert result.success.status_display == "[ACTIVE]"


def test_handle_create_failure(project_controller):
    """Test failed project creation."""
    result = project_controller.handle_create(name="error", description="Test Description")

    assert not result.is_success
    assert result.error.message == "Invalid project name"
    assert result.error.code == "VALIDATION_ERROR"


def test_handle_create_validation_error(project_controller):
    """Test validation error handling."""
    result = project_controller.handle_create(
        name="", description="Test Description"  # Empty name should raise ValueError
    )

    assert not result.is_success
    assert "Project name is required" in result.error.message
    assert result.error.code == "VALIDATION_ERROR"


def test_handle_complete_success(project_controller):
    """Test successful project completion."""
    # Use a valid UUID format
    valid_uuid = "123e4567-e89b-12d3-a456-426614174000"

    result = project_controller.handle_complete(
        project_id=valid_uuid, notes="Completed successfully"
    )

    assert result.is_success
    assert isinstance(result.success, ProjectViewModel)
    assert result.success.status_display == "[COMPLETED]"
    assert result.success.completion_info == "Completed"


def test_handle_complete_invalid_id_format(project_controller):
    """Test completion with invalid project ID format."""
    result = project_controller.handle_complete(project_id="not-a-uuid", notes="Will fail")

    assert not result.is_success
    assert "Invalid project ID format" in result.error.message
    assert result.error.code == "VALIDATION_ERROR"


def test_handle_complete_project_not_found(project_controller):
    """Test completion of non-existent project."""
    result = project_controller.handle_complete(
        project_id="550e8400-e29b-41d4-a716-446655440000",  # Valid UUID but project doesn't exist
        notes="Will fail",
    )

    assert not result.is_success
    assert "Project not found" in result.error.message
    assert result.error.code == "NOT_FOUND"
