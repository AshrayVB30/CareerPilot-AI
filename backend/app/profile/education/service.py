# service.py - Business logic for education CRUD operations.
#
# All database access for education records lives here.
# Router functions call these service functions and never touch the DB directly.
# This keeps the routing layer thin and the logic easy to test in isolation.

from sqlalchemy.orm import Session

from app.models.education import Education
from app.models.profile import CandidateProfile


def get_education(
    db: Session,
    profile: CandidateProfile,
) -> list[Education]:
    """
    Return all education records belonging to `profile`,
    ordered by start_date descending (most recent first).
    """
    return (
        db.query(Education)
        # Filter to only this profile's records
        .filter(Education.profile_id == profile.id)
        # Most recent education first; NULL dates sort to the end
        .order_by(Education.start_date.desc())
        .all()
    )


def get_education_by_id(
    db: Session,
    profile: CandidateProfile,
    education_id: int,
) -> Education | None:
    """
    Return a single education record by its primary key,
    scoped to `profile` so users cannot access other people's records.
    Returns None if not found.
    """
    return (
        db.query(Education)
        .filter(
            # Match on the record's own id
            Education.id == education_id,
            # AND ensure it belongs to the current user's profile
            Education.profile_id == profile.id,
        )
        .first()
    )


def create_education(
    db: Session,
    profile: CandidateProfile,
    data,
) -> Education:
    """
    Create a new education record linked to `profile`.
    `data` is an EducationCreate Pydantic schema instance.
    """
    # Unpack all validated fields from the Pydantic schema into the model
    education = Education(
        profile_id=profile.id,
        **data.model_dump(),
    )

    db.add(education)
    db.commit()

    # Refresh to populate server-generated fields like `id` and `created_at`
    db.refresh(education)

    return education


def update_education(
    db: Session,
    education: Education,
    data,
) -> Education:
    """
    Apply a partial update to an existing education record.
    `data` is an EducationUpdate schema — only fields that were
    explicitly sent by the client are applied (exclude_unset=True).
    """
    # exclude_unset=True means fields the client did not send are ignored
    updates = data.model_dump(exclude_unset=True)

    # Apply each provided field to the SQLAlchemy model instance
    for field, value in updates.items():
        setattr(education, field, value)

    db.commit()
    db.refresh(education)

    return education


def delete_education(
    db: Session,
    education: Education,
) -> None:
    """
    Permanently delete an education record from the database.
    The router is responsible for verifying ownership before calling this.
    """
    db.delete(education)
    db.commit()
