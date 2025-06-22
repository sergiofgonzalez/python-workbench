"""A dummy db_module.py to illustrate the concept of main in libs."""


def delete_db() -> None:
    """Delete the database."""
    print("Database deleted.")


def create_db() -> None:
    """Create the database."""
    print("Database created.")


if __name__ == "__main__":
    # This block will not execute when imported as a module.
    print("This is a dummy db_module.py file.")
    create_db()
    delete_db()
