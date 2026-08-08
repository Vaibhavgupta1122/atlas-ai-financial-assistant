import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = os.getenv(
        "APP_NAME",
        "Atlas AI Financial Assistant"
    )

    APP_ENV: str = os.getenv(
        "APP_ENV",
        "development"
    )

    DEBUG: bool = os.getenv(
        "DEBUG",
        "False"
    ).lower() == "true"

    TELEGRAM_BOT_TOKEN: str = os.getenv(
        "TELEGRAM_BOT_TOKEN",
        ""
    )

    LLM_API_KEY: str = os.getenv(
        "LLM_API_KEY",
        ""
    )

    NEWS_API_KEY: str = os.getenv(
    "NEWS_API_KEY",
    ""
    )

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        ""
    )


settings = Settings()