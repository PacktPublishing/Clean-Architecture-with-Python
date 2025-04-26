# Example transformation flow in TaskController


def handle_create(self, title: str, description: str) -> OperationResult[TaskViewModel]:

    try:

        # 1. External input to request model

        request = CreateTaskRequest(title=title, description=description)

        # 2. Request model to domain operations

        result = self.use_case.execute(request)

        if result.is_success:

            # 3. Domain result to view model

            view_model = self.presenter.present_task(result.value)

            return OperationResult.succeed(view_model)

        # 4. Error handling and formatting

        error_vm = self.presenter.present_error(result.error.message, str(result.error.code.name))

        return OperationResult.fail(error_vm.message, error_vm.code)

    except ValueError as e:

        # 5. Validation error handling

        error_vm = self.presenter.present_error(str(e), "VALIDATION_ERROR")

        return OperationResult.fail(error_vm.message, error_vm.code)
