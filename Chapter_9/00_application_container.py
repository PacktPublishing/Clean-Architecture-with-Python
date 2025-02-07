# todo_app/infrastructure/configuration/container.py
@dataclass
class Application:
    """Container which wires together all components."""

    task_repository: TaskRepository
    project_repository: ProjectRepository
    notification_service: NotificationPort
    task_presenter: TaskPresenter
    project_presenter: ProjectPresenter
