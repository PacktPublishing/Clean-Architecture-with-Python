"""
This is a judgement call as to placing all these objects in one
file or in their own files.  It's really the developer's preference
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


class TaskStatus(Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class ProjectStatus(Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


# frozen=True makes this immutable as it should be for a Value Object
@dataclass(frozen=True)
class Deadline:
    due_date: datetime

    def __post_init__(self):
        if self.due_date < datetime.now():
            raise ValueError("Deadline cannot be in the past")

    def is_overdue(self) -> bool:
        return datetime.now() > self.due_date

    def time_remaining(self) -> timedelta:
        return max(timedelta(0), self.due_date - datetime.now())

    def is_approaching(
        self, warning_threshold: timedelta = timedelta(days=1)
    ) -> bool:
        return timedelta(0) < self.time_remaining() <= warning_threshold
