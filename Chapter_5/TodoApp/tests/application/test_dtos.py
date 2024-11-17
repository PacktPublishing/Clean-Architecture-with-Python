# todo_app/tests/application/test_dtos.py
"""Tests for DTO validation logic."""

from datetime import datetime, timedelta

import pytest

from Chapter_5.TodoApp.todo_app.application.dtos.project_dtos import (
    CompleteProjectRequest,
    CreateProjectRequest,
)
from Chapter_5.TodoApp.todo_app.application.dtos.task_dtos import (
    CompleteTaskRequest,
    CreateTaskRequest,
    SetTaskPriorityRequest,
)


class TestCompleteTaskRequest:
    def test_valid_request(self):
        """Test creating request with valid data."""
        request = CompleteTaskRequest(
            task_id="123e4567-e89b-12d3-a456-426614174000",
            completion_notes="Task completed successfully"
        )
        assert request.task_id == "123e4567-e89b-12d3-a456-426614174000"
        assert request.completion_notes == "Task completed successfully"

    def test_empty_task_id(self):
        """Test validation of empty task_id."""
        with pytest.raises(ValueError, match="Task ID is required"):
            CompleteTaskRequest(task_id="   ", completion_notes="Done")

    def test_completion_notes_too_long(self):
        """Test validation of completion notes length."""
        with pytest.raises(ValueError, match="Completion notes cannot exceed 1000 characters"):
            CompleteTaskRequest(
                task_id="123e4567-e89b-12d3-a456-426614174000",
                completion_notes="x" * 1001
            )


class TestCreateTaskRequest:
    def test_valid_request(self):
        """Test creating request with valid data."""
        request = CreateTaskRequest(
            title="Test Task",
            description="Test Description",
            due_date=(datetime.now() + timedelta(days=1)).isoformat(),
            priority="HIGH",
            project_id="123e4567-e89b-12d3-a456-426614174000"
        )
        assert request.title == "Test Task"
        assert request.description == "Test Description"

    def test_empty_title(self):
        """Test validation of empty title."""
        with pytest.raises(ValueError, match="Title is required"):
            CreateTaskRequest(title="   ", description="Test")

    def test_title_too_long(self):
        """Test validation of title length."""
        with pytest.raises(ValueError, match="Title cannot exceed 200 characters"):
            CreateTaskRequest(title="x" * 201, description="Test")

    def test_description_too_long(self):
        """Test validation of description length."""
        with pytest.raises(ValueError, match="Description cannot exceed 2000 characters"):
            CreateTaskRequest(title="Test", description="x" * 2001)


class TestSetTaskPriorityRequest:
    def test_valid_request(self):
        """Test creating request with valid data."""
        request = SetTaskPriorityRequest(
            task_id="123e4567-e89b-12d3-a456-426614174000",
            priority="HIGH"
        )
        assert request.task_id == "123e4567-e89b-12d3-a456-426614174000"
        assert request.priority == "HIGH"

    def test_empty_task_id(self):
        """Test validation of empty task_id."""
        with pytest.raises(ValueError, match="Task ID is required"):
            SetTaskPriorityRequest(task_id="   ", priority="HIGH")

    def test_invalid_priority(self):
        """Test validation of invalid priority."""
        with pytest.raises(ValueError, match="Priority must be one of:"):
            SetTaskPriorityRequest(
                task_id="123e4567-e89b-12d3-a456-426614174000",
                priority="INVALID"
            )

    def test_empty_priority(self):
        """Test validation of empty priority."""
        with pytest.raises(ValueError, match="Priority must be one of:"):
            SetTaskPriorityRequest(
                task_id="123e4567-e89b-12d3-a456-426614174000",
                priority="   "
            )


class TestCreateProjectRequest:
    def test_valid_request(self):
        """Test creating request with valid data."""
        request = CreateProjectRequest(
            name="Test Project",
            description="Test Description"
        )
        assert request.name == "Test Project"
        assert request.description == "Test Description"

    def test_empty_name(self):
        """Test validation of empty name."""
        with pytest.raises(ValueError, match="Project name is required"):
            CreateProjectRequest(name="   ", description="Test")

    def test_name_too_long(self):
        """Test validation of name length."""
        with pytest.raises(ValueError, match="Project name cannot exceed 100 characters"):
            CreateProjectRequest(name="x" * 101, description="Test")

    def test_description_too_long(self):
        """Test validation of description length."""
        with pytest.raises(ValueError, match="Description cannot exceed 2000 characters"):
            CreateProjectRequest(name="Test", description="x" * 2001)


class TestCompleteProjectRequest:
    def test_valid_request(self):
        """Test creating request with valid data."""
        request = CompleteProjectRequest(
            project_id="123e4567-e89b-12d3-a456-426614174000",
            completion_notes="Project completed successfully"
        )
        assert request.project_id == "123e4567-e89b-12d3-a456-426614174000"
        assert request.completion_notes == "Project completed successfully"

    def test_empty_project_id(self):
        """Test validation of empty project_id."""
        with pytest.raises(ValueError, match="Project ID is required"):
            CompleteProjectRequest(project_id="   ", completion_notes="Done")

    def test_completion_notes_too_long(self):
        """Test validation of completion notes length."""
        with pytest.raises(ValueError, match="Completion notes cannot exceed 1000 characters"):
            CompleteProjectRequest(
                project_id="123e4567-e89b-12d3-a456-426614174000",
                completion_notes="x" * 1001
            )


def test_execution_params_conversion():
    """Test conversion of DTOs to execution parameters."""
    # Test CreateTaskRequest conversion
    task_request = CreateTaskRequest(
        title="Test Task",
        description="Test Description",
        due_date=(datetime.now() + timedelta(days=1)).isoformat(),
        priority="HIGH",
        project_id="123e4567-e89b-12d3-a456-426614174000"
    )
    task_params = task_request.to_execution_params()
    assert task_params["title"] == "Test Task"
    assert task_params["description"] == "Test Description"
    assert "deadline" in task_params
    assert "priority" in task_params
    assert "project_id" in task_params

    # Test CreateProjectRequest conversion
    project_request = CreateProjectRequest(
        name="Test Project",
        description="Test Description"
    )
    project_params = project_request.to_execution_params()
    assert project_params["name"] == "Test Project"
    assert project_params["description"] == "Test Description"