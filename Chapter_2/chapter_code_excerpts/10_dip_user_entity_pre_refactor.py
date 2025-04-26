class UserEntity:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.database = MySQLDatabase()  # Direct dependency on a low-level module

    def save(self):
        self.database.insert("users", {"id": self.user_id})


class MySQLDatabase:
    def insert(self, table: str, data: dict):
        print(f"Inserting {data} into {table} table in MySQL")
