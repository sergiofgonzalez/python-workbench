"""Oxyde Models for the Quickstart project."""

from oxyde import Field, Model


class User(Model):
    """User model for the quickstart project."""

    id: int | None = Field(default=None, db_pk=True)  # ty:ignore[invalid-assignment]
    name: str
    email: str = Field(db_unique=True)  # ty:ignore[invalid-assignment]
    age: int | None = Field(default=None)  # ty:ignore[invalid-assignment]

    class Meta:
        """Meta class for the User model."""

        table_name = "users"
        is_table = True
