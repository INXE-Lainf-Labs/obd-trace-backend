from http import HTTPStatus

from fastapi import HTTPException


class ServiceAlreadyExistsException(HTTPException):
    def __init__(self, service_id):
        super().__init__(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Service already exists with id {service_id}",
        )


class ServiceNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Service not found for given service_id",
        )
