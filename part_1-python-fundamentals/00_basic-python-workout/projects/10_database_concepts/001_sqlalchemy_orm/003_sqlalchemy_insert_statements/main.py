"""Illustrates the basics of SQLAlchemy INSERT statements."""

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    bindparam,
    create_engine,
    insert,
    select,
)

engine = create_engine("sqlite+pysqlite:///app.db", echo=True)

metadata_obj = MetaData()


def setup_db() -> None:
    """Create the tables."""
    Table(
        "user_account",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("name", String(30), nullable=False),
        Column("fullname", String),
    )

    Table(
        "address",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("user_id", ForeignKey("user_account.id"), nullable=False),
        Column("email_address", String, nullable=False),
    )

    metadata_obj.create_all(engine)


def insert_single_row_with_values() -> None:
    """Insert a single row using the values() method."""
    user_account = metadata_obj.tables["user_account"]

    insert_stmt = insert(user_account).values(
        name="spongebob",
        fullname="Spongebob Squarepants",
    )

    with engine.begin() as conn:
        result = conn.execute(insert_stmt)
        print(f"Inserted row with id: {result.inserted_primary_key}")
        print(f"Returned value from INSERT: {result.inserted_primary_key}")

    print(f"{insert_stmt=}")
    compiled_stmt = insert_stmt.compile()
    print(f"{compiled_stmt=}")
    print(f"{compiled_stmt.params=}")

    input(
        "Open the DB to verify the inserted row...",
    )  # Keep the console open to view the output


def insert_multiple_records_without_values() -> None:
    """Insert multiple records using the values() method."""
    user_account = metadata_obj.tables["user_account"]

    insert_stmt = insert(user_account)

    with engine.begin() as conn:
        result = conn.execute(
            insert_stmt,
            [
                {"name": "patrick", "fullname": "Patrick Star"},
                {"name": "sandy", "fullname": "Sandy Cheeks"},
            ],
        )
        print(f"Inserted rows with ids: {result.inserted_primary_key_rows}")

    input(
        "Open the DB to verify the inserted rows...",
    )  # Keep the console open to view the output


def insert_with_values_being_scalar_subquery() -> None:
    """Insert a row with values being scalar subqueries."""
    user_account = metadata_obj.tables["user_account"]
    address = metadata_obj.tables["address"]

    scalar_subquery_stmt = (
        select(user_account.c.id)
        .where(user_account.c.name == bindparam("username"))
        .scalar_subquery()
    )

    insert_stmt = insert(address).values(
        user_id=scalar_subquery_stmt,
    )

    with engine.begin() as conn:
        result = conn.execute(  # noqa: F841
            insert_stmt,
            [
                {"username": "spongebob", "email_address": "spongebob@example.com"},
                {"username": "patrick", "email_address": "patrick@example.com"},
                {"username": "sandy", "email_address": "sandy@example.com"},
            ],
        )
    input("Open the DB to verify the inserted rows in address...")


def insert_returning() -> None:
    """Insert a row and return the inserted primary key."""
    user_account = metadata_obj.tables["user_account"]
    address = metadata_obj.tables["address"]

    with engine.begin() as conn:
        result = conn.execute(
            insert(user_account),
            [
                {"name": "squidward", "fullname": "Squidward Tentacles"},
                {"name": "krabs", "fullname": "Eugene Krabs"},
            ],
        )

    scalar_subquery_stmt = (
        select(user_account.c.id)
        .where(user_account.c.name == bindparam("username"))
        .scalar_subquery()
    )

    insert_stmt = (
        insert(address)
        .values(
            user_id=scalar_subquery_stmt,
        )
        .returning(address.c.id, address.c.user_id, address.c.email_address)
    )

    with engine.begin() as conn:
        result = conn.execute(
            insert_stmt,
            [
                {"username": "squidward", "email_address": "squidward@example.com"},
                {"username": "krabs", "email_address": "krabs@example.com"},
            ],
        )
    print("Inserted rows with the following ids and email addresses:")
    for row in result:
        print(f"ID: {row.id}, User ID: {row.user_id}, Email: {row.email_address}")
    input("Open the DB to verify the inserted rows in address...")


def insert_from() -> None:
    """Insert rows from a select statement."""
    user_account = metadata_obj.tables["user_account"]
    address = metadata_obj.tables["address"]

    with engine.begin() as conn:
        result = conn.execute(  # noqa: F841
            insert(user_account),
            [
                {"name": "pearl", "fullname": "Pearl Krabs"},
                {"name": "gary", "fullname": "Gary the Snail"},
            ],
        )

    with engine.begin() as conn:
        conn.execute(
            insert(address).from_select(
                ["user_id", "email_address"],
                select(user_account.c.id, user_account.c.name + "@example.com")
                .where(user_account.c.name.in_(["pearl", "gary"])),
            ),
        )
    input("Open the DB to verify the inserted rows in address...")


def main() -> None:
    """Application entry point."""
    try:
        setup_db()

        # Practicing insert()
        insert_single_row_with_values()
        insert_multiple_records_without_values()

        # Complex queries: scalar subqueries
        insert_with_values_being_scalar_subquery()

        # Complex queries: insert...returning
        insert_returning()

        # complex queries: insert...from_select
        insert_from()

    finally:
        metadata_obj.drop_all(engine)  # Clean up the database after testing


if __name__ == "__main__":
    main()
