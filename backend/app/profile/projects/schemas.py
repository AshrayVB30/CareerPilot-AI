# schemas.py - Pydantic schemas for the Projects API.
#
# Three schemas:
#   - ProjectCreate  : fields accepted when creating a project.
#   - ProjectUpdate  : all fields optional for partial PATCH updates.
#   - ProjectResponse: returned by every endpoint.
#
# project_url and github_url are validated as proper URLs (HttpUrl).
# mode="json" is used in the service so Pydantic serialises HttpUrl → str
# before passing values to the SQLAlchemy model.

from pydantic import BaseModel, ConfigDict, HttpUrl


# Schema for POST /api/v1/profile/projects
# Only `name` is required.
class ProjectCreate(BaseModel):
    # Project name, e.g. "CareerPilot AI" (required)
    name: str

    # What the project does, stack, goals, etc. (optional)
    description: str | None = None

    # Technologies used — freeform string, e.g. "Python, FastAPI, React" (optional)
    technologies: str | None = None

    # URL of the live/deployed project (optional, validated as a URL)
    project_url: HttpUrl | None = None

    # GitHub or other source-code repository URL (optional, validated as a URL)
    github_url: HttpUrl | None = None


# Schema for PATCH /api/v1/profile/projects/{id}
# Every field is optional — only provided fields are updated.
class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    technologies: str | None = None
    project_url: HttpUrl | None = None
    github_url: HttpUrl | None = None


# Schema returned by GET, POST, and PATCH endpoints.
# Inherits all ProjectCreate fields and adds DB-generated fields.
class ProjectResponse(ProjectCreate):
    # from_attributes=True lets Pydantic read from SQLAlchemy model instances
    model_config = ConfigDict(from_attributes=True)

    # Database primary key
    id: int

    # Foreign key linking this project to the owning candidate profile
    profile_id: int
