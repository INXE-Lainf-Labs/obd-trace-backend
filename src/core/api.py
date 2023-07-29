from fastapi import APIRouter

from src.auth.v1.routes import auth_v1_router
from src.core.healthcheck import healthcheck_router
from src.orders.v1.routes import orders_v1_router
from src.services.v1.routes import services_v1_router
from src.users.v1.routes import users_v1_router
from src.vehicles.v1.routes import vehicles_v1_router

api_router = APIRouter(prefix="/api")

api_router.include_router(healthcheck_router)
api_router.include_router(auth_v1_router)
api_router.include_router(users_v1_router)
api_router.include_router(vehicles_v1_router)
api_router.include_router(services_v1_router)
api_router.include_router(orders_v1_router)
