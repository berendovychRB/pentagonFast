from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import database
from app.users import schemas
from app.users.services import UserService

router = APIRouter(tags=["Users"])
get_session = database.get_session
userService = UserService()


@router.get("/user/all", response_model=List[schemas.User])
def all_users(
    service: UserService = Depends(),
    current_user: schemas.User = Depends(userService.get_current_user),
):
    return service.get_users()


@router.patch("/user/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(
    id: int,
    request: schemas.UserCreate,
    service: UserService = Depends(),
    # current_user: schemas.User = Depends(UserService.get_current_user),
):
    return service.update_user(request, id)


@router.get("/user/{id}", status_code=200, response_model=schemas.User)
def get_user(
    id: int,
    service: UserService = Depends(),
    # current_user: schemas.User = Depends(userService.get_current_user),
):
    return service.get_user(id)


@router.delete("/user/{id}", responses={204: {"model": None}})
def delete_user(
    id: int,
    service: UserService = Depends(),
    # current_user: schemas.User = Depends(userService.get_current_user),
):
    return service.delete_user(id)


@router.get("/user/me/", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(UserService.get_current_user)):
    return current_user


@router.post("/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(),
):
    return service.authentication(request)


@router.post("/registration", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def sing_up(request: schemas.UserCreate, service: UserService = Depends()):
    return service.registration(request)
