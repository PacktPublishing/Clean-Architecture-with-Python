from datetime import datetime, timezone
from typing import Optional


def _format_due_date(self, due_date: Optional[datetime]) -> str:
    """Format due date for web display."""
    if not due_date:
        return ""

    is_overdue = due_date < datetime.now(timezone.utc)
    date_str = due_date.strftime("%Y-%m-%d")
    return f"Overdue: {date_str}" if is_overdue else date_str
