from sqlmodel import Field

from src.core.models import TimestampMixin


class Service(TimestampMixin, table=True):
    id: int | None = Field(unique=True, nullable=False, default=None, primary_key=True)
    name: str = Field(nullable=False)
    price: float = Field(nullable=False)
    description: str = Field(nullable=False)
    image: str | None = Field(nullable=False, default=None)
    estimated_time: int = Field(nullable=False)
    category: str = Field(nullable=False, default="maintenance")
