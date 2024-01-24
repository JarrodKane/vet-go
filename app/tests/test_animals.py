# /app/tests/test_animals.py
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import joinedload
from app.schemas.responses import AnimalBaseResponse
from fastapi import status



from app.main import app
from app.models import Animal, User

async def test_create_new_animal(
    client: AsyncClient, default_user_headers, session: AsyncSession
):
    animal_data = {
        "name": "animal_1",
        "animal_types": "Dog",
        "date_of_birth": datetime.strptime("2022-01-01", "%Y-%m-%d").date().isoformat(),
        "active": True
    }

    response = await client.post(
        app.url_path_for("create_new_animal"),
        headers=default_user_headers,
        json=animal_data,
    )
    assert response.status_code == 201

    response_data = response.json()
    expected_data = {
        "id": response_data["id"], 
        "name": animal_data["name"],
        "animal_types": animal_data["animal_types"],
        "date_of_birth": datetime.strptime("2022-01-01", "%Y-%m-%d").date().isoformat(),
        "active": animal_data["active"],
        "owners": response_data["owners"],
    }

    
    assert len(response_data) == len(expected_data)
    for key, expected_value in expected_data.items():
        assert key in response_data
    if key == "owners":
        assert isinstance(response_data[key], list)  # Check that 'owners' is a list
    else:
        assert response_data[key] == expected_value


async def test_get_all_animals(
    client: AsyncClient,
    default_user_headers,
    default_animal1: Animal,
    default_animal2: Animal
):
    # Retrieve all animals
    response = await client.get(
        app.url_path_for("get_all_animals"), headers=default_user_headers
    )

    assert response.status_code == status.HTTP_200_OK

    # Validate response
    animals = [AnimalBaseResponse.model_validate(animal) for animal in response.json()]
    assert len(animals) >= 2  # Expect at least the two default animals

    # Check that the default animals are in the response
    animal_ids = [animal.id for animal in animals]
    assert default_animal1.id in animal_ids
    assert default_animal2.id in animal_ids

    # Check attributes of each animal
    for animal in animals:
        assert all([
            animal.id is not None,
            animal.name is not None,
            animal.animal_types is not None,
            animal.date_of_birth is not None,
            animal.active is not None
        ])



async def test_update_animal(
    client: AsyncClient,
    default_user_headers,
    default_animal1: Animal,
    session: AsyncSession
):
    animal_data = {
        "identifier": "1234",
        "name": "animal_1",
        "sex": "Male",
        "height": 1.5,
        "animal_types": "Dog",
        "color": "Brown",
        "description": "A brown dog",
        "image": "dog.jpg",
        "date_of_death": None,
        "active": True
    }

    response = await client.patch(
        app.url_path_for("update_animal", animal_id=default_animal1.id),
        headers=default_user_headers,
        json=animal_data,
    )
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    expected_data = {
        "id": response_data["id"], 
        "identifier": animal_data["identifier"],
        "name": animal_data["name"],
        "sex": animal_data["sex"],
        "height": animal_data["height"],
        "animal_types": animal_data["animal_types"],
        "color": animal_data["color"],
        "description": animal_data["description"],
        "image": animal_data["image"],
        "date_of_death": animal_data["date_of_death"],
        "active": animal_data["active"],
        "owners": response_data["owners"],
    }

    assert len(response_data) == len(expected_data)
    for key, expected_value in expected_data.items():
        assert key in response_data
    if key == "owners":
        assert isinstance(response_data[key], list)  # Check that 'owners' is a list
    else:
        assert response_data[key] == expected_value



async def test_update_animal_weight(
    client: AsyncClient,
    default_user_headers,
    default_animal1: Animal,
    session: AsyncSession
):
    animal_data = {
        "weight": 1.5,
        "change_date": datetime.strptime("2022-01-01", "%Y-%m-%d").date().isoformat(),
        "animal_id": default_animal1.id
    }

    response = await client.post(
        app.url_path_for("add_weight", animal_id=default_animal1.id),
        headers=default_user_headers,
        json=animal_data,
    )
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    expected_data = {
        "weight": animal_data["weight"],
        "change_date": animal_data["change_date"],
        "animal_id": animal_data["animal_id"]
    }

    assert len(response_data) == len(expected_data)
    for key, expected_value in expected_data.items():
        assert key in response_data
    assert response_data[key] == expected_value
        














