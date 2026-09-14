# routes for auth endpoints
# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException, status
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session

# import Pydantic schemas
from app.auth.schemas import (
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
)
# import services
from app.auth.service import (
    authenticate_user,
    create_user,
    get_user_by_email,
)
# import security utilities
from app.core.security import create_access_token
# pyrefly: ignore [missing-import]  
from app.db.database import get_db
# Router
router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)
# Register endpoint
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
# register user
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db),
):
    # check if user already exists
    existing_user = get_user_by_email(
        db,
        user_data.email,
    )
    # if user already exists, raise HTTPException
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        )
    # create user
    return create_user(
        db,
        user_data,
    )

# Login endpoint
@router.post(
    "/login",
    response_model=TokenResponse,
)
# login user
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db,
        user_data.email,
        user_data.password,
    )
    # if user does not exist, raise HTTPException
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    # create access token
    token = create_access_token(
        subject=str(user.id),
    )
    # return token
    return {
        "access_token": token,
        "token_type": "bearer",
    }