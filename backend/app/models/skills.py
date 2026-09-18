# Skills Model

# Import datetime for the record creation timestamp
from datetime import datetime

# SQLAlchemy imports for datetime, float, foreign key, and string columns
from sqlalchemy import ( DateTime, Float, ForeignKey, String, )
# SQLAlchemy imports for mapped columns and relationships   
from sqlalchemy.orm import Mapped, mapped_column, relationship
# Base class for all models
from app.db.database import Base

# Model for candidate skills    
class CandidateSkill(Base):
    __tablename__ = "candidate_skills"
    # Primary key
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    # Foreign key to candidate profiles
    profile_id: Mapped[int] = mapped_column(
        ForeignKey(
            "candidate_profiles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # Name of the skill
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # Category of the skill
    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # Proficiency of the skill (0.0-1.0)
    proficiency: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    
    # Years of experience in the skill
    years_of_experience: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    
    # Source of the skill (manual, ai_extracted, import)
    source: Mapped[str] = mapped_column(
        String(50),
        default="manual",
        nullable=False,
    )

    # Record creation timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    
    # Relationship with candidate profiles
    profile = relationship(
        "CandidateProfile",
        back_populates="skills",
    )