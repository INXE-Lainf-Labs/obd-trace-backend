from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, APIRouter, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config.database.setup import get_db_session
from src.core.middlewares.authentication_middleware import (
    check_authorization,
    check_customer_authorization,
)
from src.users.schemas import (
    NewCustomer,
    NewEmployee,
    UserResponse,
    UserUpdateRequest,
    CustomerResponse,
)
from src.users.service import (
    get_users,
    create_customer,
    create_employee,
    update_customer,
    get_customers,
)

users_v1_router = APIRouter(prefix="/v1/users")


@users_v1_router.get("/", response_model=list[UserResponse])
async def list_users(
    authorization: Annotated[str | None, Header()] = None,
    db_session: AsyncSession = Depends(get_db_session),
):
    is_authorized = await check_authorization(authorization)
    if is_authorized:
        return await get_users(db_session)


@users_v1_router.get("/customers/", response_model=list[CustomerResponse])
async def list_customers(
    authorization: Annotated[str | None, Header()] = None,
    db_session: AsyncSession = Depends(get_db_session),
):
    is_authorized = await check_authorization(authorization)
    if is_authorized:
        customers = await get_customers(db_session)
        return customers


@users_v1_router.post(
    "/customer/",
    response_model=NewCustomer,
    response_model_exclude={"address_id"},
    status_code=HTTPStatus.CREATED,
)
async def post_customer(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    authorization: Annotated[str | None, Header()] = None,
    db_session: AsyncSession = Depends(get_db_session),
):
    is_authorized = await check_authorization(authorization)
    if is_authorized:
        customer = await create_customer(
            username=form_data.username,
            password=form_data.password,
            db_session=db_session,
        )
        return customer


@users_v1_router.put(
    "/customer/{customer_id}/",
    response_model=UserResponse,
    status_code=HTTPStatus.OK,
)
async def put_customer(
    customer_id: int,
    body: UserUpdateRequest,
    authorization: Annotated[str | None, Header()] = None,
    db_session: AsyncSession = Depends(get_db_session),
):
    is_authorized = await check_customer_authorization(authorization, customer_id)
    if is_authorized:
        customer = await update_customer(
            user_id=customer_id,
            username=body.username,
            password=body.password,
            first_name=body.first_name,
            last_name=body.last_name,
            address=body.address,
            db_session=db_session,
        )
        return customer


@users_v1_router.post(
    "/employee/",
    response_model=NewEmployee,
    response_model_exclude={"hashed_password"},
    status_code=HTTPStatus.CREATED,
)
async def post_employee(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    authorization: Annotated[str | None, Header()] = None,
    db_session: AsyncSession = Depends(get_db_session),
):
    is_authorized = await check_authorization(authorization)
    if is_authorized:
        employee = await create_employee(
            username=form_data.username,
            password=form_data.password,
            db_session=db_session,
        )
        return employee
