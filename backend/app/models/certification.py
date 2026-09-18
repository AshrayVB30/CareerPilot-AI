# certification.py - SQLAlchemy model for candidate certifications.
#
# Each certification belongs to one CandidateProfile (many-to-one).
# Deleting a profile cascades to delete all its certifications.

from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Certification(Base):
    """Represents a professional certification on a candidate's profile."""

    __tablename__ = "candidate_certifications"

    # Primary key — auto-incremented by PostgreSQL
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    # Foreign key to candidate_profiles.id
    # ondelete="CASCADE" — deleting a profile removes all its certifications
    profile_id: Mapped[int] = mapped_column(
        ForeignKey(
            "candidate_profiles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # Certification name, e.g. "AWS Certified Developer" (required)
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Organisation that issued the certificate, e.g. "Amazon Web Services" (optional)
    issuing_organization: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # Date the certification was issued (optional)
    issue_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # Date the certification expires; None means it never expires (optional)
    expiration_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # Unique credential/badge ID provided by the issuing organisation (optional)
    credential_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # URL to verify the credential online (optional)
    credential_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # Timestamp when this record was created
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    # Many-to-one relationship back to CandidateProfile
    # back_populates="certifications" connects to the list on CandidateProfile
    profile = relationship(
        "CandidateProfile",
        back_populates="certifications",
    )
