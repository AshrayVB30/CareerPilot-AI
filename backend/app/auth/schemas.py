#  this is for validation (request/response) schemas(Pydantic v2)
# import pydantic
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ConfigDict, EmailStr, Field

# user registration schema
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
    )
# user login schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str
# user response schema
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    is_active: bool
# token response schema
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"