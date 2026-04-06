"""Illustrates the basics of SQLAlchemy Core."""

from sqlalchemy import create_engine, text


def main() -> None:
    """Application entry point."""
    # Part 1: Create an engine that connects to a particular DB server.
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    print("=" * 80)

    # Part 2: Connect to the DB server and execute a simple statement.
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 'Hello, World!'"))
        print(f"{result.all()=}")
    print("=" * 80)

    # Part 3: Execute a transaction using commit as you go.
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE some_table (x INT, y INT)"))
        conn.execute(text("INSERT INTO some_table (x, y) VALUES (1, 1)"))
        conn.execute(text("INSERT INTO some_table (x, y) VALUES (2, 4)"))
        conn.execute(text("INSERT INTO some_table (x, y) VALUES (3, 9)"))
        conn.commit()
    print("=" * 80)

    # Part 4: Using the begin once technique to execute a transaction.
    with engine.begin() as conn:
        conn.execute(text("INSERT INTO some_table (x, y) VALUES (4, 16)"))
        conn.execute(text("INSERT INTO some_table (x, y) VALUES (5, 25)"))
    print("=" * 80)

    # Part 5: Querying data using different techniques
    with engine.connect() as conn:
        result = conn.execute(text("SELECT x, y FROM some_table"))
        for row in result:
            print(f"{row.x=}, {row.y=}")
    print("-" * 80)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT x, y FROM some_table"))
        for x, y in result:
            print(f"{x=}, {y=}")
    print("-" * 80)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT x, y FROM some_table"))
        for row in result:
            print(f"{row[0]=} {row[1]=}")
    print("-" * 80)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT x, y FROM some_table"))
        for row in result.mappings():
            print(f"{row['x']=} {row['y']=}")
    print("=" * 80)

    # Part 6: Using parameters to the query.
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT x, y FROM some_table WHERE y > :y"),
            {"y": 2},
        )
        for row in result:
            print(f"{row.x=}, {row.y=}")
    print("=" * 80)
    with engine.begin() as conn:
        result = conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 6, "y": 36}, {"x": 7, "y": 49}],
        )
    print("=" * 80)

    with engine.connect() as conn:
        result = conn.execute(text("SELECT x, y FROM some_table"))
        print(f"{result.all()=}")


if __name__ == "__main__":
    main()
