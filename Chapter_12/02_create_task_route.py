# How validation works with FastAPI/Pydantic
@app.post("/tasks/")
def create_task(task_data: CreateTaskRequest):
    # FastAPI has already validated all fields
    # Invalid requests are rejected with 422 Unprocessable Entity

    result = task_controller.handle_create(title=task_data.title, description=task_data.description)
    return result.success


# If a client sends invalid data, such as an empty title:

"""
{
  "title": "",
  "description": "Test description"
}
"""

# FastAPI automatically responds with a validation error:

"""
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length",
      "ctx": {"limit_value": 1}
    }
  ]
}
"""
