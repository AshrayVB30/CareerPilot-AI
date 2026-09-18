# service.py - Business logic for skills CRUD operations.
#
# All database access for skill records lives here.
# Routers call these functions and never touch the DB directly.
#
# Note: the model file is skills.py (plural) — import accordingly.

from sqlalchemy.orm import Session

from app.models.profile import CandidateProfile
from app.models.skills import CandidateSkill  # file is skills.py (plural)


def get_skills(
    db: Session,
    profile: CandidateProfile,
) -> list[CandidateSkill]:
    """
    Return all skills belonging to `profile`,
    ordered alphabetically by name.
    """
    return (
        db.query(CandidateSkill)
        # Scope to the current user's profile only
        .filter(CandidateSkill.profile_id == profile.id)
        # Alphabetical order makes skills easy to scan
        .order_by(CandidateSkill.name.asc())
        .all()
    )


def get_skill_by_id(
    db: Session,
    profile: CandidateProfile,
    skill_id: int,
) -> CandidateSkill | None:
    """
    Return a single skill by its primary key, scoped to `profile`.
    Returns None if not found or if it belongs to another user.
    """
    return (
        db.query(CandidateSkill)
        .filter(
            # Match the requested skill ID
            CandidateSkill.id == skill_id,
            # AND verify it belongs to the current user's profile
            CandidateSkill.profile_id == profile.id,
        )
        .first()
    )


def create_skill(
    db: Session,
    profile: CandidateProfile,
    data,
) -> CandidateSkill:
    """
    Create a new skill record linked to `profile`.
    `data` is a SkillCreate Pydantic schema instance.
    """
    # Unpack all validated fields from the Pydantic schema into the model
    skill = CandidateSkill(
        profile_id=profile.id,
        **data.model_dump(),
    )

    db.add(skill)
    db.commit()

    # Refresh to populate server-generated fields like `id` and `created_at`
    db.refresh(skill)

    return skill


def update_skill(
    db: Session,
    skill: CandidateSkill,
    data,
) -> CandidateSkill:
    """
    Apply a partial update to an existing skill record.
    Only fields explicitly sent by the client are changed (exclude_unset=True).
    """
    # exclude_unset=True ignores fields the client did not include
    updates = data.model_dump(exclude_unset=True)

    # Apply each provided field to the SQLAlchemy model instance
    for field, value in updates.items():
        setattr(skill, field, value)

    db.commit()
    db.refresh(skill)

    return skill


def delete_skill(
    db: Session,
    skill: CandidateSkill,
) -> None:
    """
    Permanently delete a skill record.
    The router verifies ownership before calling this.
    """
    db.delete(skill)
    db.commit()
