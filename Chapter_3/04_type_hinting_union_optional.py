from typing import Union, Optional


def process_input(data: Union[str, int]) -> str:
    return str(data)


def find_user(user_id: Optional[int] = None) -> Optional[str]:
    if user_id is None:
        return None
    # ... logic to find user ...
    return "User found"


# Usage
result1 = process_input("Hello")  # Works with str
result2 = process_input(42)  # Works with int
user = find_user()  # Optional parameter
