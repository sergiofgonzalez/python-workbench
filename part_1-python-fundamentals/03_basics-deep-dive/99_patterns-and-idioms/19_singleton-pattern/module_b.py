"""Another Python module that uses the database through the Singleton."""

from db_instance import Database, db_instance


def get_db_instance() -> Database:
    """Return the db_instance Singleton."""
    return db_instance
