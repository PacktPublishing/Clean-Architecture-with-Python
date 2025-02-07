# Anti-pattern: Interface-specific logic in controller
def handle_create(self, request_data: dict) -> dict:
    """DON'T: Mixing CLI formatting in controller."""
    try:
        result = self.create_use_case.execute(request_data)
        if result.is_success:
            # Wrong: CLI-specific formatting doesn't belong here
            return {"message": click.style(f"Created task: {result.value.title}", fg="green")}
    except ValueError as e:
        # Wrong: CLI-specific error formatting
        return {"error": click.style(str(e), fg="red")}
