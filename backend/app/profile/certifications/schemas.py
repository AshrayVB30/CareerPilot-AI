# schemas.py - Pydantic schemas for the Certifications API.
#
# Three schemas:
#   - CertificationCreate  : fields accepted when adding a certification.
#   - CertificationUpdate  : all fields optional for partial PATCH updates.
#   - CertificationResponse: returned by every endpoint.

from datetime import date

from pydantic import BaseModel, ConfigDict, HttpUrl


# Schema for POST /api/v1/profile/certifications
# Only `name` is required.
class CertificationCreate(BaseModel):
    # Certification name, e.g. "AWS Certified Developer" (required)
    name: str

    # Organisation that issued the certificate, e.g. "Amazon" (optional)
    issuing_organization: str | None = None

    # Date the certification was issued (optional)
    issue_date: date | None = None

    # Date the certification expires; None means it never expires (optional)
    expiration_date: date | None = None

    # Unique credential/badge ID from the issuing organisation (optional)
    credential_id: str | None = None

    # URL to verify the credential online (optional, validated as a URL)
    credential_url: HttpUrl | None = None


# Schema for PATCH /api/v1/profile/certifications/{id}
# Every field is optional — only provided fields are updated.
class CertificationUpdate(BaseModel):
    name: str | None = None
    issuing_organization: str | None = None
    issue_date: date | None = None
    expiration_date: date | None = None
    credential_id: str | None = None
    credential_url: HttpUrl | None = None


# Schema returned by GET, POST, and PATCH endpoints.
# Inherits all CertificationCreate fields and adds DB-generated fields.
class CertificationResponse(CertificationCreate):
    # from_attributes=True lets Pydantic read from SQLAlchemy model instances
    model_config = ConfigDict(from_attributes=True)

    # Database primary key
    id: int

    # Foreign key linking this certification to the owning candidate profile
    profile_id: int
