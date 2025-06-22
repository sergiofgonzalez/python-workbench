"""Illustrate how to declare default and optional arguments in a function."""


def birthday_greeting(name: str = "stranger", age: int | None = None) -> str:
    """Return a birthday greeting."""
    if age is not None:
        return f"Happy Birthday, {name}! You are now {age} years old."
    return f"Happy Birthday, {name}!"


def main() -> None:
    """Application entry point."""
    print(birthday_greeting())
    print(birthday_greeting("Alice"))
    print(birthday_greeting("Bob", 30))
    print(birthday_greeting(age=25))


if __name__ == "__main__":
    main()
