import json
from os import getenv

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from src.core.errors.errors import AppException
from src.core.middlewares.ExceptionsHandler import error_handler_middleware
from src.config.database.setup import get_session
from src.api.v1.routes import v1_router

app = FastAPI()


@app.exception_handler(AppException)
async def validation_exception_handler(request, e):
    return await error_handler_middleware(request, e)


ENVIRONMENT = getenv("ENV", None)

if ENVIRONMENT in ["production", "staging"]:
    import sentry_sdk

    sentry_dsn = getenv("SENTRY_DSN", None)

    if sentry_dsn:
        SAMPLE_RATE = getenv("SENTRY_SAMPLE_RATE", 0)

        sentry_sdk.init(
            dsn=sentry_dsn,
            traces_sample_rate=float(SAMPLE_RATE),
        )


origins = json.loads(getenv("CORS_ORIGINS"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(v1_router, dependencies=[Depends(get_session)])
