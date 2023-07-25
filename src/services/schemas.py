from pydantic import BaseModel


class ResponseService(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image: str
    estimated_time: int
    category: str
