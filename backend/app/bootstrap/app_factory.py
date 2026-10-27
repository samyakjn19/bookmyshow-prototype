from fastapi import FastAPI

from app.bootstrap.errors import register_error_handlers
from app.bootstrap.lifespan import lifespan
from app.bootstrap.logging import setup_logging
from app.bootstrap.routers import register_routers
from app.core.config import settings


def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(
        title=settings.app_name,
        lifespan=lifespan,
    )
    register_error_handlers(app)
    register_routers(app)
    return app
