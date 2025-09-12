"""Illustrate how to raise exceptions."""


def main() -> None:
    """Application entry point."""
    try:
        msg = "A general exception has been raised"
        raise Exception(msg)  # noqa: TRY002, TRY301
    except Exception as e:  # noqa: BLE001
        print(f"An error occurred: {e}")

    try:
        msg = "It was the wrong type"
        raise TypeError(msg)  # noqa: TRY301
    except Exception as e:  # noqa: BLE001
        print(f"An error occurred: {e} (exception type={type(e).__name__})")


if __name__ == "__main__":
    main()
