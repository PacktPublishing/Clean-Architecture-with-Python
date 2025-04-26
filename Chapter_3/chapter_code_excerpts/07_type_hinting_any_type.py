from typing import Any


def log_data(data: Any) -> None:
    print(f"Logged: {data}")


# Usage
log_data("A string")
log_data(42)
log_data({"key": "value"})
