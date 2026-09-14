# main.py - FastAPI application entry point.
# pyrefly: ignore [missing-import]
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

# App configuration
from app.core.config import settings

# Database
from app.db.database import Base, engine, get_db

# Models (must be imported so Base knows about them before create_all)
from app.models.user import User  # noqa: F401

# Routers
from app.auth.router import router as auth_router

# ------------------------------------------------------------------
# FastAPI application instance
# ------------------------------------------------------------------
app = FastAPI(
    title=settings.app_name,
    debug=settings.app_debug,
)

# Create all tables on startup
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router)


# ------------------------------------------------------------------
# Core endpoints
# ------------------------------------------------------------------
# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "CareerPilot AI API is running"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "careerpilot-api",
        "environment": settings.app_env,
    }

# Database health check endpoint
@app.get("/health/database")
async def database_health_check(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))
    value = result.scalar()
    return {
        "database": "connected",
        "result": value,
    }