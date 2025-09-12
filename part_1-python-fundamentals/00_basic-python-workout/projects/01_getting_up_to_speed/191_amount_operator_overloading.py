"""Illustrate operator overloading."""


class Amount:
    """Class to represent an amount with operator overloading."""

    def __init__(self, value: float, currency: str) -> None:
        """Initialize an Amount with a value and currency.

        Args:
            value (float): The numeric value of the amount.
            currency (str): The currency type of the amount.

        """
        self.value = value
        self.currency = currency

    def __gt__(self, other: "Amount") -> bool:
        """Override the greater-than operator for Amount comparison."""
        if self.currency != other.currency:
            msg = "Cannot compare amounts with different currencies."
            raise ValueError(msg)
        return self.value > other.value

    def __repr__(self) -> str:
        """Return a string representation of the Amount object."""
        return f"Amount({self.value}, {self.currency})"


def main() -> None:
    """Application entry point."""
    amount1 = Amount(100, "USD")
    amount2 = Amount(200, "USD")
    amount3 = Amount(150, "EUR")

    print(amount1 > amount2)  # False
    print(amount2 > amount1)  # True
    try:
        print(amount1 > amount3)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
