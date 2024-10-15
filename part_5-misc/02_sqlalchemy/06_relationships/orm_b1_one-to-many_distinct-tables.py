"""
One-to-many association using distinct tables.
"""

from sqlalchemy import Engine, ForeignKey, String, create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    """Acquiring a new Declarative Base by subclassing DeclarativeBase."""


class User(Base):
    """ORM mapped class for user_account table."""

    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    fullname: Mapped[str | None]

    addresses: Mapped[list["Address"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        """Provide dev level string representation of User."""
        return (
            f"User(id={self.id!r}, name={self.name!r}, "
            f"fullname={self.fullname!r})"
        )


class Address(Base):
    """ORM mapped class for address table."""

    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user_account.id"))
    email_address: Mapped[str] = mapped_column(unique=True)

    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        """Provide dev level string representation of Address."""
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


def setup(engine: Engine) -> None:
    """Set up the environment."""
    metadata_obj = Base.metadata
    metadata_obj.create_all(engine)
    session = Session(engine)
    session.add(
        User(
            name="spongebob",
            fullname="Spongebob Squarepants",
            addresses=[Address(email_address="spongebob@example.com")],
        ),
    )
    session.add(
        User(
            name="sandy",
            fullname="Sandy Cheeks",
            addresses=[
                Address(email_address="sandy@example.com"),
                Address(email_address="sandy@bikini-bottom.com"),
            ],
        ),
    )
    session.add(
        User(
            name="patrick",
            fullname="Patrick Star",
            addresses=[
                Address(email_address="patrick@example.com"),
                Address(email_address="patrick@bikini-bottom.com"),
                Address(email_address="patrick.star@example.com"),
            ],
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
        addresses=[
            Address(email_address="squidward@example.com"),
            Address(email_address="squidward@bikini-bottom.com"),
        ],
    )
    print(squidward)
    assert squidward.id is None

    # you can also start from Address
    ekrabs_address = Address(
        email_address="ekrabs@example.com",
        user=User(name="ekrabs", fullname="Eugene H. Krabs"),
    )
    print(ekrabs_address)
    assert ekrabs_address.id is None

    # now we add it to the session and commit it
    session = Session(engine)
    session.add(squidward)
    session.add(ekrabs_address)
    session.commit()

    # now the objects feature an ID because it's been sent to the DB
    # this triggers a query to retrieve the ID because of the previous commit
    assert squidward.id is not None
    print(f"addresses={squidward.addresses}")

    # because mapped classes are navigable in both directions we can do
    ekrabs = ekrabs_address.user
    print(f"{ekrabs=}")

    squidward_addresses = squidward.addresses
    print(f"{squidward_addresses=}")

    # note that you cannot have the same email_address on the db
    with Session(engine) as session:
        gary = User(
            name="gary",
            fullname="Gary the Snail",
            addresses=[Address(email_address="spongebob@example.com")],
        )
        session.add(gary)
        try:
            session.commit()
        except IntegrityError as e:
            print(e)

    # and neither the same user twice
    with Session(engine) as session:
        spongie = User(
            name="spongebob",
            fullname="Spongiebob",
            addresses=[Address(email_address="spongiebob@example.com")],
        )
        session.add(spongie)
        try:
            session.commit()
        except IntegrityError as e:
            print(e)

    # selecting all users
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
        print(f"{user.addresses=}")

    # a cleaner way is to use scalars() which returns the first column of each
    # row
    with Session(engine) as session:
        stmt = select(User).where(User.name == "spongebob")
        user = session.scalars(stmt).first()
        print(f"{user=}")
        print(f"{user.addresses=}")

    # you can submit queries on Address
    with Session(engine) as session:
        stmt = select(Address).where(
            Address.email_address == "spongebob@example.com",
        )
        user = session.scalars(stmt).first().user
        print(f"{user=}")

    # and the association is also queryable from the other end
    with Session(engine) as session:
        user = session.scalars(
            select(User).filter(
                User.addresses.any(email_address="ekrabs@example.com"),
            ),
        ).first()
        print(f"{user=}")


if __name__ == "__main__":
    main()
