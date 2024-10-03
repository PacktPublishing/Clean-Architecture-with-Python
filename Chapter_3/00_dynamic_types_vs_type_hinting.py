x = 5  # x is an integer
x = "hello"  # Now x is a string

"""
This flexibility allows for rapid development and expressive code but can lead to runtime
errors if not managed carefully. Consider the following example:
"""


def add_numbers(a, b):
    return a + b


result = add_numbers(5, 3)  # Works fine, result is 8
result = add_numbers(
    5, "3"
)  # Raises TypeError: unsupported operand type(s) for +: 'int' and 'str'


"""
Type hints, introduced in Python 3.5, allow developers to annotate variables, function
parameters, and return values with their expected types. Regarding type hints, let's
revisit the add_numbers function from chapter 2:
"""


def add_numbers(a: int, b: int) -> int:
    return a + b


result = add_numbers(5, 3)  # Works fine, result is 8
result = add_numbers(5, "3")  # IDE or type checker would flag this as an error
