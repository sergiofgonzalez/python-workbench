"""Updating objects using ORM."""

from sqlalchemy import ForeignKey, String, create_engine, select
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

    # The first way to update an object is to emit the update as part of the
    # unit of work (uow)
    session = Session(engine)
    sandy = session.execute(
        select(User).filter_by(name="sandy"),
    ).scalar_one()

    # the returned object is a proxy for the row in the db for the current
    # transaction
    sandy.fullname = "Sandy Squirrel"

    # once the object has been modified the state of the Session is aware that
    # flush is needed
    assert sandy in session.dirty

    # The value will be sent to the db automatically before the next select
    # (the logs will show an UPDATE statement)
    sandy_fullname = session.execute(
        select(User.fullname).where(User.name == "sandy"),
    ).scalar_one()
    print(sandy_fullname)

    # and now the object is no longer in "pending" state
    assert sandy not in session.dirty

    # Sesion should be closed once you're done with it.
    # Typically, the context manager will take care of that, but in
    # this example that's not the case so:
    session.close()


if __name__ == "__main__":
    main()
