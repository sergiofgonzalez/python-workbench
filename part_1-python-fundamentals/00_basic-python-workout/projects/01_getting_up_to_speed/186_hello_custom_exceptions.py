"""Illustrate how to create custom exceptions."""


class MyCustomError(Exception):
    """A custom exception for demonstration purposes."""


def main() -> None:
    """Application entry point."""
    try:
        msg = "This is a custom error message."
        raise MyCustomError(msg)  # noqa: TRY301
    except Exception as e:  # noqa: BLE001
        print(f"An error occurred: {e} (exception type={type(e).__name__})")


if __name__ == "__main__":
    main()
