"""Inserting data using Core."""

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

    # insert data
    stmt = insert(user_table).values(
        name="spongebob",
        fullname="Spongebob Squarepants",
    )
    print(stmt)

    compiled = stmt.compile()
    print(compiled)
    print(compiled.params)

    # executing the statement
    with engine.begin() as conn:
        result = conn.execute(stmt)
    print(result.inserted_primary_key)

    # insert without the values part can also be used to insert data
    stmt = insert(user_table)
    print(stmt)

    with engine.connect() as conn:
        result = conn.execute(
            insert(user_table),
            [
                {"name": "sandy", "fullname": "Sandy Cheeks"},
                {"name": "patrick", "fullname": "Patrick Star"},
            ],
        )
        conn.commit()

    # a bit of deep alchemy to populate the related user and addresses
    scalar_subquery = (
        select(user_table.c.id)
        .where(user_table.c.name == bindparam("username"))
        .scalar_subquery()
    )

    with engine.connect() as conn:
        result = conn.execute(
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

    # insert...returning (for db servers that support it)
    insert_stmt = insert(address_table).returning(
        address_table.c.id,
        address_table.c.email_address,
    )
    print(insert_stmt)

    # insert from select
    select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")
    insert_stmt = insert(address_table).from_select(
        ["user_id", "email_address"],
        select_stmt,
    )
    print(insert_stmt)


if __name__ == "__main__":
    main()
