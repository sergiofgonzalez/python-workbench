"""Proxy for StackCalculator using composition."""

from stack_calculator import StackCalculator


class SafeCalculator:
    """A proxy over StackCalculator."""

    def __init__(self, calculator: StackCalculator) -> None:
        """Initialize an instance of StackCalculator."""
        self.calculator = calculator

    def divide(self) -> float | str:
        """Proxied method that handles StackCalculator.divide differently."""
        divisor = self.calculator.peek_value()
        if divisor == 0:
            return "NaN (divide by zero)"
        return self.calculator.divide()

    def put_value(self, value: float) -> None:
        """Put a value using the delegated method: put_value."""
        self.calculator.put_value(value)

    def get_value(self) -> float:
        """Get a value using the delegated method: get_value."""
        return self.calculator.get_value()

    def peek_value(self) -> float:
        """Peek the value on top of the stack using the delegated method: peek_value."""
        return self.calculator.peek_value()

    def clear(self) -> None:
        """Clear the calculator using the delegated method: clear."""
        self.calculator.clear()

    def multiply(self) -> float:
        """Perform the multiplication using the delegated method: multiply."""
        return self.calculator.multiply()

    def __str__(self) -> str:
        """User-friendly representation using the delegated method."""
        return str(self.calculator)


def create_safe_calculator(stack_calculator: StackCalculator) -> SafeCalculator:
    """Return an instance of SafeCalculator using the Factory pattern."""
    return SafeCalculator(stack_calculator)
