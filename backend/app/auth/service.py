# represents: business logic (authentication and user management)
# import ORM classes and methods
# pyrefly: ignore [missing-import]
from sqlalchemy import select
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
# import Pydantic schemas
from app.auth.schemas import UserRegister
# import security utilities
from app.core.security import hash_password, verify_password
# import user model
from app.models.user import User
# import custom exceptions
from app.core.exceptions import UserAlreadyExistsException

# get user by email (function will be used by authentication and other services)
def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    # create SQL select statement for user by email
    statement = select(User).where(User.email == email)
    # execute query and return single result or None
    return db.execute(statement).scalar_one_or_none()

# create user (registration)
def create_user(
    db: Session,
    user_data: UserRegister,
) -> User:
    user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
    )
    # add user to database
    db.add(user)
    # persist changes
    db.commit()
    # reload user from database with any new fields (like id)
    db.refresh(user)

    return user

# authenticate user (login)
def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:
    # get user by email
    user = get_user_by_email(db, email)
    # if no user found, return None
    if not user:
        return None
    # if password is not verified, return None
    if not verify_password(password, user.password_hash):
        return None
    # return authenticated user
    return user


# Impleneting the registration logic so duplicate emails are handled explicitly.
def register_user(
    db: Session,
    user_data: UserRegister,
) -> User:
    # check if user already exists
    if get_user_by_email(db, user_data.email):
        raise UserAlreadyExistsException("User already exists")
    # create user
    user = create_user(db, user_data)
    # return user
    return user

# Delete user function
def delete_user(
    db: Session,
    user_id: int,
) -> User:
    # get user by id
    user = db.get(User, user_id)
    # if no user found, return None
    if not user:
        return None
    # delete user
    db.delete(user)
    # persist changes
    db.commit()
    # return deleted user
    return user