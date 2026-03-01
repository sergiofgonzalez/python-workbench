"""Illustrates how to use multiple SQLModel models with inheritance."""

from collections.abc import Generator
from typing import Annotated, Any

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlmodel import Field, Session, SQLModel, create_engine, select

sqlite_file = "database.db"
sqlite_url = f"sqlite:///{sqlite_file}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables() -> None:
    """Create the database and tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Get a new session."""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@app.on_event("startup")  # ty:ignore[deprecated]
def on_startup() -> None:
    """Event handler for the startup event."""
    create_db_and_tables()


class HeroBase(SQLModel):
    """Base model for a hero."""

    name: str = Field(index=True)
    age: int = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    """Model for a hero in the database."""

    id: int = Field(primary_key=True)
    secret_name: str


class HeroPublic(HeroBase):
    """Model for a public hero."""

    id: int


class HeroCreate(HeroBase):
    """Model for creating a hero."""

    secret_name: str


class HeroUpdate(HeroBase):
    """Model for updating a hero."""

    name: str | None = None
    age: int | None = None
    secret_name: str | None = None


@app.post("/heroes/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep) -> Any:  # noqa: ANN401
    """Path operation for the POST heroes endpoint."""
    hero_in_db = Hero.model_validate(hero)
    session.add(hero_in_db)
    session.commit()
    session.refresh(hero_in_db)
    return hero_in_db


@app.get("/heroes/", response_model=list[HeroPublic])
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> Any:  # noqa: ANN401
    """Path operation for the GET heroes endpoint."""
    heroes_db = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes_db  # noqa: RET504


@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep) -> Any:  # noqa: ANN401
    """Path operation for the GET hero by ID endpoint."""
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hero not found",
        )
    return hero_db


@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(
    hero_id: int,
    hero: HeroUpdate,
    session: SessionDep,
) -> Any:  # noqa: ANN401
    """Path operation for the PATCH hero by ID endpoint."""
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hero not found",
        )
    hero_dict = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_dict)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db


@app.delete("/heroes/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hero(hero_id: int, session: SessionDep) -> None:
    """Path operation for the DELETE hero by ID endpoint."""
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hero not found",
        )
    session.delete(hero_db)
    session.commit()
