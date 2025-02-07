# cli_main.py
def main() -> int:
    """Main entry point for the CLI application."""
    app = create_application(
        notification_service=NotificationRecorder(),
        task_presenter=CliTaskPresenter(),
        project_presenter=CliProjectPresenter(),
    )
    cli = ClickCli(app)
    return cli.run()
