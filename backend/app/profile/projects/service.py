# service.py - Business logic for project CRUD operations.
#
# All database access for project records lives here.
# Routers call these functions and never touch the DB directly.
#
# Note: mode="json" is used in model_dump() calls so that Pydantic
# serialises HttpUrl objects to plain strings before they are passed
# to the SQLAlchemy model (which expects str, not HttpUrl).

from sqlalchemy.orm import Session

from app.models.profile import CandidateProfile
from app.models.project import CandidateProject


def get_projects(
    db: Session,
    profile: CandidateProfile,
) -> list[CandidateProject]:
    """
    Return all projects belonging to `profile`,
    ordered by created_at descending (most recently added first).
    """
    return (
        db.query(CandidateProject)
        # Scope to the current user's profile only
        .filter(CandidateProject.profile_id == profile.id)
        # Most recently added project first
        .order_by(CandidateProject.created_at.desc())
        .all()
    )


def get_project_by_id(
    db: Session,
    profile: CandidateProfile,
    project_id: int,
) -> CandidateProject | None:
    """
    Return a single project by its primary key, scoped to `profile`.
    Returns None if not found or if it belongs to another user.
    """
    return (
        db.query(CandidateProject)
        .filter(
            # Match the requested project ID
            CandidateProject.id == project_id,
            # AND verify ownership — prevents users accessing others' data
            CandidateProject.profile_id == profile.id,
        )
        .first()
    )


def create_project(
    db: Session,
    profile: CandidateProfile,
    data,
) -> CandidateProject:
    """
    Create a new project record linked to `profile`.
    `data` is a ProjectCreate Pydantic schema instance.
    mode="json" converts HttpUrl → str before passing to SQLAlchemy.
    """
    project = CandidateProject(
        profile_id=profile.id,
        # mode="json" serialises HttpUrl objects to plain strings
        **data.model_dump(mode="json"),
    )

    db.add(project)
    db.commit()

    # Refresh to populate server-generated fields like `id` and `created_at`
    db.refresh(project)

    return project


def update_project(
    db: Session,
    project: CandidateProject,
    data,
) -> CandidateProject:
    """
    Apply a partial update to an existing project record.
    Only fields explicitly sent by the client are changed (exclude_unset=True).
    mode="json" converts HttpUrl → str before calling setattr.
    """
    # exclude_unset=True ignores fields the client did not include
    # mode="json" ensures HttpUrl values are plain strings
    updates = data.model_dump(mode="json", exclude_unset=True)

    # Apply each provided field to the SQLAlchemy model instance
    for field, value in updates.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return project


def delete_project(
    db: Session,
    project: CandidateProject,
) -> None:
    """
    Permanently delete a project record.
    The router verifies ownership before calling this.
    """
    db.delete(project)
    db.commit()
