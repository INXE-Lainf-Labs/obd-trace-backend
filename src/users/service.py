from datetime import datetime
from os import getenv

from passlib.hash import pbkdf2_sha512
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.exceptions import InvalidUsername, CustomerNotFoundException
from src.core.models import User, Customer, Employee, Address
from src.users.schemas import NewCustomer, NewEmployee, CustomerResponse

ROLES = getenv("ROLES").split(",")
EMPLOYEE_ROLE = ROLES[2]
CUSTOMER_ROLE = ROLES[1]


async def get_address(
    street: str,
    city: str,
    state: str,
    complement: str,
    zipcode: str,
    db_session: AsyncSession,
) -> Address | None:
    result = await db_session.execute(
        select(Address).where(
            Address.street == street,
            Address.city == city,
            Address.state == state,
            Address.complement == complement,
            Address.zipcode == zipcode,
        )
    )
    return result.scalar_one_or_none()


async def create_address(
    street: str,
    city: str,
    state: str,
    complement: str,
    zipcode: str,
    db_session: AsyncSession,
) -> Address:
    address = Address(
        street=street, city=city, state=state, complement=complement, zipcode=zipcode
    )
    db_session.add(address)
    await db_session.commit()
    await db_session.refresh(address)
    return address


async def get_customers(
    db_session: AsyncSession,
) -> list[CustomerResponse]:
    result = await db_session.exec(
        select(User, Customer, Address)
        .join(Customer, User.id == Customer.id)
        .join(Address, Customer.address_id == Address.id)
    )

    customers_response_list = [
        CustomerResponse(
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            role=user.role,
            street=address.street,
            city=address.city,
            state=address.state,
            complement=address.complement,
            zipcode=address.zipcode,
        )
        for user, customer, address in result.all()
    ]

    return customers_response_list


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


async def update_customer(
    user_id: int,
    username: str,
    password: str | None,
    first_name: str,
    last_name: str,
    address: Address,
    db_session: AsyncSession,
) -> User:
    user = await get_user_by_id(user_id, db_session)
    if user is None:
        raise CustomerNotFoundException()

    registered_customer = await get_customer_by_id(user_id, db_session)
    if registered_customer is None:
        raise CustomerNotFoundException()

    registered_address = await get_address(
        street=address.street,
        city=address.city,
        state=address.state,
        complement=address.complement,
        zipcode=address.zipcode,
        db_session=db_session,
    )

    if registered_address is None and address is not None:
        registered_address = await create_address(
            street=address.street,
            city=address.city,
            state=address.state,
            complement=address.complement,
            zipcode=address.zipcode,
            db_session=db_session,
        )
        registered_customer.address_id = registered_address.id
        db_session.add(registered_customer)

    user.username = username
    user.hashed_password = (
        pbkdf2_sha512.hash(password) if password else user.hashed_password
    )
    user.first_name = first_name
    user.last_name = last_name
    user.updated_at = datetime.now()
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


async def create_employee(
    username: str, password: str, db_session: AsyncSession
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
