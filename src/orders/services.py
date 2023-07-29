from datetime import datetime
from os import getenv

from dotenv import load_dotenv
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.orders.exceptions import (
    OrderAlreadyExistsException,
    OrderStatusNotFoundException,
    OrderNotFoundException,
)
from src.orders.models import Order

load_dotenv("src/config/.env")


def get_orders_status_values() -> list[str]:
    status_list = getenv("ORDER_STATUS", None)
    if status_list is None:
        raise OrderStatusNotFoundException()
    return status_list.split(",")


async def get_orders(db_session: AsyncSession) -> list[Order]:
    result = await db_session.scalars(select(Order))
    return result.all()


async def get_order(
    customer_id: int,
    customer_vehicle_ids: list[int],
    service_ids: list[int],
    employee_ids: list[int],
    start_date: datetime,
    estimated_time: datetime,
    status: str,
    db_session: AsyncSession,
) -> Order:
    result = await db_session.execute(
        select(Order)
        .where(
            Order.customer_id == customer_id,
            Order.start_date == start_date,
            Order.estimated_time == estimated_time,
            Order.status == status,
        )
        .filter(Order.customer_vehicle_ids.contains(customer_vehicle_ids))
        .filter(Order.service_ids.contains(service_ids))
        .filter(Order.employee_ids.contains(employee_ids))
    )
    return result.scalar_one_or_none()


async def get_order_by_id(order_id: int, db_session: AsyncSession) -> Order | None:
    result = await db_session.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()


async def create_order(
    customer_id: int,
    customer_vehicle_ids: list[int],
    service_ids: list[int],
    employee_ids: list[int],
    start_date: datetime,
    estimated_time: datetime,
    status: str,
    db_session: AsyncSession,
) -> Order:
    registered_order = await get_order(
        customer_id=customer_id,
        customer_vehicle_ids=customer_vehicle_ids,
        service_ids=service_ids,
        employee_ids=employee_ids,
        start_date=start_date,
        estimated_time=estimated_time,
        status=status,
        db_session=db_session,
    )
    if registered_order is not None:
        raise OrderAlreadyExistsException(registered_order.id)

    order = Order(
        customer_id=customer_id,
        customer_vehicle_ids=customer_vehicle_ids,
        service_ids=service_ids,
        employee_ids=employee_ids,
        start_date=start_date,
        estimated_time=estimated_time,
        status=status,
    )

    db_session.add(order)
    await db_session.commit()
    await db_session.refresh(order)
    return order


async def update_order(
    order_id: int,
    customer_id: int,
    customer_vehicle_ids: list[int],
    service_ids: list[int],
    employee_ids: list[int],
    start_date: datetime,
    estimated_time: datetime,
    status: str,
    db_session: AsyncSession,
) -> Order:
    result = await db_session.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if order is None:
        raise OrderNotFoundException()

    order.customer_id = customer_id
    order.customer_vehicle_ids = customer_vehicle_ids
    order.service_ids = service_ids
    order.employee_ids = employee_ids
    order.start_date = start_date
    order.estimated_time = estimated_time
    order.status = status
    db_session.add(order)
    await db_session.commit()
    await db_session.refresh(order)
    return order


async def delete_order(order_id: int, db_session: AsyncSession):
    result = await db_session.execute(select(Order).where(Order.id == order_id))
    service = result.scalar_one_or_none()
    if service is None:
        raise OrderNotFoundException()

    await db_session.delete(service)
    await db_session.commit()
