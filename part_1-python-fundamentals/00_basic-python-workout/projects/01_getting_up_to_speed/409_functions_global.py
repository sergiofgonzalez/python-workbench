"""Illustrate the use of global."""

x = 5


def funct1() -> None:  # noqa: D103
    x = 3  # noqa: F841


def funct2() -> None:  # noqa: D103
    global x  # noqa: PLW0603
    x = 2


def main() -> None:
    """Application entry point."""
    funct1()
    assert x == 5  # noqa: PLR2004
    funct2()
    assert x == 2  # noqa: PLR2004
    print("=== All assertions passed! ===")


if __name__ == "__main__":
    main()
