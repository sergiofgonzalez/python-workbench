"""Sample library exposing a function for testing demonstration purposes."""


def add(a: float, b: float) -> float:
    """Return the sum of two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The sum of the two numbers.

    Raises:
        TypeError: If either argument is not a number.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        msg = "Both arguments must be numbers."
        raise TypeError(msg)
    return a + b
