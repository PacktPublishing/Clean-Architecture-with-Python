# Framework example - requires multiple adapter components
@app.route("/tasks", methods=["POST"])
def create_task():
    """Framework requires full Interface Adapters stack"""
    result = task_controller.handle_create(  # Controller from Ch.6
        title=request.json["title"], description=request.json["description"]
    )
    return task_presenter.present(result)  # Presenter from Ch.6


# Driver example - only needs interface and implementation
class SQLiteTaskRepository(TaskRepository):  # Interface from Ch.5
    """Driver needs only basic interface implementation"""

    def save(self, task: Task) -> None:
        self.connection.execute(
            "INSERT INTO tasks (id, title) VALUES (?, ?)", (str(task.id), task.title)
        )
