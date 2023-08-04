from datetime import datetime
from os import getenv

from dotenv import load_dotenv
from sqlmodel import SQLModel, Field, Relationship

load_dotenv("src/config/.env")

ROLES = getenv("ROLES", None).split(",")
CUSTOMER_ROLE = ROLES[1]


class TimestampMixin(SQLModel):
    created_at: datetime = Field(default=datetime.now(), nullable=False)
    updated_at: datetime = Field(
        default=datetime.now(),
        schema_extra={"onupdate": datetime.now()},
        nullable=False,
    )


class Address(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    street: str = Field(default=None)
    city: str = Field(default=None)
    state: str = Field(default=None)
    complement: str = Field(default=None)
    zipcode: str = Field(default=None)
    customer: "Customer" = Relationship(back_populates="address")


class Customer(TimestampMixin, table=True):
    id: int = Field(nullable=False, foreign_key="user.id", primary_key=True)
    address_id: int | None = Field(nullable=True, foreign_key="address.id")
    address: Address | None = Relationship(back_populates="customer")
    user: "User" = Relationship(back_populates="customer")


class Employee(TimestampMixin, table=True):
    id: int = Field(nullable=False, foreign_key="user.id", primary_key=True)
    job_title: str | None = Field(nullable=True)


class User(TimestampMixin, table=True):
    id: int | None = Field(nullable=False, default=None, primary_key=True, index=True)
    username: str = Field(unique=True)
    hashed_password: str | None = Field(nullable=False)
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    is_active: bool | None = Field(nullable=False, default=True)
    role: str = Field(nullable=False, default=CUSTOMER_ROLE)
    customer: Customer | None = Relationship(back_populates="user")
