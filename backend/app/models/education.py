# Education Model - Schema for candidate education details

# Import date for education start/end dates
# Import datetime for the record creation timestamp
from datetime import date, datetime

# SQLAlchemy imports for date/time fields,
# foreign key relationships, and string/text columns
from sqlalchemy import Date, DateTime, ForeignKey, String, Text

# SQLAlchemy ORM imports for typed mapped columns and relationships
# pyright: ignore [reportMissingImports]
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Import the declarative Base class used by all database models
from app.db.database import Base


# Education Model
# Stores educational qualifications associated with a candidate profile.
class Education(Base):
    # Name of the database table for candidate education records
    __tablename__ = "candidate_education"

    # Primary key for the education record
    # Each education entry gets a unique ID.
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    # ID of the candidate profile this education record belongs to.
    # ForeignKey links this field to the primary key of candidate_profiles.
    # ondelete="CASCADE" ensures education records are automatically
    # deleted when the associated candidate profile is deleted.
    profile_id: Mapped[int] = mapped_column(
        ForeignKey(
            "candidate_profiles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # Name of the educational institution.
    # This field is required.
    institution: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Degree or qualification obtained from the institution.
    # Optional because some education records may not have a degree.
    degree: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # Area or subject in which the candidate studied.
    # Optional because a field of study may not apply to every qualification.
    field_of_study: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # Date when the candidate started the education program.
    # Optional because the start date may not always be available.
    start_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # Date when the candidate completed or left the education program.
    # Optional to support ongoing education or missing completion dates.
    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # Additional information about the education.
    # Can contain details such as achievements, coursework,
    # activities, honors, or other relevant information.
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Timestamp indicating when this education record was created.
    # timezone=True allows the database to store timezone-aware timestamps.
    # datetime.utcnow is used as the default value when a record is created.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    # Relationship to the CandidateProfile model.
    # Each education record belongs to one candidate profile.
    # back_populates connects this relationship to the corresponding
    # "education" relationship defined in CandidateProfile.
    profile = relationship(
        "CandidateProfile",
        back_populates="education",
    )