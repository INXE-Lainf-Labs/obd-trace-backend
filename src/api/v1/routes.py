from fastapi import APIRouter

from .auth.routes import auth_router
from .healthcheck import healthcheck_router

v1_router = APIRouter(prefix="/api/v1")

v1_router.include_router(auth_router)
v1_router.include_router(healthcheck_router)
