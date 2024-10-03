def get_user(user_id: int) -> dict:
    # Simulating user retrieval
    return {"id": user_id, "name": "John Doe", "email": "john@example.com"}


def send_email(user: dict, subject: str) -> None:
    print(f"Sending email to {user['email']} with subject: {subject}")


# Usage
user = get_user("123")
send_email(user, "Welcome!")

"""
mypy Chapter_3/08_type_hinting_mypy_cli.py
Chapter_3/08_type_hinting_mypy_cli.py:11: error: Argument 1 to "get_user" has incompatible type "str"; expected "int"  [arg-type]
Found 1 error in 1 file (checked 1 source file)
"""
