"""Illustrate how to create a dict with additional key_of/keys_of methods."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


class ValueDict(dict):
    """A dict subclass that provides key_of and keys_of methods."""

    def key_of(self, value: object) -> object:
        """Return the first key found for the given value."""
        for k, v in self.items():
            if v == value:
                return k
        msg = f"No key found for value: {value}"
        raise KeyError(msg)

    def keys_of(self, value: object) -> Generator[object]:
        """Return all keys found for the given value."""
        for k, v in self.items():
            if v == value:
                yield k


def main() -> None:
    """Application entry point."""
    inventory = ValueDict()
    inventory["apple"] = 2
    inventory["banana"] = 3
    inventory.update({"orange": 2})

    assert inventory == {"apple": 2, "banana": 3, "orange": 2}

    assert inventory.key_of(2) == "apple"
    assert inventory.key_of(3) == "banana"

    assert list(inventory.keys_of(2)) == ["apple", "orange"]
    print("== all tests passed ==")


if __name__ == "__main__":
    main()
