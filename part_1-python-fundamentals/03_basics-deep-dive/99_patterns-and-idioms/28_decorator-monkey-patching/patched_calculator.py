"""An implementation of the Decorator design pattern using monkey patching."""

from abc import ABC, abstractmethod

from stack_calculator import StackCalculator


class PatchedCalculator(ABC, StackCalculator):
    """Interface of the decorated object."""

    @abstractmethod
    def add() -> float:
        """Perform the addition."""

    @abstractmethod
    def divide() -> float | str:
        """Perform the division."""


def patched_calculator(calculator: StackCalculator) -> PatchedCalculator:
    """Return a decorator of the StackCalculator."""
    divide_original = calculator.divide

    def patched_divide(self: StackCalculator) -> float | str:
        """Perform division using a patched method."""
        divisor = self.peek_value()
        if divisor == 0:
            return "NaN (attempt to divide by zero)"
        return divide_original()

    calculator.divide = patched_divide.__get__(calculator, StackCalculator)

    def add(self: StackCalculator) -> float:
        """Perform addition."""
        addend2 = self.get_value()
        addend1 = self.get_value()
        result = addend1 + addend2
        self.put_value(result)
        return result

    calculator.add = add.__get__(calculator, StackCalculator)

    return calculator
