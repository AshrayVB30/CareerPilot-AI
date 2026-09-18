# schemas.py - Pydantic schemas for the Skills API.
#
# Three schemas:
#   - SkillCreate  : fields accepted when adding a new skill.
#   - SkillUpdate  : all fields optional (partial PATCH).
#   - SkillResponse: returned by every endpoint.
#
# Proficiency is validated as a float between 0 and 100:
#   0   = no proficiency
#   50  = intermediate
#   80  = strong
#   100 = expert

from pydantic import BaseModel, ConfigDict, Field


# Schema used for POST /api/v1/profile/skills
# Only `name` is required.
class SkillCreate(BaseModel):
    # Skill name, e.g. "Python", "React", "SQL" (required)
    name: str

    # Grouping category, e.g. "Backend", "Frontend", "DevOps" (optional)
    category: str | None = None

    # Self-assessed proficiency score from 0 (none) to 100 (expert)
    # ge=0 → must be >= 0; le=100 → must be <= 100
    proficiency: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    # How many years the candidate has used this skill (optional)
    years_of_experience: float | None = None

    # How the skill was added: "manual" | "ai_extracted" | "import"
    # Defaults to "manual" when added through this API.
    source: str = "manual"


# Schema used for PATCH /api/v1/profile/skills/{id}
# Every field is optional for partial updates.
class SkillUpdate(BaseModel):
    name: str | None = None
    category: str | None = None

    # Same 0–100 validation constraint applies on updates
    proficiency: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )
    years_of_experience: float | None = None
    source: str | None = None


# Schema returned by GET, POST, and PATCH endpoints.
# Inherits all SkillCreate fields and adds DB-generated fields.
class SkillResponse(SkillCreate):
    # from_attributes=True lets Pydantic read from SQLAlchemy model instances
    model_config = ConfigDict(from_attributes=True)

    # Database primary key
    id: int

    # Foreign key linking this skill to the owning candidate profile
    profile_id: int
