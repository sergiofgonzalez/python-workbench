"""Persisting and loading relationships using ORM."""

from sqlalchemy import Engine, ForeignKey, String, create_engine
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
    name: Mapped[str] = mapped_column(String(30))
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
    email_address: Mapped[str]

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
                Address(email_address="sandy.cheeks@bikinibottom.com"),
            ],
        ),
    )
    session.commit()
    session.close()


def main() -> None:
    """Application entry point."""
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    setup(engine)

    # Create a new object
    u1 = User(name="pkrabs", fullname="Pearl Krabs")
    assert u1.addresses == []

    # We can work with addresses as if it were a regular obj field
    a1 = Address(email_address="pearl.krabs@example.com")
    u1.addresses.append(a1)
    print(u1.addresses)

    # Automagically, the `Address.user` field will be synced
    # (the magic derives from the back_populates specification)
    print(a1.user)

    # This magic will also happen if we start from Address
    # (note that you don't need to manage IDs, simply object instances)
    a2 = Address(email_address="pearl@bikini.bottom.com", user=u1)
    print(u1.addresses)

    # The objects are "transient" as they haven't been added to a Session object
    # Because the objects defined above are related, adding one will trigger the
    # addition of the related ones
    session = Session(engine)
    session.add(u1)
    assert u1 in session  # expected
    assert a1 in session
    assert a2 in session

    # Because we haven't sent these objects to the db, the objects are now in
    # pending state - none of the objects feature an ID
    assert u1.id is None
    assert a1.id is None
    assert a2.id is None

    # When we commit the changes, not only those objects will be persisted,
    # but also, the INSERT statements will be generated in the correct order
    session.commit()

    # Because we've called commit, session objects in the session will go to the
    # expired state.
    # As a result, accessing them will trigger the corresponding SQL statements
    print(f"{u1.id=}")
    print(f"{a1.id=}")
    print(f"{a2.id=}")

    # Because all the objects have been persisted, I'll have my relationships
    # fully populated
    print(u1.addresses)

    # These relationships (as well as the individual properties) are
    # lazily-loaded by default, so subsequent accessed won't trigger SQL queries
    # anymore
    # (in any case, that's just an implementation aspect)
    print(u1.addresses)


if __name__ == "__main__":
    main()
