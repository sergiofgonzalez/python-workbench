"""Getting a connection."""

from sqlalchemy import create_engine, text


def main() -> None:
    """Sample code."""
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 'hello, world!'"))
        print(result.all())


if __name__ == "__main__":
    main()
