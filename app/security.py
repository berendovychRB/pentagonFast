from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings
from app.users import schemas

# For hashing passwords
from app.exceptions import IncorrectPasswordError

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

    def verify(plain_password, hashed_password):
        is_correct = pwd_cxt.verify(plain_password, hashed_password)
        if not is_correct:
            raise IncorrectPasswordError
        return is_correct


def jwt_encode(data: dict) -> str:
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def jwt_decode(token: str):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


def encode_jwt_header_auth(data: dict):
    exp = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt_encode(data={**data, "exp": exp})
    return token


def decode_jwt_header_auth(token: str, credentials_exception):
    try:
        payload = jwt_decode(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
