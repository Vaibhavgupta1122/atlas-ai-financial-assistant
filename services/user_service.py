from sqlalchemy.orm import Session

from models.user import User


def get_or_create_user(
    db: Session,
    telegram_id: str,
    username: str | None,
    first_name: str | None,
) -> User:

    user = (
        db.query(User)
        .filter(User.telegram_id == telegram_id)
        .first()
    )

    if user:
        # Keep the user's Telegram information updated
        if username is not None:
            user.username = username

        if first_name is not None:
            user.first_name = first_name

        db.commit()
        db.refresh(user)

        return user

    user = User(
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user