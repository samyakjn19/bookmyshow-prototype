import os

os.environ["DATABASE_URL"] = "sqlite+pysqlite://"

from app.core.config import settings

settings.database_url = "sqlite+pysqlite://"

from sqlalchemy.pool import StaticPool
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.features.bookings import models as bookings_models  # noqa: F401
from app.features.cities import models as cities_models  # noqa: F401
from app.features.movies import models as movies_models  # noqa: F401
from app.features.shows import models as shows_models  # noqa: F401
from app.db import session as db_session

test_engine = create_engine(
    "sqlite+pysqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    future=True,
)
TestingSessionLocal = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)
db_session.engine = test_engine
db_session.SessionLocal = TestingSessionLocal
Base.metadata.create_all(bind=test_engine)

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    Base.metadata.create_all(bind=test_engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
