from database.database import Base, engine

from models.user import User
from models.conversation import Conversation


def init_database():
    Base.metadata.create_all(bind=engine)

    print("Database initialized successfully.")


if __name__ == "__main__":
    init_database()