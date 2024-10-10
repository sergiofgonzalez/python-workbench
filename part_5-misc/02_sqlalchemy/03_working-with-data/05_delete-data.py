"""Deleting data using Core."""

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    bindparam,
    create_engine,
    delete,
    insert,
    select,
)


def main() -> None:
    """Application entry point."""
    # setup the environment
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
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

    metadata_obj.create_all(engine)

    with engine.connect() as conn:
        _ = conn.execute(
            insert(user_table),
            [
                {"name": "spongebob", "fullname": "Spongebob Squarepants"},
                {"name": "sandy", "fullname": "Sandy Cheeks"},
                {"name": "patrick", "fullname": "Patrick Star"},
            ],
        )
        scalar_subquery = (
            select(user_table.c.id)
            .where(user_table.c.name == bindparam("username"))
            .scalar_subquery()
        )
        conn.commit()

        _ = conn.execute(
            insert(address_table).values(user_id=scalar_subquery),
            [
                {
                    "username": "spongebob",
                    "email_address": "spongebob@example.com",
                },
                {"username": "sandy", "email_address": "sandy@example.com"},
                {
                    "username": "sandy",
                    "email_address": "sandy.cheeks@example.com",
                },
            ],
        )
        conn.commit()

    # Basic delete
    stmt = delete(user_table).where(user_table.c.name == "patrick")
    print(stmt)

    # Getting affected row counts in delete
    with engine.connect() as conn:
        result = conn.execute(
            delete(user_table).where(user_table.c.name == "patrick"),
        )
        print(f"rows affected: {result.rowcount}")

    # using RETURNING with DELETE
    delete_stmt = (
        delete(user_table)
        .where(user_table.c.name == "patrick")
        .returning(user_table.c.id, user_table.c.name)
    )
    print(delete_stmt)


if __name__ == "__main__":
    main()
