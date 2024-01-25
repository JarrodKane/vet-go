"""
Put here any Python code that must be runned before application startup.
It is included in `init.sh` script.

By defualt `main` create a superuser if not exists
"""

import asyncio

from sqlalchemy import select

from app.core import config, security
import uuid

from app.core.session import async_session
from app.models import User, Animal, AnimalType
from datetime import date


async def main() -> None:
    print("Start initial data")
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.email == config.settings.FIRST_SUPERUSER_EMAIL)
        )
        user = result.scalars().first()

        if user is None:
            new_superuser = User(
                email=config.settings.FIRST_SUPERUSER_EMAIL,
                hashed_password=security.get_password_hash(
                    config.settings.FIRST_SUPERUSER_PASSWORD
                ),
            )
            session.add(new_superuser)
            await session.commit()
            print("Superuser was created")
        else:
            print("Superuser already exists in database")

        # result = await session.execute(select(Animal).where(Animal.id == uuid.UUID('877b4aa9-4feb-4cc6-aee9-d87a60064d01')))
        # animal1 = result.scalars().first()
        # if animal1 is None:
        #     animal1 = Animal(id=uuid.UUID('877b4aa9-4feb-4cc6-aee9-d87a60064d01'), name="Animal1", animal_types=AnimalType.Dog.value, date_of_birth=date.today())
        #     animal1.owners.append(user)
        #     session.add(animal1)

        # user.animals = [animal1, animal2]
        # await session.commit()
        print("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())
