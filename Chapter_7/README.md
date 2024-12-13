# Chapter 7

This chapter completes the Clean Architecture implementation of the task management application by adding the Frameworks and Drivers layer. The code demonstrates how to integrate external frameworks, databases, and services while maintaining clean architectural boundaries.

## Running the Task Management Application

### Prerequisites
- Python 3.13 or higher
- Optional: SendGrid account and API key (for email notifications)

### Installation
1. Clone the repository
2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
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
cd Chapter_7/TodoApp
python main.py
```

## Project Structure
The complete application structure including the Frameworks and Drivers layer:

```text
└── todo_app
    ├── application          # (From Chapter 5)
    │    ├── common
    │    ├── dtos
    │    ├── ports
    │    ├── repositories
    │    └── use_cases
    │
    ├── domain              # (From Chapter 4)
    │    ├── entities
    │    ├── exceptions.py
    │    ├── services
    │    └── value_objects.py
    │
    ├── interfaces          # (From Chapter 6)
    │    ├── controllers
    │    ├── presenters
    │    └── view_models
    │
    └── infrastructure      # (New in Chapter 7)
         ├── cli
         │    └── click_cli_app.py
         ├── configuration
         │    └── container.py
         ├── notifications
         │    ├── recorder.py
         │    └── sendgrid.py
         ├── persistence
         │    ├── memory.py
         │    └── file.py
         ├── config.py
         └── repository_factory.py
```

## Key Features
- Command-line interface using Click framework
- Choice of in-memory or file-based storage
- Task and project management
- Optional email notifications for task completion

## Using the Application
The application provides an interactive CLI for managing tasks and projects:

1. View and select projects using numbers (e.g., "1")
2. View and select tasks using project.task format (e.g., "1.a")
3. Create new projects using "np" command
4. Create tasks within projects or in the default INBOX
5. Complete, update, and delete tasks
6. Edit project details and manage project completion

## Implementation Notes
- The infrastructure layer demonstrates Clean Architecture's approach to external dependencies
- Framework adapters (CLI) maintain separation from business logic
- Repository implementations show flexible storage options
- Optional notification services demonstrate clean integration of external services