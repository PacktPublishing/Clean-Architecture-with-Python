# Chapter 11

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
export TODO_LOG_DIR="logs"            # log directory path
export TODO_LOG_FILE="app.log"        # log file path

# Optional: Email Notification Configuration
# Will default to (offline) NotificationRecorder if not set
export TODO_SENDGRID_API_KEY="your_api_key"
export TODO_NOTIFICATION_EMAIL="recipient@example.com"
```

### Running the Application
```bash
cd Chapter_10/TodoApp
pytest
python web_main.py
# OR
python cli_main.py
```