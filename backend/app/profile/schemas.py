# schemas - Schemas are used to define the data structure of the request and response
# These are created to ensure that the data coming from the frontend is in the correct format
# and that the data going back to the frontend is in the correct format

# pyrefly: ignore [missing-import]
from datetime import datetime
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ConfigDict, HttpUrl

# @profile create   
class ProfileCreate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    location: str | None = None
    professional_summary: str | None = None
    linkedin_url: HttpUrl | None = None
    github_url: HttpUrl | None = None
    portfolio_url: HttpUrl | None = None

# @profile update   
class ProfileUpdate(ProfileCreate):
    pass

# @profile response   
class ProfileResponse(ProfileCreate):
    model_config = ConfigDict(from_attributes=True)
    # @field
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime