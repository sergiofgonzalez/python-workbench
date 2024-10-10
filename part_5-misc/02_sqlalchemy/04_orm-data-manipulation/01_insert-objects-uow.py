"""Inserting objects using ORM."""

from sqlalchemy import ForeignKey, String, create_engine
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


def main() -> None:
    """Application entry point."""
    # setup the environment
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    metadata_obj = Base.metadata
    metadata_obj.create_all(engine)

    # instances of mapped classes represent rows in the db
    squidward = User(name="squidward", fullname="Squidward Tentacles")
    krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")
    print(squidward)

    # adding objects to a session
    # at these point, the objects are said to be in a state called "transient"
    # they are not associated with any database state.
    session = Session(engine)
    session.add(squidward)
    session.add(krabs)

    # once added to a session they're said to be in "pending" state, meaning
    # they're not transient, but haven't been inserted into the db yet
    print(session.new)

    # the session follows the unit of work pattern. As such, it accumulates
    # changes one at a time but does not send them to the db until needed.
    # This communication happens in a process known "flush".
    session.flush()

    # This creates a new transaction that will remain open until
    # Session.commit(), Session.rollback(), or Session.close() are called.
    # Once the objects have been inserted, they will be given their primary
    # key attributes:
    print(squidward.id)
    print(krabs.id)

    # Objects can be retrieved from the session using Session.get()
    obj_1 = session.get(User, 1)
    print(obj_1)
    assert obj_1 is squidward

    # Note that the object hasn't been committed yet until you call commit()
    # on the session
    session.commit()

    # Sesion should be closed once you're done with it.
    # Typically, the context manager will take care of that, but in
    # this example that's not the case so:
    session.close()


if __name__ == "__main__":
    main()
