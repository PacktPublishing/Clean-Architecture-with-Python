# todo_app/tests/application/test_task_use_cases.py
"""Tests for task-related use cases."""

from uuid import uuid4

import pytest

from Chapter_5.TodoApp.tests.application.conftest import (
    InMemoryTaskRepository,
    InMemoryProjectRepository,
    NotificationRecorder,
)
from Chapter_5.TodoApp.todo_app.application.common.result import ErrorCode
from Chapter_5.TodoApp.todo_app.application.dtos.task_dtos import (
    CreateTaskRequest,
    CompleteTaskRequest,
    SetTaskPriorityRequest,
)
from Chapter_5.TodoApp.todo_app.application.use_cases.task_use_cases import (
    CreateTaskUseCase,
    CompleteTaskUseCase,
    SetTaskPriorityUseCase,
)
from Chapter_5.TodoApp.todo_app.domain.entities.project import Project
from Chapter_5.TodoApp.todo_app.domain.entities.task import Task
from Chapter_5.TodoApp.todo_app.domain.exceptions import (
    BusinessRuleViolation,
    ValidationError,
)
from Chapter_5.TodoApp.todo_app.domain.value_objects import Priority, TaskStatus


def test_create_task_basic():
    """Test creating a task with basic information."""
    # Arrange
    repo = InMemoryTaskRepository()
    project_repo = InMemoryProjectRepository()
    use_case = CreateTaskUseCase(repo, project_repo)

    request = CreateTaskRequest(
        title="Test Task", description="Test Description"
    )

    # Act
    result = use_case.execute(request)

    # Assert
    assert result.is_success
    assert result.value.title == "Test Task"
    assert result.value.description == "Test Description"
    assert result.value.status == TaskStatus.TODO.value
    assert result.value.priority == Priority.MEDIUM.value


def test_create_task_with_project():
    """Test creating a task associated with a project."""
    # Arrange
    task_repo = InMemoryTaskRepository()
    project_repo = InMemoryProjectRepository()
    use_case = CreateTaskUseCase(task_repo, project_repo)

    # Create a project first
    project = Project(name="Test Project")
    project_repo.save(project)

    request = CreateTaskRequest(
        title="Test Task",
        description="Test Description",
        project_id=str(project.id),
    )

    # Act
    result = use_case.execute(request)

    # Assert
    assert result.is_success
    assert result.value.project_id == str(project.id)


def test_create_task_with_invalid_project():
    """Test creating a task with non-existent project ID."""
    # Arrange
    task_repo = InMemoryTaskRepository()
    project_repo = InMemoryProjectRepository()
    use_case = CreateTaskUseCase(task_repo, project_repo)

    request = CreateTaskRequest(
        title="Test Task",
        description="Test Description",
        project_id=str(uuid4()),
    )

    # Act
    result = use_case.execute(request)

    # Assert
    assert not result.is_success
    assert result.error.code.value == "NOT_FOUND"


def test_complete_task():
    """Test completing a task."""
    # Arrange
    repo = InMemoryTaskRepository()
    notifications = NotificationRecorder()
    use_case = CompleteTaskUseCase(repo, notifications)

    # Create and save a task
    task = Task(title="Test Task", description="Test Description")
    repo.save(task)

    request = CompleteTaskRequest(
        task_id=str(task.id), completion_notes="Done!"
    )

    # Act
    result = use_case.execute(request)

    # Assert
    assert result.is_success
    assert result.value.status == TaskStatus.DONE.value
    assert result.value.completion_notes == "Done!"
    assert task.id in notifications.completed_tasks


def test_complete_nonexistent_task():
    """Test completing a task that doesn't exist."""
    # Arrange
    repo = InMemoryTaskRepository()
    notifications = NotificationRecorder()
    use_case = CompleteTaskUseCase(repo, notifications)

    request = CompleteTaskRequest(
        task_id=str(uuid4()), completion_notes="Done!"
    )

    # Act
    result = use_case.execute(request)

    # Assert
    assert not result.is_success
    assert result.error.code.value == "NOT_FOUND"
    assert not notifications.completed_tasks  # No notification sent


def test_set_task_priority():
    """Test setting a task's priority."""
    # Arrange
    repo = InMemoryTaskRepository()
    notifications = NotificationRecorder()
    use_case = SetTaskPriorityUseCase(repo, notifications)

    # Create and save a task
    task = Task(title="Test Task", description="Test Description")
    repo.save(task)

    request = SetTaskPriorityRequest(task_id=str(task.id), priority="HIGH")

    # Act
    result = use_case.execute(request)

    # Assert
    assert result.is_success
    assert result.value.priority == Priority.HIGH.value
    assert task.id in notifications.high_priority_tasks


def test_set_task_invalid_priority():
    """Test setting an invalid priority."""
    # Arrange
    repo = InMemoryTaskRepository()
    notifications = NotificationRecorder()
    use_case = SetTaskPriorityUseCase(repo, notifications)

    task = Task(title="Test Task", description="Test Description")
    repo.save(task)

    with pytest.raises(ValueError) as exc_info:
        SetTaskPriorityRequest(task_id=str(task.id), priority="INVALID")

    assert "Priority must be one of" in str(exc_info.value)


