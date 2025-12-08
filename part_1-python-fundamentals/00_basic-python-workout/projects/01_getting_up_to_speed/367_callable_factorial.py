"""Illustrate how to create a callable class for calculating factorial."""


class Factorial:
    """A callable class to compute factorial of a number."""

    def __init__(self) -> None:
        """Initialize Factorial instances."""
        self._cache = {0: 1, 1: 1}

    def __call__(self, n: int) -> int:
        """Compute the factorial of a number."""
        if n in self._cache:
            return self._cache[n]
        if n == 0:
            return 1
        result = n * self(n - 1)
        self._cache[n] = result
        return result

def main() -> None:
    """Application entry point."""
    factorial = Factorial()
    print(f"Factorial of 5: {factorial(5)}")
    print(f"Factorial of 7: {factorial(7)}")
    print(f"Factorial of 10: {factorial(10)}")

if __name__ == "__main__":
    main()
