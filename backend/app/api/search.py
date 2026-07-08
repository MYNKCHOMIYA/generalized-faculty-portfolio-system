from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.faculty_profile import FacultyProfile

# Assuming these are the names of your MVP models!
from app.models.publication import Publication

router = APIRouter()


@router.get("/", response_model=List[dict])
def search_faculty(
    department: Optional[str] = Query(None, description="Filter by department"),
    designation: Optional[str] = Query(None, description="Filter by designation"),
    skill: Optional[str] = Query(None, description="Search within skills text"),
    min_publications: Optional[int] = Query(
        None, description="Minimum number of publications"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    # 1. Start with a base query
    query = db.query(FacultyProfile)

    # 2. Apply text-based filters dynamically
    # (Adding type: ignore to keep VS Code's Pylance happy with SQLAlchemy dynamic filtering)
    if department:
        query = query.filter(FacultyProfile.department.ilike(f"%{department}%"))  # type: ignore
    if designation:
        query = query.filter(FacultyProfile.designation.ilike(f"%{designation}%"))  # type: ignore

    if skill:
        query = query.filter(FacultyProfile.skills.ilike(f"%{skill}%"))  # type: ignore

    # 3. Apply advanced relational filters using your actual column name: faculty_id
    if min_publications is not None and min_publications > 0:
        query = (
            query.outerjoin(Publication, FacultyProfile.id == Publication.faculty_id)
            .group_by(FacultyProfile.id)
            .having(func.count(Publication.id) >= min_publications)
        )  # type: ignore

    # 4. Execute the final generated SQL query
    results = query.all()

    # 5. Format the lightweight response
    formatted_results = []
    for profile in results:
        formatted_results.append(
            {
                "id": profile.id,
                "user_id": str(profile.user_id),
                "first_name": profile.first_name,
                "last_name": profile.last_name,
                "department": profile.department or "N/A",
                "designation": profile.designation,
                "total_publications": (
                    len(profile.publications) if profile.publications else 0
                ),
                "total_projects": (
                    len(profile.projects)
                    if hasattr(profile, "projects") and profile.projects
                    else 0
                ),
            }
        )

    return formatted_results
