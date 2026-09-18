# Profile - contains information about the candidate's profile

# import modules
from datetime import datetime

# import sqlalchemy modules
from sqlalchemy import DateTime, ForeignKey, String, Text

# import sqlalchemy orm modules
from sqlalchemy.orm import Mapped, mapped_column, relationship

# import database
from app.db.database import Base

# Candidate Profile Model
class CandidateProfile(Base):
    """Candidate Profile Model"""
    __tablename__ = "candidate_profiles"
    # id - Primary Key
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )
    # user id - Foreign Key to users table
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    # first name - String(100), nullable = True
    first_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    # last name - String(100), nullable = True
    last_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    # phone - String(30), nullable = True
    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )
    # location - String(255), nullable = True
    location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    # professional summary - Text, nullable = True
    professional_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    # linkedin url - String(500), nullable = True
    linkedin_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    # github url - String(500), nullable = True
    github_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    # portfolio url - String(500), nullable = True
    portfolio_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    # created at - DateTime(timezone=True), default = datetime.utcnow
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    # updated at - DateTime(timezone=True), default = datetime.utcnow, onupdate = datetime.utcnow
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    # user - relationship to users table
    user = relationship(
        "User",
        back_populates="profile",
    )

    # one-to-many relationships with education, experience, and skills
    education = relationship(
        "Education",
        back_populates="profile",
        cascade="all, delete-orphan",
    )
    experience = relationship(
        "Experience",
        back_populates="profile",
        cascade="all, delete-orphan",
    )
    skills = relationship(
        "CandidateSkill",
        back_populates="profile",
        cascade="all, delete-orphan",
    )

    # One-to-many: a profile can have many projects
    projects = relationship(
        "CandidateProject",
        back_populates="profile",
        cascade="all, delete-orphan",
    )

    # One-to-many: a profile can have many certifications
    certifications = relationship(
        "Certification",
        back_populates="profile",
        cascade="all, delete-orphan",
    )