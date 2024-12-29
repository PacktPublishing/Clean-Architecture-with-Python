# pseudo-code example of a CLI app working with a OperationResult 

result = app.task_controller.handle_create(title, description)   

if result.is_success: 

    task = result.success 

    print(f"{task.status_display} [{task.priority_display}] {task.title}") 

    return 0  

print(result.error.message, fg='red', err=True) 

    return 1