from pydantic import BaseModel, EmailStr
from typing import Union
from pydantic import BaseModel
from uuid import UUID

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: Union[str, int]

class UserLogin(BaseModel):
    email: EmailStr
    password: Union[str, int]

class URLbase(BaseModel):
    id: UUID
    original_url: str
    shortened_url: str