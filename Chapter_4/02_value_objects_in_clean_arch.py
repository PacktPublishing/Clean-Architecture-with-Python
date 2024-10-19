# Using string (problematic)
from Chapter_4.TodoApp.todo_app.domain.entities.task import Task
from Chapter_4.TodoApp.todo_app.domain.value_objects import TaskStatus

task = Task("Complete project", "The important project")
task.status = "Finished"  # Allowed, but invalid
print(task.status == "done")  # False, case-sensitive

# Using TaskStatus enum (robust)
task = Task("Complete project", "The important project")
task.status = TaskStatus.DONE  # Type-safe
print(task.status == TaskStatus.DONE)  # True, no case issues
