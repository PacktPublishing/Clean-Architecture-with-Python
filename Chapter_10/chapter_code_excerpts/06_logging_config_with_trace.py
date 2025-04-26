# todo_app/infrastructure/logging/config.py
def configure_logging(app_context: Literal["CLI", "WEB"]) -> None:
    config = {
        "formatters": {
            "json": {"()": JsonFormatter, "app_context": app_context},
            "standard": {
                "format": "%(asctime)s [%(trace_id)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        # ... rest of configuration
    }
