"""Creature data layer"""

from model.explorer import Explorer

from cryptid.data.init import curs

if curs is not None:
    curs.execute(
        """
        CREATE TABLE IF NOT EXISTS explorer
            (name TEXT PRIMARY KEY,
             country TEXT,
             description TEXT)
        """
    )
else:
    raise TypeError("cursor not initialized")


def row_to_model(row: tuple) -> Explorer:
    name, country, description = row
    return Explorer(name=name, country=country, description=description)


def model_to_dict(creature: Explorer) -> dict:
    return creature.model_dump()


def get_one(name: str) -> Explorer:
    query = """
        SELECT * FROM explorer
         WHERE name = :name
    """
    params = {"name": name}
    curs.execute(query, params)
    row = curs.fetchone()
    return row_to_model(row)


def get_all() -> list[Explorer]:
    query = """
        SELECT * FROM explorer
    """
    curs.execute(query)
    rows = list(curs.fetchall())
    return [row_to_model(row) for row in rows]


def create(explorer: Explorer) -> Explorer:
    query = """
        INSERT INTO explorer
        VALUES (:name, :country, :description)
    """
    params = model_to_dict(explorer)
    curs.execute(query, params)
    return get_one(explorer.name)


def modify(name: str, explorer: Explorer) -> Explorer:
    query = """
        UPDATE explorer
           SET country = :country,
               name = :name,
               description = :description
         WHERE name = :name_orig
    """
    params = model_to_dict(explorer)
    params["name_orig"] = name
    _ = curs.execute(query, params)
    return get_one(explorer.name)


def delete(explorer: Explorer) -> bool:
    query = """
        DELETE FROM explorer
         WHERE name = :name
    """
    params = {"name": explorer.name}
    res = curs.execute(query, params)
    return bool(res)
