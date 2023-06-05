from enum import Enum


# Python does not support enum inheritance, so we're using comments
class Slug(Enum):
    user_not_found = "user_not_found"
    invalid_payload = "invalid_payload"
    internal_server_error = "internal_server_error"
