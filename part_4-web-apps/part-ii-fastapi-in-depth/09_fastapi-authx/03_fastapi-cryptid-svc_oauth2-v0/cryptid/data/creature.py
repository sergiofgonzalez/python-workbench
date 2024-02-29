"""Creature data layer"""

from sqlite3 import IntegrityError

from cryptid.data.errors import DuplicateError, InvalidStateError, MissingError
from cryptid.data.init import curs
from cryptid.model.creature import Creature
from cryptid.utils.log_config import get_logger

log = get_logger(__name__)

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
    raise InvalidStateError(
        "Uninitialized cursor: cannot create creature table"
    )


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
    if curs:
        curs.execute(query, params)
        row = curs.fetchone()
        if row:
            return row_to_model(row)
        else:
            raise MissingError(f"Creature {name!r} not found")
    else:
        raise InvalidStateError("Cursor not initialized")


def get_all() -> list[Creature]:
    query = """
        SELECT * FROM creature
    """
    if curs:
        curs.execute(query)
        rows = list(curs.fetchall())
        return [row_to_model(row) for row in rows]
    else:
        raise InvalidStateError("Cursor not initialized")


def create(creature: Creature) -> Creature:
    query = """
        INSERT INTO creature
        VALUES (:name, :description, :country, :area, :aka)
    """
    params = model_to_dict(creature)
    if curs:
        try:
            curs.execute(query, params)
            return get_one(creature.name)
        except IntegrityError as e:
            log.error(
                "IntegrityError: cannot create creature %s: %s",
                creature.name,
                e,
            )
            raise DuplicateError(
                f"Creature {creature.name} already exists"
            ) from e
    else:
        raise InvalidStateError("Uninitialized error")


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
    if curs:
        try:
            curs.execute(query, params)
        except IntegrityError as e:
            log.error(
                "Update will cause a duplicated record: name_orig=%s, name=%s",
                name,
                creature.name,
            )
            raise DuplicateError(
                f"Creature {creature.name} already exists"
            ) from e
        if curs.rowcount == 1:
            return get_one(creature.name)
        else:
            raise MissingError(f"Creature {name} not found")
    else:
        raise InvalidStateError("Cursor not initialized")


def delete(creature: Creature):
    query = """
        DELETE FROM creature
         WHERE name = :name
    """
    params = {"name": creature.name}
    if curs:
        curs.execute(query, params)
        if curs.rowcount != 1:
            raise MissingError(f"Creature {creature.name} not found")
    else:
        raise InvalidStateError("Cursor not initialized")
