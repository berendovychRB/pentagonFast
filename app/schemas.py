from pydantic import BaseModel


class User(BaseModel):
    email: str
    name: str
    hashed_password: str
    is_admin: bool
