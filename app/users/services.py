from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import get_session
from app.exceptions import (
    CredentialException,
    InvalidCredentialError,
    ShortPasswordError,
    UserNotFoundError,
)
from app.security import Hash, encode_jwt_header_auth, jwt_decode
from app.users import models, schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class UserService:
    def __init__(self, db: Session = Depends(get_session)):
        self.session = db

    def _get_user_by_id(self, id):
        user = self.session.query(models.User).filter(models.User.id == id).first()
        if not user:
            raise UserNotFoundError
        return user

    def _get_user_by_email(self, email):
        user = self.session.query(models.User).filter(models.User.email == email).first()
        if not user:
            raise InvalidCredentialError
        return user

    def get_users(self):
        return self.session.query(models.User).order_by(models.User.id).all()

    def update_user(self, user: schemas.UserCreate, id: int):
        existing_user = self._get_user_by_id(id)

        update_data = user.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(existing_user, key, value)

        self.session.commit()

        return user

    def get_user(self, id: int):
        return self._get_user_by_id(id)

    def delete_user(self, id: int):
        user = self._get_user_by_id(id)
        self.session.delete(user)
        self.session.commit()

    def authentication(self, email, password):
        user = self._get_user_by_email(email)
        Hash.verify(
            password,
            user.hashed_password,
        )
        access_token = encode_jwt_header_auth(data={"sub": user.email})
        return {"access_token": access_token}

    def registration(self, user: schemas.UserCreate):
        if len(user.hashed_password) < 8:
            raise ShortPasswordError
        data = user.dict()
        data["hashed_password"] = Hash.bcrypt(user.hashed_password)
        new_user = models.User(**data)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)

        return new_user


def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):

    try:
        data = jwt_decode(token)
        email: str = data.get("sub")
        if email is None:
            raise CredentialException
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise CredentialException
    user = session.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        raise CredentialException
    return user
