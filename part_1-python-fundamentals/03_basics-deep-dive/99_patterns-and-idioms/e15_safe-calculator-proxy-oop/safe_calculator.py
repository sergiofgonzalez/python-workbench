"""Proxy for StackCalculator using composition."""

from typing import override

from calculator import Calculator
from stack_calculator import StackCalculator


class SafeCalculator(Calculator):
    """A proxy over StackCalculator."""

    def __init__(self, calculator: StackCalculator) -> None:
        """Initialize an instance of StackCalculator."""
        self.calculator = calculator

    @override
    def divide(self) -> float | str:
        """Proxied method that handles StackCalculator.divide differently."""
        divisor = self.calculator.peek_value()
        if divisor == 0:
            return "NaN (divide by zero)"
        return self.calculator.divide()

    @override
    def put_value(self, value: float) -> None:
        """Put a value using the delegated method: put_value."""
        self.calculator.put_value(value)

    @override
    def get_value(self) -> float:
        """Get a value using the delegated method: get_value."""
        return self.calculator.get_value()

    @override
    def peek_value(self) -> float:
        """Peek the value on top of the stack using the delegated method: peek_value."""
        return self.calculator.peek_value()

    @override
    def clear(self) -> None:
        """Clear the calculator using the delegated method: clear."""
        self.calculator.clear()

    @override
    def multiply(self) -> float:
        """Perform the multiplication using the delegated method: multiply."""
        return self.calculator.multiply()

    def __str__(self) -> str:
        """User-friendly representation using the delegated method."""
        return str(self.calculator)


def create_safe_calculator(stack_calculator: StackCalculator) -> SafeCalculator:
    """Return an instance of SafeCalculator using the Factory pattern."""
    return SafeCalculator(stack_calculator)
