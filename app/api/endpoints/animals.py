from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import subqueryload

from app.api import deps
from app.models import Animal, User, AnimalWeightHistory
from app.schemas.requests import (
    AnimalCreateRequest,
    AnimalUpdateRequest,
    AnimalWeightHistoryCreateRequest,
)
from app.schemas.responses import (
    AnimalBaseResponse,
    AnimalExtendedResponse,
    AnimalWeightHistoryResponse,
)
from app.utils.services import update_record
from datetime import datetime
from datetime import datetime, timedelta

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
        select(Animal)
        .options(subqueryload(Animal.owners))
        .where(Animal.owners.any(id=current_user.id))
    )
    animals = result.scalars().all()
    return animals


# ------------------
# Animal by ID update
# ------------------


@router.patch(
    "/update/{animal_id}", response_model=AnimalExtendedResponse, status_code=200
)
async def update_animal(
    animal_id: str,
    animal_update: AnimalUpdateRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """Updates animal. Only for logged users."""

    result = await session.execute(
        select(Animal)
        .options(subqueryload(Animal.owners))
        .where(Animal.owners.any(id=current_user.id))
        .where(Animal.id == animal_id)
    )
    animal = result.scalars().first()
    new_values = animal_update.model_dump(exclude_unset=True)
    await update_record(session, animal, new_values)
    return animal


# ------------------
# Weight History
# ------------------


@router.post(
    "/weight/{animal_id}", response_model=AnimalWeightHistoryResponse, status_code=200
)
async def add_weight(
    animal_id: str,
    weight_history_create: AnimalWeightHistoryCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """Adds weight to animal. Only for logged users."""

    result = await session.execute(
        select(Animal)
        .options(subqueryload(Animal.owners))
        .where(Animal.owners.any(id=current_user.id))
        .where(Animal.id == animal_id)
    )
    animal = result.scalars().first()

    if animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")

    weight_history = AnimalWeightHistory(
        **weight_history_create.model_dump(), animal_id=animal.id
    )
    naive_change_date = weight_history_create.change_date.replace(tzinfo=None)
    weight_history.change_date = naive_change_date
    session.add(weight_history)

    await session.commit()

    return AnimalWeightHistoryResponse(
        id=weight_history.id,
        weight=weight_history_create.weight,
        change_date=weight_history_create.change_date,
    )


# Alter animal weight history with put, this is for that specifc animal weight history


@router.put(
    "/weight/{animal_id}/{history_id}",
    response_model=AnimalWeightHistoryResponse,
    status_code=200,
)
async def alter_weight(
    animal_id: str,
    history_id: str,
    weight_history_create: AnimalWeightHistoryCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """Adds weight to animal. Only for logged users."""

    result = await session.execute(
        select(Animal)
        .options(subqueryload(Animal.owners))
        .where(Animal.owners.any(id=current_user.id))
        .where(Animal.id == animal_id)
    )
    animal = result.scalars().first()

    result = await session.execute(
        select(AnimalWeightHistory)
        .where(AnimalWeightHistory.id == history_id)
        .where(AnimalWeightHistory.animal_id == animal_id)
    )

    weight_history = result.scalars().first()

    if weight_history is None:
        raise HTTPException(status_code=404, detail="Weight history not found")

    weight_history.weight = weight_history_create.weight
    naive_change_date = weight_history_create.change_date.replace(tzinfo=None)
    weight_history.change_date = naive_change_date

    new_values = weight_history_create.model_dump(exclude_unset=True)
    new_values["change_date"] = naive_change_date

    await update_record(session, weight_history, new_values)

    return AnimalWeightHistoryResponse(
        id=weight_history.id,
        weight=weight_history.weight,
        change_date=weight_history.change_date,
    )


# Deleting the weight selected


@router.delete(
    "/weight/{animal_id}/{history_id}",
    response_model=AnimalWeightHistoryResponse,
    status_code=200,
)
async def delete_weight(
    animal_id: str,
    history_id: str,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """Deletes weight history for an animal. Only for logged users."""

    result = await session.execute(
        select(Animal)
        .options(subqueryload(Animal.owners))
        .where(Animal.owners.any(id=current_user.id))
        .where(Animal.id == animal_id)
    )

    result = await session.execute(
        select(AnimalWeightHistory)
        .where(AnimalWeightHistory.id == history_id)
        .where(AnimalWeightHistory.animal_id == animal_id)
    )
    weight_history = result.scalars().first()

    if weight_history is None:
        raise HTTPException(status_code=404, detail="Weight history not found")

    response = AnimalWeightHistoryResponse(
        id=weight_history.id,
        weight=weight_history.weight,
        change_date=weight_history.change_date,
    )

    await session.delete(weight_history)
    await session.commit()

    return response


# Get all weight history for an animal


@router.get(
    "/weight/{animal_id}",
    response_model=list[AnimalWeightHistoryResponse],
    status_code=200,
)
async def get_weight_history(
    animal_id: str,
    range: int = 1,
    unit: str = "days",
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """Gets weight history for an animal. Only for logged users."""

    result = await session.execute(
        select(Animal)
        .options(subqueryload(Animal.owners))
        .where(Animal.owners.any(id=current_user.id))
        .where(Animal.id == animal_id)
    )

    result = await session.execute(
        select(AnimalWeightHistory).where(AnimalWeightHistory.animal_id == animal_id)
    )
    weight_history = result.scalars().all()

    if unit == "days":
        start_date = datetime.now() - timedelta(days=range)
    elif unit == "weeks":
        start_date = datetime.now() - timedelta(weeks=range)
    elif unit == "months":
        start_date = datetime.now() - timedelta(days=30 * range)
    elif unit == "years":
        start_date = datetime.now() - timedelta(days=365 * range)
    elif unit == "all":
        start_date = datetime.min
    else:
        raise HTTPException(status_code=400, detail="Invalid unit")

    filtered_weight_history = [
        AnimalWeightHistoryResponse(
            id=wh.id, weight=wh.weight, change_date=wh.change_date
        )
        for wh in weight_history
        if wh.change_date >= start_date
    ]

    return filtered_weight_history
