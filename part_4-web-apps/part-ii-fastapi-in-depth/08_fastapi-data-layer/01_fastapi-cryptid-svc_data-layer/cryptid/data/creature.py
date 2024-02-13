"""Creature data layer"""

from model.creature import Creature

from cryptid.data.init import curs

if curs is not None:
    curs.execute(
        """
        CREATE TABLE IF NOT EXISTS creature
            (name TEXT PRIMARY KEY,
             description TEXT,
             country TEXT,
             area TEXT,
             aka TEXT)
        """
    )
else:
    raise TypeError("cursor not initialized")


def row_to_model(row: tuple) -> Creature:
    name, description, country, area, aka = row
    return Creature(
        name=name, description=description, country=country, area=area, aka=aka
    )


def model_to_dict(creature: Creature) -> dict:
    return creature.model_dump()


def get_one(name: str) -> Creature:
    query = """
        SELECT * FROM creature
         WHERE name = :name
    """
    params = {"name": name}
    curs.execute(query, params)
    row = curs.fetchone()
    return row_to_model(row)


def get_all() -> list[Creature]:
    query = """
        SELECT * FROM creature
    """
    curs.execute(query)
    rows = list(curs.fetchall())
    return [row_to_model(row) for row in rows]


def create(creature: Creature) -> Creature:
    query = """
        INSERT INTO creature
        VALUES (:name, :description, :country, :area, :aka)
    """
    params = model_to_dict(creature)
    curs.execute(query, params)
    return get_one(creature.name)


def modify(name: str, creature: Creature) -> Creature:
    query = """
        UPDATE creature
           SET country = :country,
               name = :name,
               description = :description,
               area = :area,
               aka = :aka
         WHERE name = :name_orig
    """
    params = model_to_dict(creature)
    params["name_orig"] = name
    _ = curs.execute(query, params)
    return get_one(creature.name)


def delete(creature: Creature) -> bool:
    query = """
        DELETE FROM creature
         WHERE name = :name
    """
    params = {"name": creature.name}
    res = curs.execute(query, params)
    return bool(res)
