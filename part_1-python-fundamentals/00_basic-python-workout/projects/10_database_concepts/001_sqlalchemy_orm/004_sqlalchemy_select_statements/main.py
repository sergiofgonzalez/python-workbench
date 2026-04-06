"""Basics of SELECT statement in SQLALchemy."""

import rich
from sqlalchemy import (
    JSON,
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    and_,
    bindparam,
    cast,
    create_engine,
    exists,
    func,
    insert,
    literal_column,
    or_,
    select,
    text,
    type_coerce,
)

metadata_obj = MetaData()
engine = create_engine("sqlite+pysqlite:///app.db", echo=True)


def setup_db() -> None:
    """Create tables in the database."""
    user_table = Table(
        "user_account",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("name", String(30), nullable=False),
        Column("fullname", String),
    )

    address_table = Table(
        "address",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("email_address", String, nullable=False),
        Column("user_id", Integer, ForeignKey("user_account.id"), nullable=False),
    )

    spanish_table = Table(
        "num_esp",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("desc", String(30), nullable=False),
    )

    english_table = Table(
        "num_eng",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("desc", String(30), nullable=False),
    )

    metadata_obj.create_all(engine)

    with engine.begin() as conn:
        conn.execute(
            insert(user_table).values(
                [
                    {"name": "spongebob", "fullname": "Spongebob Squarepants"},
                    {"name": "patrick", "fullname": "Patrick Star"},
                    {"name": "sandy", "fullname": "Sandy Cheeks"},
                    {"name": "squidward", "fullname": "Squidward Tentacles"},
                    {"name": "gary", "fullname": "Gary the Snail"},
                    {"name": "mrkrabs", "fullname": "Eugene H. Krabs"},
                    {"name": "pearl", "fullname": "Pearl Krabs"},
                ],
            ),
        )

        scalar_subquery_stmt = (
            select(user_table.c.id)
            .where(user_table.c.name == bindparam("username"))
            .scalar_subquery()
        )

        conn.execute(
            insert(address_table).values(user_id=scalar_subquery_stmt),
            [
                {"email_address": "spongebob@example.com", "username": "spongebob"},
                {"email_address": "sandy@example.com", "username": "sandy"},
                {"email_address": "squidward@example.com", "username": "squidward"},
                {"email_address": "pearl@example.com", "username": "pearl"},
                {"email_address": "pearl@foo.com", "username": "pearl"},
                {"email_address": "sandy@bar.com", "username": "sandy"},
            ],
        )

    with engine.begin() as conn:
        conn.execute(
            insert(spanish_table).values(
                [
                    {"desc": "uno"},
                    {"desc": "dos"},
                    {"desc": "tres"},
                ],
            ),
        )

        conn.execute(
            insert(english_table).values(
                [
                    {"id": 1, "desc": "one"},
                    {"id": 2, "desc": "two"},
                    {"id": 4, "desc": "four"},
                ],
            ),
        )


def simple_select() -> None:
    """Simple SELECTs labs."""
    user_table = metadata_obj.tables["user_account"]
    address_table = metadata_obj.tables["address"]

    # SELECT * FROM user_account
    stmt = select(user_table)
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(row)

    # SELECT * FROM user_account WHERE name = 'spongebob'
    stmt = select(user_table).where(user_table.c.name == "spongebob")
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(row)

    # SELECT name, fullname FROM user_account WHERE name = 'spongebob'
    stmt = select(user_table.c.name, user_table.c.fullname).where(
        user_table.c.name == "spongebob",
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.name=}, {row.fullname=}")

    # SELECT name, fullname FROM user_account WHERE name = 'spongebob'
    # using an alternative syntax
    stmt = select(user_table.c["name", "fullname"]).where(  # ty:ignore[no-matching-overload]
        user_table.c.name == "spongebob",
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.name=}, {row.fullname=}")

    # Dynamically selecting the columns to be selected
    columns_to_select = [
        {"colname": "id", "selected": False},
        {"colname": "user_id", "selected": False},
        {"colname": "email_address", "selected": False},
    ]
    for column in columns_to_select:
        user_input = input(
            f"Do you want to select the column {column['colname']}? (y/n): ",
        )
        column["selected"] = user_input.lower() == "y"

    selected_column_names = [
        column["colname"] for column in columns_to_select if column["selected"]
    ]

    stmt = select(address_table.c[*selected_column_names]).where(  # ty:ignore[no-matching-overload]
        address_table.c.email_address == "spongebob@example.com",
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row=}")

    # Dynamically selecting the columns to be selected
    # Achieving the same result using the regular syntax instead of [*] unpacking syntax
    columns_to_select = [
        {"colname": "address_id", "column": address_table.c.id, "selected": False},
        {"colname": "user_id", "column": address_table.c.user_id, "selected": False},
        {
            "colname": "email_address",
            "column": address_table.c.email_address,
            "selected": False,
        },
    ]
    for column in columns_to_select:
        user_input = input(
            f"Do you want to select the column {column['colname']}? (y/n): ",
        )
        column["selected"] = user_input.lower() == "y"

    selected_column_names = [
        column["colname"] for column in columns_to_select if column["selected"]
    ]

    stmt = select(
        *[column["column"] for column in columns_to_select if column["selected"]],
    ).where(  # ty:ignore[no-matching-overload]
        address_table.c.email_address == "spongebob@example.com",
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row=}")


