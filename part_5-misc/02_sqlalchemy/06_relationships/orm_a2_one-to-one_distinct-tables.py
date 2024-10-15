"""
One-to-one bidirectional association using distinct tables.
"""

from sqlalchemy import Engine, ForeignKey, String, create_engine, insert, select
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

    address: Mapped["Address"] = relationship(back_populates="user")

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
    user_id = mapped_column(ForeignKey("user_account.id"), unique=True)
    email_address: Mapped[str] = mapped_column(unique=True)

    user: Mapped[User] = relationship(back_populates="address")

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
            address=Address(email_address="spongebob@example.com"),
        ),
    )
    session.add(
        User(
            name="sandy",
            fullname="Sandy Cheeks",
            address=Address(email_address="sandy@example.com"),
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
        address=Address(email_address="squidward@example.com"),
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
    print(f"address={squidward.address}")

    # because mapped classes are navigable in both directions we can do
    ekrabs = ekrabs_address.user
    print(f"{ekrabs=}")

    squidward_address = squidward.address
    print(f"{squidward_address=}")

    # note that we had to include `unique=True` in both mapped classes to ensure
    # a one-to-one relationship (otherwise, same emails could've been associated
    # to the same user and vice versa)
    with Session(engine) as session:
        gary = User(
            name="gary",
            fullname="Gary the Snail",
            address=Address(email_address="spongebob@example.com"),
        )
        session.add(gary)
        try:
            session.commit()
        except IntegrityError as e:
            print(e)

    with Session(engine) as session:
        spongie = User(
            name="spongebob",
            fullname="Spongiebob",
            address=Address(email_address="spongiebob@example.com"),
        )
        session.add(spongie)
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
        print(f"{user.address=}")

    # a cleaner way is to use scalars() which returns the first column of each
    # row
    with Session(engine) as session:
        stmt = select(User).where(User.name == "spongebob")
        user = session.scalars(stmt).first()
        print(f"{user=}")
        print(f"{user.address=}")

    # because address is a real entity you can submit queries on Address
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
                User.address.has(email_address="ekrabs@example.com"),
            ),
        ).first()
        print(f"{user=}")

    # using distinct tables for one-to-one looks very similar to one-to-many
    # with respect to the created tables - let's make sure the tables maintain
    # a one-to-one and do not support a one-to-many
    # (note: we switch to core)
    user_table = User.__table__
    address_table = Address.__table__

    # try to insert a second email for spongebob
    with engine.connect() as conn:
        row_spongebob = conn.execute(
            select(user_table).where(user_table.c.name == "spongebob"),
        ).first()
        try:
            conn.execute(
                insert(address_table),
                [
                    {
                        "user_id": row_spongebob.id,
                        "email_address": "spongebob@bikini-bottom.com",
                    },
                ],
            )
            conn.commit()
        except IntegrityError as e:
            print({e})

    # retrieve the emails associated to spongebob
    with engine.connect() as conn:
        rows = conn.execute(
            select(address_table).where(
                address_table.c.user_id == row_spongebob.id,
            ),
        ).all()
        for row in rows:
            print(row)


if __name__ == "__main__":
    main()
