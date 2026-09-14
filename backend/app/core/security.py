# authentication and password hashing utilities.
# pyrefly: ignore [missing-import]
from datetime import datetime, timedelta, timezone
# used for JWT operations
from jose import JWTError, jwt
# used for password hashing
from passlib.context import CryptContext
# import settings
from app.core.config import settings

# create a CryptContext instance for password hashing.
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)
# hashes a plain password using bcrypt. (Converts plain text password → hashed password)
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# verifies a plain password against a hashed password (Entered password -> compared with stored hashed password -> TRUE or FALSE)
def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )
# creates a JWT access token with the given subject and expiration time.(jwt containing the user's identity.)
def create_access_token(
    subject: str,
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    # JWT payload
    payload = {
        "sub": subject,
        "exp": expire,
    }
    # encoded using JWT secret key and algorithm
    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
# Decodes a JWT access token and returns the subject if valid.(Checks whether the token is valid. If valid, returns the user's ID.)
def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        # get subject from payload
        subject = payload.get("sub")
        # return subject if valid
        if not subject:
            return None
        return subject
    # catch JWT errors
    except JWTError:
        return None