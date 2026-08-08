from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config.settings import settings


if not settings.DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is missing from the .env file."
    )


engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()