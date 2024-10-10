"""Loading strategies when using ORM."""

from sqlalchemy import Engine, ForeignKey, String, create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    contains_eager,
    joinedload,
    mapped_column,
    relationship,
    selectinload,
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

    # Loading strategies (in particular lazy loading) is always controversial
    # when using ORMs as a multitude of queries can be trigger implicitly behind
    # the scenes when accessing an object's property (e.g., when it has been
    # committed).
    # It can also cause some problems when the transaction has been closed, or
    # when dealing with concurrency patterns.
    # To make sure you're dealing with lazy loading effectively, test the
    # application with SQL echoing set to True and analyze the logs to detect if
    # there's anything that could be improved (e.g., accessing detached objects
    # that are triggering SQL queries).
    # If needed, fine-tune the loading strategies via Select.options()
    session = Session(engine)
    for user_obj in session.execute(
        select(User).options(selectinload(User.addresses)),
    ).scalars():
        print(user_obj.addresses)

    # selectinload() is the most useful loader in modern SQLAlchemy.
    stmt = select(User).options(selectinload(User.addresses)).order_by(User.id)
    for row in session.execute(stmt):
        print(
            f"{row.User.name} ({', '.join(a.email_address for a in row.User.addresses)})"
        )

    # Somehow syntax is easier with scalars
    for user in session.execute(stmt).scalars():
        print(
            f"{user.name} ({', '.join(a.email_address for a in user.addresses)})"
        )

    # The joinedLoad() eager load strategy is the oldest eager loader in
    # SQLAlchemy and well suited for loading many-to-one objects.
    stmt = (
        select(Address)
        .options(joinedload(Address.user, innerjoin=True))
        .order_by(Address.id)
    )
    for row in session.execute(stmt):
        print(f"{row.Address.email_address} {row.Address.user.name}")

    # contains_eager() is similar to joinedload() but you have to set up the
    # JOIN ourselves
    stmt = (
        select(Address)
        .join(Address.user)
        .where(User.name == "pkrabs")
        .options(contains_eager(Address.user))
        .order_by(Address.id)
    )
    for row in session.execute(stmt):
        print(f"{row.Address.email_address} {row.Address.user.name}")


    # raiseload() is used to prevent an application from having the N+1 problem
    # by raising an error when that would occur.
    # It can be configured to raise an error to block all load operations, or
    # only the ones that will cause an N+1 problem



if __name__ == "__main__":
    main()
