# router.py - HTTP route handlers for the Experience API.
#
# Endpoints:
#   GET    /api/v1/profile/experience           → list all experience records
#   POST   /api/v1/profile/experience           → add a new experience record
#   PATCH  /api/v1/profile/experience/{id}      → partially update a record
#   DELETE /api/v1/profile/experience/{id}      → delete a record
#
# All endpoints require a valid JWT token (via get_current_user).
# Ownership is enforced by scoping all queries to the current user's profile.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.profile.service import get_profile
from app.profile.experience.schemas import (
    ExperienceCreate,
    ExperienceResponse,
    ExperienceUpdate,
)
from app.profile.experience.service import (
    create_experience,
    delete_experience,
    get_experience,
    get_experience_by_id,
    update_experience,
)


# All routes are prefixed with /api/v1/profile/experience
# and grouped under "Experience" in the Swagger UI docs.
router = APIRouter(
    prefix="/api/v1/profile/experience",
    tags=["Experience"],
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
# GET /api/v1/profile/experience
# ---------------------------------------------------------------
@router.get(
    "",
    response_model=list[ExperienceResponse],
    summary="List all experience records",
)
def list_experience(
    # JWT dependency — validates the Bearer token and returns the User
    current_user: User = Depends(get_current_user),
    # DB session injected by FastAPI's dependency system
    db: Session = Depends(get_db),
):
    """
    Return all experience entries for the authenticated user,
    ordered by start_date descending (most recent role first).
    """
    # Resolve the user's profile (raises 404 if missing)
    profile = get_current_profile(db, current_user)

    # Fetch and return all experience records for this profile
    return get_experience(db, profile)


# ---------------------------------------------------------------
# POST /api/v1/profile/experience
# ---------------------------------------------------------------
@router.post(
    "",
    response_model=ExperienceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new experience record",
)
def add_experience(
    # Validated request body
    data: ExperienceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new experience entry linked to the authenticated user's profile.
    """
    profile = get_current_profile(db, current_user)

    # Delegate creation to the service layer
    return create_experience(db, profile, data)


# ---------------------------------------------------------------
# PATCH /api/v1/profile/experience/{experience_id}
# ---------------------------------------------------------------
@router.patch(
    "/{experience_id}",
    response_model=ExperienceResponse,
    summary="Update an experience record",
)
def edit_experience(
    # Path parameter: ID of the experience record to update
    experience_id: int,
    # Only fields present in the request body will be updated
    data: ExperienceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Partially update an experience record.
    Returns 404 if the record does not exist or belongs to another user.
    """
    profile = get_current_profile(db, current_user)

    # Look up the record, scoped to this profile for ownership enforcement
    experience = get_experience_by_id(db, profile, experience_id)

    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience record not found",
        )

    return update_experience(db, experience, data)


# ---------------------------------------------------------------
# DELETE /api/v1/profile/experience/{experience_id}
# ---------------------------------------------------------------
@router.delete(
    "/{experience_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an experience record",
)
def remove_experience(
    # Path parameter: ID of the experience record to delete
    experience_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Permanently delete an experience record.
    Returns 204 No Content on success.
    Returns 404 if the record does not exist or belongs to another user.
    """
    profile = get_current_profile(db, current_user)

    experience = get_experience_by_id(db, profile, experience_id)

    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience record not found",
        )

    # Delegate deletion to the service layer
    delete_experience(db, experience)
    # FastAPI returns 204 No Content automatically — no return value needed
