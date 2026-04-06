"""Illustrates the basics of SQLAlchemy ORM API."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, event, select
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    selectinload,
)

if TYPE_CHECKING:
    import sqlite3

    from sqlalchemy.pool import ConnectionPoolEntry

from rich import print  # noqa: A004


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all ORM models."""


class User(Base):
    """Represents a user in the system."""

    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    fullname: Mapped[str]

    addresses: Mapped[list[Address]] = relationship()

    def __repr__(self) -> str:
        """Return a developer-friendly string representation of the User instance."""
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    """Represents an address associated with a user."""

    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))

    user: Mapped[User] = relationship()

    def __repr__(self) -> str:
        """Return a developer-friendly string representation of the Address instance."""
        return (
            f"Address(id={self.id!r}, email_address={self.email_address!r}, "
            f"user_id={self.user_id!r})"
        )


async_engine = create_async_engine("sqlite+aiosqlite:///app.db", echo=True)


# async_sessionmaker is a factory for new AsyncSession objects.
# It is not stateful, so it can be shared across the application.
# expire_on_commit=False will let you access objects after commit.
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


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
    print(
        "[green]SQLite PRAGMA settings applied: "
        "foreign_keys=ON, journal_mode=WAL[/green]",
    )


async def lab_separator(msg: str) -> None:
    """Wait for user input with a message."""
    loop = asyncio.get_running_loop()
    print(f"\n[bold magenta]{msg}[/bold magenta]", end="")
    await loop.run_in_executor(None, input)


