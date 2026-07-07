from enum import Enum
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from typing import Optional


# 1. Lock down the exact roles allowed in the system
class UserRole(str, Enum):
    FACULTY = "faculty"
    HOD = "hod"
    ADMIN = "admin"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.FACULTY  # Default safely to the Enum
    department_id: Optional[str] = None

    # 2. Intercept and validate the email domain before it hits the database
    @field_validator("email")
    @classmethod
    def validate_skit_domain(cls, value: str):
        if not value.endswith("@skit.ac.in"):
            raise ValueError(
                "Unauthorized domain. Only @skit.ac.in emails are permitted."
            )
        return value


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    is_active: bool
    role: UserRole  # Upgraded to match the Enum
    department_id: Optional[str]

    # Required to read data from SQLAlchemy model instances
    model_config = ConfigDict(from_attributes=True)
