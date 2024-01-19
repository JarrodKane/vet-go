# /app/tests/test_animals.py
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.main import app
from app.models import Animal, User



async def test_get_all_my_animals(
    client: AsyncClient, default_user_headers, default_user: User, session: AsyncSession
):
    animalDefault = Animal(name="animal_1", type='dog')
    animalDefault.owners.append(default_user)
    session.add(animalDefault)
    await session.commit()

    response = await client.get(
        app.url_path_for("create_new_animal"),
        headers=default_user_headers,
    )
    assert response.status_code == 200

    response_data = response.json()
    expected_data = {
            "name": animalDefault.name,
            "id": animalDefault.id,
        }
    
    assert len(response_data) == len(expected_data)
    for expected_item in expected_data:
        assert expected_item in response_data


async def test_get_all_my_animals(
    client: AsyncClient, default_user_headers, default_user: User, session: AsyncSession
):
    animal1 = Animal(name="animal_1", type='dog')
    animal1.owners.append(default_user)
    animal2 = Animal(name="animal_2" , type='cat')
    animal2.owners.append(default_user)
    session.add(animal1)
    session.add(animal2)
    await session.commit()

    response = await client.get(
        app.url_path_for("get_all_animals"),
        headers=default_user_headers,
    )
    assert response.status_code == 200

    response_data = response.json()
    expected_data = [
        {
            # "user_id": default_user.id,
            "name": animal1.name,
            "id": animal1.id,
        },
        {
            # "user_id": default_user.id,
            "name": animal2.name,
            "id": animal2.id,
        },
    ]

    assert len(response_data) == len(expected_data)
    for expected_item in expected_data:
        assert expected_item in response_data