"""TypedList Class Implementation."""


class TypedList:
    """A list that only accepts items of a specified type."""

    def __init__(
        self,
        example_item: object,
        initial_items: list[object] | None = None,
    ) -> None:
        """Initialize the TypedList with a specific item type."""
        self._item_type = type(example_item)
        self._items = []
        if initial_items is not None:
            for item in initial_items:
                self.append(item)

    def _fail_if_not_correct_type(self, item: object) -> None:
        """Raise TypeError if the item is not of the correct type."""
        if not isinstance(item, self._item_type):
            msg = f"Item must be of type {self._item_type.__name__}"
            raise TypeError(msg)

    def append(self, item: object) -> None:
        """Append an item to the list if it matches the specified type."""
        self._fail_if_not_correct_type(item)
        self._items.append(item)

    def __getitem__(self, index: int) -> object:
        """Get an item by index."""
        return self._items[index]

    def __setitem__(self, index: int, item: object) -> None:
        """Set an item at a specific index if it matches the specified type."""
        self._fail_if_not_correct_type(item)
        self._items[index] = item

    def __len__(self) -> int:
        """Get the length of the list."""
        return len(self._items)

    def __delitem__(self, index: int) -> None:
        """Delete an item at a specific index."""
        del self._items[index]

    def __add__(self, other: "TypedList") -> "TypedList":
        """Concatenate two TypedLists of the same type."""
        if self._item_type != other._item_type:
            msg = "Cannot concatenate TypedLists of different types"
            raise TypeError(msg)
        return TypedList(self._items[0], self._items + other._items)

    def __mul__(self, n: int) -> "TypedList":
        """Repeat the TypedList n times."""
        return TypedList(self._items[0], self._items * n)

    def __rmul__(self, n: int) -> "TypedList":
        """Repeat the TypedList n times (right multiplication)."""
        return self.__mul__(n)

    def __repr__(self) -> str:
        """Return a string representation of the TypedList."""
        return f"TypedList({self._items})"
