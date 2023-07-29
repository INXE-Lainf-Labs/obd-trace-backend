from datetime import datetime

from sqlalchemy import Column, Integer
from sqlalchemy.dialects import postgresql
from sqlmodel import Field

from src.core.models import TimestampMixin


class Order(TimestampMixin, table=True):
    id: int | None = Field(nullable=False, default=None, primary_key=True, index=True)
    customer_id: int = Field(nullable=False, foreign_key="customer.id")
    customer_vehicle_ids: list[int] = Field(
        nullable=False, sa_column=Column(postgresql.ARRAY(Integer()))
    )
    service_ids: list[int] = Field(
        nullable=False, sa_column=Column(postgresql.ARRAY(Integer()))
    )
    employee_ids: list[int] | None = Field(
        default=None, sa_column=Column(postgresql.ARRAY(Integer()))
    )
    start_date: datetime = Field(default=None)
    estimated_time: datetime = Field(nullable=False)
    status: str = Field(nullable=False, default="REQUESTED")
