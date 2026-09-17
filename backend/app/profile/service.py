# service - Profile-related database operations

# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session

# pyrefly: ignore [missing-import]
from app.models.profile import CandidateProfile
# pyrefly: ignore [missing-import]
from app.models.user import User

# pyrefly: ignore [missing-import]
from app.profile.schemas import ProfileCreate, ProfileUpdate


# Get the profile associated with a specific user.
def get_profile(
    db: Session,
    user: User,
):
    # Query the CandidateProfile table and find the profile
    # belonging to the given user.
    return (
        db.query(CandidateProfile)
        .filter(CandidateProfile.user_id == user.id)
        .first()
    )


# Create a new candidate profile for a user.
def create_profile(
    db: Session,
    user: User,
    data: ProfileCreate,
):
    # Create a CandidateProfile using the user's ID and
    # the validated profile data.
    profile = CandidateProfile(
        user_id=user.id,
        **data.model_dump(mode="json"),
    )

    # Add the new profile to the database session.
    db.add(profile)

    # Commit the transaction so the profile is saved.
    db.commit()

    # Refresh the object to load database-generated values,
    # such as the profile ID.
    db.refresh(profile)

    # Return the newly created profile.
    return profile


# Update an existing candidate profile.
def update_profile(
    db: Session,
    profile: CandidateProfile,
    data: ProfileUpdate,
):
    # Convert the update schema into a dictionary.
    # exclude_unset=True ensures that only fields explicitly
    # provided by the client are included.
    updates = data.model_dump(
        mode="json",
        exclude_unset=True,
    )

    # Update each provided field on the profile object.
    for field, value in updates.items():
        setattr(profile, field, value)

    # Commit the changes to the database.
    db.commit()

    # Refresh the profile to ensure it contains the latest
    # values from the database.
    db.refresh(profile)

    # Return the updated profile.
    return profile
