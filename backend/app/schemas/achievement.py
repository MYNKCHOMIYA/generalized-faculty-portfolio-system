from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class AchievementBase(BaseModel):
    title: str
    category: str
    achievement_date: Optional[date] = None
    description: Optional[str] = None

class AchievementCreate(AchievementBase):
    pass

class AchievementResponse(AchievementBase):
    id: str
    faculty_id: str
    model_config = ConfigDict(from_attributes=True)