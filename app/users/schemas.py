from typing import Optional

from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    email: Optional[EmailStr]
    name: str
    is_admin: bool


class User(BaseUser):
    id: Optional[int]
    hashed_password: str

    class Config:
        orm_mode = True


class UserCreate(BaseUser):
    hashed_password: str

    class Config:
        orm_mode = True



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
