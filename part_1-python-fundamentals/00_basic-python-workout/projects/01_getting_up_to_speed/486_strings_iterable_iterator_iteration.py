"""Illustrates the diffs between iterable, iterator, and iteration with strings."""


def main() -> None:
    """Application entry point."""
    # string is an interesting example to illustrate iterable vs iterator vs iteration
    sample_string = "Hello"

    # strings support iteration
    for char in sample_string:
        print(char)
    print("-" * 40)

    # Iterator: An object that represents a stream of data
    # it returns the next item when next() is called
    # strings are not iterators themselves
    try:
        next(sample_string)  # ty:ignore[invalid-argument-type]
    except TypeError as e:
        print(f"TypeError when calling next() on string: {e}")
    print("-" * 40)

    # Iterable: An object that can return an iterator (typically via __iter__ method)
    # strings are iterable, as they implement __iter__ (and __getitem__)
    print(f"Is sample_string iterable? {'__iter__' in dir(sample_string)}")
    print(f"Can elements be accessed by item? {'__getitem__' in dir(sample_string)}")
    string_iterator = iter(sample_string)
    print(f"Type of string_iterator: {type(string_iterator)}")
    print("Iterating using the iterator:")
    for index in range(len(sample_string)):
        print(f"str[{index}]: {next(string_iterator)}")
    print("-" * 40)

    # this calls gets items by index using __getitem__
    print("Iterating using indexing:")
    for index in range(len(sample_string)):
        print(f"str[{index}]: {sample_string[index]}")
    print("=" * 40)


if __name__ == "__main__":
    main()
