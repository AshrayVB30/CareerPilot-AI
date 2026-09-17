from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.profile.schemas import (
    ProfileCreate,
    ProfileResponse,
    ProfileUpdate,
)
from app.profile.service import (
    create_profile,
    get_profile,
    update_profile,
)


# Create an API router for profile-related endpoints.
router = APIRouter(
    prefix="/api/v1/profile",
    tags=["Profile"],
)


# Get the current user's profile.
@router.get(
    "",
    response_model=ProfileResponse,
)
def read_profile(
    # Get the currently authenticated user.
    current_user: User = Depends(get_current_user),

    # Get a database session.
    db: Session = Depends(get_db),
):
    # Fetch the profile belonging to the current user.
    profile = get_profile(db, current_user)

    # If no profile exists, return a 404 error.
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )

    # Return the user's profile.
    return profile


# Create a profile for the current user.
@router.post(
    "",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_candidate_profile(
    # Validate and receive profile data from the request body.
    data: ProfileCreate,

    # Get the currently authenticated user.
    current_user: User = Depends(get_current_user),

    # Get a database session.
    db: Session = Depends(get_db),
):
    # Check whether the current user already has a profile.
    existing_profile = get_profile(
        db,
        current_user,
    )

    # Prevent creating more than one profile for the same user.
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Profile already exists",
        )

    # Create and save the new profile.
    return create_profile(
        db,
        current_user,
        data,
    )


# Update the current user's existing profile.
@router.patch(
    "",
    response_model=ProfileResponse,
)
def update_candidate_profile(
    # Validate and receive the fields to update.
    data: ProfileUpdate,

    # Get the currently authenticated user.
    current_user: User = Depends(get_current_user),

    # Get a database session.
    db: Session = Depends(get_db),
):
    # Find the profile belonging to the current user.
    profile = get_profile(
        db,
        current_user,
    )

    # If the profile does not exist, return a 404 error.
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )

    # Apply the requested updates and save the changes.
    return update_profile(
        db,
        profile,
        data,
    )