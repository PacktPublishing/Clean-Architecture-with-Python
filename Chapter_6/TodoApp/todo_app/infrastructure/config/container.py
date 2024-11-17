from dataclasses import dataclass


from todo_app.application.ports.notifications import NotificationPort
from todo_app.application.repositories.project_repository import ProjectRepository
from todo_app.application.repositories.task_repository import TaskRepository
from todo_app.interfaces.presenters.base import ProjectPresenter, TaskPresenter
from todo_app.application.use_cases.project_use_cases import CompleteProjectUseCase, CreateProjectUseCase
from todo_app.application.use_cases.task_use_cases import CompleteTaskUseCase, CreateTaskUseCase
from todo_app.interfaces.controllers.project_controller import ProjectController
from todo_app.interfaces.controllers.task_controller import TaskController 

@dataclass
class Application:
    """
    Application container that configures and wires together all components.
    This acts as our composition root.
    """
    task_repository: TaskRepository
    project_repository: ProjectRepository
    notification_service: NotificationPort
    task_presenter: TaskPresenter
    project_presenter: ProjectPresenter

    def __post_init__(self):
        # Wire up use cases
        self.create_task_use_case = CreateTaskUseCase(
            self.task_repository, 
            self.project_repository
        )
        self.complete_task_use_case = CompleteTaskUseCase(
            self.task_repository, 
            self.notification_service
        )
        self.create_project_use_case = CreateProjectUseCase(
            self.project_repository
        )
        self.complete_project_use_case = CompleteProjectUseCase(
            self.project_repository,
            self.task_repository,
            self.notification_service,
        )
        
        # Wire up controllers with their dependencies
        self.task_controller = TaskController(
            create_use_case=self.create_task_use_case,
            complete_use_case=self.complete_task_use_case,
            presenter=self.task_presenter
        )
        self.project_controller = ProjectController(
            create_use_case=self.create_project_use_case,
            complete_use_case=self.complete_project_use_case,
            presenter=self.project_presenter
        )
    