def getting_results() -> None:
    """Getting the results using first(), all(), scalars() methods."""
    user_table = metadata_obj.tables["user_account"]

    # Selecting all the rows from the user_account table
    with engine.connect() as conn:
        rows = conn.execute(select(user_table)).all()
        rich.print(f"[yellow]{rows}[/yellow]")
        rich.print(
            f"[yellow]{type(rows)=}; {type(rows[0])=}[/yellow]",
        )
    input("Press Enter to continue...")

    # Selecting all the rows from the user_account table
    with engine.connect() as conn:
        row = conn.execute(select(user_table)).first()
        rich.print(f"[yellow]{rows}[/yellow]")
        rich.print(
            f"[yellow]{type(row)=}[/yellow]",
        )
    input("Press Enter to continue...")


def ordering_results() -> None:
    """Ordering the results using order_by() method."""
    user_table = metadata_obj.tables["user_account"]
    address_table = metadata_obj.tables["address"]

    stmt = (
        select(user_table.c.name, address_table)
        .where(user_table.c.id == address_table.c.user_id)
        .order_by(address_table.c.id)
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(row)


def using_label() -> None:
    """Using label() to label the columns in the result set."""
    user_table = metadata_obj.tables["user_account"]

    stmt = select(
        ("Username: " + user_table.c.name).label("username"),
    ).order_by(user_table.c.name)
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.username=}")


def using_text() -> None:
    """Using text() to write raw SQL queries."""
    user_table = metadata_obj.tables["user_account"]

    stmt = select(
        text("'some text'"),
        user_table.c.name,
    ).order_by(user_table.c.name)
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row=}")


def using_literal_column() -> None:
    """Using literal_column() to write raw SQL queries."""
    user_table = metadata_obj.tables["user_account"]

    stmt = select(
        literal_column("'some text'").label("p"),
        user_table.c.name,
    ).order_by(user_table.c.name)
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.p=}, {row.name=}")


def using_where_and_or() -> None:
    """Using where(), and_(), or_() methods to build complex WHERE clauses."""
    user_table = metadata_obj.tables["user_account"]
    address_table = metadata_obj.tables["address"]

    # simple WHERE clause
    stmt = select(user_table).where(user_table.c.name == "squidward")
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row=}")

    # another simple WHERE clause
    stmt = select(user_table).where(user_table.c.id >= 5)  # noqa: PLR2004
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row=}")

    # using multiple where() to model AND conditions in a WHERE clause
    stmt = (
        select(address_table.c.email_address)
        .where(user_table.c.name == "squidward")
        .where(user_table.c.id == address_table.c.user_id)
    )

    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.email_address=}")

    # using single where() with two arguments to model AND conditions in a WHERE clause
    stmt = select(address_table.c.email_address).where(
        user_table.c.name == "squidward",
        user_table.c.id == address_table.c.user_id,
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.email_address=}")

    # using and_() and or_() functions to model complex conditions in a WHERE clause
    stmt = select(address_table.c.email_address).where(
        and_(
            or_(
                user_table.c.name == "squidward",
                user_table.c.name == "sandy",
            ),
            user_table.c.id == address_table.c.user_id,
        ),
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.email_address=}")


def using_filter_by() -> None:
    """Using filter_by() method to build simple WHERE clauses."""
    user_table = metadata_obj.tables["user_account"]

    stmt = select(user_table).filter_by(
        name="spongebob",
        fullname="Spongebob Squarepants",
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row=}")


