"""Defining Table Metadata when using ORM."""

from typing import List

from sqlalchemy import ForeignKey, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Acquiring a new Declarative Base by subclassing DeclarativeBase."""


class User(Base):
    """ORM mapped class for user_account table."""

    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str | None]

    addresses: Mapped[list["Address"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        """Provide dev level string representation of User."""
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    """ORM mapped class for address table."""

    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user_account.id"))
    email_address: Mapped[str]

    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        """Provide dev level string representation of Address."""
        return f"Address(id={self.id!r}, email_address={self.email!r})"


def main() -> None:
    """Entry point for the app."""
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()
