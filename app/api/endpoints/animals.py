from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import Animal, User
from app.schemas.requests import AnimalCreateRequest
from app.schemas.responses import AnimalResponse

from sqlalchemy.orm import joinedload
from sqlalchemy.orm import subqueryload


router = APIRouter()


@router.post("/create", response_model=AnimalResponse, status_code=201)
async def create_new_animal(
    new_animal: AnimalCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """Creates new animal. Only for logged users."""

    animal = Animal(
        name=new_animal.name,
        animal_types=new_animal.animal_types,
        date_of_birth=new_animal.date_of_birth,
        active=new_animal.active,
    )
    animal.owners.append(current_user)
    
    session.add(animal)
    await session.commit()
    return animal




@router.get("/all", response_model=list[AnimalResponse], status_code=200)
async def get_all_animals(
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """Returns all animals. Only for logged users."""

    result = await session.execute(
        select(Animal).options(subqueryload(Animal.owners)).where(Animal.owners.any(id=current_user.id))
    )
    animals = result.scalars().all()
    return animals