def using_joins_and_explicit_from() -> None:
    """Using join_from(), join(), select_from() to write JOINs and explicit FROMs."""
    user_table = metadata_obj.tables["user_account"]
    address_table = metadata_obj.tables["address"]

    # in general there's no need to use FROM
    stmt = select(user_table, address_table)
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row=}")

    # you can specify specific columns to retrieve from the tables
    stmt = select(user_table.c.name, address_table.c.email_address)
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.name=} {row.email_address=}")

    # you can use join_from() to make it more explicit
    stmt = select(user_table.c.name, address_table.c.email_address).join_from(
        user_table,
        address_table,
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.name=} {row.email_address=}")

    # join() infers the left table from the columns being selected, so you can
    # skip the first argument to join() if the left table can be inferred
    stmt = select(user_table.c.name, address_table.c.email_address).join(
        address_table,
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.name=} {row.email_address=}")

    # select_from() can be used to specify the FROM clause explicitly
    # which is required in certain situations like when you count records
    stmt = select(func.count("*")).select_from(user_table)
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row=}")

    # explicit ON clause in JOINs
    stmt = select(address_table.c.email_address).join(
        user_table,
        address_table.c.user_id == user_table.c.id,
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.email_address=}")


def exploring_joins() -> None:  # noqa: PLR0915
    """Exploring different types of JOINs."""
    num_esp = metadata_obj.tables["num_esp"]
    num_eng = metadata_obj.tables["num_eng"]
    user_table = metadata_obj.tables["user_account"]
    address_table = metadata_obj.tables["address"]

    # INNER JOIN (default JOIN)
    stmt = select(num_esp, num_eng).join(
        num_eng,
        num_esp.c.id == num_eng.c.id,
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row=}")

    # LEFT OUTER JOIN
    stmt = select(num_esp, num_eng).join(
        num_eng,
        num_esp.c.id == num_eng.c.id,
        isouter=True,
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row=}")

    # RIGHT OUTER JOIN is a reversed (i.e., swapping the tables) LEFT OUTER JOIN
    stmt = select(num_eng, num_esp).join(
        num_esp,
        num_eng.c.id == num_esp.c.id,
        isouter=True,
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row=}")

    # FULL OUTER JOIN is a reversed (i.e., swapping the tables) LEFT OUTER JOIN
    stmt = select(num_esp, num_eng).join(
        num_eng,
        num_esp.c.id == num_eng.c.id,
        full=True,
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row=}")

    # INNER JOIN: getting all the users and their email addresses
    stmt = select(user_table.c.name, address_table.c.email_address).join(
        address_table,
        user_table.c.id == address_table.c.user_id,
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.name=} {row.email_address=}")

    # LEFT OUTER JOIN: getting all the users and their email addresses
    # (if they have one)
    stmt = select(user_table.c.name, address_table.c.email_address).join(
        address_table,
        user_table.c.id == address_table.c.user_id,
        isouter=True,
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.name=} {row.email_address=}")

    # FULL OUTER JOIN
    stmt = select(user_table.c.name, address_table.c.email_address).join(
        address_table,
        user_table.c.id == address_table.c.user_id,
        full=True,
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.name=} {row.email_address=}")

    # Alternative syntax for FULL OUTER JOIN
    stmt = select(user_table.c.name, address_table.c.email_address).outerjoin(
        address_table,
        user_table.c.id == address_table.c.user_id,
        full=True,
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.name=} {row.email_address=}")


def exploring_order_by() -> None:
    """Exploring different ways to use ORDER BY."""
    user_table = metadata_obj.tables["user_account"]

    # ordering by a single column in ascending order
    stmt = select(user_table).order_by(user_table.c.name)
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row=}")

    # ordering by a single column in descending order
    stmt = select(user_table).order_by(user_table.c.name.desc())
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row=}")

    # ordering by a single column in ascending order (explicitly)
    stmt = select(user_table).order_by(user_table.c.name.asc())
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row=}")

    # ordering by multiple columns
    stmt = select(user_table).order_by(
        user_table.c.name,
        user_table.c.fullname.desc(),
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row=}")


