from datetime import datetime

from todo_app.domain.entities.project import Project
from todo_app.domain.entities.task import Task
from todo_app.domain.value_objects import Deadline, Priority

# Project usage
project = Project("Website Redesign")
task1 = Task(
    title="Design homepage",
    description="Create new homepage layout",
    due_date=Deadline(datetime(2023, 12, 31)),
    priority=Priority.HIGH,
)
task2 = Task(
    title="Implement login",
    description="Add user authentication",
    due_date=Deadline(datetime(2023, 11, 30)),
    priority=Priority.MEDIUM,
)
project.add_task(task1)
project.add_task(task2)

print(f"Project: {project.name}")
print(f"Number of tasks: {len(project.tasks)}")
print(f"First task: {project.tasks[0].title}")
