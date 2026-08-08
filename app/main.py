from fastapi import FastAPI
from sqlalchemy import text

from config.settings import settings
from database.database import engine


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered financial assistant for finance professionals.",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {
        "message": "Atlas AI Financial Assistant is running",
        "environment": settings.APP_ENV,
        "status": "online",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "atlas-ai-financial-assistant",
    }


@app.get("/health/database")
async def database_health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception as error:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(error),
        }