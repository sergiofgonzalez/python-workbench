"""Implementing a One-to-One relationship using distinct tables using Core."""

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
        Column("email_id", ForeignKey("address.id")),
        UniqueConstraint("name", name="user_account_idx_0"),
        UniqueConstraint("email_id", name="user_account_idx_1"),
    )

    address_table = Table(
        "address",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("email_address", String),
        UniqueConstraint("email_address", name="address_idx_0"),
    )

    # create the tables defined in the metadata object
    metadata_obj.create_all(engine)

    # insert some data to validate using a bit of deep alchemy to populate the
    # related user and address correctly
    scalar_subquery = (
        select(address_table.c.id)
        .where(address_table.c.email_address == bindparam("email"))
        .scalar_subquery()
    )
    print(scalar_subquery)

    with engine.connect() as conn:
        conn.execute(
            insert(address_table),
            [
                {"username": "sandy", "email_address": "sandy@example.com"},
                {
                    "username": "spongebob",
                    "email_address": "spongebob@example.com",
                },
                {
                    "username": "patrick",
                    "email_address": "patrick@example.com",
                },
            ],
        )

        conn.execute(
            insert(user_table).values(email_id=scalar_subquery),
            [
                {
                    "name": "spongebob",
                    "fullname": "Spongebob Squarepants",
                    "email": "spongebob@example.com",
                },
                {
                    "name": "patrick",
                    "fullname": "Patrick Star",
                    "email": "patrick@example.com",
                },
                {
                    "name": "sandy",
                    "fullname": "Sandy Cheeks",
                    "email": "sandy@example.com",
                },
            ],
        )
        conn.commit()

    # check that relationship is well established through the FK
    with engine.connect() as conn:
        rows = conn.execute(select(user_table)).all()
        print(rows)
        rows = conn.execute(select(address_table)).all()
        print(rows)

    # getting user + email requires a join
    with engine.connect() as conn:
        stmt = select(
            user_table.c.name,
            user_table.c.fullname,
            address_table.c.email_address,
        ).join_from(
            user_table,
            address_table,
        )
        rows = conn.execute(stmt)
        for row in rows:
            print(row)

    # alternatively, you can join using`Select.join()` which needs only the
    # right side of the JOIN and the left is inferred
    with engine.connect() as conn:
        stmt = select(
            user_table.c.name,
            user_table.c.fullname,
            address_table.c.email_address,
        ).join(
            address_table,
        )
        rows = conn.execute(stmt)
        for row in rows:
            print(row)

    # getting an individual row
    with engine.connect() as conn:
        stmt = (
            select(
                user_table.c.name,
                user_table.c.fullname,
                address_table.c.email_address,
            )
            .where(user_table.c.email_id == address_table.c.id)
            .where(user_table.c.name == "spongebob")
        )
        user_details = conn.execute(stmt).first()
        print(user_details)


if __name__ == "__main__":
    main()
