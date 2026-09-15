# Routes for authentication-related endpoints.
# This file contains endpoints for:
# 1. User registration
# 2. User login
# 3. Getting the currently authenticated user's information


# Import FastAPI utilities:
# - APIRouter: Used to group related API routes.
# - Depends: Used for dependency injection.
# - HTTPException: Used to return HTTP errors.
# - status: Provides readable HTTP status code constants.
from fastapi import APIRouter, Depends, HTTPException, status


# Import SQLAlchemy Session.
# Session is used to communicate with the database.
from sqlalchemy.orm import Session


# Import the dependency that identifies the currently logged-in user.
# This dependency validates the JWT token and retrieves the User from the database.
from app.core.dependencies import get_current_user

# Import the User SQLAlchemy model.
from app.models.user import User


# Import Pydantic schemas.
# These schemas validate incoming request data and format outgoing responses.
from app.auth.schemas import (
    TokenResponse,   # Schema for the login response containing the access token.
    UserLogin,       # Schema for login request data.
    UserRegister,   # Schema for registration request data.
    UserResponse,    # Schema for the registered user response.
)


# Import authentication/user-related service functions.
# Business logic is kept inside the service layer instead of the route functions.
from app.auth.service import (
    authenticate_user,   # Checks email and password and returns the user.
    create_user,         # Creates and saves a new user.
    get_user_by_email,   # Finds a user by their email address.
)


# Import the function used to create JWT access tokens.
from app.core.security import create_access_token


# Import the database dependency.
# get_db provides a SQLAlchemy database session to each request.
from app.db.database import get_db


# Create an API router for authentication endpoints.
router = APIRouter(
    # All routes in this router will start with /api/v1/auth.
    prefix="/api/v1/auth",

    # Groups these endpoints under "Authentication"
    # in the automatically generated FastAPI documentation.
    tags=["Authentication"],
)


# -------------------------------------------------------------------
# Register Endpoint
# -------------------------------------------------------------------

@router.post(
    "/register",

    # Specifies the structure of the successful response.
    # FastAPI will validate/serialize the returned User using this schema.
    response_model=UserResponse,

    # 201 means a new resource (user) was successfully created.
    status_code=status.HTTP_201_CREATED,
)
def register(
    # UserRegister validates the registration request body.
    # For example, it may contain email, password, name, etc.
    user_data: UserRegister,

    # FastAPI automatically creates/provides a database session
    # using the get_db dependency.
    db: Session = Depends(get_db),
):
    # Check whether a user with this email already exists.
    existing_user = get_user_by_email(
        db,
        user_data.email,
    )

    # If a user already exists with this email,
    # return HTTP 409 Conflict.
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        )

    # Create the new user using the service layer.
    # The service handles the actual database operation.
    return create_user(
        db,
        user_data,
    )


# -------------------------------------------------------------------
# Login Endpoint
# -------------------------------------------------------------------

@router.post(
    "/login",

    # The successful response will follow the TokenResponse schema.
    # Typically this contains access_token and token_type.
    response_model=TokenResponse,
)
def login(
    # UserLogin validates the login request body.
    # It normally contains the user's email and password.
    user_data: UserLogin,

    # Get a database session using the get_db dependency.
    db: Session = Depends(get_db),
):
    # Authenticate the user using the email and password.
    #
    # The service should:
    # 1. Find the user by email.
    # 2. Verify the provided password.
    # 3. Return the user if authentication succeeds.
    # 4. Return None/False if authentication fails.
    user = authenticate_user(
        db,
        user_data.email,
        user_data.password,
    )

    # If authentication failed, return HTTP 401 Unauthorized.
    #
    # Using the same error message for invalid email/password
    # avoids revealing whether a particular email exists.
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Create a JWT access token for the authenticated user.
    #
    # The user's ID is stored as the "sub" (subject) claim.
    # It is converted to a string because JWT claims commonly
    # store the subject as a string.
    token = create_access_token(
        subject=str(user.id),
    )

    # Return the generated access token to the client.
    #
    # The client can then send it in future requests as:
    # Authorization: Bearer <access_token>
    return {
        "access_token": token,
        "token_type": "bearer",
    }


# -------------------------------------------------------------------
# Get Current User Endpoint
# -------------------------------------------------------------------

@router.get("/me")
def get_me(
    # get_current_user is a dependency that:
    # 1. Reads the Bearer token from the Authorization header.
    # 2. Validates/decodes the JWT.
    # 3. Gets the user ID from the token.
    # 4. Finds the user in the database.
    # 5. Checks whether the user is active.
    #
    # If any authentication check fails, it raises an HTTPException.
    current_user: User = Depends(get_current_user),
):
    # Return information about the currently authenticated user.
    #
    # current_user is the User object returned by get_current_user().
    return {
        "id": current_user.id,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at,
    }
