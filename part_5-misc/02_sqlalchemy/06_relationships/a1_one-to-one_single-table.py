"""Implementing a One-to-One relationship using a single table using Core."""

from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    UniqueConstraint,
    create_engine,
    func,
    insert,
    select,
)
from sqlalchemy.exc import IntegrityError


def main() -> None:
    """Entry point for the app."""
    # setup the engine and the Metadata object
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    metadata_obj = MetaData()

    # create the table with the address field and the unique constraint
    user_table = Table(
        "user_account",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("name", String(30)),
        Column("fullname", String),
        Column("address", String, nullable=False),
        UniqueConstraint("name", name="user_account_idx_0"),
        UniqueConstraint("address", name="user_account_idx_1"),
    )

    # create the tables defined in the metadata object
    metadata_obj.create_all(engine)

    # insert some data to validate
    stmt = insert(user_table)
    with engine.begin() as conn:
        conn.execute(
            stmt,
            [
                {
                    "name": "spongebob",
                    "fullname": "Spongebob Squarepant",
                    "address": "spongebob@example.com",
                },
                {
                    "name": "patrick",
                    "fullname": "Patrick Star",
                    "address": "patrick@example.com",
                },
                {
                    "name": "sandy",
                    "fullname": "Sandy Cheeks",
                    "address": "sandy@example.com",
                },
            ],
        )

    # check three rows have been inserted
    stmt = select(func.count("*")).select_from(user_table)
    with engine.connect() as conn:
        result = conn.execute(stmt).scalar_one()
        assert result == 3

    # check that duplicated user names are not allowed
    stmt = insert(user_table)
    with engine.connect() as conn:
        try:
            conn.execute(
                stmt,
                [
                    {
                        "name": "spongebob",
                        "address": "spongiebob@bikini-bottom.com",
                    },
                ],
            )
        except IntegrityError as e:
            print(
                f"IntegrityError (duplicated username): this was expected: {e}",
            )

    # check that duplicated email are not allowed
    stmt = insert(user_table)
    with engine.connect() as conn:
        try:
            conn.execute(
                stmt,
                [
                    {
                        "name": "spongiebob",
                        "address": "spongebob@example.com",
                    },
                ],
            )
        except IntegrityError as e:
            print(
                f"IntegrityError (duplicated address): this was expected: {e}"
            )


if __name__ == "__main__":
    main()
