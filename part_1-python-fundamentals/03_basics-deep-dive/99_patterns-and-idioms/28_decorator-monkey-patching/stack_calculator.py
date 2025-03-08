"""A simple StackCalculator."""

from io import StringIO


class StackCalculator:
    """StackCalculator class."""

    def __init__(self) -> None:
        """Initialize a StackCalculator instance."""
        self.stack = []

    def put_value(self, value: float) -> None:
        """Put a number into the internal stack."""
        self.stack.append(value)

    def get_value(self) -> float:
        """Pop a number from the internal stack."""
        return self.stack.pop()

    def peek_value(self) -> float:
        """Peeks the number at the top of the stack without removing it."""
        return self.stack[-1]

    def clear(self) -> None:
        """Remove all the numbers from the internal stack."""
        self.stack.clear()

    def divide(self) -> float:
        """Perform a division."""
        divisor = self.get_value()
        dividend = self.get_value()
        result = dividend / divisor
        self.put_value(result)
        return result

    def multiply(self) -> float:
        """Perform a multiplication."""
        multiplier = self.get_value()
        multiplicand = self.get_value()
        result = multiplicand * multiplier
        self.put_value(result)
        return result

    def __str__(self) -> str:
        """Display the content of the stack in a user-friendly way."""
        result = StringIO()
        result.write("=" * 80)
        result.write("\n")
        for i, value in enumerate(self.stack):
            result.write(f"{len(self.stack) - 1 - i}: {value}\n")
        result.write("=" * 80)
        result.write("\n")
        return result.getvalue()
