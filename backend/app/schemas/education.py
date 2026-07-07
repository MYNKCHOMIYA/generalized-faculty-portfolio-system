from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class EducationBase(BaseModel):
    degree: str
    institution: str
    field_of_study: str
    start_date: date
    end_date: Optional[date] = None
    grade: Optional[str] = None

class EducationCreate(EducationBase):
    pass

class EducationResponse(EducationBase):
    id: str
    faculty_id: str
    model_config = ConfigDict(from_attributes=True)