"""Fetching rows."""

from sqlalchemy import Engine, create_engine, text


def setup(engine: Engine) -> None:
    """Create a table and inserts some data to be used later."""
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE my_table (x int, y int)"))
        conn.execute(
            text("INSERT INTO my_table (x, y) VALUES (:x, :y)"),
            [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
        )


def main() -> None:
    """Fetch rows from a table."""
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    setup(engine)

    # default: as named tuples
    with engine.begin() as conn:
        result = conn.execute(text("SELECT x, y FROM my_table"))
        for row in result:
            print(f"x: {row.x} y: {row.y}")

    # unpacking
    with engine.begin() as conn:
        result = conn.execute(text("SELECT x, y FROM my_table"))
        for x, y in result:
            print(f"{x=} {y=}")

    # integer indexing
    with engine.begin() as conn:
        result = conn.execute(text("SELECT x, y FROM my_table"))
        for row in result:
            print(f"x: {row[0]} y: {row[1]}")

    # as read-only dicts
    with engine.begin() as conn:
        result = conn.execute(text("SELECT x, y FROM my_table"))
        for dict_row in result.mappings():
            print(f"x: {dict_row["x"]} y: {dict_row["y"]}")

    # obtaining the results as one
    with engine.begin() as conn:
        result = conn.execute(text("SELECT x, y FROM my_table"))
        print(result.all())


if __name__ == "__main__":
    main()
