"""Proxy over StackCalculator using monkey-patching."""

from stack_calculator import StackCalculator


def patch_to_safe_calculator(calculator: StackCalculator) -> StackCalculator:
    """Return an instance of StackCalculator in which the divide method has been patched."""
    divide_original = calculator.divide
    def patched_divide(self: StackCalculator) -> float | str:
        """Proxied implementation of the StackCalculator.divide method."""
        divisor = self.peek_value()
        if divisor == 0:
            return "NaN (divide by zero)"
        return divide_original()

    calculator.divide = patched_divide.__get__(calculator, StackCalculator)

    return calculator
