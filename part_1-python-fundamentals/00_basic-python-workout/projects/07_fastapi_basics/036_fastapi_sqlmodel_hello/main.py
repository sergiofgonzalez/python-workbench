"""Illustrates the basics of SQLModel with a FastAPI app."""

from collections.abc import Generator, Sequence
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Hero(SQLModel, table=True):
    """A hero in the database."""

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {
    "check_same_thread": False,  # Needed for SQLite to work with FastAPI threads
}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables() -> None:
    """Create the database and tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session]:
    """Get a new session (single session per request is ensured using yield)."""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[
    Session,
    Depends(get_session),
]  # Type alias for dependency injection


app = FastAPI()


@app.on_event("startup")  # ty:ignore[deprecated]
def on_startup() -> None:
    """Register the actions to be carried out on FastAPI app startup."""
    create_db_and_tables()


@app.post("/heroes/")
def create_hero(hero: Hero, session: SessionDep) -> Hero:
    """Create a new hero in the database."""
    if hero.id is not None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="id should not be provided",
        )
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@app.get("/heroes/")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> Sequence[Hero]:
    """Read all heroes from the database."""
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes  # noqa: RET504


@app.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: SessionDep) -> Hero:
    """Read a hero from the database by id."""
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hero not found",
        )
    return hero


@app.delete("/heroes/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hero(hero_id: int, session: SessionDep) -> None:
    """Delete a hero from the database by id."""
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hero not found",
        )
    session.delete(hero)
    session.commit()


@app.put("/heroes/{hero_id}")
def update_hero(hero_id: int, hero: Hero, session: SessionDep) -> Hero:
    """Update a hero in the database by id."""
    if hero.id is not None and int(hero.id) != hero_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="id should not be provided or should match the path parameter",
        )
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hero not found",
        )

    hero_data = hero.model_dump(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_hero, key, value)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero
