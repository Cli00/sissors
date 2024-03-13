from pydantic import BaseModel, EmailStr
from typing import Union
from pydantic import BaseModel

class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class usercreate(User):
    pass

class UserLogin(BaseModel):
    email: EmailStr
    password: Union[str, int]

class URLbase(BaseModel):
    user_id: str
    original_url: str

class urlhistory(BaseModel):
    user_id: str

