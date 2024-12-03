#!/usr/bin/env python
"""
Command Line Interface entry point for the Todo application.

This module serves as the composition root for the CLI interface,
demonstrating how Clean Architecture allows for different interfaces
to the same core application.
"""
import os
import sys


from todo_app.infrastructure.cli.click_cli_app import ClickCli
from todo_app.infrastructure.configuration.container import create_application
from todo_app.infrastructure.notifications.recorder import NotificationRecorder
from todo_app.interfaces.presenters.cli import CliTaskPresenter, CliProjectPresenter


def get_cli_implementation(cli_type: str) -> type:
    """
    Factory function to get the appropriate CLI implementation.

    Args:
        cli_type: The type of CLI to use ('simple' or 'click')

    Returns:
        The CLI class to instantiate
    """
    cli_implementations = {
        # 'simple': SimpleCli,
        "click": ClickCli
    }
    return cli_implementations.get(cli_type, ClickCli)


def main() -> int:
    """
    Main entry point for the CLI application.

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    try:
        # Get CLI type from environment variable, defaulting to 'click'
        cli_type = os.getenv("TODO_CLI_TYPE", "click")

        # Create application with dependencies
        app = create_application(
            notification_service=NotificationRecorder(),
            task_presenter=CliTaskPresenter(),
            project_presenter=CliProjectPresenter(),
        )

        # Create and run appropriate CLI implementation
        cli_class = get_cli_implementation(cli_type)
        cli = cli_class(app)
        return cli.run()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        return 0
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
