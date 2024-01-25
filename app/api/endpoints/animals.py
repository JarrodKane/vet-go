from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import subqueryload
from typing import List

from app.api import deps
from app.models import Animal, User, AnimalWeightHistory, AnimalLog, ActivityTypes
from app.schemas.requests import (
    AnimalCreateRequest,
    AnimalUpdateRequest,
    AnimalWeightHistoryCreateRequest,
    AnimalLogCreateRequest
)
from app.api.endpoints.utils import TimeUnit
from app.schemas.responses import (
    AnimalBaseResponse,
    AnimalExtendedResponse,
    AnimalWeightHistoryResponse, AnimalLogResponse
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


@router.delete("/delete/{animal_id}", response_model=AnimalBaseResponse, status_code=200)
async def delete_animal(
    animal_id: str,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """Deletes animal. Only for logged users."""

    result = await session.execute(
        select(Animal)
        .options(subqueryload(Animal.owners))
        .where(Animal.owners.any(id=current_user.id))
        .where(Animal.id == animal_id)
    )
    animal = result.scalars().first()
    if animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")

    await session.delete(animal)
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
    unit: TimeUnit = TimeUnit.DAYS,
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

    if unit == TimeUnit.DAYS:
        start_date = datetime.now() - timedelta(days=range)
    elif unit == TimeUnit.WEEKS:
        start_date = datetime.now() - timedelta(weeks=range)
    elif unit == TimeUnit.MONTHS:
        start_date = datetime.now() - timedelta(days=30 * range)
    elif unit == TimeUnit.YEARS:
        start_date = datetime.now() - timedelta(days=365 * range)
    elif unit == TimeUnit.ALL:
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

    
@router.post("/log/{animal_id}", response_model=AnimalLogResponse, status_code=200)
async def add_log(
        animal_id: str,
        log_create: AnimalLogCreateRequest,
        session: AsyncSession = Depends(deps.get_session),
        current_user: User = Depends(deps.get_current_user),
    ):
    """Adds log to animal. Only for logged users."""
    # Check if animal exists
    result = await session.execute(
        select(Animal)
        .options(subqueryload(Animal.owners))
        .where(Animal.owners.any(id=current_user.id))
        .where(Animal.id == animal_id)
    )
    animal = result.scalars().first()
    if animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")

    # Create AnimalLog
    animal_log = AnimalLog(
        animal_id=animal_id,
        date=log_create.date.replace(tzinfo=None),
        activity=log_create.activity,
        comments=log_create.comments,
    )

    session.add(animal_log)
    await session.commit()
    await session.refresh(animal_log)

    return animal_log
    
    
# need the put, delete, and get for the animal logs, very similar to the weights above
# ------------------

@router.put("/log/{log_id}", response_model=AnimalLogResponse, status_code=200)
async def update_log(
        log_id: str,
        log_update: AnimalLogCreateRequest,
        session: AsyncSession = Depends(deps.get_session),
        current_user: User = Depends(deps.get_current_user),
    ):
    """Updates log. Only for logged users."""
    # Check if log exists
    result = await session.execute(
        select(AnimalLog)
        .where(AnimalLog.id == log_id)
    )
    log = result.scalars().first()
    if log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    # date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    # Update log
    log.date = log_update.date.replace(tzinfo=None)
    log.activity = log_update.activity.name
    log.comments = log_update.comments

    await session.commit()
    await session.refresh(log)

    return log



@router.get("/log/{animal_id}", response_model=List[AnimalLogResponse], status_code=200)
async def get_log(
        animal_id: str,
        activity_types: List[ActivityTypes] = Query([], description="List of activity types to filter by"),
        range: int = 1,
        unit: TimeUnit = TimeUnit.DAYS,
        session: AsyncSession = Depends(deps.get_session),
        current_user: User = Depends(deps.get_current_user),
    ):
    """Gets logs for an animal filtered by activity type. Only for logged users."""
    # Check if animal exists
    result = await session.execute(
        select(Animal)
        .options(subqueryload(Animal.owners))
        .where(Animal.owners.any(id=current_user.id))
        .where(Animal.id == animal_id)
    )
    animal = result.scalars().first()
    if animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")

    # Calculate start date based on range and unit
    if unit == TimeUnit.DAYS:
        start_date = datetime.now() - timedelta(days=range)
    elif unit == TimeUnit.WEEKS:
        start_date = datetime.now() - timedelta(weeks=range)
    elif unit == TimeUnit.MONTHS:
        start_date = datetime.now() - timedelta(days=30 * range)
    elif unit == TimeUnit.YEARS:
        start_date = datetime.now() - timedelta(days=365 * range)
    elif unit == TimeUnit.ALL:
        start_date = datetime.min
    else:
        raise HTTPException(status_code=400, detail="Invalid unit")

    # Get logs filtered by activity type and date
    if ActivityTypes.all in activity_types or not activity_types:
        result = await session.execute(
            select(AnimalLog)
            .where(
                and_(
                    AnimalLog.animal_id == animal_id,
                    AnimalLog.date >= start_date
                )
            )
        )
    else:
        activity_names = [activity_type.name for activity_type in activity_types]
        result = await session.execute(
            select(AnimalLog)
            .where(
                and_(
                    AnimalLog.animal_id == animal_id,
                    AnimalLog.activity.in_(activity_names),
                    AnimalLog.date >= start_date
                )
            )
        )

    logs = result.scalars().all()

    return logs
    
@router.delete("/log/{log_id}", response_model=AnimalLogResponse, status_code=200)
async def delete_log(
        log_id: str,
        session: AsyncSession = Depends(deps.get_session),
        current_user: User = Depends(deps.get_current_user),
    ):
    """Deletes log. Only for logged users."""
    # Check if log exists
    result = await session.execute(
        select(AnimalLog)
        .where(AnimalLog.id == log_id)
    )
    log = result.scalars().first()
    if log is None:
        raise HTTPException(status_code=404, detail="Log not found")

    # Delete log
    await session.delete(log)
    await session.commit()

    return log
    
