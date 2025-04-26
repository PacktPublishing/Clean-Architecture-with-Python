class Task(Entity):
    """Anti-pattern: Domain entity with direct infrastructure dependencies."""

    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description
        self.db = Database()  # Direct database dependency
        self.notifier = NotificationService()  # Direct notification dependency
        self.priority = Priority.MEDIUM
        # Save to database and notify on creation
        self.id = self.db.save_task(self.as_dict())
        self.notifier(f"Task {self.id} created")


def test_new_task_priority_antipattern():
    """An anti-pattern mixing infrastructure concerns with simple domain logic."""
    # Complex setup just to test a default value
    db_connection = create_database_connection()
    notification_service = create_notification_service()
    # Just creating a task hits the database and notificaion service
    task = Task(title="Test task", description="Test description")
    # Even checking a simple property requires a database query
    saved_task = task.db.get_task(task.id)
    assert saved_task["priority"] == Priority.MEDIUM
