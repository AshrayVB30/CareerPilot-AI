# router.py - HTTP route handlers for the Education API.
#
# Endpoints:
#   GET    /api/v1/profile/education           → list all education records
#   POST   /api/v1/profile/education           → add a new education record
#   PATCH  /api/v1/profile/education/{id}      → partially update a record
#   DELETE /api/v1/profile/education/{id}      → delete a record
#
# All endpoints require a valid JWT token (via get_current_user).
# Ownership is enforced by scoping queries to the current user's profile.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.profile.service import get_profile
from app.profile.education.schemas import (
    EducationCreate,
    EducationResponse,
    EducationUpdate,
)
from app.profile.education.service import (
    create_education,
    delete_education,
    get_education,
    get_education_by_id,
    update_education,
)


# All routes in this router are prefixed with /api/v1/profile/education
# and grouped under "Education" in the Swagger UI docs.
router = APIRouter(
    prefix="/api/v1/profile/education",
    tags=["Education"],
)


def get_current_profile(
    db: Session,
    current_user: User,
):
    """
    Helper that fetches the current user's profile and raises 404
    if they haven't created one yet.
    Used by every endpoint to reduce boilerplate.
    """
    profile = get_profile(db, current_user)

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Create a profile first.",
        )

    return profile


# ---------------------------------------------------------------
# GET /api/v1/profile/education
# ---------------------------------------------------------------
@router.get(
    "",
    response_model=list[EducationResponse],
    summary="List all education records",
)
def list_education(
    # JWT dependency — validates the Bearer token and returns the User
    current_user: User = Depends(get_current_user),
    # DB session injected by FastAPI's dependency system
    db: Session = Depends(get_db),
):
    """
    Return all education entries for the authenticated user,
    ordered by start_date descending (most recent first).
    """
    # Resolve the user's profile (raises 404 if not found)
    profile = get_current_profile(db, current_user)

    # Fetch and return all education records for this profile
    return get_education(db, profile)


# ---------------------------------------------------------------
# POST /api/v1/profile/education
# ---------------------------------------------------------------
@router.post(
    "",
    response_model=EducationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new education record",
)
def add_education(
    # Validated request body
    data: EducationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new education entry linked to the authenticated user's profile.
    """
    profile = get_current_profile(db, current_user)

    # Delegate creation to the service layer
    return create_education(db, profile, data)


# ---------------------------------------------------------------
# PATCH /api/v1/profile/education/{education_id}
# ---------------------------------------------------------------
@router.patch(
    "/{education_id}",
    response_model=EducationResponse,
    summary="Update an education record",
)
def edit_education(
    # Path parameter: the ID of the education record to update
    education_id: int,
    # Only the fields the client sends will be updated
    data: EducationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Partially update an education record.
    Only fields included in the request body are modified.
    Returns 404 if the record does not exist or belongs to another user.
    """
    profile = get_current_profile(db, current_user)

    # Look up the record, scoped to this profile for ownership enforcement
    education = get_education_by_id(db, profile, education_id)

    if not education:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education record not found",
        )

    return update_education(db, education, data)


# ---------------------------------------------------------------
# DELETE /api/v1/profile/education/{education_id}
# ---------------------------------------------------------------
@router.delete(
    "/{education_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an education record",
)
def remove_education(
    # Path parameter: the ID of the education record to delete
    education_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Permanently delete an education record.
    Returns 204 No Content on success.
    Returns 404 if the record does not exist or belongs to another user.
    """
    profile = get_current_profile(db, current_user)

    education = get_education_by_id(db, profile, education_id)

    if not education:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education record not found",
        )

    # Delegate deletion to the service layer
    delete_education(db, education)
    # FastAPI returns 204 No Content automatically — no return value needed
