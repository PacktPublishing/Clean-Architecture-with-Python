# Create a new task
from Chapter_4.TodoApp.todo_app.domain.entities.task import Task
from Chapter_4.TodoApp.todo_app.domain.value_objects import Priority

task = Task(
    title="Complete project proposal",
    description="Draft and review the proposal for the new client project",
    priority=Priority.HIGH,
)

# Check task properties
print(task.title)  # "Complete project proposal"
print(task.priority)  # Priority.HIGH
print(task.status)  # TaskStatus.TODO
