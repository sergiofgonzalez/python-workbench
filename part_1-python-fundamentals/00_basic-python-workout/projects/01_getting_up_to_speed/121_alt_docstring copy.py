"""Alternative docstring for documenting functions."""


def quotient(dividend: float, divisor: float, *, taking_int: bool = False) -> float:
    """Calculate the quotient of two numbers.

    :dividend: float,  The number to be divided.
    :divisor: float, The number by which to divide.
    :taking_int: bool | None, If True, return the integer part of the quotient.
    Defaults to False

    :return: The quotient of dividend and divisor, or the integer part if taking_int is
      True.
    :raises ValueError: If divisor is zero.
    """
    if divisor == 0:
        msg = "Divisor cannot be zero."
        raise ValueError(msg)

    result = dividend / divisor
    return int(result) if taking_int else result


def main() -> None:
    """Application entry point."""
    try:
        print(quotient(10, 2))  # Should print 5.0
        print(quotient(10, 3, taking_int=True))  # Should print 3
        print(quotient(10, 0))  # Should raise ValueError
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
