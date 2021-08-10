from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import database
from app.security import Hash, encode_jwt_header_auth
from app.users import models, schemas

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    if not Hash.verify(user.hashed_password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")
    access_token = encode_jwt_header_auth(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/registration",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.User,
)
def registration(request: schemas.UserCreate, db: Session = Depends(database.get_db)):
    if len(request.hashed_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too short. At least 8 symbols!",
        )
    new_user = models.User(
        email=request.email,
        name=request.name,
        hashed_password=Hash.bcrypt(request.hashed_password),
        is_admin=False,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
