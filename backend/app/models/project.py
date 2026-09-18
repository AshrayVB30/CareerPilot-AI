# project.py - SQLAlchemy model for candidate projects.
#
# Each project belongs to one CandidateProfile (many-to-one).
# Deleting a profile cascades to delete all its projects.

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class CandidateProject(Base):
    """Represents a personal or professional project on a candidate's profile."""

    __tablename__ = "candidate_projects"

    # Primary key — auto-incremented by PostgreSQL
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    # Foreign key to candidate_profiles.id
    # ondelete="CASCADE" — deleting a profile removes all its projects
    profile_id: Mapped[int] = mapped_column(
        ForeignKey(
            "candidate_profiles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # Project name, e.g. "CareerPilot AI" (required)
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Freeform description of what the project does (optional)
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Comma-separated or freeform list of technologies used (optional)
    # e.g. "Python, FastAPI, PostgreSQL, Next.js"
    technologies: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Live URL for the deployed project (optional)
    project_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # GitHub / source code URL (optional)
    github_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # Timestamp when this record was created
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    # Timestamp updated automatically on every save
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Many-to-one relationship back to CandidateProfile
    # back_populates="projects" connects to the list defined on CandidateProfile
    profile = relationship(
        "CandidateProfile",
        back_populates="projects",
    )
