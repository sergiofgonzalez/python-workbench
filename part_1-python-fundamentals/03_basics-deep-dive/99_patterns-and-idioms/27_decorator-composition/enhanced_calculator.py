"""An implementation of the Decorator design pattern using composition."""

from stack_calculator import StackCalculator


class EnhancedCalculator:
    """Aguments a StackCalculator with additional methods and behavior."""

    def __init__(self, calculator: StackCalculator) -> None:
        """Initialize an instance of an EnhancedCalculator."""
        self._calculator = calculator

    def add(self) -> float:
        """Perform the addition: added method."""
        addend2 = self._calculator.get_value()
        addend1 = self._calculator.get_value()
        result = addend1 + addend2
        self._calculator.put_value(result)
        return result

    def divide(self) -> float | str:
        """Perform the division: intercepted method."""
        divisor = self._calculator.peek_value()
        if divisor == 0:
            return "NaN (attempt to divide by zero)"
        return self._calculator.divide()

    def put_value(self, value: float) -> None:
        """Put a number into the internal stack: delegated method."""
        self._calculator.put_value(value)

    def get_value(self) -> float:
        """Pop a number from the internal stack: delegated method."""
        return self._calculator.get_value()

    def peek_value(self) -> float:
        """Peeks the number at the top of the stack without removing it: delegated."""
        return self._calculator.peek_value()

    def clear(self) -> None:
        """Remove all the numbers from the internal stack: delegated."""
        self._calculator.clear()

    def multiply(self) -> float:
        """Perform the multiplication: delegated method."""
        return self._calculator.multiply()

    def __str__(self) -> str:
        """User friendly representation: delegated method."""
        return str(self._calculator)
