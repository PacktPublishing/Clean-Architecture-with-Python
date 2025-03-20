# Pure Clean Architecture approach with FastAPI
@app.post("/tasks/")
def create_task(
    task_data: CreateTaskRequest,
):  # Using Pydantic here is fine - we're in the Frameworks layer
    # Transform the Pydantic model to our internal domain model
    # to avoid letting Pydantic penetrate inner layers
    request = InternalCreateTaskRequest(
        title=task_data.title.strip(), description=task_data.description.strip()
    )

    # Pass our internal model to the controller
    result = task_controller.handle_create(request)
    return result.success
