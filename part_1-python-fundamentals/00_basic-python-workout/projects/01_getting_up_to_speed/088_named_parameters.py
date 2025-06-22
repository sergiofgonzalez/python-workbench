"""Invoke functions using named parameters."""


def birthday_greeting(name: str, age: int) -> str:
    """Return a birthday greeting."""
    return f"Happy Birthday, {name}! You are now {age} years old."


def main() -> None:
    """Application entry point."""
    # using positional arguments
    print(birthday_greeting("Alice", 30))

    # using named parameters
    print(birthday_greeting(name="Bob", age=25))
    print(birthday_greeting(age=40, name="Charlie"))  # order doesn't matter

    # mixing positional and named parameters
    print(birthday_greeting("Diana", age=35))  # positional first, then named


if __name__ == "__main__":
    main()
