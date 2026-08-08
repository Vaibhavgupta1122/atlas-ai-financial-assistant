from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    telegram_id = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    username = Column(
        String,
        nullable=True,
    )

    first_name = Column(
        String,
        nullable=True,
    )

    role = Column(
        String,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )