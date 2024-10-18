"""Models for the Dizziness Tracker."""

from datetime import UTC, date, datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import Engine, ForeignKey, create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
)


class DizzinessLevel(Enum):
    """Enumeration with the levels of dizziness."""

    level_0_not_dizzy = 0
    level_1_slightly_dizzy = 1
    level_2_dizzy = 2
    level_3_quite_dizzy = 3
    level_4_very_dizzy = 4
    level_5_super_dizzy = 5


def generate_uuid() -> str:
    """Generate a UUID v4 to be used for the primary key in the models."""
    return str(uuid4())


class Base(DeclarativeBase):
    """Acquiring a new Declarative Base by subclassing DeclarativeBase."""


class LevelModel(Base):
    """Represents the dizziness level in the data layer."""

    __tablename__ = "level"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=generate_uuid,
    )
    level: Mapped[DizzinessLevel] = mapped_column(nullable=False, unique=True)
    description: Mapped[str]
    symptoms: Mapped[list["SymptomModel"]] = relationship(
        back_populates="level",
    )
    entries: Mapped[list["JournalEntryModel"]] = relationship(
        back_populates="level",
    )

    def __repr__(self) -> str:
        """Developer-level string representation of LevelModel."""
        return (
            f"LevelModel(id={self.id}, level={self.level}, "
            f"description={self.description})"
        )


class SymptomModel(Base):
    """Represents a dizziness symptom in the data layer."""

    __tablename__ = "symptom"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=generate_uuid,
    )
    description: Mapped[str] = mapped_column(nullable=False)
    level_id = mapped_column(ForeignKey("level.id"))
    level: Mapped[LevelModel] = relationship(back_populates="symptoms")

    def __repr__(self) -> str:
        """Developer-level string representation of SymptomModel."""
        return f"SymptomModel(id={self.id}, description={self.description})"


class JournalEntryModel(Base):
    """Represents a dizziness journal entry in in the data layer."""

    __tablename__ = "entry"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=generate_uuid,
    )
    day: Mapped[date] = mapped_column(
        unique=True,
        default=datetime.now(tz=UTC).date(),
    )
    remarks: Mapped[str | None]
    level_id = mapped_column(ForeignKey("level.id"))
    level: Mapped[LevelModel] = relationship(back_populates="entries")

    def __repr__(self) -> None:
        """Developer-level representation of a JournalEntryModel."""
        return (
            f"JournalEntryModel(id={self.id}, day={self.day}, "
            f"remarks={self.remarks})"
        )


def create_db_tables(engine: Engine) -> None:
    """
    Create db tables by having a look at all the mapped classes registered in
    the metadata object.
    """
    metadata_obj = Base.metadata
    metadata_obj.create_all(engine)
    print("Tables created!")


if __name__ == "__main__":
    # create tables
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

    create_db_tables(engine)

    # add some levels
    with Session(engine) as session:
        session.add(
            LevelModel(
                level=DizzinessLevel.level_0_not_dizzy,
                description="Level 0: not dizzy",
                symptoms=[
                    SymptomModel(
                        description=(
                            "No symptoms, as before or after having an "
                            "episode"
                        ),
                    ),
                    SymptomModel(
                        description="Fully functional",
                    ),
                ],
            ),
        )
        session.add(
            LevelModel(
                level=DizzinessLevel.level_1_slightly_dizzy,
                description="Level 1: slightly dizzy",
                symptoms=[
                    SymptomModel(
                        description="A little light-headed",
                    ),
                    SymptomModel(
                        description="Ear ringing",
                    ),
                    SymptomModel(
                        description=(
                            "Can work, jog, walk, and eat without issues"
                        ),
                    ),
                    SymptomModel(
                        description="Still functional",
                    ),
                ],
            ),
        )
        session.add(
            LevelModel(
                level=DizzinessLevel.level_2_dizzy,
                description="Level 2: dizzy",
                symptoms=[
                    SymptomModel(
                        description="Feeling uncomfortable",
                    ),
                    SymptomModel(
                        description="Notable ear ringing",
                    ),
                    SymptomModel(
                        description="Can work, jog, eat",
                    ),
                    SymptomModel(
                        description="No stomach issues",
                    ),
                ],
            ),
        )
        session.add(
            LevelModel(
                level=DizzinessLevel.level_3_quite_dizzy,
                description="Level 3: quite dizzy",
                symptoms=[
                    SymptomModel(
                        description=(
                            "Having problems walking, while looking down"
                        ),
                    ),
                    SymptomModel(
                        description=(
                            "Can work but cannot focus properly on tasks"
                        ),
                    ),
                    SymptomModel(
                        description="Could run, but don't feel like to",
                    ),
                    SymptomModel(
                        description="Bad stomach but not puking, can eat",
                    ),
                ],
            ),
        )
        session.add(
            LevelModel(
                level=DizzinessLevel.level_4_very_dizzy,
                description="Level 4: very dizzy",
                symptoms=[
                    SymptomModel(
                        description=(
                            "Don't feel like walking, can barely walk"
                        ),
                    ),
                    SymptomModel(
                        description=("Don't feel like working or running"),
                    ),
                    SymptomModel(
                        description="No appetite",
                    ),
                ],
            ),
        )
        session.add(
            LevelModel(
                level=DizzinessLevel.level_5_super_dizzy,
                description="Level 5: super dizzy",
                symptoms=[
                    SymptomModel(
                        description=("Must be in bed or sitting down"),
                    ),
                    SymptomModel(
                        description=("Can't eat, puking"),
                    ),
                    SymptomModel(
                        description="Halo effect in sight",
                    ),
                ],
            ),
        )
        session.commit()

    with Session(engine) as session:
        # retrieve all levels
        stmt = select(LevelModel)
        for level in session.scalars(stmt).all():
            print(f"{level=}")

        # get a level and navigate to symptoms
        stmt = select(LevelModel).where(
            LevelModel.level == DizzinessLevel.level_1_slightly_dizzy
        )
        level1 = session.scalars(stmt).first()
        print(f"{level1=}")
        print(f"level1 symptoms={level1.symptoms}")

    # create an entry for level 1
    with Session(engine) as session:
        session.add(
            JournalEntryModel(
                remarks="Late evening meetings; neck hurts.",
                level=level1,
            ),
        )
        session.commit()

    # retrieve entry and navigate to symptoms
    with Session(engine) as session:
        stmt = select(JournalEntryModel).where(
            JournalEntryModel.day == datetime.now(tz=UTC).date(),
        )
        entry = session.scalars(stmt).first()
        print(f"{entry=}")
        for symptom in entry.level.symptoms:
            print(f"{symptom.description}")
