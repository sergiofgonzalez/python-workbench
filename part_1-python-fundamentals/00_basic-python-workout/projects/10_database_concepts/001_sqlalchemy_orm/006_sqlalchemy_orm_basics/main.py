"""Illustrates the basics of SQLAlchemy ORM API."""

from __future__ import annotations

from time import perf_counter
from typing import TYPE_CHECKING

import rich
from sqlalchemy import (
    ForeignKey,
    String,
    bindparam,
    create_engine,
    event,
    insert,
    select,
    text,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    aliased,
    contains_eager,
    joinedload,
    mapped_column,
    relationship,
    selectinload,
)

if TYPE_CHECKING:
    import sqlite3

    from sqlalchemy.pool import ConnectionPoolEntry


class Base(DeclarativeBase):
    """Base class for all ORM models."""


class User(Base):
    """Represents a user in the system."""

    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str]

    addresses: Mapped[list[Address]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        """Return the developer-friendly string representation of the User object."""
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    """Represents an email address associated with a user."""

    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))

    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        """Return the developer-friendly string representation of the Address object."""
        return (
            f"Address(id={self.id!r}, email_address={self.email_address!r}, "
            f"user_id={self.user_id!r})"
        )


class UserV2(Base):
    """Represents a user in the system."""

    __tablename__ = "user_account2"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str]

    addresses: Mapped[list[AddressV2]] = relationship(
        back_populates="user",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        """Return the developer-friendly string representation of the User object."""
        return f"UserV2(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class AddressV2(Base):
    """Represents an email address associated with a user."""

    __tablename__ = "address2"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account2.id"))

    user: Mapped[UserV2] = relationship(back_populates="addresses", lazy="selectin")

    def __repr__(self) -> str:
        """Return the developer-friendly string representation of the Address object."""
        return (
            f"AddressV2(id={self.id!r}, email_address={self.email_address!r}, "
            f"user_id={self.user_id!r})"
        )


class UserV3(Base):
    """Represents a user in the system."""

    __tablename__ = "user_account3"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str]

    addresses: Mapped[list[AddressV3]] = relationship(
        back_populates="user",
        lazy="raise_on_sql",
    )

    def __repr__(self) -> str:
        """Return the developer-friendly string representation of the User object."""
        return f"UserV3(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class AddressV3(Base):
    """Represents an email address associated with a user."""

    __tablename__ = "address3"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account3.id"))

    user: Mapped[UserV3] = relationship(back_populates="addresses", lazy="raise_on_sql")

    def __repr__(self) -> str:
        """Return the developer-friendly string representation of the Address object."""
        return (
            f"AddressV3(id={self.id!r}, email_address={self.email_address!r}, "
            f"user_id={self.user_id!r})"
        )


engine = create_engine("sqlite+pysqlite:///app.db", echo=True)


@event.listens_for(engine, "connect")
def set_sqlite_pragma(
    dbapi_connection: sqlite3.Connection,
    connection_record: ConnectionPoolEntry,  # noqa: ARG001
) -> None:
    """Set SQLite PRAGMA settings on connection for reasonable defaults."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()


def setup_tables() -> None:
    """Create the database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(engine)


def insert_some_data_sql() -> None:
    """Insert some data into the database using raw SQL with the Session object."""
    with Session(engine) as session:
        stmt = "INSERT INTO user_account (name, fullname) VALUES (:name, :fullname)"
        session.execute(
            text(stmt),
            [
                {"name": "spongebob", "fullname": "Spongebob Squarepants"},
                {"name": "patrick", "fullname": "Patrick Star"},
            ],
        )

        stmt = (
            "INSERT INTO address (email_address, user_id)"
            "     VALUES (:email_address, "
            "             (SELECT id FROM user_account WHERE name = 'spongebob'))"
        )
        session.execute(
            text(stmt),
            [
                {"email_address": "spongebob@example.com"},
            ],
        )
        session.commit()


