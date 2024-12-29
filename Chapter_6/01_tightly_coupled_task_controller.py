class TightlyCoupledTaskController:

    def __init__(self):

        # Direct instantiation creates tight coupling

        self.use_case = TaskUseCase(SqliteTaskRepository())

        self.presenter = CliTaskPresenter()

    def handle_create(self, title: str, description: str):

        # Implementation details...

        pass
