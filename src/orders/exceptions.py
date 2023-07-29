from http import HTTPStatus

from fastapi import HTTPException


class OrderAlreadyExistsException(HTTPException):
    def __init__(self, order_id):
        super().__init__(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Service already exists with id {order_id}",
        )


class OrderNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Service not found for given service_id",
        )


class OrderStatusNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Problem occurred when trying to load orders status",
        )
