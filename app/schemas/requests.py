from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime
from app.models import AnimalType


class BaseRequest(BaseModel):
    # may define additional fields or config shared across requests
    pass


class RefreshTokenRequest(BaseRequest):
    refresh_token: str


class UserUpdatePasswordRequest(BaseRequest):
    password: str


class UserCreateRequest(BaseRequest):
    email: EmailStr
    password: str


class UserUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    mobile_number: Optional[str] = None
    road: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None
    phone_number: Optional[str] = None


# ------------------
# Animals
# ------------------


class AnimalCreateRequest(BaseModel):
    name: str
    animal_types: AnimalType
    date_of_birth: date
    active: bool = True


class AnimalUpdateRequest(BaseModel):
    identifier: Optional[str]
    name: Optional[str]
    sex: Optional[str]
    height: Optional[float]
    animal_types: Optional[AnimalType]
    color: Optional[str]
    description: Optional[str]
    image: Optional[str]
    date_of_death: Optional[date]
    active: Optional[bool]


class AnimalWeightHistoryCreateRequest(BaseModel):
    weight: float
    change_date: datetime
