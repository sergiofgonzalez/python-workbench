"""db.py: The database module for the blogging system using SQLite."""

from pathlib import Path
from sqlite3 import Connection, connect


def create_db(db_file: Path | str) -> Connection:
    """Return a properly configured db connection object."""
    return connect(db_file)
