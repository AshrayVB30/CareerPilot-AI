# main.py - FastAPI application entry point.
# pyrefly: ignore [missing-import]
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

# App configuration
from app.core.config import settings

# Database
from app.db.database import Base, engine, get_db

# Models (must be imported so Base knows about them before create_all)
# All models must be listed here so SQLAlchemy can resolve
# relationship() references across models at startup.
from app.models.user import User  # noqa: F401
from app.models.profile import CandidateProfile  # noqa: F401
from app.models.education import Education  # noqa: F401
from app.models.experience import Experience  # noqa: F401
from app.models.skills import CandidateSkill  # noqa: F401
from app.models.project import CandidateProject  # noqa: F401
from app.models.certification import Certification  # noqa: F401

# Routers
from app.auth.router import router as auth_router

# Profile router
from app.profile.router import router as profile_router

# Education router
from app.profile.education.router import router as education_router

# Experience router
from app.profile.experience.router import router as experience_router

# Skills router
from app.profile.skills.router import router as skills_router

# Projects router
from app.profile.projects.router import router as project_router

# Certifications router
from app.profile.certifications.router import router as certification_router

# ------------------------------------------------------------------
# FastAPI application instance
# ------------------------------------------------------------------
app = FastAPI(
    title=settings.app_name,
    debug=settings.app_debug,
)

# ------------------------------------------------------------------
# CORS
# Allows the Next.js dev server (localhost:3000) to call this API.
# In production, replace with your actual frontend domain.
# ------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create all tables on startup
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(education_router)
app.include_router(experience_router)
app.include_router(skills_router)
app.include_router(project_router)
app.include_router(certification_router)

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