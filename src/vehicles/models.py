from sqlmodel import SQLModel, Field


class Vehicle(SQLModel, table=True):
    id: int | None = Field(unique=True, nullable=False, default=None, primary_key=True)
    model: str | None = Field(nullable=False, default=None)
    brand: str | None = Field(nullable=False, default=None)
    color: str | None = Field(nullable=False, default=None)
    year: str | None = Field(nullable=False, default=None)


class CustomerVehicle(SQLModel, table=True):
    __tablename__ = "customer_vehicle"
    id: int | None = Field(
        unique=True, nullable=False, default=None, primary_key=True, index=True
    )
    vin: str = Field(unique=True, nullable=False, default=None)
    plate_code: str = Field(nullable=False, default="")
    user_id: int = Field(nullable=False, default=None, foreign_key="user.id")
    vehicle_id: int = Field(nullable=False, default=None, foreign_key="vehicle.id")
