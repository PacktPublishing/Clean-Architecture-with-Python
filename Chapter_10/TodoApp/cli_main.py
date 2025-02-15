#!/usr/bin/env python
"""
Command Line Interface entry point for the Todo application.

This module serves as the composition root for the CLI interface,
demonstrating how Clean Architecture allows for different interfaces
to the same core application.
"""
import sys


from todo_app.infrastructure.cli.click_cli_app import ClickCli
from todo_app.infrastructure.configuration.container import create_application
from todo_app.infrastructure.notifications.recorder import NotificationRecorder
from todo_app.interfaces.presenters.cli import CliTaskPresenter, CliProjectPresenter

import logging
import os
from datetime import datetime

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging to log to a file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(f'logs/todo_app_{datetime.now().strftime("%Y%m%d")}.log')],
)


def main() -> int:
    """
    Main entry point for the CLI application.

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    try:
        # Create application with dependencies
        app = create_application(
            notification_service=NotificationRecorder(),
            task_presenter=CliTaskPresenter(),
            project_presenter=CliProjectPresenter(),
        )

        # Create and run appropriate CLI implementation
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
