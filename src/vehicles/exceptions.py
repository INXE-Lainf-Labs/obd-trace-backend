from http import HTTPStatus
from fastapi import HTTPException


class VehicleAlreadyExistsException(HTTPException):
    def __init__(self, vehicle_id):
        super().__init__(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Vehicle already exists with id {vehicle_id}",
        )


class VehicleNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Vehicle not found for given vehicle_id",
        )
