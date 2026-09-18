# schemas - Schemas are used to define the data structure of the request and response
# These are created to ensure that the data coming from the frontend is in the correct format
# and that the data going back to the frontend is in the correct format

# pyrefly: ignore [missing-import]
from datetime import date, datetime
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
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


# ----------------------------------------------------------------
# Nested schemas for full profile response
# ----------------------------------------------------------------

class EducationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    profile_id: int
    institution: str
    degree: str | None = None
    field_of_study: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    description: str | None = None
    created_at: datetime


class ExperienceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    profile_id: int
    company_name: str
    job_title: str
    location: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    description: str | None = None
    created_at: datetime


class SkillResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    profile_id: int
    name: str
    category: str | None = None
    proficiency: float | None = None
    years_of_experience: float | None = None
    source: str
    created_at: datetime


class ProfileFullResponse(ProfileResponse):
    """Full profile including education, experience, and skills."""
    education: list[EducationResponse] = []
    experience: list[ExperienceResponse] = []
    skills: list[SkillResponse] = []