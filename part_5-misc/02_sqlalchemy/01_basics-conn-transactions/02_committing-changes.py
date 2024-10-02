"""Committing changes."""

from sqlalchemy import create_engine, text


def main() -> None:
    """Create a table, insert some data and commit."""
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE my_table (x int, y int)"))
        conn.execute(
            text("INSERT INTO my_table (x, y) VALUES (:x, :y)"),
            [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
        )
        conn.commit()


if __name__ == "__main__":
    main()