def using_group_by_and_having() -> None:
    """Using group_by() and having() methods."""
    user_table = metadata_obj.tables["user_account"]
    address_table = metadata_obj.tables["address"]

    # Count the number of users in the user_account table using select_from()
    subq = select(func.count(user_table.c.id))
    rich.print(f"[yellow]{subq}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(subq)
        for row in result:
            rich.print(f"{row=}")

    # Count the number of email addresses for each user using group_by()
    stmt = (
        select(
            user_table.c.name,
            func.count(address_table.c.id).label("address_count"),
        )
        .join(address_table, user_table.c.id == address_table.c.user_id, isouter=True)
        .group_by(user_table.c.name)
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.name=} {row.address_count=}")
    print()

    # Count the number of users having more than 1 email address using group_by()
    # and having()
    stmt = (
        select(
            user_table.c.name,
            func.count(address_table.c.id).label("address_count"),
        )
        .join(address_table, user_table.c.id == address_table.c.user_id, isouter=True)
        .group_by(user_table.c.name)
        .having(func.count(address_table.c.id) > 1)
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.name=} {row.address_count=}")
    print()

    # Count the number of users having no email address using group_by()
    # and having()
    stmt = (
        select(
            user_table.c.name,
            func.count(address_table.c.id).label("address_count"),
        )
        .join(address_table, user_table.c.id == address_table.c.user_id, isouter=True)
        .group_by(user_table.c.name)
        .having(func.count(address_table.c.id) == 0)
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.name=} {row.address_count=}")
    print()

    # Count the number of users having no email address using group_by()
    # and order_by()
    stmt = (
        select(
            user_table.c.name,
            func.count(address_table.c.id).label("address_count"),
        )
        .join(address_table, user_table.c.id == address_table.c.user_id, isouter=True)
        .group_by(user_table.c.name)
        .having(func.count(address_table.c.id) == 0)
        .order_by(address_table.c.user_id.desc())
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.name=} {row.address_count=}")
    print()


def using_aliases() -> None:
    """Using aliases to alias tables and columns."""
    user_table = metadata_obj.tables["user_account"]

    # returning all unique pairs of user names in the user_account table using
    # self-join with aliases
    user_alias_1 = user_table.alias("u1")
    user_alias_2 = user_table.alias("u2")

    stmt = select(
        user_alias_1.c.name.label("name_1"),
        user_alias_2.c.name.label("name_2"),
    ).join(
        user_alias_2,
        user_alias_1.c.id != user_alias_2.c.id,
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.name_1=} {row.name_2=}")


def using_subqueries() -> None:
    """Using subqueries."""
    user_table = metadata_obj.tables["user_account"]
    address_table = metadata_obj.tables["address"]

    subq = (
        select(
            address_table.c.user_id,
            func.count(address_table.c.id).label("address_count"),
        )
        .group_by(address_table.c.user_id)
        .subquery()
    )
    rich.print(f"[yellow]{subq}[/yellow]")
    input("Press Enter to continue...")

    stmt = select(
        user_table.c.name,
        user_table.c.fullname,
        subq.c.address_count,
    ).join(subq, user_table.c.id == subq.c.user_id)
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.name=} {row.fullname=} {row.address_count=}")


def using_ctes() -> None:
    """Using CTEs."""
    user_table = metadata_obj.tables["user_account"]
    address_table = metadata_obj.tables["address"]

    cte = (
        select(
            address_table.c.user_id,
            func.count(address_table.c.id).label("address_count"),
        )
        .group_by(address_table.c.user_id)
        .cte("address_count_cte")
    )
    rich.print(f"[yellow]{cte}[/yellow]")
    input("Press Enter to continue...")

    stmt = select(
        user_table.c.name,
        user_table.c.fullname,
        cte.c.address_count,
    ).join(cte, user_table.c.id == cte.c.user_id)
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.name=} {row.fullname=} {row.address_count=}")


def using_scalar_subqueries() -> None:
    """Using scalar subqueries."""
    user_table = metadata_obj.tables["user_account"]
    address_table = metadata_obj.tables["address"]

    subq = (
        select(func.count(address_table.c.id))
        .where(address_table.c.user_id == user_table.c.id)
        .scalar_subquery()
    )
    rich.print(f"[yellow]{subq}[/yellow]")

    scalar_subq = subq.scalar_subquery()
    rich.print(f"[yellow]{scalar_subq}[/yellow]")
    input("Press Enter to continue...")

    subq = (
        select(
            func.count(address_table.c.id).label("address_count"),
            address_table.c.email_address,
            address_table.c.user_id,
        )
        .where(user_table.c.id == address_table.c.user_id)
        .lateral()
    )
    stmt = (
        select(user_table.c.name, subq.c.address_count, subq.c.email_address)
        .join_from(user_table, subq)
        .order_by(user_table.c.id, subq.c.email_address)
    )
    print("=== lateral subquery ===")
    rich.print(f"[yellow]{subq}[/yellow]")
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    # with engine.connect() as conn:
    #     result = conn.execute(stmt)  # noqa: ERA001
    #     for row in result:
    #         rich.print(f"{row.address_count=}")  # noqa: ERA001
    print()


