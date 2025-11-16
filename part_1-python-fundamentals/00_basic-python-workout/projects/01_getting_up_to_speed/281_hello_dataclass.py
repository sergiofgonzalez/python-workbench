"""Introduces dataclasses to reduce boilerplate code in Python data models."""

from dataclasses import dataclass
from typing import NamedTuple


@dataclass
class Bill:
    """Represents a bill with a table number, meal amount, server, and tip amount."""

    table_number: int
    meal_amount: float
    served_by: str
    tip_amount: float


@dataclass
class BillV2:
    """Represents a bill with a table number, meal amount, server, and tip amount."""

    table_number: int
    meal_amount: float
    served_by: str
    tip_amount: float = 0.0

class Billnt(NamedTuple):
    """Represents a bill as a NamedTuple."""

    table_number: int
    meal_amount: float
    served_by: str
    tip_amount: float = 0.0


def main() -> None:
    """Application entry point."""
    bill1 = Bill(5, 60.5, "Jason", 10)
    bill2 = Bill(7, 15.23, "Jane", 3.5)

    print(f"{bill1=}")
    print(f"{bill2=}")

    billv2 = BillV2(5, 60.5, "Alice")
    print(f"{billv2=}")

    # dataclasses are mutable
    billv2.served_by = "Bob"
    print(billv2.served_by)

    # NamedTuples are immutable
    billnt1 = Billnt(5, 55.5, "Charlie", 5)
    billnt2 = Billnt(8, 88.8, "Florence")

    print(f"{billnt1=}")
    print(f"{billnt2=}")

    try:
        billnt2.served_by = "Ryan" # type: ignore  # noqa: PGH003
    except AttributeError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
