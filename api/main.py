import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.routes import router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application …")
    # Infrastructure singletons are initialised in api.dependencies at import
    # time; the lifespan hook simply bookends the process lifetime.
    logger.info("Application ready.")
    yield
    logger.info("Shutting down application.")


app = FastAPI(lifespan=lifespan)
app.include_router(router)
