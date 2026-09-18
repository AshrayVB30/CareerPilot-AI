# schemas.py - Pydantic schemas for the Experience API.
#
# Three schemas:
#   - ExperienceCreate  : fields accepted when creating a new record.
#   - ExperienceUpdate  : all fields optional (partial PATCH).
#   - ExperienceResponse: returned by every endpoint.

from datetime import date

from pydantic import BaseModel, ConfigDict


# Schema used for POST /api/v1/profile/experience
# company_name and job_title are required; everything else is optional.
class ExperienceCreate(BaseModel):
    # Name of the company or organisation (required)
    company_name: str

    # Candidate's job title at that company (required)
    job_title: str

    # City / country where the role was based (optional)
    location: str | None = None

    # Date the candidate started the role (optional)
    start_date: date | None = None

    # Date the candidate left the role; None means currently employed (optional)
    end_date: date | None = None

    # Responsibilities, achievements, technologies used, etc. (optional)
    description: str | None = None


# Schema used for PATCH /api/v1/profile/experience/{id}
# Every field is optional so the client can update just one field at a time.
class ExperienceUpdate(BaseModel):
    company_name: str | None = None
    job_title: str | None = None
    location: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    description: str | None = None


# Schema returned by GET, POST, and PATCH endpoints.
# Inherits all ExperienceCreate fields and adds the DB-generated fields.
class ExperienceResponse(ExperienceCreate):
    # from_attributes=True lets Pydantic read from SQLAlchemy model instances
    model_config = ConfigDict(from_attributes=True)

    # Database primary key
    id: int

    # Foreign key linking this record to the owning candidate profile
    profile_id: int
