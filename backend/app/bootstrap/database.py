from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.features.bookings import models as bookings_models  # noqa: F401
from app.features.cities import models as cities_models  # noqa: F401
from app.features.movies import models as movies_models  # noqa: F401
from app.features.shows import models as shows_models  # noqa: F401


def init_database() -> None:
    if settings.database_url.startswith("sqlite"):
        Base.metadata.create_all(bind=engine)
