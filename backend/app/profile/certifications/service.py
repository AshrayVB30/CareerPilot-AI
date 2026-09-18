# service.py - Business logic for certification CRUD operations.
#
# All database access for certification records lives here.
# Routers call these functions and never touch the DB directly.
#
# Note: mode="json" is used in model_dump() calls so that Pydantic
# serialises HttpUrl objects to plain strings before they are passed
# to the SQLAlchemy model (which expects str, not HttpUrl).

from sqlalchemy.orm import Session

from app.models.certification import Certification
from app.models.profile import CandidateProfile


def get_certifications(
    db: Session,
    profile: CandidateProfile,
) -> list[Certification]:
    """
    Return all certifications belonging to `profile`,
    ordered by issue_date descending (most recent first).
    """
    return (
        db.query(Certification)
        # Scope to the current user's profile only
        .filter(Certification.profile_id == profile.id)
        # Most recently issued certification first; NULL dates sort to the end
        .order_by(Certification.issue_date.desc())
        .all()
    )


def get_certification_by_id(
    db: Session,
    profile: CandidateProfile,
    certification_id: int,
) -> Certification | None:
    """
    Return a single certification by its primary key, scoped to `profile`.
    Returns None if not found or if it belongs to another user.
    """
    return (
        db.query(Certification)
        .filter(
            # Match the requested certification ID
            Certification.id == certification_id,
            # AND verify ownership — prevents users accessing others' data
            Certification.profile_id == profile.id,
        )
        .first()
    )


def create_certification(
    db: Session,
    profile: CandidateProfile,
    data,
) -> Certification:
    """
    Create a new certification record linked to `profile`.
    `data` is a CertificationCreate Pydantic schema instance.
    mode="json" converts HttpUrl → str before passing to SQLAlchemy.
    """
    certification = Certification(
        profile_id=profile.id,
        # mode="json" serialises HttpUrl objects to plain strings
        **data.model_dump(mode="json"),
    )

    db.add(certification)
    db.commit()

    # Refresh to populate server-generated fields like `id` and `created_at`
    db.refresh(certification)

    return certification


def update_certification(
    db: Session,
    certification: Certification,
    data,
) -> Certification:
    """
    Apply a partial update to an existing certification record.
    Only fields explicitly sent by the client are changed (exclude_unset=True).
    """
    # exclude_unset=True ignores fields the client did not include
    # mode="json" ensures HttpUrl values are plain strings
    updates = data.model_dump(mode="json", exclude_unset=True)

    # Apply each provided field to the SQLAlchemy model instance
    for field, value in updates.items():
        setattr(certification, field, value)

    db.commit()
    db.refresh(certification)

    return certification


def delete_certification(
    db: Session,
    certification: Certification,
) -> None:
    """
    Permanently delete a certification record.
    The router verifies ownership before calling this.
    """
    db.delete(certification)
    db.commit()
