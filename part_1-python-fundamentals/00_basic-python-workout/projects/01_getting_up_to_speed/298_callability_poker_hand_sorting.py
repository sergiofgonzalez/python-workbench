"""Illustrates how to sort poker hands using callability."""

from typing import ClassVar


# This solution works but it's not very elegant
class PokerOrder:
    """Utility class used to sort a Poker hand."""

    ORDER: ClassVar[list[int | str]] = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        "J",
        "Q",
        "K",
        "A",
    ]

    def __init__(self, card: int | str) -> None:
        """Initialize an instance of PokerOrder."""
        self.card = card

    def __lt__(self, other: object) -> bool:
        """Return true if self is less than the given other."""
        if not isinstance(other, PokerOrder):
            return NotImplemented
        return self.ORDER.index(self.card) < self.ORDER.index(other.card)


# This solution is much cleaner and succinct but requires a little bit of Kung Fu
class PokerOrderV2(int):
    """Class to handle the sorting order of a hand of Poker cards."""

    def __new__(cls, x: int | str) -> "PokerOrderV2":
        """PokerOrderV2 constructor."""
        cards_to_ord_mapping = {"J": 11, "Q": 12, "K": 13, "A": 14}
        card_ord_number = cards_to_ord_mapping.get(x, x)  # pyright: ignore[reportArgumentType, reportCallIssue]
        return super().__new__(cls, card_ord_number)


def main() -> None:
    """Application entry point."""
    # my approach
    cards = [10, "K", "A", "J", 2]
    sorted_hand = sorted(cards, key=PokerOrder)
    assert sorted_hand == [2, 10, "J", "K", "A"]

    # kung fu approach
    sorted_hand = sorted(cards, key=PokerOrderV2)
    assert sorted_hand == [2, 10, "J", "K", "A"]

    print("=== PASSED ===")


if __name__ == "__main__":
    main()
