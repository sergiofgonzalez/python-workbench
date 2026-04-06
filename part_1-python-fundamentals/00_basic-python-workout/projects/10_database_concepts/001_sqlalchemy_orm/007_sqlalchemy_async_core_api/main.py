"""Illustrates the basics of SQLAlchemy Async Core API."""

import asyncio
import sqlite3

import rich
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    bindparam,
    delete,
    event,
    insert,
    select,
    update,
)
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import ConnectionPoolEntry

async_engine = create_async_engine("sqlite+aiosqlite:///app.db", echo=True)


@event.listens_for(async_engine.sync_engine, "connect")
def set_sqlite_pragma(
    dbapi_connection: sqlite3.Connection,
    connection_record: ConnectionPoolEntry,  # noqa: ARG001
) -> None:
    """Set SQLite PRAGMA settings on connection for reasonable defaults."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()


metadata_obj = MetaData()


async def lab_separator(msg: str) -> None:
    """Wait for user input with a message."""
    loop = asyncio.get_running_loop()
    rich.print(f"\n[bold magenta]{msg}[/bold magenta]", end="")
    await loop.run_in_executor(None, input)


async def create_tables() -> None:
    """Create all tables in the database."""
    async with async_engine.connect() as conn:
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
        await conn.run_sync(metadata_obj.create_all)


async def populate_tables() -> None:
    """Insert sample data into the tables."""
    user_table = metadata_obj.tables["user_account"]
    address_table = metadata_obj.tables["address"]

    async with async_engine.begin() as conn:
        await conn.execute(
            insert(user_table),
            [
                {"name": "spongebob", "fullname": "SpongeBob Squarepants"},
                {"name": "patrick", "fullname": "Patrick Star"},
                {"name": "sandy", "fullname": "Sandy Cheeks"},
                {"name": "squidward", "fullname": "Squidward Tentacles"},
                {"name": "mrkrabs", "fullname": "Eugene H. Krabs"},
                {"name": "gary", "fullname": "Gary the Snail"},
                {"name": "pearl", "fullname": "Pearl Krabs"},
            ],
        )

        subq = (
            select(user_table.c.id).where(user_table.c.name == bindparam("username"))
        ).scalar_subquery()

        await conn.execute(
            statement=insert(address_table).values(user_id=subq),
            parameters=[
                {"username": "spongebob", "email_address": "spongebob@example.com"},
                {"username": "squidward", "email_address": "squidward@example.com"},
                {"username": "pearl", "email_address": "pearl@example.com"},
                {"username": "sandy", "email_address": "sandy@example.com"},
                {"username": "pearl", "email_address": "pearl@foo.com"},
                {"username": "sandy", "email_address": "sandy@foo.com"},
            ],
        )


async def selecting_data() -> None:
    """Select and print data from the tables."""
    user_table = metadata_obj.tables["user_account"]
    address_table = metadata_obj.tables["address"]

    async with async_engine.connect() as conn:
        # Getting all rows from the user_account table
        result = await conn.execute(select(user_table))
        users = result.all()
        rich.print(f"\n[yellow]All users: {users}[/yellow]")
        await lab_separator("Result.all() done. Press Enter to continue...")

        # Getting all rows from the address table using streaming
        async_result = await conn.stream(select(address_table))
        rich.print("\n[yellow]All addresses:[/yellow]")
        async for row in async_result:
            rich.print(f"[yellow]{row}[/yellow]")
        await lab_separator("Streaming result done. Press Enter to continue...")

        # Joining tables
        stmt = (
            select(user_table.c.name, address_table.c.email_address)
            .join(user_table)
            .order_by(user_table.c.name)
        )
        result = await conn.execute(stmt)
        rich.print("\n[yellow]User names and email addresses:[/yellow]")
        for row in result:
            rich.print(f"[yellow]{row.name=}, {row.email_address=}[/yellow]")
        await lab_separator("Join query done. Press Enter to continue...")

        async_result = await conn.stream(stmt)
        rich.print("\n[yellow]Streaming user names and email addresses:[/yellow]")
        async for row in async_result:
            rich.print(f"[yellow]{row.name=}, {row.email_address=}[/yellow]")
        await lab_separator("Streaming join query done. Press Enter to continue...")


async def update_delete_data() -> None:
    """Update and delete data in the tables."""
    user_table = metadata_obj.tables["user_account"]
    address_table = metadata_obj.tables["address"]

    async with async_engine.begin() as conn:
        stmt = (
            update(user_table)
            .where(user_table.c.name == "patrick")
            .values(fullname="Patrick the Star")
        )
        await conn.execute(stmt)
    await lab_separator("Simple update done. Press Enter to continue...")

    async with async_engine.begin() as conn:
        stmt = (
            update(user_table)
            .where(user_table.c.name == bindparam("oldname"))
            .values(name=bindparam("newname"))
        )
        await conn.execute(
            stmt,
            [
                {"oldname": "sandy", "newname": "sandee"},
                {"oldname": "patrick", "newname": "pat"},
                {"oldname": "squidward", "newname": "squid-ed"},
            ],
        )
    await lab_separator("Parameterized update done. Press Enter to continue...")

    async with async_engine.begin() as conn:
        stmt = delete(user_table).where(user_table.c.name == "pat")
        await conn.execute(stmt)
    await lab_separator("Simple delete done. Press Enter to continue...")

    async with async_engine.begin() as conn:
        # Find the user_id via the email address
        subq = (
            select(address_table.c.user_id)
            .where(
                address_table.c.email_address == bindparam("email"),
            )
            .scalar_subquery()
        )

        # Delete addresses first to avoid foreign key IntegrityError
        stmt = delete(address_table).where(
            address_table.c.user_id == subq,
        )
        await conn.execute(stmt, [{"email": "sandy@example.com"}])

        # Now delete the user
        stmt = delete(user_table).where(user_table.c.id == subq)
        await conn.execute(stmt, [{"email": "sandy@example.com"}])

    await lab_separator("Delete with subquery done. Press Enter to continue...")


async def async_main() -> None:
    """Application entry point."""
    try:
        await create_tables()
        await lab_separator("Tables created. Press Enter to continue...")

        await populate_tables()
        await lab_separator("Tables populated. Press Enter to continue...")

        await selecting_data()
        await lab_separator("Selecting data done. Press Enter to continue...")

        await update_delete_data()
        await lab_separator("Update and delete done. Press Enter to continue...")

    finally:
        async with async_engine.connect() as conn:
            await conn.run_sync(metadata_obj.drop_all)
        await async_engine.dispose()


if __name__ == "__main__":
    asyncio.run(async_main())
