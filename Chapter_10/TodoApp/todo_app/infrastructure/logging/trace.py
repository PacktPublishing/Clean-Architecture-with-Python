from uuid import uuid4
from contextvars import ContextVar
from typing import Optional

# Thread-safe context variable to hold trace ID
# Initialize with None default instead of empty string
trace_id_var: ContextVar[Optional[str]] = ContextVar("trace_id", default=None)


def get_trace_id() -> str:
    """Get current trace ID or generate new one if not set."""
    current = trace_id_var.get()
    if current is None:
        current = str(uuid4())
        trace_id_var.set(current)
    return current


def set_trace_id(trace_id: Optional[str] = None) -> str:
    """Set trace ID for current context."""
    new_id = trace_id or str(uuid4())
    trace_id_var.set(new_id)
    return new_id
