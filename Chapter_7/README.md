# Chapter 7

The code exampes from the chapter can be found in the order of appearance in the files with numeric indexes (ex:
`00_error_class.py`)

## Companion task management application

This chapter completes the Clean Architecture implementation of the task management application by adding the Frameworks and Drivers layer. The code demonstrates how to integrate external frameworks, databases, and services while maintaining clean architectural boundaries.

## Running the Task Management Application

Ensure you have followed the instructions in the [Getting started](../README.md#2-getting-started) section to set up your environment.

### Configuration
The application supports configuration through environment variables:

```bash
# Repository Configuration options
export TODO_REPOSITORY_TYPE="memory"  # or "file"
export TODO_DATA_DIR="repo_data"      # used if `file` is selected for TODO_REPOSITORY_TYPE

# Optional: Email Notification Configuration
# Will default to (offline) NotificationRecorder if not set
# To set up sendgrid notifications, you will need set up a [SendGrid account](https://sendgrid.com/en-us/solutions/email-api) (There is a free tier available)
export TODO_SENDGRID_API_KEY="your_api_key"
export TODO_NOTIFICATION_EMAIL="recipient@example.com"
```

### Running the Application
```bash
cd Chapter_7/TodoApp
python main.py
```

This launches the CLI interface.


## Using the Application
The application provides an interactive CLI for managing tasks and projects:

1. View and select projects using numbers (e.g., "1")
2. View and select tasks using project.task format (e.g., "1.a")
3. Create new projects using "np" command
4. Create tasks within projects or in the default INBOX
5. Complete, update, and delete tasks
6. Edit project details and manage project completion
