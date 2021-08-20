from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

from app.operations.validators import PyObjectId


class Extract(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    card: str
    appcode: str
    trandate: str
    amount: str
    cardamount: str
    rest: str
    terminal: str
    description: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
