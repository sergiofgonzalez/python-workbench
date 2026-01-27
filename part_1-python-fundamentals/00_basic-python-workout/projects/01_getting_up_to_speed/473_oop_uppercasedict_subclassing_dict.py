"""Illustrates how to subclass dict to create a dict class that uppercases all keys."""


class UpperCaseDict(dict):
    """A dict subclass that uppercases all keys."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Initialize the UpperCaseDict, uppercasing all keys."""
        if args:
            if len(args) > 1:
                msg = f"Expected at most 1 positional argument, got {len(args)}"
                raise TypeError(msg)
            initial_data = dict(args[0])
            if initial_data:
                initial_data = {
                    str(key).upper(): value for key, value in initial_data.items()
                }
        else:
            initial_data = {}
        if kwargs:
            initial_data.update(
                {str(key).upper(): value for key, value in kwargs.items()},
            )
        super().__init__(initial_data)

    def __setitem__(self, key: str, value: object) -> None:
        """Set item, uppercasing the key."""
        if not isinstance(key, str):
            msg = "Keys must be strings"
            raise TypeError(msg)
        super().__setitem__(key.upper(), value)

    def update(self, *args: object, **kwargs: object) -> None:
        """Update the dictionary with uppercased keys."""
        for k, v in dict(*args, **kwargs).items():
            self[k] = v


def main() -> None:
    """Application entry point."""
    # Shakedown of UppercaseDict
    numbers = UpperCaseDict()
    numbers["one"] = 1
    assert numbers["ONE"] == 1
    print(numbers)  # {'ONE': 1}
    print("-" * 40)

    try:
        numbers[2] = 2.345  # raises TypeError  # ty:ignore[invalid-assignment]
    except TypeError as e:
        print(f"Caught TypeError as expected: {e}")
    print("-" * 40)

    numbers = UpperCaseDict({"one": 1, "two": 2, "three": 3})  # must apply uppercase
    print(numbers) # {'ONE': 1, 'TWO': 2, 'THREE': 3}
    assert numbers == {"ONE": 1, "TWO": 2, "THREE": 3}
    print("-" * 40)

    numbers.update({"four": 4})  # must apply uppercase (what does this do)
    print(numbers)  # {'ONE': 1, 'TWO': 2, 'THREE': 3, 'FOUR': 4}
    assert numbers == {"ONE": 1, "TWO": 2, "THREE": 3, "FOUR": 4}
    print("-" * 40)


if __name__ == "__main__":
    main()
