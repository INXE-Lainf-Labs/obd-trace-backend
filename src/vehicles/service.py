from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.exceptions import CustomerNotFoundException
from src.users.service import get_customer_by_id
from src.vehicles.exceptions import (
    VehicleAlreadyExistsException,
    VehicleNotFoundException,
)
from src.vehicles.models import Vehicle, CustomerVehicle
from src.vehicles.schemas import CustomerVehicleResponse


async def get_vehicles(db_session: AsyncSession) -> list[Vehicle]:
    result = await db_session.scalars(select(Vehicle))
    return result.all()


async def get_vehicle_by_id(
    vehicle_id: int, db_session: AsyncSession
) -> Vehicle | None:
    result = await db_session.execute(select(Vehicle).where(Vehicle.id == vehicle_id))
    return result.scalar_one_or_none()


async def create_vehicle(
    brand: str,
    model: str,
    color: str,
    year: str,
    db_session: AsyncSession,
) -> Vehicle:
    registered_vehicle = await get_vehicle(
        brand=brand, model=model, color=color, year=year, db_session=db_session
    )
    if registered_vehicle is not None:
        raise VehicleAlreadyExistsException(registered_vehicle.id)

    vehicle = Vehicle(brand=brand, model=model, color=color, year=year)

    db_session.add(vehicle)
    await db_session.commit()
    await db_session.refresh(vehicle)
    return vehicle


async def get_vehicle(
    brand: str, model: str, color: str, year: str, db_session: AsyncSession
) -> Vehicle | None:
    result = await db_session.execute(
        select(Vehicle).where(
            Vehicle.brand == brand,
            Vehicle.model == model,
            Vehicle.color == color,
            Vehicle.year == year,
        )
    )
    return result.scalar_one_or_none()


async def create_customer_vehicle(
    vin: str,
    plate_code: str | None,
    customer_id: int,
    vehicle_id: int,
    db_session: AsyncSession,
) -> CustomerVehicleResponse:
    registered_vehicle = await get_vehicle_by_id(
        vehicle_id=vehicle_id, db_session=db_session
    )
    if registered_vehicle is None:
        raise VehicleNotFoundException()

    registered_customer = await get_customer_by_id(
        customer_id=customer_id, db_session=db_session
    )
    if registered_customer is None:
        raise CustomerNotFoundException()

    customer_vehicle = CustomerVehicle(
        vin=vin, plate_code=plate_code, customer_id=customer_id, vehicle_id=vehicle_id
    )
    db_session.add(customer_vehicle)
    await db_session.commit()
    await db_session.refresh(customer_vehicle)
    return CustomerVehicleResponse(
        vin=vin, plate_code=plate_code, customer_id=customer_id, vehicle_id=vehicle_id
    )


async def create_vehicle_and_customer_vehicle(
    vin: str,
    plate_code: str | None,
    customer_id: int,
    brand: str,
    model: str,
    color: str,
    year: str,
    db_session: AsyncSession,
) -> CustomerVehicleResponse:
    new_vehicle = await create_vehicle(
        brand=brand, model=model, color=color, year=year, db_session=db_session
    )

    registered_customer = await get_customer_by_id(
        customer_id=customer_id, db_session=db_session
    )
    if registered_customer is None:
        raise CustomerNotFoundException()

    customer_vehicle = CustomerVehicle(
        vin=vin,
        plate_code=plate_code,
        customer_id=customer_id,
        vehicle_id=new_vehicle.id,
    )
    db_session.add(customer_vehicle)
    await db_session.commit()
    await db_session.refresh(customer_vehicle)
    return CustomerVehicleResponse(
        vin=vin,
        plate_code=plate_code,
        customer_id=customer_id,
        vehicle_id=new_vehicle.id,
    )
