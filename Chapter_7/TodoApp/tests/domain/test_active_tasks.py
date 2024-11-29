from uuid import uuid4
from todo_app.infrastructure.persistence.memory import InMemoryTaskRepository
from todo_app.domain.entities.task import Task
from todo_app.domain.value_objects import TaskStatus


def test_get_active_tasks_empty_repository():
    """Test getting active tasks from an empty repository."""
    repo = InMemoryTaskRepository()
    tasks = repo.get_active_tasks()
    assert len(tasks) == 0


def test_get_active_tasks_only_active():
    """Test getting active tasks when all tasks are active."""
    repo = InMemoryTaskRepository()

    # Create and save three active tasks
    task1 = Task(title="Task 1", description="Test", project_id=uuid4())
    task2 = Task(title="Task 2", description="Test", project_id=uuid4())
    task3 = Task(title="Task 3", description="Test", project_id=uuid4())

    repo.save(task1)
    repo.save(task2)
    repo.save(task3)

    tasks = repo.get_active_tasks()
    assert len(tasks) == 3
    assert all(task.status == TaskStatus.TODO for task in tasks)


def test_get_active_tasks_mixed_status():
    """Test getting active tasks with a mix of active and completed tasks."""
    repo = InMemoryTaskRepository()

    # Create and save tasks with different statuses
    todo_task = Task(title="Todo Task", description="Test", project_id=uuid4())
    in_progress_task = Task(title="In Progress Task", description="Test", project_id=uuid4())
    in_progress_task.start()  # Sets status to IN_PROGRESS
    completed_task = Task(title="Completed Task", description="Test", project_id=uuid4())
    completed_task.complete()  # Sets status to DONE

    repo.save(todo_task)
    repo.save(in_progress_task)
    repo.save(completed_task)

    tasks = repo.get_active_tasks()
    assert len(tasks) == 2  # Should only get TODO and IN_PROGRESS tasks
    assert completed_task not in tasks
    assert all(task.status != TaskStatus.DONE for task in tasks)


def test_get_active_tasks_only_completed():
    """Test getting active tasks when all tasks are completed."""
    repo = InMemoryTaskRepository()

    # Create and save three completed tasks
    task1 = Task(title="Task 1", description="Test", project_id=uuid4())
    task2 = Task(title="Task 2", description="Test", project_id=uuid4())
    task3 = Task(title="Task 3", description="Test", project_id=uuid4())

    for task in [task1, task2, task3]:
        task.complete()
        repo.save(task)

    tasks = repo.get_active_tasks()
    assert len(tasks) == 0


def test_get_active_tasks_after_completion():
    """Test getting active tasks after completing some tasks."""
    repo = InMemoryTaskRepository()

    # Create and save initial tasks
    task1 = Task(title="Task 1", description="Test", project_id=uuid4())
    task2 = Task(title="Task 2", description="Test", project_id=uuid4())
    task3 = Task(title="Task 3", description="Test", project_id=uuid4())

    repo.save(task1)
    repo.save(task2)
    repo.save(task3)

    # Initially should have all tasks
    assert len(repo.get_active_tasks()) == 3

    # Complete two tasks
    task1.complete()
    task3.complete()
    repo.save(task1)
    repo.save(task3)

    # Should now only have one active task
    active_tasks = repo.get_active_tasks()
    assert len(active_tasks) == 1
    assert task2 in active_tasks
