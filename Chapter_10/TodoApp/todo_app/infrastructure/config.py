"""
Configuration setup for the Todo application.
"""

from enum import Enum
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Repository types
class RepositoryType(Enum):
    MEMORY = "memory"
    FILE = "file"


class Config:
    """Application configuration."""

    # Default values
    DEFAULT_REPOSITORY_TYPE: RepositoryType = RepositoryType.MEMORY
    DEFAULT_DATA_DIR = "repo_data"
    DEFAULT_LOG_DIR = "logs"  # Relative to where app is run
    DEFAULT_LOG_FILE = "todo_app.log"

    @classmethod
    def get_repository_type(cls) -> RepositoryType:
        """Get the configured repository type."""
        repo_type_str = os.getenv("TODO_REPOSITORY_TYPE", cls.DEFAULT_REPOSITORY_TYPE.value)
        try:
            return RepositoryType(repo_type_str.lower())
        except ValueError:
            raise ValueError(f"Invalid repository type: {repo_type_str}")

    @classmethod
    def get_data_directory(cls) -> Path:
        """Get the data directory path."""
        data_dir = os.getenv("TODO_DATA_DIR", cls.DEFAULT_DATA_DIR)
        path = Path(data_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path

    @classmethod
    def get_sendgrid_api_key(cls) -> str:
        """Get the SendGrid API key."""
        return os.getenv("TODO_SENDGRID_API_KEY", "")

    @classmethod
    def get_notification_email(cls) -> str:
        """Get the notification recipient email."""
        return os.getenv("TODO_NOTIFICATION_EMAIL", "")

    @classmethod
    def get_log_file_path(cls) -> Path:
        """Get the log file path.

        Returns:
            Path to log file, creating parent directories if needed.
        """
        log_dir = Path(os.getenv("TODO_LOG_DIR", cls.DEFAULT_LOG_DIR))
        log_file = os.getenv("TODO_LOG_FILE", cls.DEFAULT_LOG_FILE)

        # Ensure log directory exists
        log_dir.mkdir(parents=True, exist_ok=True)

        return log_dir / log_file
