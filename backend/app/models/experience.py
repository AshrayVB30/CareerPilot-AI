# Experience - 

# Import date for education start/end dates
# Import datetime for the record creation timestamp
from datetime import date, datetime

# SQLAlchemy imports for date/time fields,
# foreign key relationships, and string/text columns
from sqlalchemy import Date, DateTime, ForeignKey, String, Text

# SQLAlchemy ORM imports for typed mapped columns and relationships
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Import Base from database.py
from app.db.database import Base


# Experience model - represents a candidate's work experience
class Experience(Base):
    # Name of the database table for candidate experience recor ds
    __tablename__ = "candidate_experience"

    # Primary key for the experience record
    # Each experience entry gets a unique ID.
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )
    # ID of the candidate profile this experience record belongs to.
    # ForeignKey links this field to the primary key of candidate_profiles.
    # ondelete="CASCADE" ensures experience records are automatically
    # deleted when the associated candidate profile is deleted.
    profile_id: Mapped[int] = mapped_column(
        ForeignKey(
            "candidate_profiles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )
    # Company name
    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Job title
    job_title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Location of the job
    location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # Start date of the job
    start_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # End date of the job
    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # Description of the job
    # Description of the job
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Timestamp indicating when this experience record was created.
    # timezone=True allows the database to store timezone-aware timestamps.
    # datetime.utcnow is used as the default value when a record is created.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    # Relationship to the CandidateProfile model.
    # Each experience record belongs to one candidate profile.
    # back_populates connects this relationship to the corresponding
    # "experience" relationship defined in CandidateProfile.
    profile = relationship(
        "CandidateProfile",
        back_populates="experience",
    )