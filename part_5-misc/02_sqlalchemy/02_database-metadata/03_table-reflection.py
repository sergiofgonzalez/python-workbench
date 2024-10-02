"""Brief into to table reflection to generate Table from existing db."""

from sqlalchemy import Engine, MetaData, Table, create_engine, text


def setup(engine: Engine) -> None:
    """Create a table and inserts some data to be used later."""
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE my_table (x int, y int)"))


def main() -> None:
    """Entry point for the app."""
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

    # create a my_table table
    setup(engine)

    # setup the db metadata obj and create a Table obj from existing table
    metadata_obj = MetaData()
    my_table = Table("my_table", metadata_obj, autoload_with=engine)

    print(my_table)


if __name__ == "__main__":
    main()
