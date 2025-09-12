"""TODO: description of the program."""

import math


def divide(dividend: float, divisor: float) -> float:
    """Divides two numbers and handles division by zero."""
    try:
        result = dividend / divisor
    except ZeroDivisionError as e:
        print(f"Error: Division by zero is not allowed: {e}")
        return float("inf")  # Return infinity or some other value to indicate error
    except TypeError as e:
        print(f"Error: Invalid types for division: {e}")
        return float("nan")  # Return NaN to indicate an invalid operation
    else:
        return result
    finally:
        print(f"{dividend} / {divisor} operation completed.")


def main() -> None:
    """Application entry point."""
    result = divide(10, 0)
    if result == float("inf"):
        print("Division failed.")
    elif math.isnan(result):
        print("Invalid division operation.")
    else:
        print(f"Division result: {result}")

    result = divide(10, "alice")  # type: ignore  # noqa: PGH003
    if result == float("inf"):
        print("Division failed.")
    elif math.isnan(result):
        print("Invalid division operation.")
    else:
        print(f"Division result: {result}")


if __name__ == "__main__":
    main()
