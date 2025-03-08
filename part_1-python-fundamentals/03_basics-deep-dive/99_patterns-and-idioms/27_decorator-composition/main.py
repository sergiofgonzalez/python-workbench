"""Application main program."""

from enhanced_calculator import EnhancedCalculator
from stack_calculator import StackCalculator


def test_stack_calculator() -> None:
    """Illustrate how to work with the StackCalculator."""
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


def test_enhanced_calculator() -> None:
    """Illustrate how to work with the decorated StackCalculator."""
    stack_calculator = StackCalculator()
    enhanced_calculator = EnhancedCalculator(stack_calculator)
    enhanced_calculator.put_value(5)
    print(enhanced_calculator)
    enhanced_calculator.put_value(6)
    print(enhanced_calculator)
    enhanced_calculator.put_value(3)
    print(enhanced_calculator)
    print(f">>> Top of the stack: {enhanced_calculator.peek_value()}")
    print(enhanced_calculator)
    print(f">>> Division: {enhanced_calculator.divide()}")
    print(enhanced_calculator)
    print(f">>> Multiplication: {enhanced_calculator.multiply()}")
    print(enhanced_calculator)
    # enhanced behavior
    enhanced_calculator.put_value(0)
    print(enhanced_calculator)
    print(f">>> Division: {enhanced_calculator.divide()}")
    print(f">>> Addition: {enhanced_calculator.add()}")
    print(enhanced_calculator)


def main() -> None:
    """Application entry point."""
    test_stack_calculator()
    print()

    test_enhanced_calculator()


if __name__ == "__main__":
    main()
