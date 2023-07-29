from datetime import datetime

from pydantic import BaseModel


class OrderResponse(BaseModel):
    id: int
    customer_id: int
    customer_vehicle_ids: list[int]
    service_ids: list[int]
    employee_ids: list[int] | None
    start_date: datetime
    estimated_time: datetime
    status: str
