from typing import List
from pydantic import BaseModel, ConfigDict, EmailStr
from app.models import AnimalType
from datetime import date, datetime

from typing import Optional


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AccessTokenResponse(BaseResponse):
    token_type: str
    access_token: str
    expires_at: int
    issued_at: int
    refresh_token: str
    refresh_token_expires_at: int
    refresh_token_issued_at: int


class UserResponse(BaseResponse):
    id: str
    email: EmailStr

class AnimalBaseResponse(BaseResponse):
    id: str 
    name: str
    animal_types : AnimalType
    date_of_birth : date
    active : bool
    owners: List[UserResponse] = []


class AnimalExtendedResponse(BaseResponse):
    id: str 
    name: str
    animal_types: AnimalType
    active: bool
    identifier: Optional[str] = None
    sex: Optional[str] = None
    height: Optional[float] = None
    color: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    date_of_death: Optional[date] = None
    owners: Optional[List[UserResponse]] = None

class AnimalWeightHistoryResponse(BaseModel):
    weight: float
    change_date: datetime
    # animal_id: str