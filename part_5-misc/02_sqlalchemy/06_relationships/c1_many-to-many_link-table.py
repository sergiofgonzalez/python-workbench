"""
Implementing a many-to-many relationship with a link table featuring a composite
PK using SQLAlchemy Core.
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
        Column("id", Integer, primary_key=True),
        Column("email_address", String),
        UniqueConstraint("email_address", name="address_idx_0"),
    )

    user_address_link_table = Table(
        "user_account_address_link",
        metadata_obj,
        Column("user_id", ForeignKey("user_account.id"), primary_key=True),
        Column("address_id", ForeignKey("address.id"), primary_key=True),
    )

    # create the tables defined in the metadata object
    metadata_obj.create_all(engine)

    # populate users and emails, then their links
    with engine.connect() as conn:
        conn.execute(
            insert(user_table),
            [
                {"name": "spongebob", "fullname": "Spongebob Squarepants"},
                {"name": "patrick", "fullname": "Patrick Star"},
                {"name": "sandy", "fullname": "Sandy Cheeks"},
            ],
        )

        conn.execute(
            insert(address_table),
            [
                {
                    "email_address": "spongebob@example.com",
                },
                {
                    "email_address": "patrick@example.com",
                },
                {
                    "email_address": "patrick@bikini-bottom.com",
                },
                {
                    "email_address": "sandy@example.com",
                },
                {
                    "email_address": "sandy@bikini-bottom.com",
                },
                {
                    "email_address": "sandy.cheeks@example.com",
                },
            ],
        )

        # we need a subquery to get the corresponding IDs that will be
        # subsequently inserted.
        # the query can be executed by itself to check it works
        subquery = (
            select(
                user_table.c.id.label("user_id"),
                address_table.c.id.label("address_id"),
            )
            .where(user_table.c.name == bindparam("username"))
            .where(address_table.c.email_address == bindparam("email"))
        ).subquery()

        # print the subquery for inspection
        print(subquery)

        # Retrieve the result of the subquery
        subquery_result = conn.execute(
            select(subquery),
            {"username": "spongebob", "email": "spongebob@example.com"},
        ).fetchone()
        print(f"{subquery_result.user_id=}")
        print(f"{subquery_result.address_id=}")

        # everything is set to populate the link table, however, a subquery
        # cannot be used in the values section as scalar_subquery() can, instead
        # insert().from_select() must be used.
        conn.execute(
            insert(user_address_link_table).from_select(
                ["user_id", "address_id"],
                select(subquery.c.user_id, subquery.c.address_id),
            ),
            [
                {
                    "username": "spongebob",
                    "email": "spongebob@example.com",
                },
                {
                    "username": "patrick",
                    "email": "patrick@example.com",
                },
                {
                    "username": "patrick",
                    "email": "patrick@bikini-bottom.com",
                },
                {
                    "username": "sandy",
                    "email": "sandy@example.com",
                },
                {
                    "username": "sandy",
                    "email": "sandy@bikini-bottom.com",
                },
                {
                    "username": "sandy",
                    "email": "sandy.cheeks@example.com",
                },
                # Patrick isn't very experienced with emails so he delegates
                # each of his addresses to sandy and spongebob
                {
                    "username": "sandy",
                    "email": "patrick@example.com",
                },
                {
                    "username": "spongebob",
                    "email": "patrick@bikini-bottom.com",
                },
            ],
        )
        conn.commit()

    # visual inspection of the tables
    with engine.connect() as conn:
        print(conn.execute(select(user_table)).all())
        print(conn.execute(select(address_table)).all())
        print(conn.execute(select(user_address_link_table)).all())

    # getting user + emails requires a complicated join
    with engine.connect() as conn:
        stmt = (
            select(
                user_table.c.name,
                user_table.c.fullname,
                address_table.c.email_address,
            )
            .select_from(user_table)
            .join(
                user_address_link_table,
                user_table.c.id == user_address_link_table.c.user_id,
            )
            .join(
                address_table,
                address_table.c.id == user_address_link_table.c.address_id,
            )
        )

        rows = conn.execute(stmt)
        for row in rows:
            print(row)

        # getting the data for an individual user
        stmt = (
            select(
                user_table.c.name,
                user_table.c.fullname,
                address_table.c.email_address,
            )
            .select_from(user_table)
            .join(
                user_address_link_table,
                user_table.c.id == user_address_link_table.c.user_id,
            )
            .join(
                address_table,
                address_table.c.id == user_address_link_table.c.address_id,
            )
            .where(user_table.c.name == "sandy")
        )

        rows = conn.execute(stmt)
        for row in rows:
            print(row)


if __name__ == "__main__":
    main()
