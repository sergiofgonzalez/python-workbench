"""
Implementing a One-to-One relationship using a distinct tables that shared
their PK using Core.
"""

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    UniqueConstraint,
    bindparam,
    create_engine,
    insert,
    select,
)


def main() -> None:
    """Entry point for the app."""
    # setup the engine and the Metadata object
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    metadata_obj = MetaData()

    user_table = Table(
        "user_account",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("name", String(30)),
        Column("fullname", String),
        UniqueConstraint("name", name="user_account_idx_0"),
    )

    address_table = Table(
        "address",
        metadata_obj,
        Column("id", Integer, ForeignKey("user_account.id"), primary_key=True),
        Column("email_address", String),
        UniqueConstraint("email_address", name="address_idx_0"),
    )

    # create the tables defined in the metadata object
    metadata_obj.create_all(engine)

    # insert some data to validate using a bit of deep alchemy to populate the
    # related user and address correctly
    scalar_subquery = (
        select(user_table.c.id)
        .where(user_table.c.name == bindparam("username"))
        .scalar_subquery()
    )

    with engine.connect() as conn:
        conn.execute(
            insert(user_table),
            [
                {
                    "name": "spongebob",
                    "fullname": "Spongebob Squarepants",
                },
                {
                    "name": "patrick",
                    "fullname": "Patrick Star",
                },
                {
                    "name": "sandy",
                    "fullname": "Sandy Cheeks",
                },
            ],
        )

        conn.execute(
            insert(address_table).values(id=scalar_subquery),
            [
                {
                    "username": "spongebob",
                    "email_address": "spongebob@example.com",
                },
                {
                    "username": "patrick",
                    "email_address": "patrick@example.com",
                },
                {"username": "sandy", "email_address": "sandy@example.com"},
            ],
        )
        conn.commit()

    # check that both tables share the PK
    with engine.connect() as conn:
        rows = conn.execute(select(user_table)).all()
        print(rows)
        rows = conn.execute(select(address_table)).all()
        print(rows)

    # getting user + email requires a join
    with engine.connect() as conn:
        stmt = select(user_table, address_table.c.email_address).where(
            user_table.c.id == address_table.c.id
        )
        rows = conn.execute(stmt)
        for row in rows:
            print(row)

    # getting an individual row
    with engine.connect() as conn:
        stmt = (
            select(user_table, address_table.c.email_address)
            .where(user_table.c.id == address_table.c.id)
            .where(user_table.c.name == "spongebob")
        )
        user_details = conn.execute(stmt).first()
        print(user_details)


if __name__ == "__main__":
    main()
