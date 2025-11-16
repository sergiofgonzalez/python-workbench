"""Illustrates the nuances of changing values of variables in different scopes."""

db_filename = "global"


def set_db_filename(filename: str) -> None:
    """Set the database filename."""
    # this is discouraged, but shown here for illustration purposes
    global db_filename  # noqa: PLW0603
    db_filename = filename


def main() -> None:
    """Application entry point."""
    print(f"Initial db_filename: {db_filename}")
    set_db_filename("updated")
    print(f"Updated db_filename: {db_filename}")


if __name__ == "__main__":
    main()
