from datetime import timedelta

from todo_app.domain.entities.task import Task
from todo_app.domain.value_objects import Priority


class TaskPriorityCalculator:
    @staticmethod
    def calculate_priority(task: Task) -> Priority:
        """
        Consider Task Priority based on impending due date

        """
        # No adjustment needed if no due date
        if task.due_date is None:
            return task.priority
        # High if overdue or due within 12 hours
        if task.is_overdue() or task.due_date.time_remaining() <= timedelta(
            hours=12
        ):
            return Priority.HIGH
        # Med if task due within 2 days
        elif task.due_date and task.due_date.time_remaining() <= timedelta(
            days=2
        ):
            return Priority.MEDIUM
        else:
            return Priority.LOW
