"""
One-to-one association using composite so that only one table is created.
"""

import dataclasses

from sqlalchemy import Engine, String, create_engine, select
from sqlalchemy.exc import ArgumentError, IntegrityError
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    composite,
    mapped_column,
)


@dataclasses.dataclass
class Address:
    """Python class representing an address."""

    email_address: str

    def __repr__(self) -> str:
        """Provide dev level string representation of Address."""
        return f"Address(email_address={self.email_address!r})"


class Base(DeclarativeBase):
    """Acquiring a new Declarative Base by subclassing DeclarativeBase."""


class User(Base):
    """ORM mapped class for user_account table."""

    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    fullname: Mapped[str | None]
    email: Mapped[str] = mapped_column(String, unique=True)

    address: Mapped[Address] = composite(Address, email)

    def __repr__(self) -> str:
        """Provide dev level string representation of User."""
        return (
            f"User(id={self.id!r}, name={self.name!r}, "
            f"fullname={self.fullname!r}, "
            f"address={self.address})"
        )


def setup(engine: Engine) -> None:
    """Set up the environment."""
    metadata_obj = Base.metadata
    metadata_obj.create_all(engine)
    session = Session(engine)
    session.add(
        User(
            name="spongebob",
            fullname="Spongebob Squarepants",
            email="spongebob@example.com",
        ),
    )
    session.add(
        User(
            name="sandy",
            fullname="Sandy Cheeks",
            email="sandy@example.com",
        ),
    )
    session.add(
        User(
            name="patrick",
            fullname="Patrick Star",
            address=Address(email_address="patrick@example.com"),
        ),
    )
    session.commit()
    session.close()


def main() -> None:
    """Application entry point."""
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    setup(engine)

    # persistence logic with sessionless objects
    squidward = User(
        name="squidward",
        fullname="Squidward Tentacles",
        email="squidward@example.com",
    )
    print(squidward)
    assert squidward.id is None

    # you can also use the address composite field
    ekrabs = User(
        name="ekrabs",
        fullname="Eugene H. Krabs",
        address=Address(email_address="ekrabs@example.com"),
    )
    print(ekrabs)
    assert ekrabs.id is None

    # if you use both fields with different values, the address one seems to win
    # and no error is generated
    pkrabs = User(
        name="pkrabs",
        fullname="Pearl Krabs",
        address=Address(email_address="pkrabs@example.com"),
        email="pkrabs@bikini-bottom.com",
    )
    print(pkrabs)
    assert pkrabs.id is None

    pkrabs = User(
        name="pkrabs",
        fullname="Pearl Krabs",
        email="pkrabs@bikini-bottom.com",
        address=Address(email_address="pkrabs@example.com"),
    )
    print(pkrabs)
    assert pkrabs.id is None

    # now we add it to the session and commit it
    session = Session(engine)
    session.add(squidward)
    session.add(ekrabs)
    session.add(pkrabs)
    session.commit()

    # now the objects feature an ID because it's been sent to the DB
    # this triggers a query to retrieve the ID because of the previous commit
    assert squidward.id is not None
    print(f"email={squidward.email}")
    print(f"address={squidward.address}")

    # note that we had to include `unique=True` to ensure a one-to-one
    # relationship (otherwise, same emails could've been associated to different
    # users)
    gary = User(
        name="gary",
        fullname="Gary the Snail",
        email="spongebob@example.com",
    )
    session.add(gary)
    try:
        session.commit()
    except IntegrityError as e:
        print(e)

    # selecting all users user
    with Session(engine) as session:
        stmt = select(User)
        for row in session.execute(stmt):
            print(f"row={row}")

    # casting the result of a query to an ORM entity is weird because you get
    # rows not objects
    with Session(engine) as session:
        stmt = select(User).where(User.name == "spongebob")
        row = session.execute(stmt).first()
        print(f"row={row}")
        user = row[0]
        print(f"{user=}")
        print(f"{user.email=}")
        print(f"{user.address=}")

    # a cleaner way is to use scalars() which returns the first column of each
    # row
    with Session(engine) as session:
        stmt = select(User).where(User.name == "spongebob")
        user = session.scalars(stmt).first()
        print(f"{user=}")
        print(f"{user.email=}")
        print(f"{user.address=}")

    # because address is not a real entity, but a data class embedded into the
    # User class you cannot submit queries on address
    try:
        stmt = select(Address).where(
            Address.email_address == "spongebob@example.com",
        )
    except ArgumentError as e:
        print({e})

    # and the association is also non-navigable from Address to user, but you
    # can user a query
    with Session(engine) as session:
        user = session.scalars(
            select(User).filter_by(email="pkrabs@example.com"),
        ).first()
        print(f"{user=}")


if __name__ == "__main__":
    main()
