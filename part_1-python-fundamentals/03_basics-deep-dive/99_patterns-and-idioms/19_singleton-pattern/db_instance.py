"""Database instance as a Singleton."""


class Database:
    """Database class."""

    def __init__(self, db_name: str, connection_details: str) -> None:
        """Initialize a Database instance."""
        self.db_name = db_name
        self.connection_details = connection_details


db_instance = Database("my_db", "my_connection_details")
