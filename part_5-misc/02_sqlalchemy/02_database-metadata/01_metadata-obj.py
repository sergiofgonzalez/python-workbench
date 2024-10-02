"""Illustrates the metadata object and how to add a table to it."""

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
)


def main() -> None:
    """Create metadata object and add a table to it."""
    metadata_obj = MetaData()

    user_table = Table(
        "user_account",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("name", String(30)),
        Column("fullname", String),
    )

    address_table = Table(
        "address",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("user_id", ForeignKey("user_account.id"), nullable=False),
        Column("email_address", String, nullable=False),
    )

    # Emit CREATE TABLE statements from the metadata object
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    metadata_obj.create_all(engine)

    # Emit DROP TABLE statements from the metadata object
    metadata_obj.drop_all(engine)


if __name__ == "__main__":
    main()
