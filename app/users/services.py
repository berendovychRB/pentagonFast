from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_session
from app.exceptions import (
    CredentialException,
    IncorrectPasswordError,
    InvalidCredentialError,
    ShortPasswordError,
    UserNotFoundError,
)
from app.security import Hash, encode_jwt_header_auth
from app.users import models, schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class UserService:
    def __init__(self, db: Session = Depends(get_session)):
        self.session = db

    def _get_user_by_id(self, id):
        return self.session.query(models.User).filter(models.User.id == id).first()

    def _get_user_by_email(self, email):
        return self.session.query(models.User).filter(models.User.email == email).first()

    def get_users(self):
        users = self.session.query(models.User).order_by(models.User.id).all()
        return users

    def update_user(self, request: schemas.UserCreate, id: int):
        user = self.session.query(models.User).filter(models.User.id == id)

        if not user.first():
            raise UserNotFoundError

        user.update(request)
        self.session.commit()

        return "Successful Updated"

    def get_user(self, id: int):
        user = self._get_user_by_id(id)

        if not user:
            raise UserNotFoundError
        return user

    def delete_user(self, id: int):
        user = self._get_user_by_id(id)

        if not user:
            raise UserNotFoundError

        user.delete(synchronize_session=False)
        self.session.commit()
        return "Successful Deleted"

    def get_current_user(self, token: str = Depends(oauth2_scheme)):

        try:
            data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: str = data.get("sub")
            if email is None:
                raise CredentialException
            token_data = schemas.TokenData(email=email)
        except JWTError:
            raise CredentialException
        user = self._get_user_by_email(token_data.email)
        if user is None:
            raise CredentialException
        return user

    def authentication(self, request):
        user = self._get_user_by_email(request.username)
        if not user:
            raise InvalidCredentialError
        if not Hash.verify(
            request.password,
            user.hashed_password,
        ):
            raise IncorrectPasswordError
        access_token = encode_jwt_header_auth(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}

    def registration(self, request):
        if len(request.hashed_password) < 8:
            raise ShortPasswordError
        data = request.dict()
        data["hashed_password"] = Hash.bcrypt(request.hashed_password)
        new_user = models.User(**data)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)

        return new_user
