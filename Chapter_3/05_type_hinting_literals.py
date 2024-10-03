from typing import Literal

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR"]


def set_log_level(level: LogLevel) -> None:
    print(f"Setting log level to {level}")


# Usage
set_log_level("DEBUG")  # Valid
set_log_level("CRITICAL")  # Type checker would flag this as an error
