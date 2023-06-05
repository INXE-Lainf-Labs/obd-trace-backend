from fastapi import APIRouter

from .use_cases.authentication_user.authentication_user import authenticate_router
from .use_cases.list_users.list import list_router
from .use_cases.create_user.create import create_router

auth_router = APIRouter(prefix="/auth")

auth_router.include_router(authenticate_router)
auth_router.include_router(list_router)
auth_router.include_router(create_router)
