"""Illustrates the basics of the MetaData object and creates tables programmatically."""

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
)

# The MetaData object is a container object for the tables and associated data.
# You will typically create a single MetaData object at the module level.
metadata_obj = MetaData()


def main() -> None:
    """Application entry point."""
    engine = create_engine("sqlite+pysqlite:///app.db", echo=True)

    user_table = Table(  # noqa: F841
        "user_account",
        metadata_obj,
        # Column definitions go here
        Column("id", Integer, primary_key=True),
        Column("name", String(30)),
        Column("fullname", String),
    )

    address_table = Table(  # noqa: F841
        "address",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("user_id", None, ForeignKey("user_account.id")),
        Column("email_address", String, nullable=False),
    )

    # Using the MetaData object's create_all() method to create all tables
    metadata_obj.create_all(engine)

    # Using the MetaData object's drop_all() method to drop all tables
    metadata_obj.drop_all(engine)


if __name__ == "__main__":
    main()
