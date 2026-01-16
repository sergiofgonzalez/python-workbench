"""Illustrates how to deal with an exception with multiple arguments."""


class MyError(Exception):
    """Custom exception class with multiple arguments."""


def main() -> None:
    """Application entry point."""
    try:
        raise MyError("An error occurred")  # noqa: EM101, TRY003, TRY301
    except MyError as e:
        print(f"Caught MyError: {e}: {e.args=}")
        e_str = str(e)
        print(f"String representation of exception: {e_str}")

    try:
        raise MyError("msg1", "msg2")  # noqa: EM101, TRY301
    except MyError as e:
        print(f"Caught MyError: {e}: {e.args=}")
        e_str = str(e)
        print(f"String representation of exception: {e_str}")


if __name__ == "__main__":
    main()
