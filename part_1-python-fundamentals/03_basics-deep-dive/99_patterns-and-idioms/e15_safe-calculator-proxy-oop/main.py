"""Main application illustating how to use StackCalculator and the Proxy."""

from safe_calculator import SafeCalculator
from stack_calculator import StackCalculator


def test_subject() -> None:
    """Illustrate how to work with the subject StackCalculator."""
    stack_calc = StackCalculator()
    stack_calc.put_value(5)
    print(stack_calc)
    stack_calc.put_value(6)
    print(stack_calc)
    stack_calc.put_value(3)
    print(stack_calc)
    print(f">>> Top of the stack: {stack_calc.peek_value()}")
    print(stack_calc)
    print(f">>> Division: {stack_calc.divide()}")
    print(stack_calc)
    print(f">>> Multiplication: {stack_calc.multiply()}")
    print(stack_calc)


def test_proxy() -> None:
    """Illustrate how to work with the Proxy."""
    stack_calc = StackCalculator()
    safe_calc = SafeCalculator(stack_calc)
    safe_calc.put_value(5)
    print(safe_calc)
    safe_calc.put_value(6)
    print(safe_calc)
    safe_calc.put_value(3)
    print(safe_calc)
    print(f">>> Top of the stack: {safe_calc.peek_value()}")
    print(safe_calc)
    print(f">>> Division: {safe_calc.divide()}")
    print(safe_calc)
    print(f">>> Multiplication: {safe_calc.multiply()}")
    print(safe_calc)
    safe_calc.put_value(0)
    print(safe_calc)
    print(f">>> Division: {safe_calc.divide()}")
    print(safe_calc)


def main() -> None:
    """Application entry point."""
    test_subject()
    print("~" * 80)
    test_proxy()


if __name__ == "__main__":
    main()
