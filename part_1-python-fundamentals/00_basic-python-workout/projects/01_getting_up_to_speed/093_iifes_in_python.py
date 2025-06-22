"""Illustrate how to immediately apply parameters to a Lambda."""


def main() -> None:
    """Application entry point."""
    num = (lambda x: x + 1)(5)  # noqa: PLC3002
    assert num == 6, "The result should be 6"  # noqa: PLR2004


if __name__ == "__main__":
    main()