def test_complete_task_handles_validation_error():
    """Test handling of ValidationError during task completion."""
    task = Task(title="Test Task", description="Test Description")

    class ValidationErrorTaskRepository(InMemoryTaskRepository):
        def save(self, task):
            raise ValidationError("Invalid completion state")

    repo = ValidationErrorTaskRepository()
    repo._tasks[task.id] = task  # Add task directly to repo
    notifications = NotificationRecorder()
    use_case = CompleteTaskUseCase(repo, notifications)

    request = CompleteTaskRequest(
        task_id=str(task.id), completion_notes="Done!"
    )

    result = use_case.execute(request)

    assert not result.is_success
    assert result.error.code == ErrorCode.VALIDATION_ERROR
    assert "Invalid completion state" in result.error.message
    assert not notifications.completed_tasks


def test_complete_task_handles_business_rule_violation():
    """Test handling of BusinessRuleViolation during task completion."""
    task = Task(title="Test Task", description="Test Description")

    class BusinessRuleTaskRepository(InMemoryTaskRepository):
        def save(self, task):
            raise BusinessRuleViolation("Cannot complete task in current state")

    repo = BusinessRuleTaskRepository()
    repo._tasks[task.id] = task  # Add task directly to repo
    notifications = NotificationRecorder()
    use_case = CompleteTaskUseCase(repo, notifications)

    request = CompleteTaskRequest(
        task_id=str(task.id), completion_notes="Done!"
    )

    result = use_case.execute(request)

    assert not result.is_success
    assert result.error.code == ErrorCode.BUSINESS_RULE_VIOLATION
    assert "Cannot complete task in current state" in result.error.message
    assert not notifications.completed_tasks


def test_create_task_request_validates_project_id_format():
    """Test that CreateTaskRequest validates project ID format."""
    # Valid UUID should work
    valid_request = CreateTaskRequest(
        title="Test Task",
        description="Test Description",
        project_id="123e4567-e89b-12d3-a456-426614174000",
    )
    assert valid_request.project_id == "123e4567-e89b-12d3-a456-426614174000"

    # Invalid UUID should raise ValueError
    with pytest.raises(ValueError, match="Invalid project ID format"):
        CreateTaskRequest(
            title="Test Task",
            description="Test Description",
            project_id="not-a-uuid",
        )

    # Empty project_id should be allowed (Optional)
    no_project_request = CreateTaskRequest(
        title="Test Task", description="Test Description", project_id=None
    )
    assert no_project_request.project_id is None


def test_create_task_handles_validation_error():
    """Test handling of ValidationError during task creation."""

    class ValidationErrorTaskRepository(InMemoryTaskRepository):
        def save(self, task):
            raise ValidationError("Invalid task data")

    task_repo = ValidationErrorTaskRepository()
    project_repo = InMemoryProjectRepository()
    use_case = CreateTaskUseCase(task_repo, project_repo)

    request = CreateTaskRequest(
        title="Test Task", description="Test Description"
    )

    result = use_case.execute(request)

    assert not result.is_success
    assert result.error.code == ErrorCode.VALIDATION_ERROR
    assert "Invalid task data" in result.error.message


def test_create_task_handles_business_rule_violation():
    """Test handling of BusinessRuleViolation during task creation."""

    class BusinessRuleTaskRepository(InMemoryTaskRepository):
        def save(self, task):
            raise BusinessRuleViolation("Task limit exceeded")

    task_repo = BusinessRuleTaskRepository()
    project_repo = InMemoryProjectRepository()
    use_case = CreateTaskUseCase(task_repo, project_repo)

    request = CreateTaskRequest(
        title="Test Task", description="Test Description"
    )

    result = use_case.execute(request)

    assert not result.is_success
    assert result.error.code == ErrorCode.BUSINESS_RULE_VIOLATION
    assert "Task limit exceeded" in result.error.message


def test_create_task_handles_validation_error_with_project():
    """Test handling of ValidationError during task creation with project."""
    project = Project(name="Test Project")

    class ValidationErrorTaskRepository(InMemoryTaskRepository):
        def save(self, task):
            raise ValidationError("Invalid task data")

    task_repo = ValidationErrorTaskRepository()
    project_repo = InMemoryProjectRepository()
    project_repo._projects[project.id] = project  # Add project directly
    use_case = CreateTaskUseCase(task_repo, project_repo)

    request = CreateTaskRequest(
        title="Test Task",
        description="Test Description",
        project_id=str(project.id),
    )

    result = use_case.execute(request)

    assert not result.is_success
    assert result.error.code == ErrorCode.VALIDATION_ERROR
    assert "Invalid task data" in result.error.message


