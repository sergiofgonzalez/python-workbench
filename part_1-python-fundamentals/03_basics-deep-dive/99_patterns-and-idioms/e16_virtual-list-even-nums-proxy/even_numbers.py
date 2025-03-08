"""A virtual list that contains all even numbers (and behaves like a list)."""


class _EvenNums:
    """A class that resembles a list with the even numbers."""

    def __getitem__(self, index: int) -> int:
        """Operator overload for []."""
        return 2 * index

    def __contains__(self, item: int) -> bool:
        """Operator overload for in."""
        return item % 2 == 0


even_numbers = _EvenNums()
