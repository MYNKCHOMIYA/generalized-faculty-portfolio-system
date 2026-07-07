from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app.api.deps import SessionDep, get_current_active_user
from app.models.user import User
from app.models.faculty_profile import FacultyProfile
from app.models.achievement import Achievement
from app.schemas.achievement import AchievementCreate, AchievementResponse

router = APIRouter()

def get_current_faculty_profile(session: Session, user_id: str) -> FacultyProfile:
    profile = session.query(FacultyProfile).filter(FacultyProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="Faculty profile required.")
    return profile

@router.post("/", response_model=AchievementResponse, status_code=status.HTTP_201_CREATED)
def create_achievement(*, session: SessionDep, ach_in: AchievementCreate, current_user: User = Depends(get_current_active_user)) -> Any:
    profile = get_current_faculty_profile(session, current_user.id)
    db_ach = Achievement(**ach_in.model_dump(), faculty_id=profile.id)
    session.add(db_ach)
    session.commit()
    session.refresh(db_ach)
    return db_ach

@router.get("/me", response_model=List[AchievementResponse])
def read_my_achievements(session: SessionDep, current_user: User = Depends(get_current_active_user)) -> Any:
    profile = get_current_faculty_profile(session, current_user.id)
    return session.query(Achievement).filter(Achievement.faculty_id == profile.id).all()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_achievement(*, session: SessionDep, id: str, current_user: User = Depends(get_current_active_user)) -> None:
    profile = get_current_faculty_profile(session, current_user.id)
    record = session.query(Achievement).filter(Achievement.id == id, Achievement.faculty_id == profile.id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Achievement not found")
    session.delete(record)
    session.commit()