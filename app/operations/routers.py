from fastapi import APIRouter
from app.database import mongo_db
from app.operations.models import Extract

router = APIRouter(tags=['Operations'], prefix='/extracts')


@router.get('/')
def list_extracts():
    extracts = []
    for extract in mongo_db.extract.find():
        extracts.append(Extract(**extract))
    return extracts
