"""Basics of the MetaData object and using reflection to import tables from a DB."""

from sqlalchemy import (
    MetaData,
    Table,
    create_engine,
    text,
)

# The MetaData object is a container object for the tables and associated data.
# You will typically create a single MetaData object at the module level.
metadata_obj = MetaData()


def main() -> None:
    """Application entry point."""
    engine = create_engine("sqlite+pysqlite:///app.db", echo=True)

    with engine.begin() as conn:
        conn.execute(
            text("CREATE TABLE IF NOT EXISTS sample_table (x INTEGER, y INTEGER)"),
        )

    # Using the MetaData object's reflect() method to load table definitions
    # from the database
    sample_table = Table("sample_table", metadata_obj, autoload_with=engine)  # noqa: F841

    # Using the MetaData object's drop_all() method to drop all tables
    metadata_obj.drop_all(engine)


if __name__ == "__main__":
    main()
