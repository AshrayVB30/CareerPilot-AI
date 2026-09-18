# router.py - HTTP route handlers for the Projects API.
#
# Endpoints:
#   GET    /api/v1/profile/projects           → list all projects (newest first)
#   POST   /api/v1/profile/projects           → add a new project
#   PATCH  /api/v1/profile/projects/{id}      → partially update a project
#   DELETE /api/v1/profile/projects/{id}      → delete a project
#
# All endpoints require a valid JWT token (via get_current_user).
# Ownership is enforced by scoping all queries to the current user's profile.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.profile.service import get_profile
from app.profile.projects.schemas import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from app.profile.projects.service import (
    create_project,
    delete_project,
    get_project_by_id,
    get_projects,
    update_project,
)


# All routes prefixed with /api/v1/profile/projects
# and grouped under "Projects" in the Swagger UI docs.
router = APIRouter(
    prefix="/api/v1/profile/projects",
    tags=["Projects"],
)


def get_current_profile(
    db: Session,
    current_user: User,
):
    """
    Shared helper: fetch the current user's profile and raise 404
    if they haven't created one yet.
    Called at the start of every endpoint to avoid repeating the same check.
    """
    profile = get_profile(db, current_user)

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Create a profile first.",
        )

    return profile


# ---------------------------------------------------------------
# GET /api/v1/profile/projects
# ---------------------------------------------------------------
@router.get(
    "",
    response_model=list[ProjectResponse],
    summary="List all projects",
)
def list_projects(
    # JWT dependency — validates the Bearer token and returns the User
    current_user: User = Depends(get_current_user),
    # DB session injected by FastAPI's dependency system
    db: Session = Depends(get_db),
):
    """
    Return all project entries for the authenticated user,
    ordered by created_at descending (most recently added first).
    """
    # Resolve the user's profile (raises 404 if missing)
    profile = get_current_profile(db, current_user)

    # Fetch and return all projects for this profile
    return get_projects(db, profile)


# ---------------------------------------------------------------
# POST /api/v1/profile/projects
# ---------------------------------------------------------------
@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new project",
)
def add_project(
    # Validated request body
    data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Add a new project to the authenticated user's profile.
    project_url and github_url must be valid URLs if provided.
    """
    profile = get_current_profile(db, current_user)

    # Delegate creation to the service layer
    return create_project(db, profile, data)


# ---------------------------------------------------------------
# PATCH /api/v1/profile/projects/{project_id}
# ---------------------------------------------------------------
@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update a project",
)
def edit_project(
    # Path parameter: ID of the project to update
    project_id: int,
    # Only fields present in the request body will be updated
    data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Partially update a project record.
    Returns 404 if the project does not exist or belongs to another user.
    """
    profile = get_current_profile(db, current_user)

    # Look up the project, scoped to this profile for ownership enforcement
    project = get_project_by_id(db, profile, project_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return update_project(db, project, data)


# ---------------------------------------------------------------
# DELETE /api/v1/profile/projects/{project_id}
# ---------------------------------------------------------------
@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project",
)
def remove_project(
    # Path parameter: ID of the project to delete
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Permanently delete a project.
    Returns 204 No Content on success.
    Returns 404 if the project does not exist or belongs to another user.
    """
    profile = get_current_profile(db, current_user)

    # Ownership check — users can only delete their own projects
    project = get_project_by_id(db, profile, project_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    # Delegate deletion to the service layer
    delete_project(db, project)
    # FastAPI returns 204 No Content automatically — no return value needed
