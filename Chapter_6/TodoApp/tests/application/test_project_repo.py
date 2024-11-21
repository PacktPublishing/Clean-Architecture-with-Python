from uuid import UUID

import pytest

from todo_app.infrastructure.persistence.memory import InMemoryProjectRepository
from todo_app.domain.entities.project import Project
from todo_app.domain.exceptions import ProjectNotFoundError



def test_project_repository_delete():
    """Test deleting a project from repository."""
    repo = InMemoryProjectRepository()
    project = Project(name="Test Project")
    repo.save(project)

    # Verify project exists
    assert repo.get(project.id) == project

    # Delete project
    repo.delete(project.id)

    # Verify project is gone
    with pytest.raises(ProjectNotFoundError):
        repo.get(project.id)


def test_project_repository_delete_nonexistent():
    """Test deleting a nonexistent project."""
    repo = InMemoryProjectRepository()
    random_id = UUID("123e4567-e89b-12d3-a456-426614174000")

    # Should not raise an error when deleting nonexistent project
    repo.delete(random_id)


def test_project_repository_delete_and_recreate():
    """Test deleting a project and then creating a new one with the same name."""
    repo = InMemoryProjectRepository()

    # Create and delete first project
    project1 = Project(name="Test Project")
    repo.save(project1)
    repo.delete(project1.id)

    # Create second project with same name
    project2 = Project(name="Test Project")
    repo.save(project2)

    # Verify new project exists and has different ID
    saved_project = repo.get(project2.id)
    assert saved_project == project2
    assert saved_project.id != project1.id
