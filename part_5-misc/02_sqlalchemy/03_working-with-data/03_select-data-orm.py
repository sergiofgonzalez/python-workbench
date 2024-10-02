"""Selecting data using Core."""

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    and_,
    bindparam,
    create_engine,
    func,
    insert,
    or_,
    select,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    aliased,
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
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


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

    ## This is part of a more advanced tutorial, but it didn't populated the
    ## Address table
    # with Session(engine) as session:
    #     session.execute(
    #         insert(User),
    #         [
    #             {
    #                 "name": "spongebob",
    #                 "fullname": "Spongebob Squarepants",
    #                 "addresses": ["spongebob@example.com"],  # no effect
    #             },
    #             {
    #                 "name": "sandy",
    #                 "fullname": "Sandy Cheeks",
    #                 "addresses": [
    #                     "sandy@example.com",  # no effect
    #                     "sandy.cheeks@example.com",  # no effect
    #                 ],
    #             },
    #         ],
    #     )
    #     session.commit()
    user_table = User.__table__

    address_table = Address.__table__

    with engine.connect() as conn:
        result = conn.execute(
            insert(user_table),
            [
                {"name": "spongebob", "fullname": "Spongebob Squarepants"},
                {"name": "sandy", "fullname": "Sandy Cheeks"},
                {"name": "patrick", "fullname": "Patrick Star"},
            ],
        )
        conn.commit()

    # a bit of deep alchemy to populate the related user and addresses
    scalar_subquery = (
        select(user_table.c.id)
        .where(user_table.c.name == bindparam("username"))
        .scalar_subquery()
    )

    with engine.connect() as conn:
        result = conn.execute(
            insert(address_table).values(user_id=scalar_subquery),
            [
                {
                    "username": "spongebob",
                    "email_address": "spongebob@example.com",
                },
                {"username": "sandy", "email_address": "sandy@example.com"},
                {
                    "username": "sandy",
                    "email_address": "sandy.cheeks@example.com",
                },
            ],
        )
        conn.commit()

    # selecting against ORM entities
    with Session(engine) as session:
        stmt = select(User).where(User.name == "spongebob")
        for row in session.execute(stmt):
            print(f"row={row}")

    # selecting the first row, which is a ORM entity
    with Session(engine) as session:
        row = session.execute(select(User)).first()
        user = row[0]
        print(f"user={user}")
        print(user.addresses)  # note that addresses is populated

    # Session.scalars() return the first colum of each row
    with Session(engine) as session:
        user = session.scalars(select(User)).first()
        print(f"user={user}")

    # Individual columns can be selected using the fields of the mapped class
    with Session(engine) as session:
        print(select(User.name, User.fullname))
        row = session.execute(select(User.name, User.fullname)).first()
        print(f"row={row}")

    with Session(engine) as session:
        result = session.execute(
            select(User.name, Address)
            .where(User.id == Address.user_id)
            .order_by(Address.id),
        ).all()
        # Patrick doesn't have an email, so it' won't be in the result set
        print(result)

    # using complex where clauses with `and_()` and `or_()`
    print(
        select(Address.email_address).where(
            and_(
                or_(
                    User.name == "squidward",
                    User.name == "sandy",
                ),
                User.id == User.id,
            ),
        ),
    )

    # filter_by() is similar to where. It accepts keyword arguments that match
    # column keys. It will filter against the leftmost FROM clause or the last
    # entity joined.
    print(
        select(User).filter_by(
            name="spongebob",
            fullname="Spongebob Squarepants",
        ),
    )

    # ORDER BY using asc() and desc() on the columns
    print(select(User).order_by(User.fullname))
    print(select(User).order_by(User.fullname.asc()))
    print(select(User).order_by(User.fullname.desc()))

    # GROUP BY / HAVING
    with Session(engine) as session:
        # find users with more than one email
        result = session.execute(
            select(
                user_table.c.name,
                func.count(Address.id).label("count"),
            )
            .join(address_table)
            .group_by(User.name)
            .having(func.count(Address.id) > 1),
        )
        print(result.all())

    # ORM Entity Aliases
    address_alias_1 = aliased(Address)
    address_alias_2 = aliased(Address)

    print(
        select(User)
        .join_from(User, address_alias_1)
        .where(address_alias_1.email_address == "patrick@example.com")
        .join_from(User, address_alias_2)
        .where(address_alias_2.email_address == "patrick.star@example.com"),
    )


if __name__ == "__main__":
    main()
