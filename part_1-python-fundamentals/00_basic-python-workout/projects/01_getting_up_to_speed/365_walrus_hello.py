"""An example using the walrus := operator."""


def get_user_input() -> str:
    """Simulate getting user input."""
    return "Y"


def main() -> None:
    """Application entry point."""
    if (user_input := get_user_input()) == "Y":
        print(f"User input is Yes: {user_input=}")
    else:
        print(f"User input is not Yes: {user_input=}")


if __name__ == "__main__":
    main()
