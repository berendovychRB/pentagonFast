import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# Form with fields which is required in creating or updating
class User(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    hashed_password: Optional[str] = None
    is_admin: Optional[bool] = None

    class Config:
        orm_mode = True


class Register(BaseModel):
    email: EmailStr
    name: str
    hashed_password: str


# Form for returning instance with fields which are writen here (In my case, all fields without password Field)
class ShowUser(BaseModel):
    id: int
    email: EmailStr
    name: str
    is_admin: bool

    # ONLY FOR DEBUG
    hashed_password: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class Login(BaseModel):
    email: EmailStr
    hashed_password: str
