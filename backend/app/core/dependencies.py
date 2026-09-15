# Dependencies
# Import FastAPI utilities for dependency injection and handling HTTP errors.
from fastapi import Depends, HTTPException, status

# HTTPBearer extracts the Bearer token from the Authorization header.
# HTTPAuthorizationCredentials contains the extracted token.
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# SQLAlchemy Session is used to interact with the database.
from sqlalchemy.orm import Session

# Function used to decode and validate the JWT access token.
from app.core.security import decode_access_token

# Database dependency that provides a database session.
from app.db.database import get_db

# User database model.
from app.models.user import User


# Create an HTTP Bearer security scheme.
# This tells FastAPI to expect an Authorization header like:
# Authorization: Bearer <access_token>
security = HTTPBearer()


def get_current_user(
    # FastAPI automatically extracts the Bearer token from the
    # Authorization header and provides the credentials here.
    credentials: HTTPAuthorizationCredentials = Depends(security),

    # FastAPI gets a database session using the get_db dependency.
    db: Session = Depends(get_db),
) -> User:

    # Extract the actual JWT token from the authorization credentials.
    token = credentials.credentials

    # decode_access_token already extracts and returns the "sub" claim
    # (the user's ID) as a plain string — not a dict.
    # So we use the return value directly as user_id.
    user_id = decode_access_token(token)

    # If the token could not be decoded, is expired, or has no subject,
    # reject the request with HTTP 401 Unauthorized.
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Look up the user in the database using the ID from the token.
    # .first() returns the first matching user or None if no user exists.
    user = db.query(User).filter(User.id == int(user_id)).first()

    # If no user exists with this ID, reject the request.
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check whether the user's account is active.
    # Inactive users are not allowed to access protected resources.
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    # Authentication and validation were successful.
    # Return the User object so the protected route can use it.
    return user
