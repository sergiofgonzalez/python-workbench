"""Basics of the MetaData object and table creation using the declarative approach."""

from __future__ import annotations

from sqlalchemy import ForeignKey, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for declarative models (represents the MetaData object in ORM)."""


class User(Base):
    """User model."""

    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str | None]

    addresses: Mapped[list[Address]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        """String representation of the User model."""
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    """Address model."""

    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))

    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        """String representation of the Address model."""
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


def main() -> None:
    """Application entry point."""
    engine = create_engine("sqlite+pysqlite:///app.db", echo=True)

    # Create all tables in the database using the Base's metadata
    Base.metadata.create_all(engine)

    # Drop all tables in the database using the Base's metadata
    Base.metadata.drop_all(engine)


if __name__ == "__main__":
    main()
