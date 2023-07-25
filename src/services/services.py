from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.services.exceptions import (
    ServiceAlreadyExistsException,
    ServiceNotFoundException,
)
from src.services.models import Service


async def get_services(db_session: AsyncSession) -> list[Service]:
    result = await db_session.scalars(select(Service))
    return result.all()


async def get_service(
    name: str,
    price: float,
    description: str,
    image: str,
    estimated_time: int,
    category: str,
    db_session: AsyncSession,
) -> Service:
    result = await db_session.execute(
        select(Service).where(
            Service.name == name,
            Service.price == price,
            Service.description == description,
            Service.image == image,
            Service.estimated_time == estimated_time,
            Service.category == category,
        )
    )
    return result.scalar_one_or_none()


async def get_service_by_id(
    service_id: int, db_session: AsyncSession
) -> Service | None:
    result = await db_session.execute(select(Service).where(Service.id == service_id))
    return result.scalar_one_or_none()


async def create_service(
    name: str,
    price: float,
    description: str,
    image: str,
    estimated_time: int,
    category: str,
    db_session: AsyncSession,
) -> Service:
    registered_service = await get_service(
        name=name,
        price=price,
        description=description,
        image=image,
        estimated_time=estimated_time,
        category=category,
        db_session=db_session,
    )
    if registered_service is not None:
        raise ServiceAlreadyExistsException(registered_service.id)

    service = Service(
        name=name,
        price=price,
        description=description,
        image=image,
        estimated_time=estimated_time,
        category=category,
    )

    db_session.add(service)
    await db_session.commit()
    await db_session.refresh(service)
    return service


async def update_service(
    service_id: int,
    name: str,
    price: float,
    description: str,
    image: str,
    estimated_time: int,
    category: str,
    db_session: AsyncSession,
) -> Service:
    result = await db_session.execute(select(Service).where(Service.id == service_id))
    service = result.scalar_one_or_none()
    if service is None:
        raise ServiceNotFoundException()

    service.name = name
    service.price = price
    service.description = description
    service.image = image
    service.estimated_time = estimated_time
    service.category = category
    db_session.add(service)
    await db_session.commit()
    await db_session.refresh(service)
    return service


async def delete_service(service_id: int, db_session: AsyncSession):
    result = await db_session.execute(select(Service).where(Service.id == service_id))
    service = result.scalar_one_or_none()
    if service is None:
        raise ServiceNotFoundException()

    await db_session.delete(service)
    await db_session.commit()
