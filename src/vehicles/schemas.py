from pydantic import BaseModel


class Vehicle(BaseModel):
    id: int | None
    model: str
    brand: str
    color: str
    year: str


class ResponseVehicle(BaseModel):
    id: int
    model: str | None
    brand: str | None
    color: str | None
    year: str | None


class CustomerVehicle(BaseModel):
    id: int | None
    vin: str
    plate_code: str
    customer_id: int
    model: str | None
    brand: str | None
    color: str | None
    year: str | None


class ResponseCustomerVehicle(BaseModel):
    vin: str
    plate_code: str
    customer_id: int
    vehicle_id: int
