@dataclass
class Application:
    """Container which wires together all components."""

    task_repository: TaskRepository
    project_repository: ProjectRepository
    notification_service: NotificationPort
    task_presenter: TaskPresenter
    project_presenter: ProjectPresenter

    def __post_init__(self):
        """Wire up use cases and controllers."""
        # Configure task use cases
        self.create_task_use_case = CreateTaskUseCase(self.task_repository, self.project_repository)
        self.complete_task_use_case = CompleteTaskUseCase(
            self.task_repository, self.notification_service
        )
        self.get_task_use_case = GetTaskUseCase(self.task_repository)
        self.delete_task_use_case = DeleteTaskUseCase(self.task_repository)
        self.update_task_use_case = UpdateTaskUseCase(
            self.task_repository, self.notification_service
        )
        # Wire up task controller
        self.task_controller = TaskController(
            create_use_case=self.create_task_use_case,
            complete_use_case=self.complete_task_use_case,
            update_use_case=self.update_task_use_case,
            delete_use_case=self.delete_task_use_case,
            get_use_case=self.get_task_use_case,
            presenter=self.task_presenter,
        )
        # ... contruction of Project use cases and controller


# The Application class provides the structure for our component relationships, but
# we still need a way to create properly configured instances to inject into the
# Application container class. This is handled by our create_application factory method:


def create_application(
    notification_service: NotificationPort,
    task_presenter: TaskPresenter,
    project_presenter: ProjectPresenter,
) -> "Application":
    """Factory function for the Application container."""
    # Call the factory methods
    task_repository, project_repository = create_repositories()
    notification_service = create_notification_service()
    return Application(
        task_repository=task_repository,
        project_repository=project_repository,
        notification_service=notification_service,
        task_presenter=task_presenter,
        project_presenter=project_presenter,
    )


# Finally, our main.py script serves as the tip of our composition root - the single
# place where all components are instantiated and wired together at application startup:
def main() -> int:
    """Main entry point for the CLI application."""
    try:
        # Create application with dependencies
        app = create_application(
            notification_service=NotificationRecorder(),
            task_presenter=CliTaskPresenter(),
            project_presenter=CliProjectPresenter(),
        )

        # Create and run CLI implementation
        cli = ClickCli(app)
        return cli.run()

    except KeyboardInterrupt:
        print("\nGoodbye!")
        return 0
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
