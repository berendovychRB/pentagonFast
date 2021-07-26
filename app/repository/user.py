from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

import models
import oauth2
from hashing import Hash
import schemas


def all(db: Session):
    users = db.query(models.User).all()
    return users


def create(request: schemas.User, db: Session):
    #
    # if not request.is_admin:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission")

    new_user = models.User(email=request.email,
                           name=request.name,
                           hashed_password=Hash.bcrypt(request.hashed_password),
                           is_admin=request.is_admin)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def update(id: int, request: schemas.User, db: Session):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} is not found')

    user.update(request)
    db.commit()

    return 'Successful Updated'


def get(id: int, db: Session):
    user = db.query(models.User).get(id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id {id} is not available')
    return user


def delete(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")

    user.delete(synchronize_session=False)
    db.commit()
    return 'Successful Deleted'

