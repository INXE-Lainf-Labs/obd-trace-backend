from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    email: str = Field(unique=True)
    password: str = Field(nullable=True)
    name: str


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)


class AuthenticationUser(SQLModel):
    email: str
    password: str
