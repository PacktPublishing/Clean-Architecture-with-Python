# Chapter 9 : Adding Web UI: Clean Architecture's Interface Flexibility

## Chapter code excerpts
The code snippets from the chapter can be found in the order of appearance in the `chapter_code_excerpts` folder. Examples: `00_error_class.py`  
These are provided for reference and are not meant to be runnable.

## Companion task management application

Ensure you have followed the instructions in the repository's [README](../README.md) section to set up your environment.

Execute all tests using pytest:
```bash
cd Chapter_9/TodoApp
pytest
```

### Configuration
The application supports configuration through environment variables:

```bash
# Repository Configuration
export TODO_REPOSITORY_TYPE="memory"  # or "file"
export TODO_DATA_DIR="repo_data"      # used with file repository

# Optional: Email Notification Configuration
# Will default to (offline) NotificationRecorder if not set
export TODO_SENDGRID_API_KEY="your_api_key"
export TODO_NOTIFICATION_EMAIL="recipient@example.com"
```

### Running the Application
```bash
cd Chapter_9/TodoApp
pytest

python web_main.py
```