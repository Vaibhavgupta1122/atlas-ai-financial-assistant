from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from database.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    telegram_id = Column(
        String,
        nullable=False,
        index=True,
    )

    role = Column(
        String,
        nullable=False,
    )

    message = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )