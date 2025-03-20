# Anti-pattern: Domain entity directly publishing events
class Task:
    def complete(self, user_id: UUID):
        self.status = TaskStatus.DONE
        self.completed_at = datetime.now()
        self.completed_by = user_id
        
        # Direct dependency on messaging system - violates Clean Architecture
        kafka_producer = KafkaProducer(bootstrap_servers='kafka:9092')
        event_data = {
            "task_id": str(self.id),
            "completed_by": str(user_id),
            "completed_at": self.completed_at.isoformat()
        }
        kafka_producer.send('task_events', json.dumps(event_data).encode())