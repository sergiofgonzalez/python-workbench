"""Fetching rows with a Session object on non-ORM scenario."""

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session


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

    # it will be automatically rolled back
    with Session(engine) as session:
        result = session.execute(
            text("SELECT x, y from my_table where y > :y"),
            {"y": 1},
        )
        for row in result:
            print(f"x: {row.x}, y: {row.y}")

    # explicitly committing
    with Session(engine) as session:
        result = session.execute(
            text("UPDATE my_table SET y = :y WHERE x = :x"),
            {"x": 2, "y": 55},
        )
        session.commit()

    with Session(engine) as session:
        result = session.execute(text("SELECT x, y from my_table"))
        print(result.all())

    # using the execute many trick
    with Session(engine) as session:
        result = session.execute(
            text("UPDATE my_table SET y = :y WHERE x = :x"),
            [{"x": 1, "y": 77}, {"x": 2, "y": 777}],
        )
        session.commit()

    with Session(engine) as session:
        result = session.execute(text("SELECT x, y from my_table"))
        print(result.all())


if __name__ == "__main__":
    main()
