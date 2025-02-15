from datetime import datetime, timedelta
from uuid import UUID

import pytest

from todo_app.domain.entities.project import Project
from todo_app.application.dtos.task_dtos import CreateTaskRequest
from todo_app.application.repositories.task_repository import TaskRepository
from todo_app.infrastructure.persistence.file import FileProjectRepository
from todo_app.domain.entities.task import Task
from todo_app.domain.value_objects import Priority, ProjectType
from unittest.mock import Mock

from todo_app.application.use_cases.task_use_cases import (
    CompleteTaskRequest,
    CompleteTaskUseCase,
    CreateTaskUseCase,
)


def test_new_task_priority():
    """Clean test focused purely on domain logic."""
    task = Task(
        title="Test task",
        description="Test description",
        project_id=UUID("12345678-1234-5678-1234-567812345678"),
    )
    assert task.priority == Priority.MEDIUM


def test_task_completion_captures_completion_time():
    """Test that completing a task records the completion timestamp."""
    # Arrange
    task = Task(
        title="Test task",
        description="Test description",
        project_id=UUID("12345678-1234-5678-1234-567812345678"),
    )

    # Act
    task.complete()

    # Assert
    assert task.completed_at is not None
    assert (datetime.now() - task.completed_at) < timedelta(seconds=1)


def test_successful_task_completion():
    """Test task completion using mock dependencies."""
    # Arrange
    task = Task(
        title="Test task",
        description="Test description",
        project_id=UUID("12345678-1234-5678-1234-567812345678"),
    )
    task_repo = Mock()
    task_repo.get.return_value = task
    notification_service = Mock()

    use_case = CompleteTaskUseCase(
        task_repository=task_repo, notification_service=notification_service
    )
    request = CompleteTaskRequest(task_id=str(task.id))
    # Act
    result = use_case.execute(request)

    # Assert
    assert result.is_success
    task_repo.save.assert_called_once_with(task)
    notification_service.notify_task_completed.assert_called_once_with(task)


@pytest.mark.parametrize(
    "request_data,expected_behavior",
    [
        # Default priority task creation
        (
            {"title": "Test Task", "description": "Basic creation"},
            {"project_type": ProjectType.INBOX, "priority": Priority.MEDIUM},
        ),
        # High priority task
        (
            {"title": "Priority Task", "description": "High priority", "priority": "HIGH"},
            {"project_type": ProjectType.INBOX, "priority": Priority.HIGH},
        ),
    ],
    ids=["basic-task", "high-priority-task"],
)
def test_task_creation_scenarios(request_data, expected_behavior, tmp_path):
    """Test task creation use case handles various input scenarios correctly."""
    # Arrange
    task_repo = Mock(spec=TaskRepository)
    project_repo = FileProjectRepository(tmp_path)  # Real project repo for INBOX

    use_case = CreateTaskUseCase(task_repository=task_repo, project_repository=project_repo)

    # Act
    result = use_case.execute(CreateTaskRequest(**request_data))

    # Assert
    assert result.is_success
    created_task = result.value
    assert UUID(created_task.project_id) == project_repo.get_inbox().id
    assert created_task.priority == expected_behavior["priority"]
