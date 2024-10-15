"""
One-to-many association using distinct tables.
"""

from sqlalchemy import (
    Column,
    Engine,
    ForeignKey,
    String,
    Table,
    create_engine,
    select,
)
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


link_table = Table(
    "user_account_address_link",
    Base.metadata,
    Column("user_id", ForeignKey("user_account.id"), primary_key=True),
    Column("address_id", ForeignKey("address.id"), primary_key=True),
)


class User(Base):
    """ORM mapped class for user_account table."""

    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    fullname: Mapped[str | None]

    addresses: Mapped[list["Address"]] = relationship(
        secondary=link_table,
        back_populates="users",
    )

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
    email_address: Mapped[str] = mapped_column(unique=True)

    users: Mapped[list[User]] = relationship(
        secondary=link_table,
        back_populates="addresses",
    )

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

    # persistence logic with sessionless objects: user with many addresses
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

    # you can also start from Address: address with many users
    ekrabs_address = Address(
        email_address="ekrabs@example.com",
        users=[
            User(name="ekrabs", fullname="Eugene H. Krabs"),
            User(name="mrkrabs", fullname="Eugene H. Krabs"),
        ],
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
    ekrabs = ekrabs_address.users
    print(f"{ekrabs=}")

    squidward_addresses = squidward.addresses
    print(f"{squidward_addresses=}")

    # note that you cannot have the same email_address record twice on the db
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

    # but you can reference an existing record (to comply with the many-to-many)
    with Session(engine) as session:
        spongebob_first_address = (
            session.scalars(
                select(User).filter_by(name="spongebob"),
            )
            .first()
            .addresses[0]
        )
        gary = User(
            name="gary",
            fullname="Gary the Snail",
            addresses=[spongebob_first_address],
        )
        session.add(gary)
        session.commit()

    # let's check we can see that the email has actually two associated users
    with Session(engine) as session:
        spongebob_first_address = session.scalars(
            select(Address).where(
                Address.email_address == "spongebob@example.com",
            ),
        ).first()
        print(spongebob_first_address.users)

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
        users = session.scalars(stmt).first().users
        print(f"{users=}")

    # and the association is also queryable from the other end
    with Session(engine) as session:
        user = session.scalars(
            select(User).filter(
                User.addresses.any(email_address="ekrabs@example.com"),
            ),
        ).first()
        print(f"{user=}")

    # and despite having a link table, you don't need to mind it when removing
    # objects

    with Session(engine) as session:
        gary = session.scalars(select(User).filter_by(name="gary")).first()
        gary_id = gary.id
        print(f"{gary.id=}")

        # before
        with engine.connect() as conn:
            rows = conn.execute(
                select(link_table).where(link_table.c.user_id == gary_id),
            ).all()
            for row in rows:
                print(row)

        session.delete(gary)
        session.commit()

    # after
    with engine.connect() as conn:
        rows = conn.execute(
            select(link_table).where(link_table.c.user_id == gary_id),
        ).all()
        for row in rows:
            print(row)


if __name__ == "__main__":
    main()
