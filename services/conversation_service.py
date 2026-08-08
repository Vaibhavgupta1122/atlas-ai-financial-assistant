from sqlalchemy.orm import Session

from models.conversation import Conversation


def save_message(
    db: Session,
    telegram_id: str,
    role: str,
    message: str,
) -> Conversation:

    conversation = Conversation(
        telegram_id=telegram_id,
        role=role,
        message=message,
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def get_recent_messages(
    db: Session,
    telegram_id: str,
    limit: int = 10,
) -> list[Conversation]:

    messages = (
        db.query(Conversation)
        .filter(
            Conversation.telegram_id == telegram_id
        )
        .order_by(
            Conversation.created_at.desc()
        )
        .limit(limit)
        .all()
    )

    return list(reversed(messages))