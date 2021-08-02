from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
# import models as models
from .. import models
# import schemas as schemas
from .. import schemas
# import database as database
from .. import database
# import jwt_token as jwt_token
from .. import jwt_token
# from hashing import Hash
from ..hashing import Hash
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid Credentials')
    if not Hash.verify(user.hashed_password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Incorrect password')
    access_token = jwt_token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/registration', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def registration(request: schemas.Register, db: Session = Depends(database.get_db)):
    if len(request.hashed_password) < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is too short. At least 8 symbols!")
    new_user = models.User(email=request.email,
                           name=request.name,
                           hashed_password=Hash.bcrypt(request.hashed_password),
                           is_admin=False)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
