from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.bootstrap.database import init_database
from app.bootstrap.elasticsearch import init_elasticsearch
from app.bootstrap.notifications import init_notifications
from app.bootstrap.redis import init_redis


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_database()
    init_redis()
    init_elasticsearch()
    init_notifications()
    yield
