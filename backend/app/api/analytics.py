from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.faculty_profile import FacultyProfile
from app.models.publication import Publication
from app.schemas.analytics import DashboardAnalytics, DepartmentStat

router = APIRouter()


@router.get("/dashboard", response_model=DashboardAnalytics)
def get_system_analytics(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)
):
    """
    Aggregates system-wide academic metrics for the admin dashboard.
    """
    # 1. High-level absolute counts
    total_faculty = db.query(FacultyProfile).count()
    total_pubs = db.query(Publication).count()

    # 2. Group by Department Analytics (The heavy lifting)
    # This creates a dynamic SQL query that groups faculty by department
    # and counts both the unique faculty members and their total publications.
    dept_stats_query = (
        db.query(
            FacultyProfile.department,
            func.count(func.distinct(FacultyProfile.id)).label("faculty_count"),
            func.count(func.distinct(Publication.id)).label("pub_count"),
        )
        .outerjoin(Publication, FacultyProfile.id == Publication.faculty_id)
        .group_by(FacultyProfile.department)
        .all()
    )

    # 3. Format the grouped data into our Pydantic schema
    dept_stats = []
    for dept, f_count, p_count in dept_stats_query:
        # Handle cases where a faculty member hasn't set a department yet
        dept_name = dept if dept else "Unassigned"

        dept_stats.append(
            DepartmentStat(
                department=dept_name, faculty_count=f_count, publication_count=p_count
            )
        )

    return DashboardAnalytics(
        total_faculty=total_faculty,
        total_publications=total_pubs,
        department_stats=dept_stats,
    )
