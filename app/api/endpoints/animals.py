from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import subqueryload

from app.api import deps
from app.models import Animal, User
from app.schemas.requests import AnimalCreateRequest, AnimalUpdateRequest, AnimalWeightHistoryCreateRequest
from app.schemas.responses import AnimalBaseResponse, AnimalExtendedResponse, AnimalWeightHistoryResponse
from app.utils.services import update_record
from datetime import datetime




router = APIRouter()


@router.post("/create", response_model=AnimalBaseResponse, status_code=201)
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



@router.get("/all", response_model=list[AnimalBaseResponse], status_code=200)
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



@router.patch("/update/{animal_id}", response_model=AnimalExtendedResponse, status_code=200)
async def update_animal(
    animal_id: str,
    animal_update: AnimalUpdateRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """Updates animal. Only for logged users."""

    result = await session.execute(
        select(Animal).options(subqueryload(Animal.owners)).where(Animal.owners.any(id=current_user.id)).where(Animal.id == animal_id)
    )
    animal = result.scalars().first()
    new_values = animal_update.model_dump(exclude_unset=True)
    await update_record(session, animal, new_values)
    return animal




@router.post('/weight/{animal_id}', response_model=AnimalWeightHistoryResponse, status_code=200)
async def add_weight(
    animal_id: str,
    weight_history_create: AnimalWeightHistoryCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """Adds weight to animal. Only for logged users."""

    result = await session.execute(
        select(Animal).options(subqueryload(Animal.owners)).where(Animal.owners.any(id=current_user.id)).where(Animal.id == animal_id)
    )
    animal = result.scalars().first()

    weight_history_create.change_date = datetime.now()
    weight_history = AnimalWeightHistoryCreateRequest(**weight_history_create.model_dump())
    new_values = {"weight_history": animal.weight_history}


    await update_record(session, animal, new_values)
    return weight_history
