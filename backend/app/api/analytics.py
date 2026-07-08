import pandas as pd
from typing import List
from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.faculty_profile import FacultyProfile
from app.models.publication import Publication
from app.schemas.analytics import DashboardAnalytics, DepartmentStat

router = APIRouter()


# --- Schemas specifically for this file ---
class TrendData(BaseModel):
    year: int
    count: int


# --- Endpoints ---


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

    # 2. Group by Department Analytics
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

    # 3. Format the grouped data
    dept_stats = []
    for dept, f_count, p_count in dept_stats_query:
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


@router.get("/trends/publications", response_model=List[TrendData])
def get_publication_trends(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)
):
    """
    Analyzes publication output over time.
    Uses Pandas to intelligently fill in missing years with 0.
    """
    pubs = (
        db.query(Publication.publication_year)
        .filter(Publication.publication_year.isnot(None))
        .all()
    )

    if not pubs:
        return []

    df = pd.DataFrame(pubs, columns=["year"])
    trend_df = df.groupby("year").size().reset_index(name="count")

    min_year = int(trend_df["year"].min())
    max_year = int(trend_df["year"].max())

    all_years = pd.DataFrame({"year": range(min_year, max_year + 1)})
    final_df = pd.merge(all_years, trend_df, on="year", how="left").fillna(0)
    final_df["count"] = final_df["count"].astype(int)

    return final_df.to_dict(orient="records")
