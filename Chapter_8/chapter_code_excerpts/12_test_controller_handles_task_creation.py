import pytest


# tests/conftest.py - Root fixtures available to all tests
@pytest.fixture
def sample_task_data():
    """Provide basic task attributes for testing."""
    return {
        "title": "Test Task",
        "description": "Sample task for testing",
        "project_id": UUID("12345678-1234-5678-1234-567812345678"),
    }


# tests/domain/conftest.py - Domain layer fixtures
@pytest.fixture
def domain_task(sample_task_data):
    """Provide a clean Task entity for domain tests."""
    return Task(**sample_task_data)


# tests/application/conftest.py - Application layer fixtures
@pytest.fixture
def mock_task_repository(domain_task):
    """Provide a pre-configured mock repository."""
    repo = Mock(spec=TaskRepository)
    repo.get.return_value = domain_task
    return repo


# tests/interfaces/conftest.py - Interface layer fixtures
@pytest.fixture
def task_controller(mock_task_repository, mock_notification_port):
    """Provide a properly configured TaskController."""
    return TaskController(
        create_use_case=CreateTaskUseCase(
            task_repository=mock_task_repository,
            project_repository=Mock(spec=ProjectRepository),
            notification_service=mock_notification_port,
        ),
        presenter=Mock(spec=TaskPresenter),
    )


@pytest.fixture
def task_request_json():
    """Provide sample request data as it would come from clients."""
    return {"title": "Test Task", "description": "Testing task creation", "priority": "HIGH"}


def test_controller_handles_task_creation(task_controller, task_request_json, mock_task_repository):
    """Test task creation through controller layer."""
    result = task_controller.handle_create(**task_request_json)

    assert result.is_success
    mock_task_repository.save.assert_called_once()
