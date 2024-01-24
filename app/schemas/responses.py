from typing import List
from pydantic import BaseModel, ConfigDict, EmailStr
from app.models import AnimalType  
from datetime import date


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

class AnimalResponse(BaseResponse):
    id: str 
    name: str
    animal_types : AnimalType
    date_of_birth : date
    active : bool
    owners: List[UserResponse] = []