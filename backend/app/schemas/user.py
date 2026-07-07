from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "faculty"  # Default to faculty, can be overridden by admin
    department_id: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    is_active: bool
    role: str
    department_id: Optional[str]

    # Required to read data from SQLAlchemy model instances
    model_config = ConfigDict(from_attributes=True)
