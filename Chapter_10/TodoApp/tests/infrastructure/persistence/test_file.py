from uuid import UUID
import pytest
from todo_app.application.dtos.task_dtos import CreateTaskRequest
from todo_app.application.use_cases.task_use_cases import CreateTaskUseCase
from todo_app.domain.value_objects import ProjectType
from todo_app.domain.entities.task import Task
from todo_app.domain.entities.project import Project
from todo_app.infrastructure.persistence.file import FileTaskRepository, FileProjectRepository


@pytest.fixture  # Pytest fixtures provide reusable test dependencies
def repository(tmp_path):  # tmp_path is a pytest builtin for temp dirs
    """Create repository using temporary directory."""
    return FileTaskRepository(data_dir=tmp_path)


def test_repository_handles_project_task_relationships(tmp_path):
    """Integration test verifying repository handles entity relationships."""
    # Arrange
    task_repo = FileTaskRepository(tmp_path)
    project_repo = FileProjectRepository(tmp_path)
    project_repo.set_task_repository(task_repo)

    # Create project and tasks through the repository
    project = Project(name="Test Project", description="Testing relationships")
    project_repo.save(project)

    task = Task(title="Test Task", description="Testing relationships", project_id=project.id)
    task_repo.save(task)

    # Act - Load project with its tasks
    loaded_project = project_repo.get(project.id)

    # Assert
    assert len(loaded_project.tasks) == 1
    assert loaded_project.tasks[0].title == "Test Task"


def test_repository_automatically_creates_inbox(tmp_path):
    """Test that project repository maintains inbox project across instantiations."""
    # Arrange - Create initial repository and verify Inbox exists
    initial_repo = FileProjectRepository(tmp_path)
    initial_inbox = initial_repo.get_inbox()
    assert initial_inbox.name == "INBOX"
    assert initial_inbox.project_type == ProjectType.INBOX

    # Act - Create new repository instance pointing to same directory
    new_repo = FileProjectRepository(tmp_path)

    # Assert - New instance maintains same Inbox
    persisted_inbox = new_repo.get_inbox()
    assert persisted_inbox.id == initial_inbox.id
    assert persisted_inbox.project_type == ProjectType.INBOX


def test_task_creation_with_persistence(tmp_path):
    """Test task creation use case with real persistence."""
    # Arrange
    task_repo = FileTaskRepository(tmp_path)
    project_repo = FileProjectRepository(tmp_path)
    project_repo.set_task_repository(task_repo)

    use_case = CreateTaskUseCase(
        task_repository=task_repo,
        project_repository=project_repo,
    )

    # Act
    result = use_case.execute(CreateTaskRequest(title="Test Task", description="Integration test"))

    # Assert - Task was persisted
    assert result.is_success
    created_task = task_repo.get(UUID(result.value.id))
    assert created_task.project_id == project_repo.get_inbox().id
