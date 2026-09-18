# schemas.py - Pydantic schemas for the Education API.
#
# Pydantic schemas serve two purposes:
#   1. Validate incoming request data (body parsing + type checking).
#   2. Serialize outgoing response data into a consistent JSON shape.
#
# Three schemas are defined here:
#   - EducationCreate  : fields accepted when creating a new record.
#   - EducationUpdate  : same fields but all optional (partial update / PATCH).
#   - EducationResponse: what the API returns to the client.

from datetime import date

from pydantic import BaseModel, ConfigDict


# Schema used for POST /api/v1/profile/education
# Only `institution` is required; all other fields are optional.
class EducationCreate(BaseModel):
    # Name of the educational institution (required)
    institution: str

    # Degree obtained, e.g. "B.Tech", "M.Sc." (optional)
    degree: str | None = None

    # Area of study, e.g. "Computer Science" (optional)
    field_of_study: str | None = None

    # Date the candidate started the program (optional)
    start_date: date | None = None

    # Date the candidate finished the program (optional)
    end_date: date | None = None

    # Additional notes, achievements, GPA, etc. (optional)
    description: str | None = None


# Schema used for PATCH /api/v1/profile/education/{id}
# Every field is optional so the client can update just one field at a time.
class EducationUpdate(BaseModel):
    # All fields mirror EducationCreate but are optional for partial updates.
    institution: str | None = None
    degree: str | None = None
    field_of_study: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    description: str | None = None


# Schema used for all responses (GET, POST, PATCH).
# Inherits all fields from EducationCreate and adds database-generated fields.
class EducationResponse(EducationCreate):
    # from_attributes=True tells Pydantic to read values from SQLAlchemy
    # model attributes instead of expecting a plain dict.
    model_config = ConfigDict(from_attributes=True)

    # Primary key assigned by the database
    id: int

    # Foreign key linking this record to the owning candidate profile
    profile_id: int
