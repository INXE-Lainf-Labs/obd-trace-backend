from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

from src.api.v1.auth.entities.user import User
from src.core.errors.errors import BadRequest
from src.core.errors.Slug import Slug


async def get_user(session: AsyncSession, user_id: int):
    try:
        order = await session.execute(select(User).where(User.id == user_id))
        return order.scalar_one()
    except NoResultFound:
        raise BadRequest(
            slug=Slug.user_not_found,
            message="User not found for given ID.",
        )
