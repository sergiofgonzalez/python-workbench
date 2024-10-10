"""Dealing with relationships in queries when using ORM."""

from sqlalchemy import Engine, ForeignKey, String, create_engine, select
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
    session.add(
        User(
            name="pkrabs",
            fullname="Pearl Krabs",
            addresses=[
                Address(email_address="pearl.krabs@example.com"),
                Address(email_address="pearl@bikinibottom.com"),
            ],
        ),
    )
    session.commit()
    session.close()


def main() -> None:
    """Application entry point."""
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    setup(engine)

    # When selecting entities, we can make use of the relationship() constructs
    # to help us set up the ON clause of a join
    print(select(Address.email_address).select_from(User).join(User.addresses))

    # The following triggers the same query
    print(
        select(Address.email_address).join_from(User, Address),
    )


if __name__ == "__main__":
    main()
