from datetime import datetime, timedelta

from dotenv import load_dotenv
from jose import JWTError, jwt, ExpiredSignatureError
from os import getenv
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from src.core.exceptions import Unauthorized, Forbidden
from src.core.models import User, UserRoleEnum

load_dotenv("src/config/.env")

JWT_SECRET = getenv("JWT_SECRET")
JWT_ALGORITHM = getenv("JWT_ALGORITHM")
JWT_EXPIRATION_DAYS = getenv("JWT_EXPIRATION_DAYS")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

context = CryptContext(
    schemes=["sha512_crypt"], deprecated="auto", default="sha512_crypt"
)


async def validate_token(access_token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(access_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])

        return User(
            id=payload["user_id"],
            username=payload["username"],
            role=payload["user_role"],
        )
    except ExpiredSignatureError:
        raise Unauthorized()
    except JWTError:
        raise Unauthorized()


async def create_token(user_id: int, username: str, role: int):
    expire = datetime.utcnow() + timedelta(days=int(JWT_EXPIRATION_DAYS))
    access_token = jwt.encode(
        {
            "user_id": user_id,
            "username": username,
            "user_role": role,
            "exp": expire,
        },
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )
    return access_token


async def check_authorization(authorization: str) -> bool:
    if authorization is None:
        raise Unauthorized()

    token = authorization.split()[1]
    token_user = await validate_token(token)
    if token_user.role is not UserRoleEnum.Admin.value:
        raise Forbidden()

    return True
