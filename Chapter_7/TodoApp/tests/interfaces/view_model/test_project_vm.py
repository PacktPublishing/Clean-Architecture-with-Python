import dataclasses
import pytest
from todo_app.domain.value_objects import ProjectType
from todo_app.interfaces.view_models.project_vm import ProjectViewModel


def test_project_view_model_creation():
    """Test creating a ProjectViewModel with all fields."""
    vm = ProjectViewModel(
        id="123",
        name="Test Project",
        project_type=ProjectType.REGULAR.value,
        description="Test Description",
        status_display="[ACTIVE]",
        task_count=5,
        completed_task_count=2,
        completion_info="Not completed",
        tasks=[],
    )

    assert vm.id == "123"
    assert vm.name == "Test Project"
    assert vm.description == "Test Description"
    assert vm.status_display == "[ACTIVE]"
    assert vm.task_count == 5
    assert vm.completed_task_count == 2
    assert vm.completion_info == "Not completed"


def test_project_view_model_immutability():
    """Test that ProjectViewModel is immutable."""
    vm = ProjectViewModel(
        id="123",
        name="Test Project",
        project_type=ProjectType.REGULAR.value,
        description="Test Description",
        status_display="[ACTIVE]",
        task_count=5,
        completed_task_count=2,
        completion_info="Not completed",
        tasks=[],
    )

    with pytest.raises(dataclasses.FrozenInstanceError):
        vm.name = "New Name"
