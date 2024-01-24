import asyncio
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import config, security
from app.core.session import async_engine, async_session
from app.main import app
from app.models import Base, User, Animal
from app.models import AnimalType
from datetime import datetime




default_user_id = "b75365d9-7bf9-4f54-add5-aeab333a087b"
default_user_email = "geralt@wiedzmin.pl"
default_user_password = "geralt"
default_user_password_hash = security.get_password_hash(default_user_password)
default_user_access_token = security.create_jwt_token(
    str(default_user_id), 60 * 60 * 24, refresh=False
)[0]


default_animal1_id = "79909c98-f3fc-4137-a2a4-d8d6a6e8900e"
default_animal1_name = "Animal1"
default_animal1_types = AnimalType.Dog
default_animal1_date_of_birth = datetime.strptime("2022-01-01", "%Y-%m-%d").date()
default_animal1_active = True

default_animal2_id = "c6697bb9-8afc-42e3-b32d-c7b50c2c3457"
default_animal2_name = "Animal2"
default_animal2_types = AnimalType.Cat
default_animal2_date_of_birth = datetime.strptime("2022-01-02", "%Y-%m-%d").date()
default_animal2_active = False


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_db_setup_sessionmaker():
    # assert if we use TEST_DB URL for 100%
    assert config.settings.ENVIRONMENT == "PYTEST"

    # always drop and create test db tables between tests session
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(autouse=True)
async def session(test_db_setup_sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

        # delete all data from all tables after test
        for name, table in Base.metadata.tables.items():
            await session.execute(delete(table))
        await session.commit()


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        client.headers.update({"Host": "localhost"})
        yield client


@pytest_asyncio.fixture
async def default_user(test_db_setup_sessionmaker) -> User:
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.email == default_user_email)
        )
        user = result.scalars().first()
        if user is None:
            new_user = User(
                email=default_user_email,
                hashed_password=default_user_password_hash,
            )
            new_user.id = default_user_id
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user
        return user


@pytest.fixture
def default_user_headers(default_user: User):
    return {"Authorization": f"Bearer {default_user_access_token}"}




@pytest.fixture(autouse=True)
async def default_animal1(test_db_setup_sessionmaker, default_user: User) -> Animal:
    async with async_session() as session:
        result = await session.execute(
            select(Animal).where(Animal.id == default_animal1_id)
        )
        animal = result.scalars().first()
        if animal is None:
            new_animal = Animal(
                id=default_animal1_id,
                name=default_animal1_name,
                animal_types=default_animal1_types,
                date_of_birth=default_animal1_date_of_birth,
                active=default_animal1_active,
            )
            new_animal.owners.append(default_user)
            session.add(new_animal)
            await session.commit()
            await session.refresh(new_animal)
            return new_animal
        return animal

@pytest.fixture(autouse=True)
async def default_animal2(test_db_setup_sessionmaker, default_user: User) -> Animal:
    async with async_session() as session:
        result = await session.execute(
            select(Animal).where(Animal.id == default_animal2_id)
        )
        animal = result.scalars().first()
        if animal is None:
            new_animal = Animal(
                id=default_animal2_id,
                name=default_animal2_name,
                animal_types=default_animal2_types,
                date_of_birth=default_animal2_date_of_birth,
                active=default_animal2_active,
            )
            new_animal.owners.append(default_user)
            session.add(new_animal)
            await session.commit()
            await session.refresh(new_animal)
            return new_animal
        return animal

