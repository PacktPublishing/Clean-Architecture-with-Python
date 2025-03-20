# Clean domain entity - no messaging dependencies
class Task:
    def complete(self, user_id: UUID) -> None:
        if self.status == TaskStatus.DONE:
            raise ValueError("Task is already completed")
        self.status = TaskStatus.DONE
        self.completed_at = datetime.now()
        self.completed_by = user_id


# Application layer handles event creation
@dataclass
class CompleteTaskUseCase:
    task_repository: TaskRepository
    event_publisher: EventPublisher  # Abstract interface, not implementation

    def execute(self, task_id: UUID, user_id: UUID) -> Result:
        try:
            task = self.task_repository.get_by_id(task_id)
            task.complete(user_id)
            self.task_repository.save(task)

            # Create domain event and publish through abstract interface
            event = TaskCompletedEvent.from_task(task, user_id)
            self.event_publisher.publish(event)

            return Result.success(task)
        except ValueError as e:
            return Result.failure(Error(str(e)))
