"""Illustrates how to create a dict that stores keys in uppercase using UserDict."""

from collections import UserDict


class UpperCaseDict(UserDict):
    """A UserDict subclass that uppercases all keys."""

    def __setitem__(self, key: object, value: object) -> None:  # ty:ignore[invalid-method-override]
        """Set item, uppercasing the key."""
        if not isinstance(key, str):
            msg = "Keys must be strings"
            raise TypeError(msg)
        super().__setitem__(key.upper(), value)


def main() -> None:
    """Application entry point."""
    # Shakedown of UppercaseDict
    numbers = UpperCaseDict()
    numbers["one"] = 1
    assert numbers["ONE"] == 1
    print(numbers)  # {'ONE': 1}
    print("-" * 40)

    try:
        numbers[2] = 2.345  # raises TypeError
    except TypeError as e:
        print(f"Caught TypeError as expected: {e}")
    print("-" * 40)

    numbers = UpperCaseDict({"one": 1, "two": 2, "three": 3})  # must apply uppercase
    print(numbers)  # {'ONE': 1, 'TWO': 2, 'THREE': 3}
    assert numbers == {"ONE": 1, "TWO": 2, "THREE": 3}
    print("-" * 40)

    numbers.update({"four": 4})  # must apply uppercase (what does this do)
    print(numbers)  # {'ONE': 1, 'TWO': 2, 'THREE': 3, 'FOUR': 4}
    assert numbers == {"ONE": 1, "TWO": 2, "THREE": 3, "FOUR": 4}
    print("-" * 40)


if __name__ == "__main__":
    main()
