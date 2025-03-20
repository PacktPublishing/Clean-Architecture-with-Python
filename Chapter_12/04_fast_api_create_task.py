# Framework layer (infrastructure/api/routes.py)
@app.post("/tasks/", response_model=TaskResponse, status_code=201)
def create_task(task_data: CreateTaskRequest):
    """Create a new task."""
    # The controller handles translation between API and domain
    result = task_controller.handle_create(
        title=task_data.title,
        description=task_data.description,
        project_id=task_data.project_id
    )
    
    if not result.is_success:
        # Error handling at the framework boundary
        raise HTTPException(status_code=400, detail=result.error.message)
        
    return result.success  # Automatic serialization to TaskResponse