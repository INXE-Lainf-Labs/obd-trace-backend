from os import getenv

from fastapi.params import Depends
from passlib.hash import pbkdf2_sha512
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config.database.setup import get_db_session
from src.core.exceptions import InvalidUsername
from src.core.models import User, Customer, Employee
from src.users.schemas import NewCustomer, NewEmployee

ROLES = getenv("ROLES").split(",")
EMPLOYEE_ROLE = ROLES[2]
CUSTOMER_ROLE = ROLES[1]


async def get_users(db_session: AsyncSession) -> list[User]:
    result = await db_session.scalars(select(User))
    return result.all()


async def get_user_by_username(username: str, db_session: AsyncSession) -> User | None:
    result = await db_session.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def get_user_by_id(user_id: int, db_session: AsyncSession) -> User | None:
    result = await db_session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_customer_by_id(
    customer_id: int, db_session: AsyncSession
) -> Customer | None:
    result = await db_session.execute(
        select(Customer).where(Customer.id == customer_id)
    )
    return result.scalar_one_or_none()


async def create_user(
    username: str,
    password: str,
    db_session: AsyncSession,
    role: str = CUSTOMER_ROLE,
) -> User:
    user = await get_user_by_username(username, db_session)
    if user is not None:
        raise InvalidUsername()

    hashed_password = pbkdf2_sha512.hash(password)
    user = User(username=username, hashed_password=hashed_password, role=role)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


async def create_customer(
    username: str, password: str, db_session: AsyncSession
) -> NewCustomer:
    user = await create_user(
        username=username,
        password=password,
        role=CUSTOMER_ROLE,
        db_session=db_session,
    )

    customer = Customer(id=user.id)
    db_session.add(customer)
    await db_session.commit()
    await db_session.refresh(customer)
    return NewCustomer(id=user.id, role=user.role, username=user.username)


async def create_employee(
    username: str, password: str, db_session: AsyncSession = Depends(get_db_session)
) -> NewEmployee:
    user = await create_user(
        username=username,
        password=password,
        role=EMPLOYEE_ROLE,
        db_session=db_session,
    )

    employee = Employee(id=user.id)
    db_session.add(employee)
    await db_session.commit()
    await db_session.refresh(employee)
    return NewEmployee(id=user.id, username=user.username)
