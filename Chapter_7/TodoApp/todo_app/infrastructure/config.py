"""
Configuration setup for the Todo application.
"""

import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Repository types
RepositoryType = Literal["memory", "file"]


class Config:
    """Application configuration."""

    # Default values
    DEFAULT_REPOSITORY_TYPE: RepositoryType = "memory"
    DEFAULT_DATA_DIR = "repo_data"

    @classmethod
    def get_repository_type(cls) -> RepositoryType:
        """Get the configured repository type."""
        repo_type = os.getenv("TODO_REPOSITORY_TYPE", cls.DEFAULT_REPOSITORY_TYPE)
        return cls.DEFAULT_REPOSITORY_TYPE if repo_type not in ("memory", "file") else repo_type

    @classmethod
    def get_data_directory(cls) -> Path:
        """Get the data directory path."""
        data_dir = os.getenv("TODO_DATA_DIR", cls.DEFAULT_DATA_DIR)
        path = Path(data_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path
