from pydantic import BaseModel


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
