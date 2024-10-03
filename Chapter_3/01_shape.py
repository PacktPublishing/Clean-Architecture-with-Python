import math
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass


class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


class Circle(Shape):
    def __init__(self, radius: float) -> None:

        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius**2


class AreaCalculator:
    def calculate_area(self, shape: Shape) -> float:

        return shape.area()
