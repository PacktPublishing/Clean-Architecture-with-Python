#!/usr/bin/env python
"""
Command Line Interface entry point for the Todo application.

This module serves as the composition root for the CLI interface,
demonstrating how Clean Architecture allows for different interfaces
to the same core application.
"""

import sys
import os
from typing import Type

from todo_app.infrastructure.cli.simple_cli_app import SimpleCli
from todo_app.infrastructure.cli.click_cli_app import ClickCli
from todo_app.infrastructure.config.container import Application
from todo_app.infrastructure.persistence.memory import (
    InMemoryTaskRepository,
    InMemoryProjectRepository,
)
from todo_app.infrastructure.notifications.recorder import NotificationRecorder
from todo_app.interfaces.presenters.cli import CliTaskPresenter, CliProjectPresenter


def create_application() -> Application:
    """
    Create and configure the application container with all required dependencies.
    This acts as our composition root where concrete implementations are selected.
    """
    return Application(
        task_repository=InMemoryTaskRepository(),
        project_repository=InMemoryProjectRepository(),
        notification_service=NotificationRecorder(),
        task_presenter=CliTaskPresenter(),
        project_presenter=CliProjectPresenter()
    )


def get_cli_implementation(cli_type: str) -> Type:
    """
    Factory function to get the appropriate CLI implementation.
    This allows us to switch between different CLI frameworks while
    maintaining the same core application logic.
    """
    cli_implementations = {
        'simple': SimpleCli,
        'click': ClickCli
    }
    return cli_implementations.get(cli_type, SimpleCli)


def main(cli_type: str) -> int:
    """
    Main entry point for the CLI application.
    
    Args:
        cli_type: Optional CLI implementation to use ('simple' or 'click')
                 If not specified, defaults to 'simple'
    
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    try:
        app = create_application()
        cli_class = get_cli_implementation(cli_type)
        cli = cli_class(app)
        
        # Handle different CLI types
        if cli_type == 'simple':
            # Get command and args from sys.argv, skipping script name
            args = sys.argv[1:]
            if not args:
                print("Error: Command required for simple CLI", file=sys.stderr)
                return 1
            command = args[0]
            # Convert remaining args to kwargs (assuming format: --key value)
            kwargs = dict(zip(args[1::2], args[2::2]))
            return cli.run(command, **kwargs)
        else:
            # Click CLI handles its own argument parsing
            return cli.run()
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    # Get CLI type from environment variable, defaulting to 'simple'
    cli_type = os.environ.get('TODO_CLI_TYPE', 'simple')
    sys.exit(main(cli_type))