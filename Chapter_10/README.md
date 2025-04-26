# Chapter 10

## Chapter code excerpts
The code snippets from the chapter can be found in the order of appearance in the `chapter_code_excerpts` folder. Examples: `00_error_class.py`  
These are provided for reference and are not meant to be runnable.

## Running the Task Management Web Application

Ensure you have followed the instructions in the repository's [README](../README.md) section to set up your environment.

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
cd Chapter_10/TodoApp
pytest
```
#### running the CLI
```bash
python cli_main.py
```
#### running the Web
```bash
python web_main.py

# navigate to http://127.0.0.1:5000
```