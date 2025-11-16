"""Illustrates how to create hierarchies of dataclasses and caveats to consider."""

from dataclasses import dataclass


@dataclass
class BaseBill:
    """Represents a base class for bills."""

    meal_amount: float


@dataclass
class TippedBill(BaseBill):
    """Represents a bill that has been tipped."""

    tip_amount: float


@dataclass
class BaseBillV2:
    """Represents a base class for bills (v2)."""

    meal_amount: float = 15.25


@dataclass
class TippedBillV2(BaseBillV2):
    """Represents a bill that has been tipped (v2)."""

    tip_amount: float  # type: ignore  # noqa: PGH003


def main() -> None:
    """Application entry point."""
    tipped_bill = TippedBill(meal_amount=55.5, tip_amount=55.5 * 0.15)
    print(f"{tipped_bill=}")

    # This fails even before instantiation!
    # because fields without default values cannot appear after fields with
    # default values

    try:
        _ = TippedBillV2(meal_amount=55.5, tip_amount=55.5 * 0.15)
    except Exception as e:  # noqa: BLE001
        print(f"Error creating TippedBillV2: {e} (type={type(e).__name__})")


if __name__ == "__main__":
    main()
