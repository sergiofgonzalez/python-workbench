"""Creature data layer"""

import os
from sqlite3 import IntegrityError

from cryptid.data.errors import DuplicateError, InvalidStateError, MissingError
from cryptid.data.init import curs
from cryptid.model.explorer import Explorer
from cryptid.utils.log_config import get_logger

log = get_logger(__name__)


def _init_table():
    """
    Creates the creature table on the given connection if it doesn't exist. This
    function should be called the first time the library is imported and every
    time a table refresh is required (e.g., when running unit tests).
    """
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
        raise InvalidStateError(
            "Uninitialized cursor: cannot create creature table"
        )


def _reset_table():
    """
    Resets the explorer table to its initial state (empty). This function should
    be called when running unit tests only!
    """
    if not (
        os.getenv("CRYPTID_UNIT_TEST")
        and os.getenv("CRYPTID_SQLITE_DB") == ":memory:"
    ):
        raise InvalidStateError("Function intended for unit tests only")

    log.warning(
        "Resetting 'explorer' table: this is intended for unit tests only!"
    )
    if curs:
        curs.execute("DROP TABLE IF EXISTS explorer")
        _init_table()
    else:
        raise InvalidStateError("Uninitialized error")


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
    if curs:
        curs.execute(query, params)
        row = curs.fetchone()
        if row:
            return row_to_model(row)
        else:
            raise MissingError(f"Explorer {name} not found")
    else:
        raise InvalidStateError("Cursor not initialized")


def get_all() -> list[Explorer]:
    query = """
        SELECT * FROM explorer
    """
    if curs:
        curs.execute(query)
        rows = list(curs.fetchall())
        return [row_to_model(row) for row in rows]
    else:
        raise InvalidStateError("Cursor not initialized")


def create(explorer: Explorer) -> Explorer:
    query = """
        INSERT INTO explorer
        VALUES (:name, :country, :description)
    """
    params = model_to_dict(explorer)
    if curs:
        try:
            curs.execute(query, params)
            return get_one(explorer.name)
        except IntegrityError as e:
            log.error(
                "IntegrityError: cannot create explorer %s: %s",
                explorer.name,
                e,
            )
            raise DuplicateError(
                f"Explorer {explorer.name} already exists"
            ) from e
    else:
        raise InvalidStateError("Uninitialized cursor")


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
    if curs:
        try:
            curs.execute(query, params)
        except IntegrityError as e:
            log.error(
                "Update will cause a duplicated record: name_orig=%s, name=%s",
                name,
                explorer.name,
            )
            raise DuplicateError(
                f"Explorer {explorer.name} already exists"
            ) from e
        if curs.rowcount == 1:
            return get_one(explorer.name)
        else:
            raise MissingError(f"Explorer {name} not found")
    else:
        raise InvalidStateError("Cursor not initialized")


def delete(explorer: Explorer):
    query = """
        DELETE FROM explorer
         WHERE name = :name
    """
    params = {"name": explorer.name}
    if curs:
        curs.execute(query, params)
        if curs.rowcount != 1:
            raise MissingError(f"Explorer {explorer.name} not found")
    else:
        raise InvalidStateError("Cursor not initialized")


# Invoke the first time the lib is imported
_init_table()
