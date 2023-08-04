from datetime import datetime, timedelta
from os import getenv

from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError

from src.core.exceptions import Unauthorized, Forbidden
from src.core.models import User

load_dotenv("src/config/.env")

ROLES = getenv("ROLES").split(",")
ADMIN_ROLE = ROLES[0]
CUSTOMER_ROLE = ROLES[1]
JWT_SECRET = getenv("JWT_SECRET")
JWT_ALGORITHM = getenv("JWT_ALGORITHM")
JWT_EXPIRATION_DAYS = getenv("JWT_EXPIRATION_DAYS")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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


async def create_token(user_id: int, username: str, role: str):
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
    if token_user.role != ADMIN_ROLE:
        raise Forbidden()

    return True


async def check_customer_authorization(authorization: str, user_id: int) -> bool:
    if authorization is None:
        raise Unauthorized()

    token = authorization.split()[1]
    token_user = await validate_token(token)

    if token_user.role not in (ADMIN_ROLE, CUSTOMER_ROLE) or token_user.id != user_id:
        raise Forbidden()

    return True
