"""Illustrates the basics of UPDATE and DELETE statements with SQLAlchemy."""

import rich
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
    update,
)

metadata_obj = MetaData()
engine = create_engine("sqlite+pysqlite:///app.db", echo=True)


def setup_db() -> None:
    """Create tables in the database."""
    user_table = Table(
        "user_account",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("name", String(30), nullable=False),
        Column("fullname", String),
    )

    address_table = Table(
        "address",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("email_address", String, nullable=False),
        Column("user_id", Integer, ForeignKey("user_account.id"), nullable=False),
    )

    metadata_obj.create_all(engine)

    with engine.begin() as conn:
        conn.execute(
            insert(user_table).values(
                [
                    {"name": "spongebob", "fullname": "Spongebob Squarepants"},
                    {"name": "patrick", "fullname": "Patrick Star"},
                    {"name": "sandy", "fullname": "Sandy Cheeks"},
                    {"name": "squidward", "fullname": "Squidward Tentacles"},
                    {"name": "gary", "fullname": "Gary the Snail"},
                    {"name": "mrkrabs", "fullname": "Eugene H. Krabs"},
                    {"name": "pearl", "fullname": "Pearl Krabs"},
                ],
            ),
        )

        scalar_subquery_stmt = (
            select(user_table.c.id)
            .where(user_table.c.name == bindparam("username"))
            .scalar_subquery()
        )

        conn.execute(
            insert(address_table).values(user_id=scalar_subquery_stmt),
            [
                {"email_address": "spongebob@example.com", "username": "spongebob"},
                {"email_address": "sandy@example.com", "username": "sandy"},
                {"email_address": "squidward@example.com", "username": "squidward"},
                {"email_address": "pearl@example.com", "username": "pearl"},
                {"email_address": "pearl@foo.com", "username": "pearl"},
                {"email_address": "sandy@bar.com", "username": "sandy"},
            ],
        )


def basic_updates() -> None:
    """Illustrate basic UPDATE statements."""
    user_table = metadata_obj.tables["user_account"]

    # simplest UPDATE statement
    stmt = (
        update(user_table)
        .where(user_table.c.name == "patrick")
        .values(fullname="Patrick the Star")
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above UPDATE statement...")

    with engine.begin() as conn:
        conn.execute(stmt)
    input("UPDATE statement executed. Press Enter to continue...")
    print()

    # using a column expression in the SET clause
    stmt = (
        update(user_table)
        .where(user_table.c.name == "patrick")
        .values(fullname="Username: " + user_table.c.name)
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above UPDATE statement...")
    with engine.begin() as conn:
        conn.execute(stmt)
    input("UPDATE statement executed. Press Enter to continue...")
    print()

    # execute many
    stmt = (
        update(user_table)
        .where(user_table.c.name == bindparam("oldname"))
        .values(fullname=bindparam("newname"))
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input(
        "Press Enter to execute the above UPDATE statement with multiple sets of parameters...",
    )
    with engine.begin() as conn:
        conn.execute(
            stmt,
            [
                {"oldname": "spongebob", "newname": "spongie bob"},
                {"oldname": "sandy", "newname": "sandee"},
                {"oldname": "squidward", "newname": "squidie ward"},
            ],
        )
    input("UPDATE statement executed. Press Enter to continue...")
    print()


def correlated_updates() -> None:
    """Illustrate correlated UPDATE statements."""
    user_table = metadata_obj.tables["user_account"]
    address_table = metadata_obj.tables["address"]

    # correlated UPDATE statement (inline subquery)
    subq = (
        select(address_table.c.email_address)
        .where(address_table.c.user_id == user_table.c.id)
        .limit(1)
        .scalar_subquery()
    )
    rich.print(f"[yellow]{subq}[/yellow]")
    input("Press Enter to continue")
    print()

    stmt = update(user_table).where(user_table.c.name == "pearl").values(fullname=subq)
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above correlated UPDATE statement...")
    print()

    with engine.begin() as conn:
        conn.execute(stmt)
    input("Correlated UPDATE statement executed. Press Enter to continue...")
    print()


def basic_deletes() -> None:
    """Illustrate basic DELETE statements."""
    user_table = metadata_obj.tables["user_account"]

    # simplest DELETE statement
    stmt = delete(user_table).where(user_table.c.name == "squidward")
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above DELETE statement...")

    with engine.begin() as conn:
        conn.execute(stmt)
    input("DELETE statement executed. Press Enter to continue...")
    print()

    # Running it again to see the error handling when no rows are matched
    with engine.begin() as conn:
        conn.execute(stmt)
    input("DELETE statement executed. Press Enter to continue...")
    print()


def correlated_deletes() -> None:
    """Illustrate correlated DELETE statements."""
    user_table = metadata_obj.tables["user_account"]
    address_table = metadata_obj.tables["address"]

    # correlated DELETE statement
    # This should delete the user "sandy"
    subq = (
        select(address_table.c.user_id)
        .where(address_table.c.email_address == "sandy@example.com")
        .scalar_subquery()
    )
    rich.print(f"[yellow]{subq}[/yellow]")
    input("Press Enter to continue")
    print()

    stmt = delete(user_table).where(user_table.c.id == subq)
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above correlated DELETE statement...")
    print()

    with engine.begin() as conn:
        conn.execute(stmt)
    input("Correlated DELETE statement executed. Press Enter to continue...")
    print()


def using_returning_on_update_delete_statements() -> None:
    """Illustrate using RETURNING on UPDATE and DELETE statements."""
    user_table = metadata_obj.tables["user_account"]

    # using RETURNING with an UPDATE statement
    stmt = (
        update(user_table)
        .where(user_table.c.name == "pearl")
        .values(fullname="Pearl the Whale")
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above UPDATE statement...")
    print()

    with engine.begin() as conn:
        result = conn.execute(stmt)
        rich.print(f"[green]Updated rows:[/green] {result.rowcount}")
    input("UPDATE statement executed. Press Enter to continue...")
    print()

    # using RETURNING with a DELETE statement
    stmt = (
        delete(user_table)
        .where(user_table.c.name == "mrkrabs")
        .returning(user_table.c.id, user_table.c.name, user_table.c.fullname)
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above DELETE statement with RETURNING...")
    print()

    with engine.begin() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.id=} {row.name=} {row.fullname=}")
    input("DELETE statement executed. Press Enter to continue...")
    print()


def main() -> None:
    """Application entry point."""
    setup_db()
    input("Database setup complete. Press Enter to continue...")
    print()

    # basic UPDATE statement
    basic_updates()
    input("Basic UPDATE complete. Press Enter to continue...")
    print()

    # correlated UPDATE statement
    correlated_updates()
    input("Correlated UPDATE complete. Press Enter to continue...")
    print()

    # basic DELETE statement
    basic_deletes()
    input("Basic DELETE complete. Press Enter to continue...")
    print()

    # correlated DELETE statement
    correlated_deletes()
    input("Correlated DELETE complete. Press Enter to continue...")
    print()

    # using RETURNING on UPDATE and DELETE statements
    using_returning_on_update_delete_statements()
    input(
        "Using RETURNING on UPDATE and DELETE statements complete. Press Enter to continue..."
    )
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nUser interrupted the execution.")
    finally:
        input("Press Enter to drop the tables and exit...")
        metadata_obj.drop_all(engine)
