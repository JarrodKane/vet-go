"""
SQL Alchemy models declaration.
https://docs.sqlalchemy.org/en/14/orm/declarative_styles.html#example-two-dataclasses-with-declarative-table
Dataclass style for powerful autocompletion support.

https://alembic.sqlalchemy.org/en/latest/tutorial.html
Note, it is used by alembic migrations logic, see `alembic/env.py`

Alembic shortcuts:
# create migration
alembic revision --autogenerate -m "migration_name"

# apply all migrations
alembic upgrade head
"""
import uuid

from sqlalchemy import String, ForeignKey, Boolean, Table, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __abstract__ = True
    road: Mapped[str] = mapped_column(String(254), nullable=True)
    city: Mapped[str] = mapped_column(String(254), nullable=True)
    state: Mapped[str] = mapped_column(String(254), nullable=True)
    zip: Mapped[str] = mapped_column(String(254), nullable=True)
    country: Mapped[str] = mapped_column(String(254), nullable=True)
    pass

#  Many to many association table
association_table = Table(
    "animal_user_association",
    Base.metadata,
    Column("animal_id", ForeignKey("animal.id")),
    Column("user_id", ForeignKey("user_model.id")),
)


class User(Base):
    __tablename__ = "user_model"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    email: Mapped[str] = mapped_column(
        String(254), nullable=False, unique=True, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    name: Mapped[str] = mapped_column(String(254), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(128), nullable=True)
    animals: Mapped[list] = relationship(
        "Animal",
        secondary=association_table,
        back_populates="owners",
    )

# An animal might belong to multiple users
# An user might have multiple animals

class Animal(Base):
    __tablename__ = "animal"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    identifier: Mapped[str] = mapped_column(String(254), nullable=True)
    name: Mapped[str] = mapped_column(String(254), nullable=True)
    age: Mapped[int] = mapped_column(String(128), nullable=True)
    sex: Mapped[str] = mapped_column(String(50), nullable=True)
    weight: Mapped[int] = mapped_column(String(128), nullable=True)
    height: Mapped[int] = mapped_column(String(128), nullable=True)
    type: Mapped[str] = mapped_column(String(128), nullable=False)
    color: Mapped[str] = mapped_column(String(128), nullable=True)
    description: Mapped[str] = mapped_column(String(128), nullable=True)
    image: Mapped[str] = mapped_column(String(128), nullable=True)
    same_address_as_owner: Mapped[bool] = mapped_column(Boolean, nullable=True)
    owners: Mapped[list] = relationship(
        "User",
        secondary=association_table,
        back_populates="animals",
    )
    