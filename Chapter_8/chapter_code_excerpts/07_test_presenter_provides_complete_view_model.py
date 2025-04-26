from uuid import UUID


def test_presenter_provides_complete_view_model(): 
    """Test presenter creates properly formatted view model with all display fields.""" 
    # Arrange 
    task = Task( 
        title="Important Task", 
        description="Testing view model creation", 
        project_id=UUID('12345678-1234-5678-1234-567812345678'), 
        priority=Priority.HIGH 
    ) 
    task.complete()  # Set status to DONE 
    task_response = TaskResponse.from_entity(task) 
    presenter = CliTaskPresenter() 
     
    # Act 
    view_model = presenter.present_task(task_response) 
     
    # Assert 
    assert view_model.title == "Important Task" 
    assert view_model.status_display == "[DONE]" 
    assert view_model.priority_display == "High" 
    assert isinstance(view_model.completion_info, str) 