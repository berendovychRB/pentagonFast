import datetime
from typing import Optional

from pydantic import BaseModel


# Form with fields which is required in creating or updating
class User(BaseModel):
    email: str
    name: str
    hashed_password: str
    is_admin: bool


# Form for returning instance with fields which are writen here (In my case, all fields without password Field)
class ShowUser(BaseModel):

    id: int
    email: str
    name: str
    is_admin: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    # ONLY FOR DEBUG
    hashed_password: str

    class Config:
        orm_mode = True


class Login(BaseModel):
    email: str
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