def read_data_orm_queries() -> None:
    """Read data from the database using ORM queries."""
    with Session(engine) as session:
        stmt = select(User)
        row = session.execute(stmt).first()
        rich.print(f"[yellow]{row=} (type={type(row)})[/yellow]")
        user = row[0]  # ty:ignore[not-subscriptable]
        rich.print(f"[yellow]{user=} (type={type(user)})[/yellow]")
        input("Press Enter to continue...")

        user = session.scalars(select(User)).first()
        rich.print(f"[yellow]{user=} (type={type(user)})[/yellow]")
        input("Press Enter to continue...")

        rows = session.execute(select(User)).all()
        for row in rows:
            rich.print(f"[yellow]{row=} (type={type(row)})[/yellow]")

        users = session.scalars(select(User)).all()
        for user in users:
            rich.print(f"[yellow]{user=} (type={type(user)})[/yellow]")
        input("Press Enter to continue...")

        stmt = select(User.name, Address).join(Address).order_by(Address.id)
        rows = session.execute(stmt).all()
        for row in rows:
            rich.print(f"[yellow]{row=} (type={type(row)})[/yellow]")

        rows = session.execute(stmt).all()
        for name, address in rows:
            rich.print(
                f"[yellow]{name=} {address=} "
                f"(type={type(name)}, {type(address)})[/yellow]",
            )
        input("Press Enter to continue...")

        patrick = session.scalars(select(User).filter_by(name="patrick")).first()
        rich.print(f"[yellow]{patrick=} (type={type(patrick)})[/yellow]")
        input("Press Enter to continue...")

        # scalar_one(): returns the first column of the first row, and raises an
        #  error if there are no rows or more than one row
        patrick = session.execute(select(User).filter_by(name="patrick")).scalar_one()
        rich.print(f"[yellow]{patrick=} (type={type(patrick)})[/yellow]")
        input("Press Enter to continue...")


def creating_and_persisting_objects_representing_rows() -> None:  # noqa: PLR0915
    """Create and persist objects representing rows in the database."""
    with Session(engine) as session:
        squidward = User(name="squidward", fullname="Squidward Tentacles")
        mrkrabs = User(name="mrkrabs", fullname="Eugene H. Krabs")
        rich.print(f"[yellow]{(squidward in session)=}[/yellow]")
        rich.print(f"[yellow]{(mrkrabs in session)=}[/yellow]")
        input("Press Enter to continue...")

        session.add(squidward)
        session.add(mrkrabs)
        rich.print(f"[yellow]{(squidward in session)=}[/yellow]")
        rich.print(f"[yellow]{(mrkrabs in session)=}[/yellow]")
        rich.print(f"[yellow]Objects managed by the session: {session.new=}[/yellow]")
        input("Press Enter to continue...")

        session.commit()
        rich.print("[yellow]COMMITTED![/yellow]")
        input("Press Enter to continue...")
        rich.print(f"[yellow]{squidward.id=}[/yellow]")
        input("You should see refresh SQL above. Press Enter to continue...")

        patrick = session.execute(select(User).filter_by(name="patrick")).scalar_one()
        patrick.fullname = "Patrick the Star"
        rich.print(f"[yellow]Session dirty objects: {session.dirty=}[/yellow]")
        input("Press Enter to continue...")

        spongebob = session.execute(
            select(User).filter_by(name="spongebob"),
        ).scalar_one()
        rich.print(f"[yellow]{spongebob=}[/yellow]")
        rich.print(f"[yellow]Session dirty objects: {session.dirty=}[/yellow]")
        input("Press Enter to continue...")

        session.delete(patrick)
        input("Press Enter to continue...")

        # Forcing autoflush
        session.execute(
            select(User).filter_by(name="spongebob"),
        )
        input("Press Enter to continue...")

        rich.print(f"[yellow]{(patrick in session)=}[/yellow]")
        input("Press Enter to continue...")

        # first we need to bring back the users into the session
        spongebob = session.execute(
            select(User).filter_by(name="spongebob"),
        ).scalar_one()

        spongebob.addresses.append(Address(email_address="spongebob@foo.com"))
        rich.print(f"[yellow]{spongebob.addresses=}[/yellow]")
        input("Press Enter to continue...")

        session.flush()
        rich.print("[yellow]Session flushed![/yellow]")
        rich.print(f"[yellow]{spongebob.addresses=}[/yellow]")
        input("Press Enter to continue...")

        session.rollback()
        rich.print("[yellow]Session rolled back![/yellow]")
        rich.print(f"[yellow]{patrick.__dict__=}[yellow]")
        input("Press Enter to continue...")
        rich.print(f"[yellow]{patrick.fullname=}[/yellow]")
        input("Press Enter to continue...")
        rich.print(f"[yellow]{patrick in session=}[/yellow]")
        rich.print(f"[yellow]{patrick.__dict__=}[yellow]")
        input("Press Enter to continue...")

    try:
        rich.print(
            f"[yellow]Trying to access Patrick's fullname outside of the session: "
            f"{patrick.fullname}[/yellow]",
        )
        rich.print(
            f"[yellow]Trying to access Patrick's addresses outside of the session: "
            f"{patrick.addresses}[/yellow]",
        )
    except Exception as e:  # noqa: BLE001
        rich.print(f"[red]Error: {e} ({type(e).__name__})[/red]")