def test_complete_task_rolls_back_on_validation_error():
    """Test that task state is rolled back on ValidationError."""
    # Set up task
    task = Task(title="Test Task", description="Test Description")

    class FailingTaskRepository(InMemoryTaskRepository):
        def save(self, task):
            if task.status == TaskStatus.DONE:
                raise ValidationError("Cannot complete task")
            super().save(task)

    repo = FailingTaskRepository()
    notifications = NotificationRecorder()

    # Save initial state
    repo.save(task)

    use_case = CompleteTaskUseCase(repo, notifications)
    request = CompleteTaskRequest(
        task_id=str(task.id), completion_notes="Done!"
    )

    # Execute use case (should fail)
    result = use_case.execute(request)

    # Verify failure
    assert not result.is_success
    assert result.error.code == ErrorCode.VALIDATION_ERROR

    # Verify task state was rolled back
    saved_task = repo.get(task.id)
    assert saved_task.status == TaskStatus.TODO
    assert saved_task.completed_at is None
    assert saved_task.completion_notes is None

    # Verify no notifications were sent
    assert not notifications.completed_tasks


def test_complete_task_rolls_back_on_business_rule_violation():
    """Test that task state is rolled back on BusinessRuleViolation."""
    # Set up task
    task = Task(title="Test Task", description="Test Description")

    class FailingTaskRepository(InMemoryTaskRepository):
        def save(self, task):
            if task.status == TaskStatus.DONE:
                raise BusinessRuleViolation("Task completion limit reached")
            super().save(task)

    repo = FailingTaskRepository()
    notifications = NotificationRecorder()

    # Save initial state
    repo.save(task)

    use_case = CompleteTaskUseCase(repo, notifications)
    request = CompleteTaskRequest(
        task_id=str(task.id), completion_notes="Done!"
    )

    # Execute use case (should fail)
    result = use_case.execute(request)

    # Verify failure
    assert not result.is_success
    assert result.error.code == ErrorCode.BUSINESS_RULE_VIOLATION

    # Verify task state was rolled back
    saved_task = repo.get(task.id)
    assert saved_task.status == TaskStatus.TODO
    assert saved_task.completed_at is None
    assert saved_task.completion_notes is None

    # Verify no notifications were sent
    assert not notifications.completed_tasks


def test_complete_task_maintains_state_on_successful_completion():
    """Test that task state changes persist when completion is successful."""
    task = Task(title="Test Task", description="Test Description")

    repo = InMemoryTaskRepository()
    notifications = NotificationRecorder()

    # Save initial state
    repo.save(task)

    use_case = CompleteTaskUseCase(repo, notifications)
    completion_notes = "Done!"
    request = CompleteTaskRequest(
        task_id=str(task.id), completion_notes=completion_notes
    )

    # Execute use case (should succeed)
    result = use_case.execute(request)

    # Verify success
    assert result.is_success

    # Verify task state was updated and persisted
    saved_task = repo.get(task.id)
    assert saved_task.status == TaskStatus.DONE
    assert saved_task.completed_at is not None
    assert saved_task.completion_notes == completion_notes

    # Verify notification was sent
    assert task.id in notifications.completed_tasks


def test_create_task_with_nonexistent_project():
    """Test handling of nonexistent project ID during task creation."""
    task_repo = InMemoryTaskRepository()
    project_repo = InMemoryProjectRepository()
    use_case = CreateTaskUseCase(task_repo, project_repo)

    # Use a valid UUID format but for a nonexistent project
    request = CreateTaskRequest(
        title="Test Task",
        description="Test Description",
        project_id="123e4567-e89b-12d3-a456-426614174000",  # Valid UUID that doesn't exist
    )

    result = use_case.execute(request)

    assert not result.is_success
    assert result.error.code == ErrorCode.NOT_FOUND
    assert (
        "Project with id 123e4567-e89b-12d3-a456-426614174000 not found"
        in result.error.message
    )


def test_create_task_fails_with_malformed_project_id():
    # Test that this raised ValueError
    with pytest.raises(ValueError, match="Invalid project ID format"):
        _ = CreateTaskRequest(
            title="Test Task",
            description="Test Description",
            project_id="malformed project id",
        )


def test_set_task_priority_fails_with_malformed_task_id():
    # Test that this raised ValueError
    with pytest.raises(ValueError, match="Invalid task ID format"):
        _ = SetTaskPriorityRequest(
            task_id="malformed project id",
            priority="HIGH",
        )


def test_set_task_priority_handles_validation_error():
    """Test handling of ValidationError during priority setting."""
    # Create a task
    task = Task(title="Test Task", description="Test Description")

    class ValidationErrorTaskRepository(InMemoryTaskRepository):
        def save(self, task):
            raise ValidationError("Invalid priority state")

    repo = ValidationErrorTaskRepository()
    repo._tasks[task.id] = task  # Add task directly to repo
    notifications = NotificationRecorder()

    use_case = SetTaskPriorityUseCase(repo, notifications)
    request = SetTaskPriorityRequest(task_id=str(task.id), priority="HIGH")

    result = use_case.execute(request)

    assert not result.is_success
    assert result.error.code == ErrorCode.VALIDATION_ERROR
    assert "Invalid priority state" in result.error.message
    assert not notifications.high_priority_tasks
