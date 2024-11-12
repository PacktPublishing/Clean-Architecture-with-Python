# todo_app/tests/domain/test_priority_and_deadline.py
"""Tests for task priority calculation and deadline value object."""

from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time

from Chapter_5.TodoApp.todo_app.domain.entities.task import Task
from Chapter_5.TodoApp.todo_app.domain.services.task_priority_calculator import (
    TaskPriorityCalculator,
)
from Chapter_5.TodoApp.todo_app.domain.value_objects import Deadline, Priority


class TestDeadline:
    def test_create_valid_future_deadline(self):
        """Test creating a deadline in the future."""
        future_date = datetime.now() + timedelta(days=1)
        deadline = Deadline(future_date)
        assert deadline.due_date == future_date

    def test_reject_past_deadline(self):
        """Test that creating a deadline in the past raises an error."""
        past_date = datetime.now() - timedelta(days=1)
        with pytest.raises(ValueError, match="Deadline cannot be in the past"):
            Deadline(past_date)

    @freeze_time("2024-01-01 12:00:00")
    def test_is_overdue(self):
        """Test checking if a deadline is overdue."""
        # Create a deadline for 1 day from now
        future_date = datetime.now() + timedelta(days=1)
        deadline = Deadline(future_date)
        assert not deadline.is_overdue()

        # Time travel to after the deadline
        with freeze_time("2024-01-03 12:00:00"):
            assert deadline.is_overdue()

    @freeze_time("2024-01-01 12:00:00")
    def test_time_remaining(self):
        """Test calculating remaining time until deadline."""
        # Create a deadline for exactly 2 days from now
        due_date = datetime.now() + timedelta(days=2)
        deadline = Deadline(due_date)

        remaining = deadline.time_remaining()
        assert remaining == timedelta(days=2)

        # Time travel to 1 day before deadline
        with freeze_time("2024-01-02 12:00:00"):
            remaining = deadline.time_remaining()
            assert remaining == timedelta(days=1)

        # Time travel past deadline
        with freeze_time("2024-01-04 12:00:00"):
            remaining = deadline.time_remaining()
            assert remaining == timedelta(0)  # Should return 0 when overdue

    @freeze_time("2024-01-01 12:00:00")
    def test_is_approaching(self):
        """Test detecting when deadline is approaching."""
        # Create deadlines at various distances
        far_date = datetime.now() + timedelta(days=5)
        near_date = datetime.now() + timedelta(hours=12)
        very_near_date = datetime.now() + timedelta(hours=1)

        far_deadline = Deadline(far_date)
        near_deadline = Deadline(near_date)
        very_near_deadline = Deadline(very_near_date)

        # Test with default 1-day warning threshold
        assert not far_deadline.is_approaching()
        assert near_deadline.is_approaching()
        assert very_near_deadline.is_approaching()

        # Test with custom warning threshold
        custom_threshold = timedelta(hours=2)
        assert not near_deadline.is_approaching(custom_threshold)
        assert very_near_deadline.is_approaching(custom_threshold)


class TestTaskPriorityCalculator:
    @freeze_time("2024-01-01 12:00:00")
    def test_calculate_priority_overdue(self):
        """Test priority calculation for overdue tasks."""
        # Create a task that will be overdue
        due_date = datetime.now() + timedelta(days=1)
        task = Task(
            title="Test Task",
            description="Test Description",
            due_date=Deadline(due_date),
        )

        # Time travel to after the deadline
        with freeze_time("2024-01-03 12:00:00"):
            priority = TaskPriorityCalculator.calculate_priority(task)
            assert priority == Priority.HIGH

    @freeze_time("2024-01-01 12:00:00")
    def test_calculate_priority_approaching_deadline(self):
        """Test priority calculation for tasks with approaching deadlines."""
        # Create a task due in 2 days
        due_date = datetime.now() + timedelta(days=2)
        task = Task(
            title="Test Task",
            description="Test Description",
            due_date=Deadline(due_date),
        )

        priority = TaskPriorityCalculator.calculate_priority(task)
        assert priority == Priority.MEDIUM

    @freeze_time("2024-01-01 12:00:00")
    def test_calculate_priority_far_deadline(self):
        """Test priority calculation for tasks with far deadlines."""
        # Create a task due in 5 days
        due_date = datetime.now() + timedelta(days=5)
        task = Task(
            title="Test Task",
            description="Test Description",
            due_date=Deadline(due_date),
        )

        priority = TaskPriorityCalculator.calculate_priority(task)
        assert priority == Priority.LOW

    def test_calculate_priority_no_deadline(self):
        """Test priority calculation for tasks without deadlines."""
        task = Task(title="Test Task", description="Test Description")
        expected_priority = task.priority
        priority = TaskPriorityCalculator.calculate_priority(task)
        assert priority == expected_priority

    @pytest.mark.parametrize(
        "days_until_due,expected_priority",
        [
            (0.5, Priority.HIGH),  # 12 hours until due
            (1, Priority.MEDIUM),  # 1 day until due
            (2, Priority.MEDIUM),  # 2 days until due
            (3, Priority.LOW),  # 3 days until due
            (7, Priority.LOW),  # 1 week until due
        ],
    )
    @freeze_time("2024-01-01 12:00:00")
    def test_priority_thresholds(self, days_until_due, expected_priority):
        """Test various deadline thresholds and their resulting priorities."""
        due_date = datetime.now() + timedelta(days=days_until_due)
        task = Task(
            title="Test Task",
            description="Test Description",
            due_date=Deadline(due_date),
        )
        priority = TaskPriorityCalculator.calculate_priority(task)
        assert priority == expected_priority
