"""Illustrate how to create immutable dataclasses."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Bill:
    """Represents a bill with a table number, meal amount, server, and tip amount."""

    table_number: int
    meal_amount: float
    served_by: str
    tip_amount: float = 0.0


def main() -> None:
    """Application entry point."""
    bill = Bill(table_number=5, meal_amount=55.5, served_by="Jason")

    try:
        bill.tip_amount = 55.5 * 0.15  # type: ignore  # noqa: PGH003
    except AttributeError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
