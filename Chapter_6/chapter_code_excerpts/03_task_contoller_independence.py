from dataclasses import dataclass


@dataclass
class TaskController:
    # Application layer interface
    create_use_case: CreateTaskUseCase
    # Interface layer abstraction
    presenter: TaskPresenter
