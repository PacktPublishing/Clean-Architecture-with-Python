# todo_app/infrastructure/web/web_app.py
"""
FastAPI web interface implementation demonstrating Clean Architecture adaptability.

This module shows how Clean Architecture enables multiple interfaces to the same
core business logic. It demonstrates:
1. How business logic remains unchanged across interfaces
2. How Clean Architecture supports different external protocols
3. How the Frameworks & Drivers layer adapts between protocols and core logic

While the CLI interface uses command-line arguments, this module shows how the
same business logic can be exposed through HTTP endpoints, demonstrating the
flexibility Clean Architecture provides.
"""

from todo_app.application.dtos.task_dtos import CreateTaskRequest
from fastapi import FastAPI, HTTPException
from todo_app.infrastructure.config.container import Application, create_application

app = FastAPI(
    title="Todo API",
    description="REST API for todo management demonstrating Clean Architecture",
)
application = create_application()

@app.post("/tasks")
async def create_task(task: CreateTaskRequest):
    """
    Create a new task through the REST interface.
    
    This endpoint demonstrates Clean Architecture's interface flexibility:
    1. HTTP request is converted to internal format
    2. Same business logic is used as CLI interface
    3. Results are converted to HTTP responses
    
    Args:
        task: Task creation request data
        
    Returns:
        Created task details
        
    Raises:
        HTTPException: If task creation fails
    """
    result = application.task_controller.handle_create(
        title=task.title,
        description=task.description
    )
    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)
    return result.value