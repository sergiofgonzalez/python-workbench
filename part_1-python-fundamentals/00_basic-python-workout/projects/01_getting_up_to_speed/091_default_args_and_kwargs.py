"""Illustrate how to declare optional and default args when using kwargs."""


def birthday_greeting(**kwargs: str | int) -> str:
    """Return a birthday greeting using keyword arguments."""
    name = kwargs.get("name", "stranger")
    age = kwargs.get("age")

    if age is not None:
        return f"Happy Birthday, {name}! You are now {age} years old."
    return f"Happy Birthday, {name}!"


def main() -> None:
    """Application entry point."""
    print(birthday_greeting())
    print(birthday_greeting(name="Alice"))
    print(birthday_greeting(name="Bob", age=30))
    print(birthday_greeting(age=25))
    print(birthday_greeting(name="Charlie"))


if __name__ == "__main__":
    main()
