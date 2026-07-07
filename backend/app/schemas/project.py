from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date


class ProjectBase(BaseModel):
    title: str
    funding_agency: Optional[str] = None
    budget: Optional[float] = None
    status: str = "Ongoing"
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: str
    faculty_id: str
    model_config = ConfigDict(from_attributes=True)
