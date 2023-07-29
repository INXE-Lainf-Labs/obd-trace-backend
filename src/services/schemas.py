from pydantic import BaseModel


class ServiceResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image: str
    estimated_time: int
    category: str
