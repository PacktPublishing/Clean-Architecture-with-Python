from uuid import UUID

from todo_app.domain.entities.task import Task
from todo_app.domain.value_objects import Priority


class TaskFactory:
    def __init__(self, user_service, project_repository):
        self.user_service = user_service
        self.project_repository = project_repository

    def create_task_in_project(
        self, title: str, description: str, project_id: UUID, assignee_id: UUID
    ):
        project = self.project_repository.get_by_id(project_id)
        assignee = self.user_service.get_user(assignee_id)

        task = Task(title, description)
        task.project = project
        task.assignee = assignee

        if project.is_high_priority() and assignee.is_manager():
            task.priority = Priority.HIGH

        project.add_task(task)
        return task
