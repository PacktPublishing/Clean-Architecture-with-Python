import pytest


@pytest.fixture
def repository(tmp_path):  # tmp_path is a pytest builtin for temp dirs
    """Create repository using temporary directory."""
    return FileTaskRepository(data_dir=tmp_path)

def test_repo_handles_project_task_relationships(tmp_path):
    # Arrange
    task_repo = FileTaskRepository(tmp_path)
    project_repo = FileProjectRepository(tmp_path)
    project_repo.set_task_repository(task_repo)

    # Create project and tasks through the repository
    project = Project(name="Test Project", 
                      description="Testing relationships")
    project_repo.save(project)

    task = Task(title="Test Task",
                description="Testing relationships",
                project_id=project.id)
    task_repo.save(task)
    # Act - Load project with its tasks
    loaded_project = project_repo.get(project.id)

    # Assert
    assert len(loaded_project.tasks) == 1
    assert loaded_project.tasks[0].title == "Test Task"

