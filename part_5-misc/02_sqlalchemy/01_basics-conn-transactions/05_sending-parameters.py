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

    with engine.begin() as conn:
        result = conn.execute(
            text("SELECT x, y FROM my_table WHERE y > :y"),
            {"y": 1},
        )
        for row in result:
            print(f"x: {row.x} y: {row.y}")


if __name__ == "__main__":
    main()
