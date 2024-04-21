"""Management of Commit and Rollback of transactions"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing_extensions import Self

DB_URL = os.getenv("DB_URL")
assert DB_URL is not None, "DB_URL environment variable needs to be defined."


class UnitOfWork:
    """Implements the Unit of Work pattern using SQLAlchemy session"""

    def __init__(self) -> None:
        self.session_maker = sessionmaker(
            bind=create_engine(DB_URL)  # type: ignore
        )

    def __enter__(self) -> Self:
        self.session = self.session_maker()
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type is not None:
            self.rollback()
            self.session.close()
        self.session.close()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
