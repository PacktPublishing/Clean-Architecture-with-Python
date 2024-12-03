import dataclasses
from datetime import datetime, timezone
from uuid import UUID
import pytest

from todo_app.domain.value_objects import ProjectStatus
from todo_app.domain.value_objects import TaskStatus, Priority
from todo_app.application.dtos.task_dtos import TaskResponse
from todo_app.application.dtos.project_dtos import CompleteProjectResponse, ProjectResponse
from todo_app.interfaces.presenters.cli import CliTaskPresenter


@pytest.fixture
def task_presenter():
    return CliTaskPresenter()


@pytest.fixture
def sample_task_response():
    return TaskResponse(
        id="550e8400-e29b-41d4-a716-446655440000",
        title="Test Task",
        description="Test Description",
        status=TaskStatus.IN_PROGRESS,
        priority=Priority.HIGH,
        due_date=datetime(2024, 1, 21, tzinfo=timezone.utc),
        project_id="660e8400-e29b-41d4-a716-446655440000",
        completion_date=None,
        completion_notes=None,
    )


def test_cli_task_presenter_formats_task(task_presenter, sample_task_response):
    """Test that task presenter formats task data correctly for CLI."""
    vm = task_presenter.present_task(sample_task_response)

    assert vm.id == "550e8400-e29b-41d4-a716-446655440000"
    assert vm.title == "Test Task"
    assert vm.status_display == "[IN_PROGRESS]"
    assert vm.priority_display == "High"
    assert vm.due_date_display == "OVERDUE - Due: 2024-01-21"
    assert vm.project_display == "Project: 660e8400-e29b-41d4-a716-446655440000"
    assert vm.completion_info == "Not completed"


def test_cli_task_presenter_handles_completed_task(task_presenter):
    """Test that presenter correctly formats completed task."""
    completed_date = datetime(2024, 1, 20, tzinfo=timezone.utc)
    response = TaskResponse(
        id="123",
        title="Test Task",
        description="Test Description",
        status=TaskStatus.DONE,
        priority=Priority.MEDIUM,
        completion_date=completed_date,
        completion_notes="All done",
    )

    vm = task_presenter.present_task(response)
    assert vm.status_display == "[DONE]"
    assert vm.completion_info == "Completed on 2024-01-20 00:00 - All done"


def test_cli_task_presenter_formats_high_priority_task(task_presenter, sample_task_response):
    """Test formatting of high priority task."""
    high_priority_task = dataclasses.replace(sample_task_response, priority=Priority.HIGH)
    vm = task_presenter.present_task(high_priority_task)
    assert vm.priority_display == "High"


def test_cli_task_presenter_formats_task_without_due_date(task_presenter, sample_task_response):
    """Test formatting of task without due date."""
    task = dataclasses.replace(sample_task_response, due_date=None)
    vm = task_presenter.present_task(task)
    assert vm.due_date_display == "No due date"


def test_cli_task_presenter_formats_completed_task_with_notes(task_presenter):
    """Test formatting of completed task with completion notes."""
    completion_date = datetime(2024, 1, 20, tzinfo=timezone.utc)
    task_response = TaskResponse(
        id="550e8400-e29b-41d4-a716-446655440000",
        title="Test Task",
        description="Test Description",
        status=TaskStatus.DONE,
        priority=Priority.MEDIUM,
        completion_date=completion_date,
        completion_notes="Task completed with additional notes",
    )

    vm = task_presenter.present_task(task_response)
    assert vm.status_display == "[DONE]"
    assert "Task completed with additional notes" in vm.completion_info


def test_cli_task_presenter_formats_overdue_task(task_presenter):
    """Test formatting of overdue task."""
    past_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
    task_response = TaskResponse(
        id="550e8400-e29b-41d4-a716-446655440000",
        title="Overdue Task",
        description="This task is overdue",
        status=TaskStatus.TODO,
        priority=Priority.HIGH,
        due_date=past_date,
    )

    vm = task_presenter.present_task(task_response)
    assert "OVERDUE" in vm.due_date_display


def test_presenter_error_validation_codes():
    """Test presenters handle all possible error codes consistently."""
    error_codes = ["VALIDATION_ERROR", "NOT_FOUND", "BUSINESS_RULE_VIOLATION"]
    presenter = CliTaskPresenter()

    for code in error_codes:
        error_vm = presenter.present_error(f"Test error for {code}", code)
        assert error_vm.code == code
        assert error_vm.message.startswith("Test error for")


def test_presenters_handle_very_long_content(task_presenter):
    """Test presenters handle very long content appropriately."""
    very_long_description = "A" * 1000
    task_response = TaskResponse(
        id="550e8400-e29b-41d4-a716-446655440000",
        title="Test Task",
        description=very_long_description,
        status=TaskStatus.TODO,
        priority=Priority.MEDIUM,
    )

    vm = task_presenter.present_task(task_response)
    assert len(vm.description) == len(very_long_description)
