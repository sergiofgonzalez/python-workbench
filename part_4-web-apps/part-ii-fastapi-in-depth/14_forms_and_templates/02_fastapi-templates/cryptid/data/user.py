"""User data layer"""

import os
from sqlite3 import IntegrityError

from cryptid.data.errors import DuplicateError, InvalidStateError, MissingError
from cryptid.data.init import curs
from cryptid.model.user import User
from cryptid.utils.log_config import get_logger

log = get_logger(__name__)


def _init_table():
    """
    Creates the user and xusers table on the given connection if they don't
    exist. This function should be called the first time the library is imported
    and every time a table refresh is required (e.g., when running unit tests).
    """
    if curs:
        # Active users
        curs.execute(
            """
            CREATE TABLE IF NOT EXISTS user (
                name TEXT PRIMARY KEY,
                password_hash TEXT
            )
            """
        )
        # Inactive users (users that has been deleted)
        curs.execute(
            """
            CREATE TABLE IF NOT EXISTS xuser (
                name TEXT PRIMARY KEY,
                password_hash TEXT
            )
            """
        )
    else:
        raise InvalidStateError(
            "Uninitialized cursor: cannot create user/xuser tables"
        )


def _reset_table():
    """
    Resets the user and xusers table to its initial state (empty). This function
    should be called when running unit tests only!
    """
    if not (
        os.getenv("CRYPTID_UNIT_TEST")
        and os.getenv("CRYPTID_SQLITE_DB") == ":memory:"
    ):
        raise InvalidStateError("Function intended for unit tests only")

    log.warning(
        (
            "Resetting 'user' and 'xuser' table: this is intended for unit "
            "tests only!"
        )
    )
    if curs:
        curs.execute("DROP TABLE IF EXISTS user")
        curs.execute("DROP TABLE IF EXISTS xuser")
        _init_table()
    else:
        raise InvalidStateError("Uninitialized error")


def row_to_model(row: tuple) -> User:
    name, password_hash = row
    return User(name=name, password_hash=password_hash)


def model_to_dict(user: User) -> dict:
    return user.model_dump()


def get_one(name: str) -> User:
    query = """
        SELECT * FROM user
         WHERE name = :name
    """
    params = {"name": name}
    if curs:
        curs.execute(query, params)
        row = curs.fetchone()
        if row:
            return row_to_model(row)
        else:
            raise MissingError(f"User {name!r} not found")
    else:
        raise InvalidStateError("Cursor not initialized")


def get_all() -> list[User]:
    query = """
        SELECT * FROM user
    """
    if curs:
        curs.execute(query)
        rows = list(curs.fetchall())
        return [row_to_model(row) for row in rows]
    else:
        raise InvalidStateError("Cursor not initialized")


def create(user: User, table: str = "user") -> User:
    """Add a user to either user or xuser table"""
    query = f"""
        INSERT INTO {table}
        VALUES (:name, :password_hash)
    """
    if table not in ("user", "xuser"):
        raise ValueError(f"Unexpected table {table!r}")
    params = model_to_dict(user)
    if curs:
        try:
            curs.execute(query, params)
            return user
        except IntegrityError as e:
            log.error(
                "IntegrityError: cannot create user %s in table %s: %s",
                user.name,
                table,
                e,
            )
            raise DuplicateError(f"User {user.name} already exists") from e
    else:
        raise InvalidStateError("Uninitialized cursor")


def modify(name: str, user: User) -> User:
    query = """
        UPDATE user
           SET name = :name,
               password_hash = :password_hash
         WHERE name = :name_orig
    """
    params = model_to_dict(user)
    params["name_orig"] = name
    if curs:
        try:
            curs.execute(query, params)
        except IntegrityError as e:
            log.error(
                (
                    "Update will cause a duplicated record in user table: "
                    "name_orig=%s, name=%s"
                ),
                name,
                user.name,
            )
            raise DuplicateError(f"User {user.name} already exists") from e
        if curs.rowcount == 1:
            return get_one(user.name)
        else:
            raise MissingError(f"User {name} not found")
    else:
        raise InvalidStateError("Cursor not initialized")


def delete(user: User):
    query = """
        DELETE FROM user
         WHERE name = :name
    """
    params = {"name": user.name}
    if curs:
        curs.execute(query, params)
        if curs.rowcount != 1:
            raise MissingError(f"User {user.name} not found")
        create(user, table="xuser")
    else:
        raise InvalidStateError("Cursor not initialized")


_init_table()
