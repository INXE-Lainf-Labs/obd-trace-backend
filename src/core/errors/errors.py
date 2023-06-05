from http.client import BAD_REQUEST, INTERNAL_SERVER_ERROR
from fastapi.responses import JSONResponse
from fastapi import Request

from .Slug import Slug


def json_response_format(status, message, slug):
    return JSONResponse(status_code=status, content={"message": message, "slug": slug})


class AppException(Exception):
    def __init__(self, slug: str, status, message: str):
        self.slug = slug
        self.status = status
        self.message = message


class BadRequest(AppException):
    def __init__(self, message, slug: Slug = Slug.invalid_payload):
        self.slug = slug.value
        self.status = BAD_REQUEST
        self.message = message
        super().__init__(message=self.message, status=self.status, slug=self.slug)


class InternalServerError(AppException):
    def __init__(self, message, slug: Slug = Slug.internal_server_error):
        self.slug = slug.value
        self.status = INTERNAL_SERVER_ERROR
        self.message = message
        super().__init__(message=self.message, status=self.status, slug=self.slug)
