# router.py - HTTP route handlers for the Skills API.
#
# Endpoints:
#   GET    /api/v1/profile/skills           → list all skills (alphabetical)
#   POST   /api/v1/profile/skills           → add a new skill
#   PATCH  /api/v1/profile/skills/{id}      → partially update a skill
#   DELETE /api/v1/profile/skills/{id}      → delete a skill
#
# All endpoints require a valid JWT token (via get_current_user).
# Ownership is enforced — every query filters by profile_id.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.profile.service import get_profile
from app.profile.skills.schemas import (
    SkillCreate,
    SkillResponse,
    SkillUpdate,
)
from app.profile.skills.service import (
    create_skill,
    delete_skill,
    get_skill_by_id,
    get_skills,
    update_skill,
)


# All routes are prefixed with /api/v1/profile/skills
# and grouped under "Skills" in the Swagger UI docs.
router = APIRouter(
    prefix="/api/v1/profile/skills",
    tags=["Skills"],
)


def get_current_profile(
    db: Session,
    current_user: User,
):
    """
    Shared helper: fetch the current user's profile and raise 404
    if they haven't created one yet.
    Called at the start of every endpoint to avoid repeating the same check.
    """
    profile = get_profile(db, current_user)

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Create a profile first.",
        )

    return profile


# ---------------------------------------------------------------
# GET /api/v1/profile/skills
# ---------------------------------------------------------------
@router.get(
    "",
    response_model=list[SkillResponse],
    summary="List all skills",
)
def list_skills(
    # JWT dependency — validates the Bearer token and returns the User
    current_user: User = Depends(get_current_user),
    # DB session injected by FastAPI's dependency system
    db: Session = Depends(get_db),
):
    """
    Return all skill entries for the authenticated user,
    ordered alphabetically by skill name.
    """
    # Resolve the user's profile (raises 404 if missing)
    profile = get_current_profile(db, current_user)

    # Fetch and return all skills for this profile
    return get_skills(db, profile)


# ---------------------------------------------------------------
# POST /api/v1/profile/skills
# ---------------------------------------------------------------
@router.post(
    "",
    response_model=SkillResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new skill",
)
def add_skill(
    # Validated request body (proficiency validated 0–100 in schema)
    data: SkillCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Add a new skill to the authenticated user's profile.
    Proficiency must be between 0 and 100 if provided.
    """
    profile = get_current_profile(db, current_user)

    # Delegate creation to the service layer
    return create_skill(db, profile, data)


# ---------------------------------------------------------------
# PATCH /api/v1/profile/skills/{skill_id}
# ---------------------------------------------------------------
@router.patch(
    "/{skill_id}",
    response_model=SkillResponse,
    summary="Update a skill",
)
def edit_skill(
    # Path parameter: ID of the skill to update
    skill_id: int,
    # Only fields present in the request body will be updated
    data: SkillUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Partially update a skill.
    Returns 404 if the skill does not exist or belongs to another user.
    """
    profile = get_current_profile(db, current_user)

    # Look up the skill, scoped to this profile for ownership enforcement
    skill = get_skill_by_id(db, profile, skill_id)

    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )

    return update_skill(db, skill, data)


# ---------------------------------------------------------------
# DELETE /api/v1/profile/skills/{skill_id}
# ---------------------------------------------------------------
@router.delete(
    "/{skill_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a skill",
)
def remove_skill(
    # Path parameter: ID of the skill to delete
    skill_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Permanently delete a skill.
    Returns 204 No Content on success.
    Returns 404 if the skill does not exist or belongs to another user.
    """
    profile = get_current_profile(db, current_user)

    # Ownership check: ensures users can only delete their own skills
    skill = get_skill_by_id(db, profile, skill_id)

    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )

    # Delegate deletion to the service layer
    delete_skill(db, skill)
    # FastAPI returns 204 No Content automatically — no return value needed
