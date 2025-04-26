# The "humble" view - simple, minimal logic, hard to test


def display_task(task_vm: TaskViewModel):

    print(f"{task_vm.status_display} [{task_vm.priority_display}] {task_vm.title}")

    if task_vm.due_date_display:

        print(f"Due: {task_vm.due_date_display}")
