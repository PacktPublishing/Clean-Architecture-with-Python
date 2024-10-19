from datetime import timedelta

from Chapter_4.TodoApp.todo_app.domain.entities.task import Task
from Chapter_4.TodoApp.todo_app.domain.value_objects import Priority


class TaskPriorityCalculator:
    @staticmethod
    def calculate_priority(task: Task) -> Priority:
        if task.is_overdue():
            return Priority.HIGH
        elif task.due_date and task.due_date.time_remaining() <= timedelta(days=2):
            return Priority.MEDIUM
        else:
            return Priority.LOW
