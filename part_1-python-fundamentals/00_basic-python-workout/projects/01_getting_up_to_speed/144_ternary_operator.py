"""Illustrate the ternary operator in Python."""


def is_adult(age: int) -> bool:
    """Return True if the passed number is ge 18."""
    return True if age >= 18 else False  # noqa: PLR2004, SIM210


def is_adult2(age: int) -> bool:
    """Return True is the passed number is ge 18."""
    return age >= 18  # noqa: PLR2004


def main() -> None:
    """Application entry point."""
    print(f"{is_adult(20)=}")
    print(f"{is_adult2(20)=}")
    print(f"{is_adult(17)=}")
    print(f"{is_adult2(17)=}")

if __name__ == "__main__":
    main()
