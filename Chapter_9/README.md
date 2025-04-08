# Chapter 9 : Adding Web UI: Clean Architecture's Interface Flexibility

The code exampes from the chapter can be found in the order of appearance in the files with numeric indexes (ex:
`00_error_class.py`)

## Companion task management application

## Running the Task Management Web Application

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
cd Chapter_9/TodoApp
pytest
python web_main.py
```