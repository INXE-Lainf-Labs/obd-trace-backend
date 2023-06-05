from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.auth.entities.user import User, UserBase
from src.config.database.setup import get_session

create_router = APIRouter()


@create_router.post("/users/")
async def create_user(user: UserBase, session: AsyncSession = Depends(get_session)):
    user = User(email=user.email, password=user.password, name=user.name)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
