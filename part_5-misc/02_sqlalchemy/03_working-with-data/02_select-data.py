"""Selecting data using Core."""

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    and_,
    bindparam,
    create_engine,
    desc,
    func,
    insert,
    literal_column,
    or_,
    select,
    text,
    union_all,
)
from sqlalchemy.dialects import oracle, postgresql


def main() -> None:
    """Application entry point."""
    # setup the environment
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    metadata_obj = MetaData()

    user_table = Table(
        "user_account",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("name", String(30)),
        Column("fullname", String),
    )

    address_table = Table(
        "address",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("user_id", ForeignKey("user_account.id"), nullable=False),
        Column("email_address", String, nullable=False),
    )

    metadata_obj.create_all(engine)

    with engine.connect() as conn:
        result = conn.execute(
            insert(user_table),
            [
                {"name": "spongebob", "fullname": "Spongebob Squarepants"},
                {"name": "sandy", "fullname": "Sandy Cheeks"},
                {"name": "patrick", "fullname": "Patrick Star"},
            ],
        )
        scalar_subquery = (
            select(user_table.c.id)
            .where(user_table.c.name == bindparam("username"))
            .scalar_subquery()
        )
        conn.commit()

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

    # selecting data
    stmt = select(user_table).where(user_table.c.name == "spongebob")
    print(stmt)
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(row)

    # selecting specific columns
    stmt = select(user_table.c.name, user_table.c.fullname)
    print(stmt)

    # alternative syntax to select only specific columns
    stmt = select(user_table.c["name", "fullname"])
    print(stmt)

    # selecting from labeled SQL Expressions
    stmt = select(
        ("Username: " + user_table.c.name).label("username"),
    ).order_by(user_table.c.name)

    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(f"{row.username}")

    # selecting with textual column expression
    stmt = select(text("'some text'"), user_table.c.name).order_by(
        user_table.c.name,
    )
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(row)

    # literal column is similar
    stmt = select(
        literal_column("'some text representing a col'").label("p"),
        user_table.c.name,
    ).order_by(
        user_table.c.name,
    )
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(f"p={row.p}, name={row.name}")

    # simple where clause
    print(user_table.c.name == "squidward")
    print(address_table.c.user_id > 10)

    print(select(user_table).where(user_table.c.name == "squidward"))

    # to produce expressions joined by AND use where() multiple times
    print(
        select(address_table.c.email_address)
        .where(user_table.c.name == "squidward")
        .where(address_table.c.user_id == user_table.c.id),
    )

    # alternatively to produce expressions joing by AND, you can simply pass
    # multiple expressions to where()
    print(
        select(address_table.c.email_address).where(
            user_table.c.name == "squidward",
            address_table.c.user_id == user_table.c.id,
        ),
    )

    # when creating complex WHERE clauses you can rely on and_() and or_()
    # functions
    print(
        select(address_table.c.email_address).where(
            and_(
                or_(
                    user_table.c.name == "squidward",
                    user_table.c.name == "sandy",
                ),
                address_table.c.user_id == user_table.c.id,
            ),
        ),
    )

    # filter_by() is similar. It accepts keyword arguments that match column
    # keys. It will filter against the leftmost FROM clause or the last entity
    # joined.
    print(
        select(user_table).filter_by(
            name="spongebob",
            fullname="Spongebob Squarepants",
        ),
    )

    # joins: usually, the FROM clause is inferred
    print(select(user_table.c.name))

    # when referring two tables, we get a comma separated FROM clause
    print(select(user_table.c.name, address_table.c.email_address))

    # in order to join you can use `Select.join_from()`
    print(
        select(user_table.c.name, address_table.c.email_address).join_from(
            user_table,
            address_table,
        ),
    )

    # alternatively you can use `Select.join()` which needs the right side of
    # the JOIN and the left is inferred
    print(
        select(user_table.c.name, address_table.c.email_address).join(
            user_table,
        ),
    )

    # while the FROM and ON clauses are inferred, you can use
    # `Select.select.from()` if the inferred statement is not the one we want
    print(
        select(
            address_table.c.email_address,
        )
        .select_from(user_table)
        .join(address_table),
    )

    # sometimes `Select.select_from()` is required because it cannot be inferred
    print(select(func.count("*")).select_from(user_table))

    # similarly in joins, we might need to explicitly tell how the ON clause
    # should be built
    print(
        select(address_table.c.email_address)
        .select_from(user_table)
        .join(address_table, user_table.c.id == address_table.c.user_id)
    )

    # if you need a particular type of join (LEFT OUTER, FULL JOIN...)
    # you can use the following
    print(select(user_table).join(address_table, isouter=True))
    print(select(user_table).join(address_table, full=True))

    # ORDER BY
    print(select(user_table).order_by(user_table.c.name))
    print(select(user_table).order_by(user_table.c.name.asc()))
    print(select(user_table).order_by(user_table.c.name.desc()))

    # Aggregate functions with GROUP BY / HAVING
    # functions to be used in aggregate look like the following
    count_fn = func.count(user_table.c.id)
    print(count_fn)

    with engine.connect() as conn:
        # find users with more than one email
        result = conn.execute(
            select(
                user_table.c.name,
                func.count(address_table.c.id).label("count"),
            )
            .join(address_table)
            .group_by(user_table.c.name)
            .having(func.count(address_table.c.id) > 1),
        )
        print(result.all())

    # GROUP BY / ORDER BY using labels
    with engine.connect() as conn:
        # find users with more than one email
        result = conn.execute(
            select(
                address_table.c.user_id,
                func.count(address_table.c.id).label("num_addresses"),
            )
            .group_by("user_id")
            .order_by("user_id", desc("num_addresses")),
        )
        print(result.all())

    # using aliases when you need to refer to the same table multiple times
    user_alias_1 = user_table.alias()
    user_alias_2 = user_table.alias()
    print(
        select(user_alias_1.c.name, user_alias_2.c.name).join_from(
            user_alias_1,
            user_alias_2,
            user_alias_1.c.id > user_alias_2.c.id,
        ),
    )

    # subqueries: used when you have a SELECT stement rendered within
    # parenthesis and placed within the context of an enclosing statement
    # (SELECT or other)
    subq = (
        select(
            func.count(address_table.c.id).label("count"),
            address_table.c.user_id,
        )
        .group_by(address_table.c.user_id)
        .subquery()
    )
    print(subq)

    print(select(subq.c.user_id, subq.c.count))

    stmt = select(
        user_table.c.name,
        user_table.c.fullname,
        subq.c.count,
    ).join_from(user_table, subq)
    print(stmt)

    # UNION ALL
    stmt1 = select(user_table).where(user_table.c.name == "sandy")
    stmt2 = select(user_table).where(user_table.c.name == "spongebob")
    u = union_all(stmt1, stmt2)

    with engine.connect() as conn:
        result = conn.execute(u)
        print(result.all())

    # EXISTS
    subq = (
        select(func.count(address_table.c.id))
        .where(user_table.c.id == address_table.c.user_id)
        .group_by(address_table.c.user_id)
        .having(func.count(address_table.c.id) > 1)
    ).exists()

    with engine.connect() as conn:
        result = conn.execute(select(user_table.c.name).where(subq))
        print(result.all())

    # NOT EXISTS
    subq = (
        select(address_table.c.id)
        .where(user_table.c.id == address_table.c.user_id)
        .exists()
    )
    with engine.connect() as conn:
        result = conn.execute(select(user_table.c.name).where(~subq))
        print(result.all())

    # functions: COUNT(), LOWER(), CURRENT_TIMESTAMP(), ...
    print(select(func.count()).select_from(user_table))

    print(select(func.lower("Hello, world!")))
    stmt = select(func.now())
    with engine.connect() as conn:
        result = conn.execute(stmt)
        print(result.all())

    print(select(func.now()).compile(dialect=postgresql.dialect()))
    print(select(func.now()).compile(dialect=oracle.dialect()))


if __name__ == "__main__":
    main()
