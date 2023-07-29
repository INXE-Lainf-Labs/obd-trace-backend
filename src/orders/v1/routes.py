from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Header
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config.database.setup import get_db_session
from src.core.middlewares.authentication_middleware import check_authorization
from src.orders.models import Order
from src.orders.schemas import OrderResponse
from src.orders.services import (
    get_orders,
    get_order_by_id,
    create_order,
    update_order,
    delete_order,
)

orders_v1_router = APIRouter(prefix="/v1/orders")


@orders_v1_router.get("/", response_model=list[OrderResponse], summary="Get all Orders")
async def list_orders(
    db_session: AsyncSession = Depends(get_db_session),
):
    return await get_orders(db_session)


@orders_v1_router.get(
    "/{order_id}/",
    response_model=OrderResponse,
    summary="Get order details for a given id",
)
async def get_service(
    order_id: Annotated[int, Path(title="The ID of the order", ge=0, le=1000)],
    db_session: AsyncSession = Depends(get_db_session),
):
    return await get_order_by_id(order_id, db_session)


@orders_v1_router.post(
    "/",
    response_model=OrderResponse,
    status_code=HTTPStatus.CREATED,
    summary="Create new order",
)
async def post_order(
    order: Order,
    authorization: Annotated[str | None, Header()] = None,
    db_session: AsyncSession = Depends(get_db_session),
):
    is_authorized = await check_authorization(authorization)
    if is_authorized:
        new_service = await create_order(
            customer_id=order.customer_id,
            customer_vehicle_ids=order.customer_vehicle_ids,
            service_ids=order.service_ids,
            employee_ids=order.employee_ids,
            start_date=order.start_date,
            estimated_time=order.estimated_time,
            status=order.status,
            db_session=db_session,
        )
        return new_service


@orders_v1_router.put(
    "/{order_id}/",
    response_model=OrderResponse,
    status_code=HTTPStatus.OK,
    summary="Update an order",
)
async def put_order(
    order_id: int,
    order: Order,
    authorization: Annotated[str | None, Header()] = None,
    db_session: AsyncSession = Depends(get_db_session),
):
    is_authorized = await check_authorization(authorization)
    if is_authorized:
        updated_service = await update_order(
            order_id=order_id,
            customer_id=order.customer_id,
            customer_vehicle_ids=order.customer_vehicle_ids,
            service_ids=order.service_ids,
            employee_ids=order.employee_ids,
            start_date=order.start_date,
            estimated_time=order.estimated_time,
            status=order.status,
            db_session=db_session,
        )
        return updated_service


@orders_v1_router.delete(
    "/{order_id}/",
    status_code=HTTPStatus.OK,
    summary="Delete an order",
)
async def del_order(
    order_id: int,
    authorization: Annotated[str | None, Header()] = None,
    db_session: AsyncSession = Depends(get_db_session),
):
    is_authorized = await check_authorization(authorization)
    if is_authorized:
        await delete_order(order_id=order_id, db_session=db_session)
