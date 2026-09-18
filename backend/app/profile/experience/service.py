# service.py - Business logic for experience CRUD operations.
#
# All database access for experience records lives here.
# Routers call these functions and never touch the DB directly.

from sqlalchemy.orm import Session

from app.models.experience import Experience
from app.models.profile import CandidateProfile


def get_experience(
    db: Session,
    profile: CandidateProfile,
) -> list[Experience]:
    """
    Return all experience records belonging to `profile`,
    ordered by start_date descending (most recent role first).
    """
    return (
        db.query(Experience)
        # Scope to the current user's profile only
        .filter(Experience.profile_id == profile.id)
        # Most recent experience first; NULL dates sort to the end
        .order_by(Experience.start_date.desc())
        .all()
    )


def get_experience_by_id(
    db: Session,
    profile: CandidateProfile,
    experience_id: int,
) -> Experience | None:
    """
    Return a single experience record by its primary key,
    scoped to `profile` to enforce ownership.
    Returns None if not found or if it belongs to another user.
    """
    return (
        db.query(Experience)
        .filter(
            # Match the requested record ID
            Experience.id == experience_id,
            # AND verify it belongs to the current user's profile
            Experience.profile_id == profile.id,
        )
        .first()
    )


def create_experience(
    db: Session,
    profile: CandidateProfile,
    data,
) -> Experience:
    """
    Create a new experience record linked to `profile`.
    `data` is an ExperienceCreate Pydantic schema instance.
    """
    # Unpack all validated fields from the Pydantic schema into the model
    experience = Experience(
        profile_id=profile.id,
        **data.model_dump(),
    )

    db.add(experience)
    db.commit()

    # Refresh to populate server-generated fields like `id` and `created_at`
    db.refresh(experience)

    return experience


def update_experience(
    db: Session,
    experience: Experience,
    data,
) -> Experience:
    """
    Apply a partial update to an existing experience record.
    Only fields explicitly sent by the client are changed (exclude_unset=True).
    """
    # exclude_unset=True ignores fields the client did not include in the body
    updates = data.model_dump(exclude_unset=True)

    # Apply each provided field to the SQLAlchemy model instance
    for field, value in updates.items():
        setattr(experience, field, value)

    db.commit()
    db.refresh(experience)

    return experience


def delete_experience(
    db: Session,
    experience: Experience,
) -> None:
    """
    Permanently delete an experience record.
    The router verifies ownership before calling this.
    """
    db.delete(experience)
    db.commit()