def getting_objects_from_the_session() -> None:
    """Get objects from the session."""
    with Session(engine) as session:
        squidward = session.execute(
            select(User).filter_by(name="squidward"),
        ).scalar_one()
        some_squidward = session.get(User, squidward.id)
        rich.print(f"[yellow]{squidward is some_squidward=}[/yellow]")
        input("Press Enter to continue...")


def using_bulk_insert_orm() -> None:
    """Use bulk insert ORM to insert many rows at once."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    entities = [(User, Address), (UserV2, AddressV2), (UserV3, AddressV3)]

    with Session(engine) as session:
        for user_entity, address_entity in entities:
            session.execute(
                insert(user_entity),
                [
                    {"name": "spongebob", "fullname": "Spongebob Squarepants"},
                    {"name": "patrick", "fullname": "Patrick Star"},
                    {"name": "sandy", "fullname": "Sandy Cheeks"},
                    {"name": "mrkrabs", "fullname": "Eugene H. Krabs"},
                    {"name": "squidward", "fullname": "Squidward Tentacles"},
                    {"name": "gary", "fullname": "Gary the Snail"},
                    {"name": "pearl", "fullname": "Pearl Krabs"},
                ],
            )

            subq = (
                select(User.id)
                .where(User.name == bindparam("username"))
                .scalar_subquery()
            )

            session.execute(
                insert(address_entity).values(user_id=subq),
                [
                    {
                        "email_address": "spongebob@example.com",
                        "username": "spongebob",
                        "user_id": subq,
                    },
                    {
                        "email_address": "sandy@example.com",
                        "username": "sandy",
                        "user_id": subq,
                    },
                    {
                        "email_address": "sandy@foobar.com",
                        "username": "sandy",
                        "user_id": subq,
                    },
                    {
                        "email_address": "squidward@example.com",
                        "username": "squidward",
                        "user_id": subq,
                    },
                    {
                        "email_address": "pearl@example.com",
                        "username": "pearl",
                        "user_id": subq,
                    },
                    {
                        "email_address": "pearl@foobar.com",
                        "username": "pearl",
                        "user_id": subq,
                    },
                ],
            )
            session.commit()
    input("Inserted many rows using bulk insert ORM. Press Enter to continue...")


def subqueries_and_ctes() -> None:
    """Illustrate subqueries and CTEs."""
    with Session(engine) as session:
        subq = (
            select(Address)
            .where(~Address.email_address.like("%@foobar.com"))
            .subquery()
        )

        stmt = (
            select(User, subq.c.email_address)
            .join(subq, subq.c.user_id == User.id)
            .order_by(subq.c.id)
        )
        rows = session.execute(stmt)
        for row in rows:
            rich.print(f"[yellow]{row=} (type={type(row)})[/yellow]")
        input("Press Enter to continue...")

        cte_subq = (
            select(Address).where(~Address.email_address.like("%@foobar.com")).cte()
        )

        stmt = (
            select(User, cte_subq.c.email_address)
            .join(cte_subq, cte_subq.c.user_id == User.id)
            .order_by(cte_subq.c.id)
        )
        rows = session.execute(stmt)
        for row in rows:
            rich.print(f"[yellow]{row=} (type={type(row)})[/yellow]")
        input("Press Enter to continue...")


def unions_with_orm() -> None:
    """Illustrate unions with ORM."""
    with Session(engine) as session:
        stmt1 = select(User).filter_by(name="spongebob")
        stmt2 = select(User).filter_by(name="sandy")
        union_stmt = stmt1.union(stmt2)
        rows = session.execute(union_stmt)
        for row in rows:
            rich.print(f"[yellow]{row=} (type={type(row)})[/yellow]")
        input("Press Enter to continue...")

        stmt = select(User).from_statement(union_stmt)
        rows = session.execute(stmt)
        for row in rows:
            rich.print(f"[yellow]{row=} (type={type(row)})[/yellow]")
        input("Press Enter to continue...")

        # This is a more flexible way to use the union statement, as it allows us
        #  to use the ORM features
        user_alias = aliased(User, union_stmt.subquery())
        orm_stmt = select(user_alias).order_by(user_alias.id)
        for obj in session.execute(orm_stmt).scalars():
            rich.print(f"[yellow]{obj=} (type={type(obj)})[/yellow]")
        input("Press Enter to continue...")


def grokking_relationships() -> None:
    """Illustrate working with relationships."""
    with Session(engine) as session:
        gary = session.execute(select(User).filter_by(name="gary")).scalar_one()
        rich.print(f"[yellow]{gary.addresses=}[/yellow]")

    a1 = Address(email_address="gary@example.com")
    gary.addresses.append(a1)
    rich.print(f"[yellow]{gary.addresses=}[/yellow]")
    rich.print(f"[yellow]{a1.user=}; {a1.user_id=}[/yellow]")
    input("Added an address to Gary. Press Enter to continue...")

    a2 = Address(email_address="gary@foobar.com")
    gary.addresses.append(a2)
    rich.print(f"[yellow]{gary.addresses=}[/yellow]")
    rich.print(f"[yellow]{a2.user=}; {a2.user_id=}[/yellow]")
    input("Added another address to Gary. Press Enter to continue...")

    with Session(engine) as session:
        rich.print(f"[yellow]{gary in session=}[/yellow]")
        rich.print(f"[yellow]{a1 in session=}[/yellow]")
        rich.print(f"[yellow]{a2 in session=}[/yellow]")
        input("Press Enter to continue...")

        session.add(gary)
        rich.print(f"[yellow]{gary in session=}[/yellow]")
        rich.print(f"[yellow]{a1 in session=}[/yellow]")
        rich.print(f"[yellow]{a2 in session=}[/yellow]")
        input("Press Enter to continue...")

        session.commit()
        rich.print("[yellow]COMMITTED![/yellow]")
        input("Press Enter to continue...")


def loading_relationships() -> None:  # noqa: PLR0915
    """Illustrate loading relationships."""
    with Session(engine) as session:
        pearl = session.execute(
            select(User).filter_by(name="pearl"),
        ).scalar_one()
        input("Press Enter to continue...")
        rich.print(f"[yellow]{pearl.id=}[/yellow]")
        input("No SQL should've been submitted. Press Enter to continue...")
        rich.print(f"[yellow]{pearl.name=}[/yellow]")
        input("No SQL should've been submitted. Press Enter to continue...")
        rich.print(f"[yellow]{pearl.fullname=}[/yellow]")
        input("No SQL should've been submitted. Press Enter to continue...")
        rich.print(f"[yellow]{pearl.addresses=}[/yellow]")
        input(
            "SQL should've been submitted to load the addresses. Press Enter to continue...",  # noqa: E501
        )

        stmt = select(User.name).join(Address)
        for (name,) in session.execute(stmt):
            rich.print(f"[yellow]{name=}[/yellow]")
        input(
            "Check that ON clause was generated automatically. "
            "Press Enter to continue...",
        )

    with Session(engine) as session:
        start_time = perf_counter()
        stmt = select(User)
        users = session.execute(stmt).scalars().all()
        for user in users:
            rich.print(f"[yellow]{user.addresses=}[/yellow]")
        end_time = perf_counter()
        rich.print(
            "[yellow]Time taken to load all users: "
            f"{end_time - start_time:.6f} seconds[/yellow]",
        )
        input("Press Enter to continue...")

        start_time = perf_counter()
        stmt = select(User).options(selectinload(User.addresses))
        users = session.execute(stmt).scalars().all()
        for user in users:
            rich.print(f"[yellow]{user.addresses=}[/yellow]")
        end_time = perf_counter()
        rich.print(
            "[yellow]Time taken to load all users: "
            f"{end_time - start_time:.6f} seconds[/yellow]",
        )
        input("Press Enter to continue...")

        start_time = perf_counter()
        stmt = select(Address).options(joinedload(Address.user)).order_by(Address.id)

        for (address,) in session.execute(stmt):
            rich.print(f"[yellow]{address.email_address=}[/yellow]")
        end_time = perf_counter()
        rich.print(
            "[yellow]Time taken to load all addresses: "
            f"{end_time - start_time:.6f} seconds[/yellow]",
        )
        input("Press Enter to continue...")

        start_time = perf_counter()
        stmt = (
            select(Address)
            .options(joinedload(Address.user, innerjoin=True))
            .order_by(Address.id)
        )

        for (address,) in session.execute(stmt):
            rich.print(f"[yellow]{address.email_address=}[/yellow]")
        end_time = perf_counter()
        rich.print(
            "[yellow]Time taken to load all addresses with inner join: "
            f"{end_time - start_time:.6f} seconds[/yellow]",
        )
        input("Press Enter to continue...")

        stmt = (
            select(Address)
            .options(contains_eager(Address.user))
            .join(User)
            .where(User.name == "pearl")
        )
        for (address,) in session.execute(stmt):
            rich.print(f"[yellow]{address.email_address=}[/yellow]")
            rich.print(f"[yellow]{address.user=}[/yellow]")
        input("Press Enter to continue...")

        users = session.execute(select(UserV2)).scalars().all()
        for user in users:
            rich.print(f"[yellow]{user=}[/yellow]")
            rich.print(f"[yellow]{user.addresses=}[/yellow]")
            input("Press Enter to continue...")

        users = session.execute(select(UserV3)).scalars().all()
        for user in users:
            rich.print(f"[yellow]{user=}[/yellow]")
            try:
                rich.print(f"[yellow]{user.addresses=}[/yellow]")
            except Exception as e:  # noqa: BLE001
                rich.print(f"[red]Error: {e} ({type(e).__name__})[/red]")
            input("Press Enter to continue...")


def main() -> None:
    """Application entry point."""
    setup_tables()
    input("Tables created. Press Enter to continue...")

    insert_some_data_sql()
    input("Inserted some data using raw SQL. Press Enter to continue...")

    read_data_orm_queries()
    input("Read data using ORM queries. Press Enter to continue...")

    creating_and_persisting_objects_representing_rows()
    input("Created/persisted objects representing rows. Press Enter to continue...")

    getting_objects_from_the_session()
    input("Got objects from the session. Press Enter to continue...")

    using_bulk_insert_orm()
    input("Used bulk insert ORM. Press Enter to continue...")

    subqueries_and_ctes()
    input("Subqueries and CTEs. Press Enter to continue...")

    unions_with_orm()
    input("Unions with ORM. Press Enter to continue...")

    grokking_relationships()
    input("Grokking relationships. Press Enter to continue...")

    loading_relationships()
    input("Loading relationships. Press Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    finally:
        print("Cleaning up the database...")
        Base.metadata.drop_all(engine)
