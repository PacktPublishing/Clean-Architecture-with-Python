# Anti-pattern: Domain entity accessing web state
from datetime import datetime


class Task:
    def complete(self, web_app_contatiner):
        # Wrong: Task shouldn't know about web sessions
        self.completed_by = web_app_contatiner.user.id
        self.completed_at = datetime.now()
