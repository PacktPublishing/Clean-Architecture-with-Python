from typing import Sequence


def calculate_total(items: Sequence[float]) -> float:
    return sum(items)


# Usage
print(calculate_total([1.0, 2.0, 3.0]))  # Works with list
print(calculate_total((4.0, 5.0, 6.0)))  # Also works with tuple
