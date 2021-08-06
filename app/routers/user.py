from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import schemas
from .. import database
from app.repository import user
from ..repository.user import get_current_user

router = APIRouter(
    prefix='/user',
    tags=['Users']
)
get_db = database.get_db


@router.get('/all', response_model=List[schemas.ShowUser])
def all_users(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return user.get_all(db)


# Method is needed to fix updated_at Field
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ShowUser)
def update(id: int, request: schemas.User, db: Session = Depends(get_db),
           current_user: schemas.User = Depends(get_current_user)):
    return user.update(id, request, db)


@router.get('/{id}', status_code=200, response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return user.get(id, db)


@router.delete('/{id}', responses={204: {'model': None}})
def delete_user(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return user.delete(id, db)


@router.get("/me/", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user
