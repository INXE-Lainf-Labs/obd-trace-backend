from jose import jwt
from http.client import OK
from os import getenv
from passlib.context import CryptContext
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta

from src.core.errors.errors import BadRequest, InternalServerError
from src.api.v1.auth.entities.user import User, AuthenticationUser
from src.config.database.setup import get_session

authenticate_router = APIRouter()

JWT_SECRET = getenv("JWT_SECRET")
JWT_EXPIRATION_DAYS = getenv("JWT_EXPIRATION_DAYS")
JWT_ALGORITHM = getenv("JWT_ALGORITHM")


@authenticate_router.post("/")
async def authentication_user(
    credentials: AuthenticationUser, session: AsyncSession = Depends(get_session)
):
    try:
        result = await session.execute(
            select(User).where(User.email == credentials.email)
        )
        user = result.scalar()
    except:
        raise InternalServerError(message="Error getting user data")

    context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not (user and context.verify(credentials.password, user.password)):
        raise BadRequest(message="Wrong credentials")

    expire = datetime.utcnow() + timedelta(days=int(JWT_EXPIRATION_DAYS))
    access_token = jwt.encode(
        {
            "user_id": user.id,
            "user_name": user.name,
            "user_email": user.email,
            "exp": expire,
        },
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )

    return JSONResponse(status_code=OK, content={"token": access_token})
