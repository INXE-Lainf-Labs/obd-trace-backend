from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, APIRouter, Header, Path
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config.database.setup import get_db_session
from src.core.middlewares.authentication_middleware import check_authorization
from src.vehicles.schemas import (
    ResponseVehicle,
    Vehicle,
    CustomerVehicle,
    ResponseCustomerVehicle,
)
from src.vehicles.service import (
    get_vehicles,
    create_vehicle,
    get_vehicle_by_id,
    create_customer_vehicle,
    create_vehicle_and_customer_vehicle,
)

vehicles_v1_router = APIRouter(prefix="/v1/vehicles")


@vehicles_v1_router.get("/", response_model=list[ResponseVehicle])
async def list_vehicles(
    db_session: AsyncSession = Depends(get_db_session),
):
    return await get_vehicles(db_session)


@vehicles_v1_router.get("/{vehicle_id}/", response_model=ResponseVehicle)
async def get_vehicle(
    vehicle_id: Annotated[int, Path(title="The ID of the vehicle", ge=0, le=10000)],
    db_session: AsyncSession = Depends(get_db_session),
):
    return await get_vehicle_by_id(vehicle_id, db_session)


@vehicles_v1_router.post(
    "/",
    response_model=ResponseVehicle,
    status_code=HTTPStatus.CREATED,
)
async def post_vehicle(
    vehicle: Vehicle,
    authorization: Annotated[str | None, Header()] = None,
    db_session: AsyncSession = Depends(get_db_session),
):
    is_authorized = await check_authorization(authorization)
    if is_authorized:
        customer = await create_vehicle(
            brand=vehicle.brand,
            model=vehicle.model,
            color=vehicle.color,
            year=vehicle.year,
            db_session=db_session,
        )
        return customer


@vehicles_v1_router.post(
    "/customer/{vehicle_id}",
    response_model=ResponseCustomerVehicle,
    status_code=HTTPStatus.CREATED,
)
async def post_customer_vehicle(
    customer_vehicle: CustomerVehicle,
    vehicle_id: int,
    authorization: Annotated[str | None, Header()] = None,
    db_session: AsyncSession = Depends(get_db_session),
):
    is_authorized = await check_authorization(authorization)
    if is_authorized:
        customer = await create_customer_vehicle(
            vin=customer_vehicle.vin,
            plate_code=customer_vehicle.plate_code,
            user_id=customer_vehicle.customer_id,
            vehicle_id=vehicle_id,
            db_session=db_session,
        )
        return customer


@vehicles_v1_router.post(
    "/customer/",
    response_model=ResponseCustomerVehicle,
    status_code=HTTPStatus.CREATED,
)
async def post_vehicle_and_customer_vehicle(
    customer_vehicle: CustomerVehicle,
    authorization: Annotated[str | None, Header()] = None,
    db_session: AsyncSession = Depends(get_db_session),
):
    is_authorized = await check_authorization(authorization)
    if is_authorized:
        customer = await create_vehicle_and_customer_vehicle(
            vin=customer_vehicle.vin,
            plate_code=customer_vehicle.plate_code,
            user_id=customer_vehicle.customer_id,
            brand=customer_vehicle.brand,
            model=customer_vehicle.model,
            color=customer_vehicle.color,
            year=customer_vehicle.year,
            db_session=db_session,
        )
        return customer