def using_union_and_union_all() -> None:
    """Using UNION and UNION ALL."""
    user_table = metadata_obj.tables["user_account"]
    address_table = metadata_obj.tables["address"]

    stmt1 = select(user_table).where(user_table.c.name.like("s%"))
    stmt2 = select(user_table).where(user_table.c.name.like("p%"))
    union_stmt = stmt1.union(stmt2)
    union_all_stmt = stmt1.union_all(stmt2)
    rich.print(f"[yellow]{union_stmt}[/yellow]")
    rich.print(f"[yellow]{union_all_stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        print("=== UNION ===")
        result = conn.execute(union_stmt)
        for row in result:
            rich.print(f"{row=}")
        result = conn.execute(union_all_stmt)
        print("=== UNION ALL ===")
        for row in result:
            rich.print(f"{row=}")
    input("Press Enter to continue...")

    subq = union_stmt.subquery()
    stmt = select(subq.c.name, address_table.c.email_address).join(
        address_table,
        onclause=subq.c.id == address_table.c.user_id,
        isouter=True,
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.name=} {row.email_address=}")
    print()


def using_exists() -> None:
    """Using EXISTS."""
    user_table = metadata_obj.tables["user_account"]
    address_table = metadata_obj.tables["address"]

    # Users with no email address
    subq = select(address_table.c.id).where(address_table.c.user_id == user_table.c.id)
    stmt = select(user_table.c.name).where(~exists(subq))
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")
    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(f"{row.name=}")
    print()

    # Users with more than one email
    subq = (
        select(func.count(address_table.c.id))
        .where(user_table.c.id == address_table.c.user_id)
        .group_by(address_table.c.user_id)
        .having(func.count(address_table.c.id) > 1)
    ).exists()

    with engine.connect() as conn:
        print("=== USERS WITH MORE THAN ONE EMAIL ===")
        result = conn.execute(select(user_table.c.name).where(subq))
        for row in result:
            rich.print(f"{row.name=}")
        print("=== USERS WITH NO EMAIL ===")
        subq = select(address_table.c.id).where(
            address_table.c.user_id == user_table.c.id,
        )
        result = conn.execute(select(user_table.c.name).where(~exists(subq)))
        for row in result:
            rich.print(f"{row.name=}")
    input("Press Enter to continue...")


def using_sql_functions() -> None:
    """Using SQL functions."""
    user_table = metadata_obj.tables["user_account"]

    stmt = (
        select(func.count().label("user_count"))
        .select_from(user_table)
        .where(user_table.c.name.like("p%"))
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        print("=== COUNT OF USERS WITH NAME STARTING WITH 'p' ===")
        for row in result:
            rich.print(f"{row.user_count=}")
    input("Press Enter to continue...")

    stmt = select(func.lower("Hello to Jason Isaacs!"))
    with engine.connect() as conn:
        result = conn.execute(stmt)
        print("=== LOWERCASE FUNCTION ===")
        for row in result:
            rich.print(f"{row=}")

    stmt = select(func.upper(user_table.c.name).label("username"))
    with engine.connect() as conn:
        result = conn.execute(stmt)
        print("=== UPPERCASE FUNCTION ===")
        for row in result:
            rich.print(f"{row.username=}")

    stmt = select(func.now())
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        print("=== now() function ===")
        for row in result:
            rich.print(f"{row=}")

    # inspecting return types
    rich.print(f"[yellow]{type(func.count())=}; {func.count().type=}[/yellow]")
    rich.print(f"[yellow]{type(func.concat())=}; {func.concat().type=}[/yellow]")
    rich.print(f"[yellow]{type(func.now())=}; {func.now().type=}[/yellow]")


def using_window_functions() -> None:
    """Using window functions (OVER (PARTITION BY ... ORDER BY ...))."""
    user_table = metadata_obj.tables["user_account"]
    address_table = metadata_obj.tables["address"]

    # read the name and email address of each user along with a row number for
    # each user partitioned by name and ordered by email address
    stmt = (
        select(
            func.row_number().over(partition_by=user_table.c.name).label("row_number"),
            user_table.c.name,
            address_table.c.email_address,
        )
        .join(address_table, user_table.c.id == address_table.c.user_id)
        .order_by(user_table.c.name)
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(
                f"{row.row_number=} {row.name=} {row.email_address=}",
            )
    input("Press Enter to continue...")

    # another example: not sure about how useful this is but it demonstrates
    # that how you can use window functions
    stmt = (
        select(
            user_table.c.name,
            address_table.c.email_address,
            func.count().over(order_by=user_table.c.name).label("index_no"),
        )
        .join(address_table, user_table.c.id == address_table.c.user_id)
        .order_by(user_table.c.name)
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(
                f"{row.index_no=} {row.name=} {row.email_address=}",
            )
    input("Press Enter to continue...")


def using_data_casts_and_type_coerce() -> None:
    """Using data casts and type_coerce."""
    user_table = metadata_obj.tables["user_account"]

    stmt = select(
        cast(user_table.c.id, String).label("id_as_string"),
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(
                f"{row.id_as_string=}",
            )
    input("Press Enter to continue...")

    # casting to a JSON object (if supported by the database)
    stmt = select(cast('{"key": "value"}', JSON)["key"].label("json_data"))
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    stmt = select(
        type_coerce(user_table.c.id, String).label("id_as_string"),
    )
    rich.print(f"[yellow]{stmt}[/yellow]")
    input("Press Enter to execute the above statement...")

    with engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            rich.print(
                f"{row.id_as_string=}",
            )
    input("Press Enter to continue...")


def main() -> None:  # noqa: PLR0915
    """Application entry point."""
    setup_db()
    input("Database setup complete. Press Enter to continue...")
    print()

    # Simple SELECT / SELECT ...FROM ... WHERE ...
    simple_select()
    input("Simple SELECT statements complete. Press Enter to continue...")
    print()

    # Getting the results using first(), all()
    getting_results()
    input("Getting results complete. Press Enter to continue...")
    print()

    # Ordering the results using order_by()
    ordering_results()
    input("Ordering results complete. Press Enter to continue...")
    print()

    # Using label() to label the columns in the result set
    using_label()
    input("Using label() complete. Press Enter to continue...")
    print()

    # Using text()
    using_text()
    input("Using text() complete. Press Enter to continue...")
    print()

    # Using literal_column()
    using_literal_column()
    input("Using literal_column() complete. Press Enter to continue...")
    print()

    # Using where(), and_(), or_() methods to build complex WHERE clauses
    using_where_and_or()
    input("Using where(), and_(), or_() complete. Press Enter to continue...")
    print()

    # Using filter_by() method to build simple WHERE clauses
    using_filter_by()
    input("Using filter_by() complete. Press Enter to continue...")
    print()

    # JOINs and explicit FROM: join_from(), join(), select_from()
    using_joins_and_explicit_from()
    input(
        "Using join_from(), join(), select_from() complete. Press Enter to continue...",
    )
    print()

    # exploring JOINs
    exploring_joins()
    input("Exploring JOINs complete. Press Enter to continue...")
    print()

    # exploring ORDER BY
    exploring_order_by()
    input("Ordering results complete. Press Enter to continue...")
    print()

    # using group_by() and having() methods
    using_group_by_and_having()
    input("Using group_by() and having() complete. Press Enter to continue...")
    print()

    # using aliases
    using_aliases()
    input("Using aliases complete. Press Enter to continue...")
    print()

    # using non-scalar subqueries
    using_subqueries()
    input("Using subqueries complete. Press Enter to continue...")
    print()

    # using CTEs
    using_ctes()
    input("Using CTEs complete. Press Enter to continue...")
    print()

    # Using scalar subqueries
    using_scalar_subqueries()
    input("Using scalar subqueries complete. Press Enter to continue...")
    print()

    # UNION and UNION ALL
    using_union_and_union_all()
    input("Using UNION and UNION ALL complete. Press Enter to continue...")
    print()

    # EXISTS
    using_exists()
    input("Using EXISTS complete. Press Enter to continue...")
    print()

    # SQL functions
    using_sql_functions()
    input("Using SQL functions complete. Press Enter to continue...")
    print()

    # window functions (OVER (PARTITION BY ... ORDER BY ...))
    using_window_functions()
    input("Using window functions complete. Press Enter to continue...")
    print()

    # data casts and type_coerce
    using_data_casts_and_type_coerce()
    input("CAST and type_coerce complete. Press Enter to continue...")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nUser interrupted the execution.")
    finally:
        input("Press Enter to drop the tables and exit...")
        metadata_obj.drop_all(engine)
