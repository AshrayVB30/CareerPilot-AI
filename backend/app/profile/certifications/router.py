# router.py - HTTP route handlers for the Certifications API.
#
# Endpoints:
#   GET    /api/v1/profile/certifications           → list all certifications
#   POST   /api/v1/profile/certifications           → add a new certification
#   PATCH  /api/v1/profile/certifications/{id}      → partially update one
#   DELETE /api/v1/profile/certifications/{id}      → delete one
#
# All endpoints require a valid JWT token (via get_current_user).
# Ownership is enforced by scoping all queries to the current user's profile.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.profile.service import get_profile
from app.profile.certifications.schemas import (
    CertificationCreate,
    CertificationResponse,
    CertificationUpdate,
)
from app.profile.certifications.service import (
    create_certification,
    delete_certification,
    get_certification_by_id,
    get_certifications,
    update_certification,
)


# All routes prefixed with /api/v1/profile/certifications
# and grouped under "Certifications" in the Swagger UI docs.
router = APIRouter(
    prefix="/api/v1/profile/certifications",
    tags=["Certifications"],
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
# GET /api/v1/profile/certifications
# ---------------------------------------------------------------
@router.get(
    "",
    response_model=list[CertificationResponse],
    summary="List all certifications",
)
def list_certifications(
    # JWT dependency — validates the Bearer token and returns the User
    current_user: User = Depends(get_current_user),
    # DB session injected by FastAPI's dependency system
    db: Session = Depends(get_db),
):
    """
    Return all certifications for the authenticated user,
    ordered by issue_date descending (most recent first).
    """
    # Resolve the user's profile (raises 404 if missing)
    profile = get_current_profile(db, current_user)

    # Fetch and return all certifications for this profile
    return get_certifications(db, profile)


# ---------------------------------------------------------------
# POST /api/v1/profile/certifications
# ---------------------------------------------------------------
@router.post(
    "",
    response_model=CertificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new certification",
)
def add_certification(
    # Validated request body
    data: CertificationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Add a new certification to the authenticated user's profile.
    credential_url must be a valid URL if provided.
    """
    profile = get_current_profile(db, current_user)

    # Delegate creation to the service layer
    return create_certification(db, profile, data)


# ---------------------------------------------------------------
# PATCH /api/v1/profile/certifications/{certification_id}
# ---------------------------------------------------------------
@router.patch(
    "/{certification_id}",
    response_model=CertificationResponse,
    summary="Update a certification",
)
def edit_certification(
    # Path parameter: ID of the certification to update
    certification_id: int,
    # Only fields present in the request body will be updated
    data: CertificationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Partially update a certification record.
    Returns 404 if the record does not exist or belongs to another user.
    """
    profile = get_current_profile(db, current_user)

    # Look up the certification, scoped to this profile for ownership
    certification = get_certification_by_id(db, profile, certification_id)

    if not certification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification not found",
        )

    return update_certification(db, certification, data)


# ---------------------------------------------------------------
# DELETE /api/v1/profile/certifications/{certification_id}
# ---------------------------------------------------------------
@router.delete(
    "/{certification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a certification",
)
def remove_certification(
    # Path parameter: ID of the certification to delete
    certification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Permanently delete a certification.
    Returns 204 No Content on success.
    Returns 404 if the record does not exist or belongs to another user.
    """
    profile = get_current_profile(db, current_user)

    # Ownership check — users can only delete their own certifications
    certification = get_certification_by_id(db, profile, certification_id)

    if not certification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification not found",
        )

    # Delegate deletion to the service layer
    delete_certification(db, certification)
    # FastAPI returns 204 No Content automatically — no return value needed
