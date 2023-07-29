from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, APIRouter, Header, Path
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config.database.setup import get_db_session
from src.core.middlewares.authentication_middleware import check_authorization
from src.services.models import Service
from src.services.schemas import ServiceResponse
from src.services.services import (
    get_services,
    get_service_by_id,
    create_service,
    update_service,
    delete_service,
)

services_v1_router = APIRouter(prefix="/v1/services")


@services_v1_router.get("/", response_model=list[Service], summary="Get all Services")
async def list_services(
    db_session: AsyncSession = Depends(get_db_session),
):
    return await get_services(db_session)


@services_v1_router.get(
    "/{service_id}/",
    response_model=Service,
    summary="Get service details for a given id",
)
async def get_service(
    service_id: Annotated[int, Path(title="The ID of the service", ge=0, le=1000)],
    db_session: AsyncSession = Depends(get_db_session),
):
    return await get_service_by_id(service_id, db_session)


@services_v1_router.post(
    "/",
    response_model=ServiceResponse,
    status_code=HTTPStatus.CREATED,
    summary="Create new service",
)
async def post_service(
    service: Service,
    authorization: Annotated[str | None, Header()] = None,
    db_session: AsyncSession = Depends(get_db_session),
):
    is_authorized = await check_authorization(authorization)
    if is_authorized:
        new_service = await create_service(
            name=service.name,
            price=service.price,
            description=service.description,
            estimated_time=service.estimated_time,
            image=service.image,
            category=service.category,
            db_session=db_session,
        )
        return new_service


@services_v1_router.put(
    "/{service_id}/",
    response_model=ServiceResponse,
    status_code=HTTPStatus.OK,
    summary="Update a service",
)
async def put_service(
    service_id: int,
    service: Service,
    authorization: Annotated[str | None, Header()] = None,
    db_session: AsyncSession = Depends(get_db_session),
):
    is_authorized = await check_authorization(authorization)
    if is_authorized:
        updated_service = await update_service(
            service_id=service_id,
            name=service.name,
            price=service.price,
            description=service.description,
            estimated_time=service.estimated_time,
            image=service.image,
            category=service.category,
            db_session=db_session,
        )
        return updated_service


@services_v1_router.delete(
    "/{service_id}/",
    status_code=HTTPStatus.OK,
    summary="Delete a service",
)
async def del_service(
    service_id: int,
    authorization: Annotated[str | None, Header()] = None,
    db_session: AsyncSession = Depends(get_db_session),
):
    is_authorized = await check_authorization(authorization)
    if is_authorized:
        await delete_service(service_id=service_id, db_session=db_session)
