from pydantic import BaseModel

from src.core.models import Address


class NewCustomer(BaseModel):
    id: int
    role: str
    username: str


class NewEmployee(BaseModel):
    id: int
    username: str


class UserResponse(BaseModel):
    id: int
    username: str
    first_name: str | None
    last_name: str | None
    is_active: bool
    role: str


class UserUpdateRequest(BaseModel):
    username: str
    password: str | None
    first_name: str
    last_name: str
    address: Address


class CustomerResponse(BaseModel):
    username: str
    first_name: str | None
    last_name: str | None
    is_active: bool
    role: str
    street: str | None
    city: str | None
    state: str | None
    complement: str | None
    zipcode: str | None
