# main.py - FastAPI application entry point.
# pyrefly: ignore [missing-import]
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
# pyrefly: ignore [missing-import]
from sqlalchemy import text
from app.core.config import settings
from app.db.database import get_db
# app - FastAPI application instance.
app = FastAPI(
    title=settings.app_name,
    debug=settings.app_debug,
)

# @app.get("/") - A simple root endpoint.
@app.get("/")
async def root():
    return {
        "message": "CareerPilot AI API is running"
    }

# @app.get("/health") - Checks if the API is healthy.
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "careerpilot-api",
        "environment": settings.app_env,
    }

# @app.get("/health/database") - Checks if the database is healthy. 
@app.get("/health/database")
async def database_health_check(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))
    value = result.scalar()
    # returns - database connected message.
    return {
        "database": "connected",
        "result": value,
    }