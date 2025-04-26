from dataclasses import dataclass


@dataclass
class TaskController:
    create_use_case: CreateTaskUseCase
    # ... additional use cases as needed
    presenter: TaskPresenter

    def handle_create(self, title: str, description: str) -> OperationResult[TaskViewModel]:
        try:
            request = CreateTaskRequest(title=title, description=description)
            result = self.create_use_case.execute(request)

            if result.is_success:
                view_model = self.presenter.present_task(result.value)
                return OperationResult.succeed(view_model)

            error_vm = self.presenter.present_error(
                result.error.message, str(result.error.code.name)
            )
            return OperationResult.fail(error_vm.message, error_vm.code)

        except ValueError as e:
            error_vm = self.presenter.present_error(str(e), "VALIDATION_ERROR")
            return OperationResult.fail(error_vm.message, error_vm.code)
