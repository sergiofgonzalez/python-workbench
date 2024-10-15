"""A few SQL joins using SQLite as the backend."""

from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    insert,
    text,
)


def main() -> None:
    """Entry point for the app."""
    # setup the engine and the Metadata object
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    metadata_obj = MetaData()

    esp_table = Table(
        "esp",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("desc", String(30)),
    )

    eng_table = Table(
        "eng",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("desc", String(30)),
    )

    # create the tables defined in the metadata object
    metadata_obj.create_all(engine)

    # insert some data in the tables
    stmt = insert(esp_table)
    with engine.begin() as conn:
        conn.execute(
            stmt,
            [
                {"id": 1, "desc": "uno"},
                {"id": 2, "desc": "dos"},
                {"id": 3, "desc": "tres"},
            ],
        )

    stmt = insert(eng_table)
    with engine.begin() as conn:
        conn.execute(
            stmt,
            [
                {"id": 1, "desc": "one"},
                {"id": 2, "desc": "two"},
                {"id": 4, "desc": "four"},
            ],
        )

    # Plain join is the cartesian product of AxB
    stmt = text("SELECT * FROM esp, eng")
    with engine.begin() as conn:
        rows = conn.execute(stmt).all()
        assert rows == [
            (1, "uno", 1, "one"),
            (1, "uno", 2, "two"),
            (1, "uno", 4, "four"),
            (2, "dos", 1, "one"),
            (2, "dos", 2, "two"),
            (2, "dos", 4, "four"),
            (3, "tres", 1, "one"),
            (3, "tres", 2, "two"),
            (3, "tres", 4, "four"),
        ]

    # Plain join reversing the tables
    stmt = text("SELECT * FROM eng, esp")
    with engine.begin() as conn:
        rows = conn.execute(stmt).all()
        assert rows == [
            (1, "one", 1, "uno"),
            (1, "one", 2, "dos"),
            (1, "one", 3, "tres"),
            (2, "two", 1, "uno"),
            (2, "two", 2, "dos"),
            (2, "two", 3, "tres"),
            (4, "four", 1, "uno"),
            (4, "four", 2, "dos"),
            (4, "four", 3, "tres"),
        ]

    # Plain join using WHERE on identical keys
    # returns:
    #  (id, desc_esp, desc_eng) for keys that exist on both tables
    #  nothing for keys that exist only on one of the tables
    stmt = text(
        "SELECT a.id, a.desc, b.desc FROM esp a, eng b WHERE a.id = b.id",
    )
    with engine.begin() as conn:
        rows = conn.execute(stmt).all()
        assert rows == [
            (1, "uno", "one"),
            (2, "dos", "two"),
        ]

    # Inner join (is the same as plain join)
    #  (id, desc_esp, desc_eng) for keys that exist on both tables
    #  nothing for keys that exist only on one of the tables
    stmt = text("""
                SELECT a.id, a.desc, b.desc
                  FROM esp a
            INNER JOIN eng b ON a.id = b.id
                """)
    with engine.begin() as conn:
        rows = conn.execute(stmt).all()
        assert rows == [
            (1, "uno", "one"),
            (2, "dos", "two"),
        ]

    # left outer join
    # returns:
    #  (id, desc_esp, desc_eng) for keys that exist on both tables
    #  (id, desc_esp, None) for keys that exist only on the left table
    #  nothing for keys that exist only on the right
    stmt = text("""
                SELECT a.id, a.desc, b.desc
                  FROM esp a
            LEFT OUTER JOIN eng b ON a.id = b.id
                """)
    with engine.begin() as conn:
        rows = conn.execute(stmt).all()
        assert rows == [
            (1, "uno", "one"),
            (2, "dos", "two"),
            (3, "tres", None),
        ]

    # left outer join (reversed)
    # returns:
    #  (id, desc_eng, desc_esp) for keys that exist on both tables
    #  (id, desc_eng, None) for keys that exist only on the left table
    #  nothing for keys that exist only on the right
    stmt = text("""
                SELECT a.id, a.desc, b.desc
                  FROM eng a
            LEFT OUTER JOIN esp b ON a.id = b.id
                """)
    with engine.begin() as conn:
        rows = conn.execute(stmt).all()
        assert rows == [
            (1, "one", "uno"),
            (2, "two", "dos"),
            (4, "four", None),
        ]

    # At the time of writing SQLite doesn't support RIGHT OUTER and FULL OUTER
    # joins, but you get the idea:
    # RIGHT OUTER JOIN returns
    #   (id, desc_esp, desc_eng) for keys that exist on both tables
    #   (id, None, desc_eng) for keys that exist only on right table
    #   nothing for keys that exist only on the left
    # FULL OUTER JOIN returns
    #   (id, desc_esp, desc_eng) for keys that exist on both tables
    #   (id, desc_esp, None) for keys that exist only on left table
    #   (id, None, desc_eng) for keys that exist only on right table


if __name__ == "__main__":
    main()
