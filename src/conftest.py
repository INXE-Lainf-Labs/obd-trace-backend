from datetime import datetime, timedelta
from os import getenv

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from httpx import AsyncClient
from jose import jwt
from passlib.handlers.pbkdf2 import pbkdf2_sha512
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.services import signin_user
from src.config.database.setup import get_db_session
from src.core.models import User
from src.main import app
from src.services.models import Service
from src.users.service import create_customer
from src.vehicles.models import Vehicle

load_dotenv("src/config/.env")

ROLES = getenv("ROLES")
ADMIN_ROLE = ROLES[0]
CUSTOMER_ROLE = ROLES[1]
EMPLOYEE_ROLE = ROLES[2]
JWT_EXPIRATION_DAYS = getenv("JWT_EXPIRATION_DAYS")
JWT_SECRET = getenv("JWT_SECRET")
JWT_ALGORITHM = getenv("JWT_ALGORITHM")

TEST_SQLALCHEMY_DATABASE_URL = getenv("TEST_DATABASE_URL", None)
ENVIRONMENT = getenv("ENV", None)

db_logs = "debug" if ENVIRONMENT == "development" else True


@pytest_asyncio.fixture
async def db_engine():
    engine = create_async_engine(TEST_SQLALCHEMY_DATABASE_URL, echo=db_logs)
    yield engine


@pytest_asyncio.fixture
async def db_connection(db_engine):
    async with db_engine.connect() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        yield conn
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session(db_connection) -> AsyncSession:
    async_session = sessionmaker(
        bind=db_connection, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def setup_db(db_session):
    # Add database setup instructions here if necessary.
    pass


@pytest_asyncio.fixture
async def client(db_session, setup_db) -> AsyncClient:
    app.dependency_overrides[get_db_session] = lambda: db_session
    async with AsyncClient(
        app=app, base_url="http://test", headers={"X-User-Fingerprint": "Test"}
    ) as client:
        yield client


@pytest.fixture
def admin_role():
    return ADMIN_ROLE


@pytest.fixture
def customer_role():
    return CUSTOMER_ROLE


@pytest.fixture
def employee_role():
    return EMPLOYEE_ROLE


@pytest.fixture
def user_payload():
    return {"username": "john.doe@email.com", "password": "test123"}


@pytest.fixture
def user2_payload():
    return {"username": "alicia.doe@email.com", "password": "test456"}


@pytest.fixture
def admin_payload():
    return {"username": "alex.doe@email.com", "password": "test789"}


@pytest.fixture
def customer(db_session, user_payload):
    async def _customer():
        customer = await create_customer(
            user_payload.get("username"), user_payload.get("password"), db_session
        )
        return customer

    return _customer


@pytest_asyncio.fixture
async def admin(db_session, admin_payload):
    password = admin_payload["password"]
    hashed_password = pbkdf2_sha512.hash(password)
    admin = User(
        username=admin_payload["username"],
        hashed_password=hashed_password,
        role=ADMIN_ROLE,
    )
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)
    return admin


@pytest.fixture
def admin_token(db_session, admin, admin_payload):
    async def _token():
        auth_admin = await signin_user(
            username=admin_payload["username"],
            password=admin_payload["password"],
            db_session=db_session,
        )
        return auth_admin.token

    return _token


@pytest.fixture
def user_token(db_session, customer, user_payload):
    async def _token():
        await customer()
        auth_user = await signin_user(
            username=user_payload["username"],
            password=user_payload["password"],
            db_session=db_session,
        )
        return auth_user.token

    return _token


@pytest.fixture
def expired_token(admin):
    async def _expired_token():
        expire = datetime.utcnow() - timedelta(days=int(JWT_EXPIRATION_DAYS))
        expired_token = jwt.encode(
            {
                "user_id": admin.id,
                "username": admin.username,
                "user_role": admin.role,
                "exp": expire,
            },
            JWT_SECRET,
            algorithm=JWT_ALGORITHM,
        )
        return expired_token

    return _expired_token


@pytest.fixture
def vehicle_payload():
    return {
        "id": 1,
        "brand": "chevrolet",
        "model": "corsa",
        "color": "black",
        "year": "2007",
    }


@pytest_asyncio.fixture
async def vehicle(db_session, vehicle_payload):
    test_vehicle = Vehicle(
        brand=vehicle_payload["brand"],
        model=vehicle_payload["model"],
        color=vehicle_payload["color"],
        year=vehicle_payload["year"],
    )
    db_session.add(test_vehicle)
    await db_session.commit()
    await db_session.refresh(test_vehicle)
    return test_vehicle


@pytest.fixture
def service_payload():
    return {
        "id": 1,
        "name": "Oil change",
        "price": 80.00,
        "description": "Drain motor oil and replace it",
        "image": "https://images.wisegeek.com/oil-change.jpg",
        "estimated_time": timedelta(hours=1).seconds,
        "category": "maintenance",
    }


@pytest_asyncio.fixture
async def service(db_session, service_payload):
    test_service = Service(
        name=service_payload["name"],
        price=service_payload["price"],
        description=service_payload["description"],
        image=service_payload["image"],
        estimated_time=service_payload["estimated_time"],
    )
    db_session.add(test_service)
    await db_session.commit()
    await db_session.refresh(test_service)
    return test_service
