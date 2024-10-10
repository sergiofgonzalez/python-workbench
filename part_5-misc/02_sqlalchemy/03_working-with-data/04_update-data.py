"""Updating data using Core."""

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
    update,
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

    # Basic update
    stmt = (
        update(user_table)
        .where(user_table.c.name == "patrick")
        .values(fullname="Patrick the Star")
    )
    print(stmt)

    # Update with expressions in the VALUES
    stmt = update(user_table).values(fullname="Username: " + user_table.c.name)
    print(stmt)

    # bindparam() will be useful to bind parameters that are replaced in the
    # values when using the "executemany" approach
    stmt = (
        update(user_table)
        .where(user_table.c.name == bindparam("oldname"))
        .values(name=bindparam("newname"))
    )

    with engine.begin() as conn:
        conn.execute(
            stmt,
            [
                {"oldname": "jack", "newname": "ed"},
                {"oldname": "wendy", "newname": "mary"},
                {"oldname": "jim", "newname": "jake"},
            ],
        )

    # correlated updates (UPDATE statements using rows from other tables)
    scalar_subq = (
        select(address_table.c.email_address)
        .where(address_table.c.user_id == user_table.c.id)
        .order_by(address_table.c.id)
        .limit(1)
        .scalar_subquery()
    )
    update_stmt = update(user_table).values(fullname=scalar_subq)
    print(update_stmt)

    # UPDATE FROM as supported by Postgres
    update_stmt = (
        update(user_table)
        .where(user_table.c.id == address_table.c.user_id)
        .where(address_table.c.email_address == "patrick@example.com")
        .values(fullname="Pat")
    )
    print(update_stmt)

    # Getting affected row count in UPDATE
    with engine.connect() as conn:
        result = conn.execute(
            update(user_table)
            .values(fullname="Patric McStar")
            .where(user_table.c.name == "patrick"),
        )
        print(f"rows affected: {result.rowcount}")

    # using RETURNING with UPDATE
    update_stmt = (
        update(user_table)
        .where(user_table.c.name == "patrick")
        .values(fullname="Patric the Star")
        .returning(user_table.c.id, user_table.c.name)
    )
    print(update_stmt)


if __name__ == "__main__":
    main()
