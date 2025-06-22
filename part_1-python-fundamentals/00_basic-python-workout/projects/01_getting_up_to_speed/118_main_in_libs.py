"""Illustrate the use of main in libraries."""

from utils.db_module import create_db, delete_db


def main() -> None:
    """Application entry point."""
    print("Starting the database operations...")
    delete_db()
    create_db()


if __name__ == "__main__":
    main()
