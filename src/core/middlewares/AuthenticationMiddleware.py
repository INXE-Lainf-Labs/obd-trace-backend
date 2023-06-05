from unicodedata import name
from jose import JWTError, jwt
from os import getenv
from http.client import UNAUTHORIZED
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from src.api.v1.auth.entities.user import User

JWT_SECRET = getenv("JWT_SECRET")
JWT_ALGORITHM = getenv("JWT_ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authentication_middleware(access_token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            access_token.encode(), key=JWT_SECRET, algorithms=[JWT_ALGORITHM]
        )

        return User(
            id=payload["user_id"],
            name=payload["user_name"],
            email=payload["user_email"],
        )
    except JWTError:
        raise HTTPException(
            status_code=UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"Authorization": "Bearer"},
        )
