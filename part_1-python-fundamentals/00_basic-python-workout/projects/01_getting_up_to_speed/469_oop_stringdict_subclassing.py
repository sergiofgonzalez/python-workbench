"""Illustrates how to create a StringDict by subclassing the dict class."""


class StringDict(dict):
    """A simple dictionary that only allows string keys and values."""

    def __setitem__(self, key: object, value: object) -> None:
        """Set an item in the dictionary after validating the key type."""
        if not isinstance(key, str):
            msg = f"Key {key} is not of type str"
            raise TypeError(msg)
        if not isinstance(value, str):
            msg = f"Value {value} is not of type str"
            raise TypeError(msg)
        super().__setitem__(key, value)


def main() -> None:
    """Application entry point."""
    # Create a StringDict instance
    sd = StringDict()
    sd["key1"] = "value1"
    print(sd)
    print("-" * 40)

    # Attempt to set a non-string key
    try:
        sd[123] = "value2"
    except TypeError as e:
        print(f"Caught an error while assigning a non-string key: {e}")
    print("-" * 40)

    # Attempt to set a non-string value
    try:
        sd["key2"] = 456
    except TypeError as e:
        print(f"Caught an error while assigning a non-string value: {e}")
    print("-" * 40)

    # it behaves like a normal dictionary for string keys and values
    sd["key3"] = "value3"
    for key, value in sd.items():
        print(f"{key}: {value}")
    print("-" * 40)


if __name__ == "__main__":
    main()