async def setup_tables() -> None:
    """Create database tables based on ORM models."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def insert_some_objects() -> None:
    """Insert sample User and Address objects into the database."""
    async with async_session() as session, session.begin():
        spongebob = User(name="spongebob", fullname="Spongebob Squarepants")
        patrick = User(name="patrick", fullname="Patrick Star")
        sandy = User(name="sandy", fullname="Sandy Cheeks")
        spongebob.addresses.append(Address(email_address="spongebob@example.com"))
        sandy.addresses.append(Address(email_address="sandy@example.com"))
        sandy.addresses.append(Address(email_address="sandy@foobar.com"))
        session.add_all([spongebob, patrick, sandy])

        print(f"[yellow]spongebob: {spongebob}[/yellow]")
        print(f"[yellow]{spongebob.addresses}[/yellow]")
        print(f"[yellow]{'-' * 40}[/yellow]")
        print(f"[yellow]patrick: {patrick}[/yellow]")
        print(f"[yellow]{patrick.addresses}[/yellow]")
        print(f"[yellow]{'-' * 40}[/yellow]")
        print(f"[yellow]sandy: {sandy}[/yellow]")
        print(f"[yellow]{sandy.addresses}[/yellow]")
        print(f"[yellow]{'-' * 40}[/yellow]")

    await lab_separator("Objects committed to the database. Press Enter to continue...")

    # This will work all right because we set expire_on_commit=False when
    # creating the async_sessionmaker.
    print(f"[yellow]spongebob: {spongebob}[/yellow]")
    print(f"[yellow]{spongebob.addresses}[/yellow]")
    print(f"[yellow]{'-' * 40}[/yellow]")
    print(f"[yellow]sandy: {sandy}[/yellow]")
    print(f"[yellow]{sandy.addresses}[/yellow]")
    print(f"[yellow]{'-' * 40}[/yellow]")
    await lab_separator(
        "Objects printed after transaction commit. Press Enter to continue...",
    )

    # However, accessing patrick.addresses will trigger a lazy load, which will
    # raise an exception.
    # This is because patrick's addresses were not explicitly set in the transaction
    try:
        print(f"[yellow]patrick: {patrick}[/yellow]")
        print(f"[yellow]{patrick.addresses}[/yellow]")
        print(f"[yellow]{'-' * 40}[/yellow]")
    except Exception as e:  # noqa: BLE001
        print(f"[red]Error accessing patrick.addresses: {e} ({type(e).__name__})[/red]")


async def get_objects() -> None:
    """Reading objects from the database using session.get()."""
    async with async_session() as session:
        patrick = await session.get(User, 2)
        print(f"[yellow]patrick: {patrick}[/yellow]")
        # This will triger a lazy load of patrick.addresses, which will raise
        # an exception.
        try:
            if patrick:
                print(f"[yellow]{patrick.addresses}[/yellow]")
        except Exception as e:  # noqa: BLE001
            print(
                "[red]Error accessing patrick.addresses: "
                f"{e} ({type(e).__name__})[/red]",
            )


async def select_objects() -> None:
    """Reading objects from the database using ORM queries."""
    async with async_session() as session:
        # preventing lazy loading using selectinload()
        stmt = (
            select(User)
            .where(User.name == "patrick")
            .options(selectinload(User.addresses))
        )
        result = await session.execute(stmt)
        patrick = result.scalar_one()
        print(f"[yellow]patrick: {patrick}[/yellow]")
        print(f"[yellow]{patrick.addresses}[/yellow]")
        print(f"[yellow]{'-' * 40}[/yellow]")
        await lab_separator("Object read with selectinload. Press Enter to continue...")

        stmt = select(User.name, Address).join(Address).order_by(User.name)
        result = await session.execute(stmt)
        rows = result.all()
        for name, address in rows:
            print(f"[yellow]{name}: {address}[/yellow]")
        await lab_separator(
            "Objects read with a join query. Press Enter to continue...",
        )


async def update_objects() -> None:
    """Updating objects in the database using ORM API."""
    async with async_session() as session:
        stmt = (
            select(User)
            .order_by(User.id)
            .limit(1)
            .options(selectinload(User.addresses))
        )
        result = await session.execute(stmt)
        one_user = result.scalars().one()

        print(f"[yellow]{one_user=}[/yellow]")
        print(f"[yellow]{one_user.addresses=}[/yellow]")
        await lab_separator("Object read with selectinload. Press Enter to continue...")

        one_user.fullname = one_user.fullname + " (first user)"
        await session.commit()
        await lab_separator("Object updated and committed. Press Enter to continue...")

        # accessing an attribute after commit will not trigger a lazy load
        # as expire_on_commit=False was set when creating the async_sessionmaker.
        print(f"[yellow]{one_user=}[/yellow]")

        # attributes can also be loaded using awaitable_attrs without forcing
        # a lazy load
        for address in await one_user.awaitable_attrs.addresses:
            print(f"[yellow]{address=}[/yellow]")
        await lab_separator("Object after commit. Press Enter to continue...")


async def delete_objects() -> None:
    """Deleting objects from the database using ORM API."""
    async with async_session() as session:
        stmt = select(User).filter_by(name="patrick").limit(1)
        result = await session.execute(stmt)
        patrick = result.scalars().one()

        print(f"[yellow]{patrick=}[/yellow]")
        await lab_separator("Object read. Press Enter to continue...")

        await session.delete(patrick)
        await session.commit()
        await lab_separator("Object deleted and committed. Press Enter to continue...")

        stmt = select(User).options(selectinload(User.addresses)).order_by(User.name)
        result = await session.execute(stmt)
        users = result.scalars().all()
        for user in users:
            print(f"[yellow]{user=}[/yellow]")
            print(f"[yellow]{user.addresses=}[/yellow]")
            print(f"[yellow]{'-' * 40}[/yellow]")
        await lab_separator(
            "Remaining objects read with selectinload. Press Enter to continue...",
        )


async def read_objects_streaming() -> None:
    """Reading objects from the database using streaming."""
    async with async_session() as session:
        stmt = select(User).options(selectinload(User.addresses)).order_by(User.name)
        result = await session.stream(stmt)
        async for user in result.scalars():
            print(f"[yellow]{user=}[/yellow]")
            print(f"[yellow]{user.addresses=}[/yellow]")
            print(f"[yellow]{'-' * 40}[/yellow]")
        await lab_separator(
            "Objects read using streaming. Press Enter to continue...",
        )


async def async_main() -> None:
    """Application entry point."""
    try:
        await setup_tables()
        await lab_separator("Tables created. Press Enter to continue...")

        await insert_some_objects()
        await lab_separator("Objects inserted. Press Enter to continue...")

        await get_objects()
        await lab_separator(
            "Objects queried using session.get(). Press Enter to continue...",
        )

        await select_objects()
        await lab_separator(
            "Objects read using ORM queries. Press Enter to continue...",
        )

        await update_objects()
        await lab_separator(
            "Objects updated using ORM API. Press Enter to continue...",
        )

        await delete_objects()
        await lab_separator(
            "Objects deleted using ORM API. Press Enter to continue...",
        )

        await read_objects_streaming()
        await lab_separator(
            "Objects read using streaming. Press Enter to continue...",
        )

    finally:
        await lab_separator("Cleaning up: dropping tables. Press Enter to continue...")
        async with async_engine.connect() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await async_engine.dispose()


if __name__ == "__main__":
    # start the event loop in the current thread and schedule async_main() to run.
    asyncio.run(async_main())
