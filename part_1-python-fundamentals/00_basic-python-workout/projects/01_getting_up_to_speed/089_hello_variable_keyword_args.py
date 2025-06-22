"""Illustrate the ** operator for getting keyworded, variable-length args."""


def birthday(name: str, age: int) -> None:
    """Return a birthday greeting."""
    print(f"{name=}, {age=}")


def print_birthday(**kwargs: str) -> None:
    """Print a birthday greeting using variable keyword arguments."""
    print(kwargs)


def main() -> None:
    """Application entry point."""
    # explicitly passing parameters
    birthday("Alice", 30)

    bob = {"name": "Bob", "age": 25}

    # using the ** operator to unpack a dictionary into keyword arguments
    birthday(**bob)

    # using the ** operator to pass variable keyword arguments to a function
    # that expects keyword arguments
    print_birthday(**bob)


if __name__ == "__main__":
    main()
