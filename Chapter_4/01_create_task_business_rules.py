# Create a task
from datetime import datetime, timedelta

from Chapter_4.TodoApp.todo_app.domain.entities.task import Task
from Chapter_4.TodoApp.todo_app.domain.value_objects import Deadline, Priority

task = Task(
    title="Complete project proposal",
    description="Draft and review the proposal for the new client project",
    due_date=Deadline(datetime.now() + timedelta(days=7)),
    priority=Priority.HIGH,
)

# Start the task
task.start()
print(task.status)  # TaskStatus.IN_PROGRESS

# Complete the task
task.complete()
print(task.status)  # TaskStatus.DONE

# Try to start a completed task
try:
    task.start()  # This will raise a ValueError
except ValueError as e:
    print(str(e))  # "Only tasks with 'TODO' status can be started"

# Check if the task is overdue
print(task.is_overdue())  # False
