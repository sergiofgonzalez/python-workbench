"""Illustrate the nuances of global variables in Python."""

my_global_var = "Hello to Jason!"


def print_greeting() -> None:
    """Print a greeting using the global variable."""
    print(my_global_var)


def update_global_var(new_value: str) -> None:
    """Update the global variable."""
    global my_global_var  # noqa: PLW0603
    my_global_var = new_value
    print(f"Global variable updated to: {my_global_var}")


def main() -> None:
    """Application entry point."""
    print_greeting()
    print(f"{my_global_var=!r}")
    # Trying to modify the global variable makes it a local and
    # will break the code
    # my_global_var = "Hello to Jason! (modified-main)"  # noqa: ERA001
    update_global_var("Hello to Jason! (modified-main)")


if __name__ == "__main__":
    print(f"{my_global_var=!r}")
    print("=" * 20 + " Invoking main will modify " + "=" * 20)
    main()
    print(f"{my_global_var=!r}")
    my_global_var = "Hello to Jason! (modified)"
    print("=" * 20 + " After modification " + "=" * 20)
    print(f"{my_global_var=!r}")
    main()
